# 제품 요구사항 정의서 (PRD)
## 프로젝트명: SAP 연계 FTA 원산지 판정 시뮬레이터

---

## 1. 개요 (Overview)
본 프로젝트는 **현대오토에버 SAP ERP 직무 지원**을 위한 포트폴리오용 사이드 프로젝트입니다.
실제 제조 기업의 ERP 환경에서 이루어지는 **FTA 원산지 판정 프로세스**를 로컬 환경(MVP)에서 구현하여, **SAP 데이터 구조(Master Data)**에 대한 이해도와 **비즈니스 로직(Business Logic)** 구현 역량을 증명하는 것을 목표로 합니다.

## 2. 목적 및 배경 (Goals & Background)
- **지원 직무 적합성 강조**: SAP 모듈(MM, PP, SD)과 연계된 개발/운영 역량 어필.
- **도메인 지식 증명**: 제조업의 핵심 프로세스인 BOM(자재명세서) 구조와 FTA 판정 로직(CTSH 등)에 대한 이해도 입증.
- **구현 능력 검증**: Python과 SQL을 활용하여 백엔드 로직부터 프론트엔드 대시보드까지 Full-Cycle 개발 능력 시연.

## 3. 타겟 사용자 (Target Role)
- **면접관/채용 담당자**: 지원자의 직무 역량(SAP 데이터 이해, 로직 구현)을 검증하고자 하는 실무자.

## 4. 유저 스토리 (User Stories)
1. **마스터 데이터 조회**: 사용자는 ERP 내의 자재(Material) 정보와 BOM 구조를 조회하여 제품의 구성 요소를 파악할 수 있다.
2. **원산지 시뮬레이션**: 사용자는 특정 완제품을 선택하여 FTA 원산지 판정(CTSH 기준)을 수행할 수 있다.
3. **결과 및 근거 확인**: 사용자는 판정 결과(충족/불충족)와 그 근거(어떤 자재에서 세번 변경이 실패했는지)를 상세 로그를 통해 확인할 수 있다.
4. **이력 관리**: 사용자는 과거의 판정 이력을 조회하여 언제 어떤 판정이 내려졌는지 추적할 수 있다.

## 5. 상세 기능 요구사항 (Functional Requirements)

### 5.1 데이터베이스 구축 (SAP 모사)
- **자재 마스터 (ZMM_MATERIAL)**
    - 자재번호(MATNR), 자재유형(MTART), 내역(MAKTX), HS Code(HSCODE), 원산지(ORIGIN), 단가(PRICE) 관리.
    - *Key Point*: 완제품(FERT), 반제품(HALB), 원자재(ROH) 구분 및 HS Code 관리.
- **BOM 마스터 (ZPP_BOM)**
    - 모자재(MATNR_P), 자자재(MATNR_C), 소요량(MENGE) 관리.
    - *Key Point*: 다단계(Multi-level) BOM 구조 표현 가능성 (현재 MVP는 1-2 Level 예시).
- **판정 이력 (ZSD_FTA_HIST)**
    - 판정 ID, 대상 품목, 판정 결과, 적용 규칙, 판정 일시 저장.

### 5.2 더미 데이터 생성
- **시나리오**: 전기차 배터리 팩(EV Battery Pack).
    - **이슈 케이스**: 중국산 '리튬 셀(8507.90)'이 한국산 '배터리 모듈(8507.90)' 및 '배터리 팩(8507.60)'으로 조립될 때의 세번 변경 여부 확인.

### 5.3 비즈니스 로직 (원산지 판정)
- **CTSH (Change of Tariff Sub-Heading)** 알고리즘 구현.
    - **Step 1**: 완제품의 BOM을 최하위 레벨(Leaf Node)까지 전개(Explosion).
    - **Step 2**: 역외산(Foreign) 원자재 식별.
    - **Step 3**: 완제품의 HS Code(4단위)와 역외산 원자재의 HS Code(4단위) 비교.
    - **Step 4**: 
        - 하나라도 HS Code 4단위가 동일하면 -> **불충족(Foreign)**.
        - 모든 역외산 자재의 HS Code가 변경되었으면 -> **충족(KR)**.

### 5.4 UI/UX (Streamlit)
- **Layout**: 2분할 화면 (좌측: 데이터 조회 / 우측: 시뮬레이션).
- **Control**: 완제품 선택 Dropdown, 판정 실행 Button.
- **Feedback**: 성공(풍선 효과) 및 실패(에러 메시지) 시각화, 상세 로직 로그 출력.

## 6. 기술 스택 (Tech Stack)
- **Language**: Python 3.13+
- **Database**: SQLite (내장형 DB)
- **FrameWork**: Streamlit (Data App UI)
- **Libraries**: Pandas (데이터 처리)

## 7. 향후 개선 계획 (Future Improvements)
- **RVC(부가가치기준) 로직 추가**: 공제법/집적법 계산 로직 구현.
- **BOM 시각화**: Tree 그래프를 이용한 BOM 구조 시각화.
- **SAP RFC 연동**: 실제 SAP 서버와 RFC 통신을 통한 데이터 송수신 기능(가능 시).
