# RECODE OF LEAGUE OF LEGEND

**AI를 이용한 LoL(League of Legends) 전적 사이트**  
AI 기반의 승률 예측 서비스 개발 프로젝트

---

## 📌 프로젝트 개요

- **프로젝트명**: RECODE OF LEAGUE OF LEGEND
- **목표**:  
  - LoL 유저의 전적 데이터 분석
  - AI로 승률 예측 모델 구축
  - 웹을 통한 데이터 제공 및 시각화
- **팀원 및 역할**
  - 김영현 (YoungHyeon1) - 팀장, AWS 구축
  - 강동균 (DongGyunKang) - Front-End 개발
  - 홍태의 (Undery33) - AI 개발, 자료 작성
  - 김동욱 (YoungHyeon1) - Back-End 개발

---

## 🛠 사용 기술

### AI/ML
- PyTorch Tabular
- Transformer 기반 모델
- Multihead Attention
- TabTransformer 구조 비교
- Feature Engineering 및 전처리
  - Null/NaN 제거
  - 범주형/수치형 구분 전처리
  - Label Encoding
  - Median Imputation
  - 불필요 컬럼 제거

### Back-End
- Python
- FastAPI
- SQLAlchemy
- Alembic (DB Migration)

### Front-End
- 기술 스택 명시되지 않음 (PDF 기준)

### Infrastructure
- AWS
  - VPC
  - EC2
  - Lambda
  - Fargate
  - RDS
  - S3
  - SNS
  - Secrets Manager
  - IGW/NAT Gateway
- Docker / Containers
- BastionHost

---

## ⚙️ 데이터 구성

- Riot API 사용
  - LEAGUE-V4
  - SUMMONER-V4
  - MATCH-V5
- 데이터 샘플
  - 총 6,690,481 rows
  - 총 60 columns
  - 범주형 데이터: 25개
  - 수치형 데이터: 35개
- 주요 컬럼 예시
  - champion
  - tier
  - position
  - teamId
  - kill / death / assist
  - gold
  - level
  - items
  - target
  - win

---

## 🗄 데이터베이스 설계

### 주요 테이블
- **Matches**
- **Users**
- **Users_Matches**
- **League**
- **Users_Leagues**
- **Request**
- **Task**
- **APIKeyUsage**

### Alembic Migration Log 예시
| Revision ID | Description |
|-------------|-------------|
| 060ccd07_add_riot_table | Riot API Key 관리용 테이블 생성 |
| 0d57079_fix_league_user | League와 users_leagues 필드 수정 |
| 4db5e2a_request_table | Request/Task 관리 테이블 생성 |
| A83bfc7_fix_leagues | Users_leagues 생성, league 정규화 |
| E2753dc_init_table | Matches, users, users_matches 테이블 초기 생성 |
| Ed921c9_fix_users_add | League, users 테이블 생성 및 정규화 |

---

## 🔎 AI 모델링

### 데이터 전처리
- 중복 컬럼 제거
- Null 값 제거 및 대체
- bool → int 변환
- Label Encoding
- 데이터 타입 통일

### 모델 성능 (예시)
- Loss: 0.1123
- Accuracy: 0.9664
- F1 Score: 0.9663
- AUC-ROC: 0.9940

### 주의사항
- 데이터 양 부족 시 과적합 가능성
- 데이터 누수 여부 확인 필요
- 편향된 데이터는 성능 과대평가 유발

---

## 🗂 프로젝트 타임라인

- 4/1: 계획 작성
- 5/1: API 크롤링, AI 코드 작성/학습
- 6/1: Front-End / Back-End 개발
- GIT 레포지토리 생성
- 최종 보고서 작성

---

## 📈 Hyperparameters (예시)

| Parameter         | Value       |
|--------------------|-------------|
| Batch Size         | 512         |
| Embedding Size     | 32          |
| Heads              | 4           |
| Layers             | 6           |
| Dropout Rate       | 0.2         |
| Learning Rate      | 0.00001     |
| Weight Decay / L2  | 0.01        |

---

## 💻 System Spec

- CPU: Ryzen 5 3600 6-Core
- GPU: GeForce RTX 3060 Ti
- CUDA 지원
- IDE 환경에서 개발

---

## 🔗 Riot API 사용 예시

```json
{
  "tier": "CHALLENGER",
  "summonerId": "eN2A3vyude4eCiG0JDoMzVp0cAtGZ4dLFv4PdTVO7FHEMSIOiBZzAApRzA",
  "puuid": "yT0ek4ED57brX47eLe5M7gFX8GRr3M0FTesKlNK5Vw2QRh0_bn-lH-tF55-5L08ytrQYpjVJEpIlQw",
  "gameId": 6432696459,
  "gameDuration": 2288,
  "gameEndTimestamp": 1680394818355
}
```

## 👥 Contributors

* 김영현 (YoungHyeon1)

* 강동균 (DongGyunKang)

* 홍태의 (Undery33)

* 김동욱 (YoungHyeon1)

---

> 본 프로젝트는 Riot API 데이터를 기반으로 AI로 게임 전적을 분석 및 승률을 예측하며, AWS 클라우드 인프라 위에서 동작하는 웹 서비스를 개발한 팀 프로젝트입니다.