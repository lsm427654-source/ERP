import streamlit as st
import sqlite3
import pandas as pd
import random

# ==========================================
# 1. Database & Config Setup
# ==========================================
DB_FILE = 'sap_fta.db'

def init_db():
    """
    Initialize SQLite database and Create Tables if not exist.
    Simulating SAP Tables:
    - ZMM_MATERIAL: Material Master (Material Code, Type, HS Code, Origin, Price)
    - ZPP_BOM: Bill of Materials (Parent, Child, Quantity)
    - ZSD_FTA_HIST: FTA Determination History
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 1.1 Material Master (ZMM_MATERIAL)
    c.execute('''
        CREATE TABLE IF NOT EXISTS ZMM_MATERIAL (
            MATNR TEXT PRIMARY KEY,   -- Material Number
            MTART TEXT,               -- Material Type (FERT: Finished, ROH: Raw)
            MAKTX TEXT,               -- Material Description
            HSCODE TEXT,              -- HS Code (6 digits for simplicity)
            ORIGIN TEXT,              -- Origin Country (KR, CN, US, DE...)
            PRICE REAL                -- Price (Currency assumed KRW)
        )
    ''')

    # 1.2 BOM Master (ZPP_BOM)
    c.execute('''
        CREATE TABLE IF NOT EXISTS ZPP_BOM (
            MATNR_P TEXT,    -- Parent Material
            MATNR_C TEXT,    -- Child Material
            MENGE REAL,      -- Quantity
            FOREIGN KEY(MATNR_P) REFERENCES ZMM_MATERIAL(MATNR),
            FOREIGN KEY(MATNR_C) REFERENCES ZMM_MATERIAL(MATNR)
        )
    ''')

    # 1.3 FTA History (ZSD_FTA_HIST)
    c.execute('''
        CREATE TABLE IF NOT EXISTS ZSD_FTA_HIST (
            DETERMINE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            MATNR TEXT,         -- Finished Good
            DEST_COUNTRY TEXT,  -- Destination Country
            RESULT TEXT,        -- Origin Result (KR/FOREIGN)
            RULE_APPLIED TEXT,  -- Rule Applied (e.g., CTSH)
            DETERMINE_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def reset_and_seed_data():
    """
    Reset tables and Insert Dummy Data for 'EV Battery' Scenario.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Clear existing data
    c.execute("DELETE FROM ZMM_MATERIAL")
    c.execute("DELETE FROM ZPP_BOM")
    c.execute("DELETE FROM ZSD_FTA_HIST")

    # --- Dummy Data Generation ---
    # Scenario: EV Battery Pack (Finished Good)
    # Structure: 
    #   EV_BATTERY_PACK (KR) -> 8507.60
    #       - BATTERY_MODULE (KR) (Sub-assembly) -> 8507.90
    #           - LITHIUM_CELL (CN) (Raw Material) -> 8507.90 (Same Heading as Module!)
    #           - AL_CASE (KR) -> 7604.29
    #       - BMS_CONTROLLER (DE) -> 8537.10
    #       - COOLING_FAN (VN) -> 8414.59
    
    materials = [
        # (MATNR, MTART, MAKTX, HSCODE, ORIGIN, PRICE)
        ('EV_BATTERY_PACK', 'FERT', 'High Performance EV Battery Pack', '850760', 'KR', 5000000),
        
        ('BATTERY_MODULE', 'HALB', 'Li-ion Battery Module', '850790', 'KR', 1000000),
        ('LITHIUM_CELL', 'ROH', 'Li-ion Cell 3.7V', '850790', 'CN', 50000), # Risk Item for CTSH
        ('AL_CASE', 'ROH', 'Aluminum Module Case', '760429', 'KR', 20000),
        
        ('BMS_CONTROLLER', 'ROH', 'Battery Management System', '853710', 'DE', 300000), # Change of Heading OK
        ('COOLING_FAN', 'ROH', 'Cooling Fan Unit', '841459', 'VN', 50000), # Change of Heading OK
        
        ('SCREW_SET', 'ROH', 'Steel Screw Set', '731815', 'CN', 100) # Minor part
    ]
    
    c.executemany("INSERT INTO ZMM_MATERIAL VALUES (?, ?, ?, ?, ?, ?)", materials)

    boms = [
        # (MATNR_P, MATNR_C, MENGE)
        # 1. Pack BOM
        ('EV_BATTERY_PACK', 'BATTERY_MODULE', 4),
        ('EV_BATTERY_PACK', 'BMS_CONTROLLER', 1),
        ('EV_BATTERY_PACK', 'COOLING_FAN', 2),
        ('EV_BATTERY_PACK', 'SCREW_SET', 20),
        
        # 2. Module BOM
        ('BATTERY_MODULE', 'LITHIUM_CELL', 12),
        ('BATTERY_MODULE', 'AL_CASE', 1),
        ('BATTERY_MODULE', 'SCREW_SET', 8)
    ]
    
    c.executemany("INSERT INTO ZPP_BOM VALUES (?, ?, ?)", boms)

    conn.commit()
    conn.close()

# ==========================================
# 2. Business Logic: FTA Determination
# ==========================================

def get_hscode_heading(hscode):
    """Returns the first 4 digits of HS Code (Heading)."""
    return hscode[:4] if hscode and len(hscode) >= 4 else ''

def explode_bom(matnr, conn, level=0):
    """
    Recursively fetch BOM to find all raw materials (Leaf nodes).
    Returns a list of dictionaries containing material info details.
    """
    exploded_parts = []
    
    # Query children
    query = """
        SELECT c.MATNR, c.MTART, c.HSCODE, c.ORIGIN, b.MENGE
        FROM ZPP_BOM b
        JOIN ZMM_MATERIAL c ON b.MATNR_C = c.MATNR
        WHERE b.MATNR_P = ?
    """
    df_children = pd.read_sql_query(query, conn, params=(matnr,))
    
    for _, row in df_children.iterrows():
        # Add current child
        part_info = {
            'MATNR': row['MATNR'],
            'MTART': row['MTART'],
            'HSCODE': row['HSCODE'],
            'ORIGIN': row['ORIGIN'],
            'LEVEL': level + 1,
            'PARENT': matnr
        }
        exploded_parts.append(part_info)
        
        # Recursive call if it's not a raw material (assuming ROH is leaf, but traversing all just in case)
        # In this simplified logic, we traverse down. 
        # Ideally check if it has children.
        children = explode_bom(row['MATNR'], conn, level + 1)
        exploded_parts.extend(children)
        
    return exploded_parts

def determine_origin_ctsh(finished_good_matnr):
    """
    Perform CTSH (Change of Tariff Subheading - 4 digit level) Origin Determination.
    Logic:
    1. Get Finished Good HS Code.
    2. Explode BOM to get all components.
    3. Identify 'Foreign' components (ORIGIN != 'KR').
    4. For each Foreign component, compare its HS Heading (4 digit) with FG HS Heading.
    5. If ANY Foreign component has SAME Heading as FG -> Fail CTSH -> Origin NOT KR.
    6. If ALL Foreign components have DIFFERENT Heading -> Pass CTSH -> Origin KR.
    """
    conn = sqlite3.connect(DB_FILE)
    
    # Get FG Info
    fg_df = pd.read_sql_query("SELECT * FROM ZMM_MATERIAL WHERE MATNR = ?", conn, params=(finished_good_matnr,))
    if fg_df.empty:
        conn.close()
        return "Error: Material Not Found", []
        
    fg_hscode = fg_df.iloc[0]['HSCODE']
    fg_heading = get_hscode_heading(fg_hscode)
    
    # Explode BOM
    components = explode_bom(finished_good_matnr, conn)
    
    determination_log = []
    is_origin_kr = True
    
    if not components:
        determination_log.append("No components found. Assumed KR.")
        conn.close()
        return "KR", determination_log

    for part in components:
        # Check if Foreign
        if part['ORIGIN'] != 'KR':
            part_heading = get_hscode_heading(part['HSCODE'])
            
            # Message
            log_msg = f"Part: {part['MATNR']} (Origin: {part['ORIGIN']}, HS: {part['HSCODE']})"
            
            if part_heading == fg_heading:
                is_origin_kr = False
                log_msg += f" -> [FAIL] Same Heading as FG ({fg_heading})."
                determination_log.append(log_msg)
                # In strict logic, one fail is enough. But we continue to show full log.
            else:
                log_msg += f" -> [PASS] Heading Change ({part_heading} -> {fg_heading})."
                determination_log.append(log_msg)
    
    result = "KR" if is_origin_kr else "FOREIGN"
    
    # Save History
    c = conn.cursor()
    c.execute("INSERT INTO ZSD_FTA_HIST (MATNR, DEST_COUNTRY, RESULT, RULE_APPLIED) VALUES (?, ?, ?, ?)",
              (finished_good_matnr, "GLOBAL", result, "CTSH (4-digit)"))
    conn.commit()
    conn.close()
    
    return result, determination_log

# ==========================================
# 3. Streamlit UI
# ==========================================

st.set_page_config(layout="wide", page_title="SAP FTA 시뮬레이터")

# Init App
if 'init_done' not in st.session_state:
    init_db()
    reset_and_seed_data()
    st.session_state['init_done'] = True

st.title("🏭 SAP 연계 FTA 원산지 판정 시뮬레이터")
st.markdown("### 지원 직무: 현대오토에버 SAP ERP 전문가")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 SAP 마스터 데이터 (모의)")
    
    conn = sqlite3.connect(DB_FILE)
    
    st.write("**자재 마스터 (ZMM_MATERIAL)**")
    df_mat = pd.read_sql_query("SELECT * FROM ZMM_MATERIAL", conn)
    st.dataframe(df_mat, use_container_width=True)
    
    st.write("**BOM 마스터 (ZPP_BOM)**")
    df_bom = pd.read_sql_query("SELECT * FROM ZPP_BOM", conn)
    st.dataframe(df_bom, use_container_width=True)
    
    conn.close()

with col2:
    st.subheader("🚢 원산지 판정 엔진")
    
    conn = sqlite3.connect(DB_FILE)
    # Fetch FERT materials
    fert_list = pd.read_sql_query("SELECT MATNR FROM ZMM_MATERIAL WHERE MTART='FERT'", conn)['MATNR'].tolist()
    conn.close()
    
    selected_fert = st.selectbox("완제품 선택 (FERT)", fert_list)
    
    if st.button("🔍 원산지 판정 실행 (CTSH 기준)"):
        with st.spinner("BOM 구조 및 HS Code 분석 중..."):
            result, logs = determine_origin_ctsh(selected_fert)
        
        st.divider()
        if result == "KR":
            st.success(f"### 판정 결과: {result} (충족 - 한국산)")
            st.balloons()
        else:
            st.error(f"### 판정 결과: {result} (불충족 - 역외산)")
            
        st.write("#### 📜 판정 로직 로그")
        for log in logs:
            if "[FAIL]" in log:
                st.markdown(f"- :red[{log}]")
            else:
                st.markdown(f"- {log}")
                
    st.divider()
    st.write("#### 🕒 판정 이력 (ZSD_FTA_HIST)")
    conn = sqlite3.connect(DB_FILE)
    df_hist = pd.read_sql_query("SELECT * FROM ZSD_FTA_HIST ORDER BY DETERMINE_ID DESC", conn)
    st.dataframe(df_hist, use_container_width=True)
    conn.close()
