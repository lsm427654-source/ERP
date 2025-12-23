# SAP 연계 FTA 원산지 판정 시뮬레이터

> 현대오토에버 SAP ERP 직무 지원 포트폴리오 프로젝트

## 📊 프레젠테이션 보기

**👉 [프레젠테이션 열기](https://lsm427654-source.github.io/ERP/presentation.html)**

---

## 프로젝트 개요

실제 제조 기업의 **FTA 원산지 판정 프로세스**를 MVP로 구현한 시뮬레이터입니다.

### 주요 목표
- SAP 데이터 구조(Master Data) 및 비즈니스 로직 역량 증명
- 제조업 핵심 프로세스(BOM, FTA CTSH) 도메인 지식 입증
- SAP SD 모듈 및 수출/FTA 프로세스 이해도 증명

### 비즈니스 시나리오
- **대상 품목**: 전기차 배터리 팩 (EV Battery Pack)
- **핵심 이슈**: 중국산 리튬 셀을 사용한 한국산 배터리 팩의 원산지 판정
- **판정 기준**: CTSH (Change of Tariff Sub-Heading, 4단위 세번변경기준)

## 기술 스택

- **Core**: Python 3.13+
- **Database**: SQLite (Embedded DB)
- **UI Framework**: Streamlit
- **Data Analysis**: Pandas

## 파일 구조

```
ERP/
├── presentation.html          # 프레젠테이션 (HTML)
├── presentation.md            # 프레젠테이션 소스 (Markdown)
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Pages 자동 배포
└── README.md                  # 이 파일
```

## 프로젝트 배경

현대자동차그룹은 글로벌 법인 운영으로 **수출 및 통관(FTA) 이슈**가 핵심입니다. 
본 프로젝트는 단순 문법 공부를 넘어, 현업(SD)에서 가장 필요한 **수출/FTA 프로세스**를 직접 모델링하여 도메인 이해도를 증명합니다.

---

**Contact**: lsm427654-source  
**Repository**: https://github.com/lsm427654-source/ERP
