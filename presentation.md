---
marp: true
theme: gaia
_class: lead
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SAP 연계 FTA 원산지 판정 시뮬레이터
## 포트폴리오 프로젝트

### 현대오토에버 SAP ERP 직무 지원

---

# 1. 프로젝트 선정 배경 및 전략

- **Target 역량**: SAP ABAP 개발, SD 모듈 지식, 수출/FTA 프로세스 경험
- **현대자동차그룹의 특징**:
  - 글로벌 법인 운영으로 **수출 및 통관(FTA) 이슈**가 핵심
  - 우대사항: **"SAP 수출패키지 운영, 원산지(FTA) 프로세스 업무 경험"**
- **기획 의도**:
  - 단순 문법 공부를 넘어, 현업(SD)에서 가장 필요한 **수출/FTA 프로세스**를 직접 모델링
  - **주문(SO) ➡ 출하(Delivery) ➡ 대금청구(Billing)** 흐름과 **원산지 판정**의 연계성을 구현하여 도메인 이해도 증명

---

# 2. 프로젝트 개요 및 목적

- **개요**: 실제 제조 기업의 **FTA 원산지 판정 프로세스**를 MVP로 구현
- **목표**:
  - SAP 데이터 구조(Master Data) 및 비즈니스 로직 역량 증명
  - 제조업 핵심 프로세스(BOM, FTA CTSH) 도메인 지식 입증
- **타겟**: SAP 직무 채용 담당자 및 실무 면접관

---

# 3. 비즈니스 시나리오 (Use Case)

- **대상 품목**: 전기차 배터리 팩 (EV Battery Pack)
- **핵심 이슈**:
  - 🇨🇳 중국산 **리튬 셀 (HS 8507.90)**
  - 🇰🇷 한국산 **배터리 모듈 (HS 8507.90)** 로 제조
  - 최종 **배터리 팩 (HS 8507.60)** 의 원산지가 **한국(KR)** 로 인정될 수 있는가?
- **판정 기준**: **CTSH** (Change of Tariff Sub-Heading, 4단위 세번변경기준)

---

# 4. 시스템 아키텍처 및 DB 설계

- **ERP 모사 데이터베이스 (SQLite)**:
  - **ZMM_MATERIAL**: 자재 마스터 (자재유형, HS Code, 원산지)
  - **ZPP_BOM**: BOM 마스터 (부모-자식 관계, 소요량)
  - **ZSD_FTA_HIST**: 판정 이력 및 결과 로그
- **비즈니스 로직**:
  - BOM 전개 (Explosion) -> 최하위 자재 탐색
  - HS Code 비교 -> 세번 변경 여부 자동 판정

---

# 5. 구현 기능 (Features)

1. **마스터 데이터 관리**: 자재 및 BOM 구조의 계층적 데이터 표현
2. **원산지 시뮬레이션**:
   - 완제품 선택 시 CTSH 알고리즘 즉시 실행
   - 역외산 자재 식별 및 판정 근거 제시
3. **이력 추적**: 모든 시뮬레이션 결과의 DB 저장 및 조회
4. **Interactive Dashboard**: Streamlit 기반의 직관적인 2-Column UI

---

# 6. 기술 스택 (Tech Stack)

- **Core**: Python 3.13+
- **Database**: SQLite (Embedded DB)
- **UI Framework**: Streamlit
- **Data Analysis**: Pandas

---

# 7. 향후 개선 계획

- **로직 고도화**: RVC (부가가치기준) 판정 알고리즘 추가
- **시각화 강화**: Graphviz 등을 활용한 BOM Tree 구조 시각화
- **시스템 연동**: SAP RFC (Remote Function Call) 연동 테스트

---

<!-- _class: lead -->

# 감사합니다
## Q & A
