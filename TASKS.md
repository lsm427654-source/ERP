# 프로젝트 태스크 리스트 (TASKS.md)
## 프로젝트명: SAP 연계 FTA 원산지 판정 시뮬레이터

---

## 1. 프로젝트 착수 및 환경 설정
- [x] **요구사항 분석**: 채용 공고 분석 및 PRD 작성 (포트폴리오 방향성 수립).
- [x] **개발 환경 구축**:
    - [x] Git 리포지토리 초기화 (`ERP.git`).
    - [x] Python 가상환경 설정 및 `.gitignore` 구성.
    - [x] 필수 라이브러리 선정 (`requirements.txt`: streamlit, pandas, sqlite3).

## 2. 데이터베이스 설계 및 구축 (SQLite)
- [x] **테이블 스키마 설계**:
    - [x] **ZMM_MATERIAL** (자재 마스터): PK, 속성(유형, HS Code, 원산지 등) 정의.
    - [x] **ZPP_BOM** (BOM 마스터): 부모-자식 관계 및 소요량 정의.
    - [x] **ZSD_FTA_HIST** (판정 이력): 이력 관리를 위한 로그 테이블 정의.
- [x] **더미 데이터 생성 로직 구현**:
    - [x] 시나리오 정의: 전기차 배터리 팩 (완제품) vs 리튬 셀 (중국산 원자재).
    - [x] 데이터 적재 스크립트 작성 (`init_db`, `reset_and_seed_data`).

## 3. 핵심 비즈니스 로직 개발
- [x] **BOM 전개 (Explosion) 기능**:
    - [x] `explode_bom` 함수: 재귀적(Recursive) 탐색을 통해 최하위 자재 조회.
- [x] **원산지 판정 알고리즘 (CTSH)**:
    - [x] HS Code 4단위(Heading) 추출 유틸리티 구현.
    - [x] 역외산(Origin != KR) 부품 식별 로직.
    - [x] 완제품 vs 부품 HS Heading 비교 및 판정 로직.
    - [x] 판정 결과 이력 저장 로직 (`insert_history`).

## 4. UI/UX 개발 (Streamlit)
- [x] **화면 레이아웃 구성**:
    - [x] `st.columns` 활용 좌/우 2분할 (마스터 데이터 vs 시뮬레이터).
- [x] **마스터 데이터 조회 뷰**:
    - [x] Pandas DataFrame을 활용한 테이블 조회 (`st.dataframe`).
- [x] **시뮬레이션 컨트롤 패널**:
    - [x] 완제품 선택 Selectbox 구현.
    - [x] 판정 실행 Button 및 Spinner(로딩) 적용.
- [x] **결과 시각화**:
    - [x] 성공/실패에 따른 Status Message 및 Effect(`st.balloons`).
    - [x] 상세 의사결정 로그 출력 (판정 근거).

## 5. 테스트 및 검증
- [x] **단위 테스트 (Unit Test)**:
    - [x] `test_app.py` 작성: DB 생성 및 로직 함수 검증.
- [x] **통합 테스트 (Integration Test)**:
    - [x] UI 상에서 전체 시나리오 구동 확인 (배터리 팩 판정 결과 검증).

## 6. 문서화 (Documentation)
- [x] **README.md 작성**: 프로젝트 소개 및 실행법.
- [x] **PRD.md 작성**: 제품 요구사항 정의서.
- [x] **TASKS.md 작성**: 작업 분류 체계(WBS) 문서화.
