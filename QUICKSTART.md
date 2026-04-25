# ⚡ 빠른 시작 가이드

이 문서는 프로젝트를 **5분 안에** GitHub에 푸시하고 배포를 시작하는 방법을 설명합니다!

---

## 🚀 1단계: GitHub에 푸시 (1분)

### Databricks에서:

1. **GitHub Auto Deploy 노트북** 열기
   - 경로: `/Users/mirr001003@hanyang.ac.kr/GitHub Auto Deploy`

2. **두 번째 셀 실행**
   - "GitHub 전체 프로젝트 푸시" 셀
   - 자동으로 전체 프로젝트를 GitHub에 업로드합니다!

3. **결과 확인**
   - GitHub: https://github.com/yooooongsung/investment-advisor
   - 36개 파일이 업로드되어야 합니다

---

## 🔷 2단계: Backend 배포 (2분)

### Render.com에서:

1. **https://render.com** 로그인 (GitHub 계정)
2. **New → Web Service**
3. 리포지토리 선택: `investment-advisor`
4. 설정:
   ```
   Name: investment-advisor-api
   Root Directory: backend
   Build: pip install -r requirements.txt
   Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```
5. **Environment Variables** 추가:
   ```bash
   DATABRICKS_SERVER_HOSTNAME=dbc-00f9187e-c67a.cloud.databricks.com
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/0fb9e42986df6d4b
   DATABRICKS_ACCESS_TOKEN=your-token-here
   SECRET_KEY=random-secret-key
   CORS_ORIGINS=["http://localhost:3000"]
   ```
6. **Create Web Service** 클릭
7. **URL 복사**: `https://your-app.onrender.com`

---

## 🔷 3단계: Frontend 배포 (1분)

### Vercel.com에서:

1. **https://vercel.com** 로그인 (GitHub 계정)
2. **Add New → Project**
3. 리포지토리 선택: `investment-advisor`
4. 설정:
   ```
   Framework: Create React App
   Root Directory: frontend
   ```
5. **Environment Variable** 추가:
   ```bash
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```
   (2단계에서 복사한 Backend URL 사용!)
6. **Deploy** 클릭
7. **URL 복사**: `https://your-app.vercel.app`

---

## 🔷 4단계: CORS 업데이트 (30초)

### Render Dashboard에서:

1. Backend 서비스 선택
2. **Environment** 탭
3. `CORS_ORIGINS` 값 수정:
   ```json
   ["http://localhost:3000","https://your-app.vercel.app"]
   ```
   (3단계에서 복사한 Frontend URL 사용!)
4. **Save Changes** 클릭
5. 자동 재배포 대기 (1-2분)

---

## ✅ 완료!

### 테스트:

1. Frontend URL 접속: `https://your-app.vercel.app`
2. 회원가입 → 로그인
3. 대시보드 확인
4. AI 리포트 버튼 클릭

### 문제 발생 시:

- **CORS 에러**: 4단계 다시 확인
- **API 연결 실패**: Backend URL 확인
- **500 에러**: Render 로그 확인

---

## 📚 더 자세한 가이드:

- **전체 배포 가이드**: `DEPLOYMENT_GUIDE.md`
- **프로젝트 문서**: `README.md`

---

## 🎉 축하합니다!

당신은 이제 **프로페셔널 풀스택 AI 투자 비서 앱**을 소유하고 있습니다!

**기술 스택:**
- ⚛️ React 18 + Material-UI
- 🐍 FastAPI + Python 3.11
- 📊 Databricks Unity Catalog
- 🤖 Multi Agent AI (CrewAI + GPT-4)
- ☁️ Vercel + Render (무료!)

**총 개발 시간**: 오늘 하루
**총 비용**: $0
**포트폴리오 가치**: 무한대! 🚀
