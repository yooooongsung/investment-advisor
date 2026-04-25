# 🤖 AI Investment Advisor - Full Stack Application

React + FastAPI 기반의 **AI 투자 비서 시스템**입니다.

---

## 🏗️ **시스템 아키텍처**

```
User Browser
    ↓ HTTPS
React Frontend (Vercel)
    ↓ REST API (JWT Auth)
FastAPI Backend (Render)
    ↓ databricks-sql-connector
Databricks Unity Catalog
    - default.users (사용자 정보)
    - default.market_signals_summary (시장 데이터)
    - default.investment_reports (AI 분석 리포트)
    ↓ Scheduled Jobs (9:00 AM, 9:30 AM KST)
Multi Agent System (CrewAI + GPT-4)
```

---

## 📦 **프로젝트 구조**

```
investment-advisor-fullstack/
├── frontend/              # React 18 + Material-UI
│   ├── src/
│   │   ├── components/    # MarketOverview, AIReport
│   │   ├── pages/         # Login, Signup, Dashboard
│   │   ├── services/      # API 통신 (Axios)
│   │   ├── contexts/      # AuthContext (JWT 관리)
│   │   └── App.js
│   ├── package.json
│   └── vercel.json        # Vercel 배포 설정
│
├── backend/               # FastAPI + Python 3.11
│   ├── app/
│   │   ├── api/routes/    # Auth, Market, Reports, Multi-Agent
│   │   ├── core/          # Config, Security, Databricks
│   │   ├── models/        # Pydantic 모델
│   │   ├── services/      # UserService
│   │   └── main.py        # FastAPI 앱
│   ├── requirements.txt
│   ├── Dockerfile
│   └── render.yaml        # Render 배포 설정
│
└── README.md
```

---

## 🚀 **로컬 개발 환경 설정**

### 1️⃣ **Backend (FastAPI)**

```bash
cd backend

# 가상환경 생성 및 활성화
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# .env 파일 생성 (아래 참조)
cp .env.example .env
# .env 파일을 열고 Databricks 정보 입력!

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

**Backend .env 설정:**
```bash
DATABRICKS_SERVER_HOSTNAME=dbc-00f9187e-c67a.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/0fb9e42986df6d4b
DATABRICKS_ACCESS_TOKEN=your-token-here
DATABRICKS_CATALOG=default
SECRET_KEY=your-super-secret-key-here
CORS_ORIGINS=["http://localhost:3000"]
```

**API 문서:** http://localhost:8000/docs

---

### 2️⃣ **Frontend (React)**

```bash
cd frontend

# 패키지 설치
npm install

# .env 파일 생성
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# 개발 서버 실행
npm start
```

**Frontend 접속:** http://localhost:3000

---

## ☁️ **배포 가이드**

### 🔷 **Backend → Render (무료)**

1. **Render.com 가입 및 로그인**
   - https://render.com

2. **New Web Service 생성**
   - Connect GitHub repository
   - Select `investment-advisor-fullstack` repo
   - Root Directory: `backend`

3. **환경 변수 설정** (Dashboard → Environment)
   ```
   DATABRICKS_SERVER_HOSTNAME=dbc-00f9187e-c67a.cloud.databricks.com
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/0fb9e42986df6d4b
   DATABRICKS_ACCESS_TOKEN=your-token-here
   SECRET_KEY=random-secure-key-here
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```

4. **Deploy!**
   - Auto-deploy는 자동으로 켜짐
   - Backend URL: `https://your-app.onrender.com`

---

### 🔷 **Frontend → Vercel (무료)**

1. **Vercel.com 가입 및 로그인**
   - https://vercel.com

2. **New Project 생성**
   - Import Git Repository
   - Select `investment-advisor-fullstack`
   - Root Directory: `frontend`
   - Framework Preset: Create React App

3. **환경 변수 설정**
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```

4. **Deploy!**
   - Frontend URL: `https://your-app.vercel.app`

5. **Backend CORS 업데이트**
   - Render Dashboard → Backend → Environment
   - `CORS_ORIGINS`에 Vercel URL 추가
   - Restart Backend

---

## 🎯 **주요 기능**

### ✅ **JWT 기반 로그인 시스템**
- 회원가입 시 bcrypt 비밀번호 해싱
- JWT 토큰 자동 갱신 (7일 유효)
- 페이지 새로고침해도 로그인 유지! ✨

### 📊 **실시간 시장 데이터**
- KOSPI, KOSDAQ, NASDAQ, Bitcoin
- RSI 지표 기반 과매수/과매도 알림
- 일일 수익률 차트

### 🤖 **AI 투자 분석**
- CrewAI + GPT-4 기반 Multi Agent 시스템
- 3명의 AI 에이전트 (시장 분석가, 주식 전문가, 전략가)
- 월요일 특별 기능: 주간 추천 종목 5-7개
- **버튼 한 번으로 AI 분석 실행!**

### 🔐 **보안**
- JWT 인증
- bcrypt 비밀번호 해싱
- CORS 설정
- SQL Injection 방지 (Parameterized queries)

---

## 📅 **자동화 시스템**

Databricks Jobs가 매일 자동 실행됩니다:
- **09:00 AM KST** - 시장 데이터 수집 (Data Storing Notebook)
- **09:30 AM KST** - AI 분석 실행 (Multi Agent Notebook)

---

## 🛠️ **기술 스택**

### Frontend
- React 18
- Material-UI (MUI)
- Recharts
- React Router v6
- Axios
- JWT Decode

### Backend
- FastAPI
- Databricks SQL Connector
- Python-JOSE (JWT)
- Passlib (bcrypt)
- Pydantic v2
- Uvicorn

### Infrastructure
- **Frontend Hosting:** Vercel (Free)
- **Backend Hosting:** Render (Free)
- **Database:** Databricks Unity Catalog
- **Data Processing:** Databricks Notebooks
- **Scheduler:** Databricks Jobs
- **AI:** OpenAI GPT-4 + CrewAI

---

## 📊 **데이터베이스 스키마**

### **default.users**
| 컬럼 | 타입 | 설명 |
|------|------|------|
| username | STRING | 사용자 ID (PK) |
| password_hash | STRING | bcrypt 해시 |
| name | STRING | 이름 |
| age | INT | 나이 |
| investment_style | STRING | 투자 성향 |
| investment_goal | STRING | 투자 목표 |
| budget | INT | 투자 예산 |
| experience | STRING | 투자 경험 |
| created_at | TIMESTAMP | 가입일 |
| updated_at | TIMESTAMP | 수정일 |

### **default.market_signals_summary**
| 컬럼 | 타입 | 설명 |
|------|------|------|
| market | STRING | 시장 (KOSPI, KOSDAQ, ...) |
| date | DATE | 날짜 |
| close | DOUBLE | 종가 |
| rsi | DOUBLE | RSI 지표 |
| daily_return | DOUBLE | 일일 수익률 |
| signal | STRING | 매매 신호 |

### **default.investment_reports**
| 컬럼 | 타입 | 설명 |
|------|------|------|
| report_title | STRING | 리포트 제목 |
| recommendations | STRING | AI 분석 내용 |
| created_at | TIMESTAMP | 생성일 |
| day_of_week | STRING | 요일 |

---

## 🔧 **문제 해결**

### Backend 연결 실패
- `.env` 파일의 Databricks 정보 확인
- Databricks SQL Warehouse가 실행 중인지 확인
- Personal Access Token 유효 기간 확인

### Frontend API 호출 실패
- `.env`의 `REACT_APP_API_URL` 확인
- Backend CORS 설정에 Frontend URL 포함 여부 확인
- 브라우저 Console에서 에러 확인 (F12)

### 로그인 유지 안 됨
- localStorage에 token 저장 확인 (F12 → Application → Local Storage)
- JWT 만료 시간 확인 (기본: 7일)
- Backend `/api/auth/profile` 엔드포인트 테스트

---

## 📝 **라이선스**

MIT License

---

## 👨‍💻 **개발자**

**Yong Sung Mirr**
- Email: mirr001003@hanyang.ac.kr
- GitHub: [@yooooongsung](https://github.com/yooooongsung)

---

## 🙏 **감사의 말**

이 프로젝트는 Databricks, OpenAI, CrewAI의 도움으로 만들어졌습니다!

---

**🚀 Happy Investing with AI!**
