# 🚀 배포 가이드

이 가이드는 React + FastAPI 풀스택 앱을 **Vercel (프론트엔드)**와 **Render (백엔드)**에 배포하는 방법을 설명합니다.

---

## 📋 **사전 준비**

### 1. GitHub 리포지토리 준비
```bash
cd investment-advisor-fullstack
git init
git add .
git commit -m "🚀 Initial commit: React + FastAPI 풀스택 앱"
git branch -M main
git remote add origin https://github.com/yooooongsung/investment-advisor.git
git push -u origin main
```

### 2. 필요한 계정
- ✅ [GitHub](https://github.com) 계정
- ✅ [Vercel](https://vercel.com) 계정 (GitHub 연동)
- ✅ [Render](https://render.com) 계정 (GitHub 연동)
- ✅ Databricks Personal Access Token

---

## 🔷 **1단계: Backend 배포 (Render)**

### A. Render.com 설정

1. **Render.com 로그인**
   - https://render.com 접속
   - GitHub 계정으로 로그인

2. **New Web Service 생성**
   - Dashboard → **New** → **Web Service**
   - **Connect GitHub repository** 선택
   - `investment-advisor` 리포지토리 선택

3. **서비스 설정**
   ```
   Name: investment-advisor-api
   Region: Oregon (US West)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Plan 선택**
   - **Free** 선택 (무료 티어)
   - 750시간/월 제공

### B. 환경 변수 설정

**Dashboard → Environment 탭**에서 다음 변수 추가:

```bash
# Databricks 설정
DATABRICKS_SERVER_HOSTNAME=dbc-00f9187e-c67a.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/0fb9e42986df6d4b
DATABRICKS_ACCESS_TOKEN=your-databricks-token-here
DATABRICKS_CATALOG=default

# JWT Secret Key (랜덤 생성 권장)
SECRET_KEY=your-super-secret-key-change-this-in-production

# CORS Origins (Vercel URL 추가 필요 - 프론트엔드 배포 후)
CORS_ORIGINS=["http://localhost:3000"]
```

**⚠️ 중요**: `DATABRICKS_ACCESS_TOKEN`을 실제 토큰으로 교체하세요!

### C. 배포 시작

- **Create Web Service** 버튼 클릭
- 빌드 시작 (약 3-5분 소요)
- 배포 완료 후 URL 확인: `https://investment-advisor-api.onrender.com`

### D. API 테스트

배포된 Backend URL에 접속:
```
https://your-app.onrender.com/health
```

응답:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": 1714032000.123
}
```

API 문서:
```
https://your-app.onrender.com/docs
```

---

## 🔷 **2단계: Frontend 배포 (Vercel)**

### A. Vercel 설정

1. **Vercel.com 로그인**
   - https://vercel.com 접속
   - GitHub 계정으로 로그인

2. **New Project 생성**
   - Dashboard → **Add New** → **Project**
   - **Import Git Repository** 선택
   - `investment-advisor` 리포지토리 선택

3. **프로젝트 설정**
   ```
   Project Name: investment-advisor-frontend
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm run build (자동 감지)
   Output Directory: build (자동 감지)
   Install Command: npm install (자동 감지)
   ```

### B. 환경 변수 설정

**Configure Project → Environment Variables**:

```bash
REACT_APP_API_URL=https://your-backend-app.onrender.com
```

**⚠️ 중요**: 
- Render에서 배포한 Backend URL로 교체하세요!
- `https://` 포함해야 합니다!

### C. 배포 시작

- **Deploy** 버튼 클릭
- 빌드 & 배포 시작 (약 1-2분 소요)
- 배포 완료 후 URL 확인: `https://your-app.vercel.app`

---

## 🔷 **3단계: CORS 업데이트**

Frontend가 배포되면 Backend의 CORS 설정을 업데이트해야 합니다!

### Render Dashboard에서:

1. **Backend 서비스** 선택
2. **Environment** 탭
3. `CORS_ORIGINS` 변수 찾기
4. **값 수정**:
   ```json
   ["http://localhost:3000","https://your-app.vercel.app"]
   ```
5. **Save Changes** 클릭
6. 자동 재배포 시작 (1-2분)

**⚠️ 중요**: Vercel URL을 정확히 입력하세요!

---

## 🎉 **배포 완료!**

### ✅ 최종 체크리스트

- [ ] Backend API가 정상 작동 (`/health` 엔드포인트 확인)
- [ ] Frontend가 Backend API를 호출할 수 있음
- [ ] 로그인/회원가입 작동
- [ ] 시장 데이터 표시
- [ ] AI 리포트 조회 작동
- [ ] Multi Agent 트리거 버튼 작동

### 🔗 배포된 URL

- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-app.onrender.com`
- **API Docs**: `https://your-app.onrender.com/docs`

---

## 🔧 **문제 해결**

### 1. Backend 빌드 실패

**문제**: `ModuleNotFoundError` 또는 `ImportError`

**해결**:
- `backend/requirements.txt` 확인
- Python 버전 확인 (3.11 권장)
- Render 로그 확인: Dashboard → Logs 탭

### 2. Frontend 빌드 실패

**문제**: `npm install` 실패 또는 빌드 에러

**해결**:
- `frontend/package.json` 확인
- Node 버전 확인 (18.x 이상)
- Vercel 로그 확인: Dashboard → Deployments → 로그 보기

### 3. CORS 에러

**문제**: 브라우저 콘솔에 `CORS policy` 에러

**해결**:
- Render 환경 변수 `CORS_ORIGINS`에 Vercel URL 추가
- `https://` 포함 확인
- 대소문자 정확히 입력
- 배포 후 Backend 재시작

### 4. API 연결 실패

**문제**: Frontend에서 API 호출 실패

**해결**:
- Vercel 환경 변수 `REACT_APP_API_URL` 확인
- Render Backend URL이 정확한지 확인
- Network 탭에서 요청 URL 확인 (F12)

### 5. Databricks 연결 실패

**문제**: `INSUFFICIENT_PERMISSIONS` 또는 `Connection timeout`

**해결**:
- Personal Access Token 유효성 확인
- SQL Warehouse가 실행 중인지 확인
- Warehouse ID가 정확한지 확인

---

## 📊 **모니터링**

### Render (Backend)

- **Logs**: Dashboard → 서비스 → Logs
- **Metrics**: Dashboard → 서비스 → Metrics
- **Health**: `/health` 엔드포인트 모니터링

### Vercel (Frontend)

- **Analytics**: Dashboard → 프로젝트 → Analytics
- **Logs**: Dashboard → 프로젝트 → Deployments → 로그
- **Speed Insights**: 성능 모니터링

---

## 🔄 **자동 배포 (CD)**

### GitHub Push → 자동 배포

두 플랫폼 모두 **GitHub 연동**으로 자동 배포 지원:

```bash
# 코드 수정 후
git add .
git commit -m "✨ 새 기능 추가"
git push origin main

# → Vercel & Render가 자동으로 감지하고 재배포!
```

- **Vercel**: 모든 커밋마다 자동 배포 (1-2분)
- **Render**: 모든 커밋마다 자동 배포 (3-5분)

---

## 💰 **비용**

| 서비스 | 플랜 | 비용 | 제약사항 |
|--------|------|------|----------|
| **Vercel** | Free | $0 | 100GB 대역폭/월 |
| **Render** | Free | $0 | 750시간/월, 15분 idle 후 sleep |
| **Databricks** | 기존 | 변동 | 기존 사용량 유지 |

**총 추가 비용: $0** ✅

---

## 🎯 **추가 최적화**

### 1. Render Sleep 방지

Render 무료 티어는 15분 비활성 후 sleep 모드:

**해결책**: 
- UptimeRobot 같은 무료 모니터링 서비스로 5분마다 `/health` 호출
- 또는 Frontend에서 주기적으로 health check

### 2. CDN & 캐싱

Vercel은 자동으로 CDN 제공:
- 정적 파일 자동 캐싱
- 이미지 최적화
- 전 세계 엣지 서버

### 3. 환경별 설정

```bash
# 개발 환경
REACT_APP_API_URL=http://localhost:8000

# 프로덕션 환경
REACT_APP_API_URL=https://your-app.onrender.com
```

---

## 🆘 **지원**

문제가 해결되지 않으면:

1. **GitHub Issues** 생성
2. **Render Community** 포럼
3. **Vercel Discord** 채널
4. **Databricks Documentation** 참조

---

**🎉 축하합니다! 풀스택 AI 투자 비서 앱 배포 완료!**
