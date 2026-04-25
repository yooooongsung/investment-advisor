# 🚀 배포 가이드

## 📦 준비물
- GitHub 계정
- Streamlit Cloud 계정 (무료)

---

## 1️⃣ GitHub에 코드 업로드

### 방법 A: GitHub Desktop (초보자 추천)

1. **GitHub Desktop 설치**
   - https://desktop.github.com/ 에서 다운로드

2. **새 저장소 생성**
   - GitHub.com → "+" 버튼 → "New repository"
   - 이름: `ai-investment-advisor`
   - Public으로 설정
   - Create repository

3. **코드 업로드**
   - GitHub Desktop에서 "Add existing repository" 클릭
   - investment-advisor 폴더 선택
   - "Publish repository" 클릭

### 방법 B: Git 명령어 (개발자)

```bash
# 1. investment-advisor 폴더로 이동
cd investment-advisor

# 2. Git 초기화
git init

# 3. 파일 추가
git add .

# 4. 커밋
git commit -m "Initial commit: AI Investment Advisor prototype"

# 5. GitHub 저장소 연결
# (GitHub에서 저장소를 먼저 생성한 후)
git remote add origin https://github.com/<your-username>/ai-investment-advisor.git

# 6. 푸시
git branch -M main
git push -u origin main
```

---

## 2️⃣ Streamlit Cloud 배포

### 단계별 가이드

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인

2. **새 앱 만들기**
   - "New app" 버튼 클릭

3. **저장소 연결**
   - Repository: `<your-username>/ai-investment-advisor`
   - Branch: `main`
   - Main file path: `app.py`

4. **배포 시작**
   - "Deploy!" 버튼 클릭
   - 1-2분 대기

5. **완료!**
   - 자동으로 URL 생성됨
   - 예: `https://ai-investment-advisor.streamlit.app`

---

## 3️⃣ 친구들에게 공유

배포가 완료되면:

1. **URL 복사**
   - Streamlit Cloud에서 자동 생성된 URL 복사

2. **공유**
   - 카카오톡, 이메일 등으로 링크 공유
   - Databricks 계정 없이도 누구나 접속 가능!

3. **커스텀 도메인 (선택)**
   - Streamlit Cloud 유료 플랜에서 가능
   - 예: `invest.yourdomain.com`

---

## 🔧 문제 해결

### 배포 실패 시

1. **로그 확인**
   - Streamlit Cloud에서 "Manage app" → "Logs" 확인

2. **흔한 문제**
   - requirements.txt 오타: 패키지 이름 확인
   - Python 버전: requirements.txt에 `python>=3.8` 추가
   - 파일 경로: app.py가 루트에 있는지 확인

3. **재배포**
   - 코드 수정 후 GitHub에 푸시하면 자동 재배포

---

## 📊 다음 단계 (선택)

### Databricks 실시간 데이터 연동

1. **Databricks API 토큰 생성**
   - Databricks → Settings → Access tokens
   - 토큰 생성 및 복사

2. **Streamlit Secrets 설정**
   - Streamlit Cloud → App settings → Secrets
   - 다음 추가:
     ```toml
     DATABRICKS_HOST = "https://dbc-00f9187e-c67a.cloud.databricks.com"
     DATABRICKS_TOKEN = "your-token-here"
     DATABRICKS_WAREHOUSE_ID = "your-warehouse-id"
     ```

3. **app.py 수정**
   - 데모 데이터 대신 REST API 호출로 변경

---

## ✅ 체크리스트

배포 전:
- [ ] 모든 파일이 GitHub에 푸시되었는지 확인
- [ ] .gitignore가 제대로 작동하는지 확인
- [ ] README.md가 있는지 확인

배포 후:
- [ ] 앱이 정상 작동하는지 테스트
- [ ] 모든 탭이 로드되는지 확인
- [ ] 모바일에서도 테스트
- [ ] 친구들에게 공유!

---

## 💡 팁

* **무료 플랜 제한**: 월 1GB 대역폭, 3개 앱
* **앱 슬립 모드**: 7일 미사용 시 슬립, 접속 시 자동 재시작
* **업데이트**: GitHub에 푸시하면 자동으로 앱 업데이트
* **분석**: Streamlit Cloud에서 방문자 수 확인 가능

---

## 🎉 완료!

이제 당신만의 AI 투자 비서 앱이 전 세계에 공개되었습니다!

**다음 단계:**
- 친구들 피드백 받기
- 기능 개선하기
- Databricks 실시간 데이터 연동하기
- 사용자 데이터 저장 기능 추가하기 (Firebase 등)
