# DA_product_growth_analytics

사용자 행동 로그 기반으로 전환 퍼널·리텐션·ROI·A/B 테스트를 수행하는 그로스 분석 프로젝트

## 1. 프로젝트 개요

이 프로젝트는 카페 주문 앱(패스오더와 유사한 가상의 서비스)을 가정하고,
공개 데이터셋을 활용해 다음을 수행합니다.

- 사용자 행동 데이터 기반 퍼널/전환율 분석
- 코호트 & 리텐션 분석
- 마케팅 캠페인 성과(CAC, ROAS, ROI) 분석
- A/B 테스트 및 실험 설계
- 데이터 파이프라인(ETL/ELT) 설계 및 시각화

목표는 **“감이 아닌 데이터로 의사결정하는 그로스해커”** 역량을 보여주는 것입니다.

## 2. 사용 데이터셋

1. E-commerce Website Funnel Analysis (Kaggle)
2. eCommerce Events History (Cosmetics Shop Events, Kaggle)
3. Marketing Campaign Performance Dataset (Kaggle)

각 데이터는 `data/` 디렉토리에 CSV 형태로 위치합니다.

## 3. 폴더 구조

```bash
.
├── README.md
├── data/
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_funnel_analysis.ipynb
│   ├── 03_cohort_retention.ipynb
│   ├── 04_marketing_kpi_abtest.ipynb
│   └── 05_insights_and_growth_plan.ipynb
├── src/
│   ├── loaders.py
│   ├── utils_time.py
│   ├── funnel.py
│   ├── cohort.py
│   ├── marketing.py
│   └── viz_templates.py
└── reports/
    └── portfolio_summary.pdf
```

## 4. 환경 설정

- Python 3.10
- 주요 패키지: `pandas`, `numpy`, `matplotlib`, `seaborn`, `statsmodels`, `jupyter`

```bash
conda create -n growth python=3.10
conda activate growth
pip install pandas numpy matplotlib seaborn statsmodels jupyter notebook tqdm
```

## 5. 분석 흐름

1. `01_data_understanding.ipynb`

   - 각 데이터셋 구조 파악, 기본 통계, 결측치 처리, 파생 변수 생성.

2. `02_funnel_analysis.ipynb`

   - 이벤트를 퍼널 스테이지로 매핑
   - 단계별 CVR/Drop-off 분석 및 시각화
   - 세그먼트별 퍼널 비교

3. `03_cohort_retention.ipynb`

   - 가입월 코호트 생성
   - 월별 리텐션 매트릭스 & 히트맵
   - 코호트별 리텐션 곡선 비교

4. `04_marketing_kpi_abtest.ipynb`

   - 캠페인별 CAC/ROAS/ROI 계산
   - 가상의 A/B 테스트 설계 및 통계 검정

5. `05_insights_and_growth_plan.ipynb`

   - 분석 결과를 비즈니스 언어로 해석
   - 구체적인 CRM/그로스 실험 로드맵 제안

## 6. 결과물

- 분석 노트북(.ipynb)
- 주요 그래프 및 인사이트를 정리한 `summary.pdf`
