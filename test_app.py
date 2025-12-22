from app import init_db, reset_and_seed_data, determine_origin_ctsh
import os

def test_logic():
    print("Testing DB Init...")
    init_db()
    if os.path.exists('sap_fta.db'):
        print("DB File Created.")
    
    print("Testing Data Seeding...")
    reset_and_seed_data()
    print("Data Seeded.")
    
    print("Testing Determination Logic...")
    result, logs = determine_origin_ctsh('EV_BATTERY_PACK')
    print(f"Result: {result}")
    print("Logs:")
    for log in logs:
        print(log)

if __name__ == "__main__":
    test_logic()
