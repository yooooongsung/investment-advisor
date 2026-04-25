# 💰 AI 투자 비서

사용자 맞춤형 투자 전략을 제공하는 AI 기반 투자 비서 웹앱

## 🌟 주요 기능

* **사용자 프로필 분석**: 나이, 투자 성향, 목적, 예산 기반 맞춤 분석
* **시장 현황**: KOSPI, KOSDAQ, NASDAQ, Bitcoin 실시간 분석
* **자산 배분 추천**: 투자 성향별 최적 포트폴리오 제안
* **구체적 종목 추천**: 실행 가능한 투자 전략 제공

## 🚀 로컬 실행 방법

```bash
# 1. 저장소 클론
git clone <your-repo-url>
cd investment-advisor

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 앱 실행
streamlit run app.py
```

앱이 `http://localhost:8501`에서 실행됩니다.

## ☁️ Streamlit Cloud 배포

1. GitHub에 코드 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud) 접속
3. "New app" 클릭
4. GitHub 저장소 연결
5. `app.py` 선택
6. Deploy!

## 🔧 기술 스택

* **Frontend**: Streamlit
* **Data Visualization**: Plotly
* **Backend**: Python
* **Data Source**: Databricks (선택적)

## 📊 데이터 소스

현재는 데모 데이터를 사용하지만, Databricks REST API를 통해 실시간 데이터로 업그레이드 가능합니다.

### Databricks 연동 (선택)

```python
# Databricks REST API를 통한 데이터 가져오기
import requests

def fetch_market_data():
    # TODO: Databricks SQL Warehouse REST API 호출
    pass
```

## ⚠️ 면책 조항

본 서비스는 투자 참고용이며, 실제 투자 결정의 책임은 사용자 본인에게 있습니다.

## 📝 라이선스

MIT License

## 👨‍💻 개발자

Powered by Databricks AI & Multi-Agent System
