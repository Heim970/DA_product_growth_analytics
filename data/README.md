# 데이터 구조

## `users.csv`

### 전체 구조

| 컬럼명             | 설명                         | 이유                                        |
| ------------------ | ---------------------------- | ------------------------------------------- |
| user_id            | AAA, AAB … 형식              | 랜덤 정수보다 깔끔함, synthetic 느낌도 좋음 |
| signup_date        | 2024-12-01 ~ 2025-11-30      | 1년치 코호트·리텐션 분석용                  |
| device             | iOS / Android                | iOS가 리텐션 높게 나오는 패턴 가능          |
| channel            | organic / ad / push / social | CAC/ROAS 계산·퍼널 비교 가능                |
| price_sensitivity  | 0~1                          | 할인/가격 반응 실험(A/B) 가능               |
| impulse_level      | 0~1                          | Cart→Purchase CVR에 영향                    |
| return_prob        | 0~1                          | 리텐션 시뮬레이션 핵심                      |
| preferred_category | coffee/beverage/dessert      | 메뉴 추천·구매패턴 클러스터링 가능          |

### 생성 규칙

#### device 생성 규칙

    - iOS: 40%
    - Andriod: 60%

#### channel

    - organic: 55%
    - ad: 25%
    - push: 10%
    - social: 10%

#### price_sensitivity (0 ~ 1)

    - 0: 전혀 가격에 민감하지 않음
    - 1: 가격제 매우 민감함(할인 메뉴에 강하게 반응)

#### impulse_level (0 ~ 1)

    - 0: 매우 신중
    - 1: 충동구매 성향 강함

#### return_prob (0 ~ 1)

    - 리텐션의 핵심 변수
    - 0.1 ~ 0.5 사이 값 사용, 평균 0.25

#### preferred_category

    - coffee: 60%
    - beverage: 25%
    - dessert: 15%

### 예시

| user_id | signup_date | device  | channel | price_sensitivity | impulse_level | return_prob | preferred_category |
| ------- | ----------- | ------- | ------- | ----------------- | ------------- | ----------- | ------------------ |
| AAA     | 2024-12-02  | iOS     | organic | 0.41              | 0.83          | 0.31        | coffee             |
| AAB     | 2025-01-15  | Android | ad      | 0.92              | 0.27          | 0.18        | beverage           |
| AAC     | 2025-03-01  | Android | push    | 0.33              | 0.12          | 0.44        | coffee             |
| AAD     | 2025-05-20  | iOS     | social  | 0.65              | 0.90          | 0.52        | dessert            |
| AAE     | 2024-12-31  | Android | organic | 0.13              | 0.51          | 0.29        | coffee             |

---

## `events.csv`

### event_type 흐름

> 실제 카페앱 기반 행동 시퀀스

1. AppOpen
2. SearchMenu (확률적)
3. ViewMenu (1~4번 랜덤)
4. AddToCart (impulse_level 영향)
5. CheckoutStart
6. PaymentSuccess (A/B 테스트 영향)

### events 컬럼 구성

| 컬럼             | 설명                    |
| ---------------- | ----------------------- |
| timestamp        | 이벤트 발생 시간        |
| user_id          | Users.csv               |
| session_id       | 세션 ID                 |
| event_type       | AppOpen / ViewMenu …    |
| menu_id          | 메뉴 조회/장바구니/구매 |
| price            | menu price              |
| category         | menu category           |
| experiment_group | A/B                     |
| device           | user.device             |
| channel          | user.channel            |

### 행동 시뮬레이션 논리

#### 1) 오늘 앱을 열 확률

> `return_prob` + `signup_date` 경과일 반영

| signup_date (일) | 방문율                    |
| ---------------- | ------------------------- |
| ~ 30             | 높음                      |
| 31 ~ 90          | 조금 감소                 |
| 91 ~             | 개인별 `return_prob` 유지 |

#### 2) 하루 방문 횟수

| user segment            | visit_count |
| ----------------------- | ----------- |
| `impulse_level` > 0.7   | 하루 1~2회  |
| `impulse_level` 0.3~0.7 | 하루 1회    |
| `impulse_level` < 0.3   | 이틀에 1회  |

#### 3) 이벤트 시퀀스 생성

> 방문 1회당

- `AppOpen`
- `SearchMenu`: 60%
- `ViewMenu` x (1~4번)
- `AddToCart`: impulse_level
- `CheckoutStart`: impulse_level \* 0.8
- `PaymentSuccess`: base_CVR \* experiment_group_effect

#### 4) A/B 테스트

> `Menus.csv`에서 일부 메뉴는 `discount_flag` = `1`로 배정

- A 그룹: 기본 전환률
- B 그룹: 전환률 x (1.15 ~ 1.3 상승)

---

## menus.csv

### menus 컬럼 구성

| 컬럼명        | 설명     |
| ------------- | -------- |
| menu_id       | 메뉴번호 |
| name          | 이름     |
| category      | 카테고리 |
| price         | 가격     |
| discount_flag | 할인여부 |

---

## purchases.csv

### purchase 컬럼 구성

| 컬럼             | 설명          |
| ---------------- | ------------- |
| purchase_id      | 고유 ID       |
| user_id          | 구매자        |
| timestamp        | 구매 시점     |
| menu_id          | 구매한 메뉴   |
| price            | 지불 금액     |
| category         | 메뉴 카테고리 |
| experiment_group | A/B 그룹      |
| device           | iOS/Android   |
| channel          | 유입 경로     |
