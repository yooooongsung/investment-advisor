import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from databricks import sql
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import requests

# 페이지 설정
st.set_page_config(
    page_title="AI 투자 비서",
    page_icon="💰",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.big-title {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(120deg, #1f77b4, #ff7f0e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 3rem;
}
</style>
""", unsafe_allow_html=True)

# 인증 설정 (간단한 버전 - 실제로는 DB에 저장)
credentials = {
    'usernames': {
        'demo': {
            'name': '데모 사용자',
            'password': st.secrets.get('DEMO_PASSWORD', 'demo123'),  # 실제로는 해시화
            'age': 30,
            'investment_style': '중립',
            'investment_goal': '장기 자산 증식 (3년+)',
            'budget': '1,000만원 ~ 5,000만원',
            'experience': '1-3년'
        }
    }
}

# Databricks 연결 함수
@st.cache_resource
def get_databricks_connection():
    """Databricks SQL Warehouse에 연결"""
    try:
        connection = sql.connect(
            server_hostname=st.secrets["DATABRICKS_HOST"].replace("https://", ""),
            http_path=f"/sql/1.0/warehouses/{st.secrets['DATABRICKS_WAREHOUSE_ID']}",
            access_token=st.secrets["DATABRICKS_TOKEN"]
        )
        return connection
    except Exception as e:
        st.error(f"⚠️ Databricks 연결 실패: {e}")
        return None

# Multi Agent 실행 함수
def trigger_multi_agent():
    """Databricks Jobs API를 통해 Multi Agent 노트북 실행"""
    try:
        job_id = 32251191378772  # Daily Multi Agent Analysis Job ID
        
        url = f"{st.secrets['DATABRICKS_HOST']}/api/2.1/jobs/run-now"
        headers = {
            "Authorization": f"Bearer {st.secrets['DATABRICKS_TOKEN']}",
            "Content-Type": "application/json"
        }
        data = {"job_id": job_id}
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            run_id = response.json().get('run_id')
            return True, f"Multi Agent 분석 시작! (Run ID: {run_id})"
        else:
            return False, f"실행 실패: {response.text}"
            
    except Exception as e:
        return False, f"에러 발생: {str(e)}"

# 시장 데이터 가져오기
@st.cache_data(ttl=600)  # 10분 캐시
def fetch_market_data():
    """Databricks에서 시장 데이터 가져오기"""
    conn = get_databricks_connection()
    
    demo_data = {
        "KOSPI": {"price": 6388.47, "change": 2.72, "rsi": 75.9, "signal": "⚠️ 과매수"},
        "KOSDAQ": {"price": 1179.03, "change": 0.36, "rsi": 61.9, "signal": "✅ 정상"},
        "NASDAQ": {"price": 24404.39, "change": -0.26, "rsi": 98.3, "signal": "⚠️ 과매수"},
        "BITCOIN": {"price": 76236.01, "change": 0.48, "rsi": 62.1, "signal": "✅ 정상"}
    }
    
    if conn is None:
        return demo_data
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT asset, close, rsi, signals
            FROM default.market_signals_summary
        """)
        results = cursor.fetchall()
        cursor.close()
        
        if not results:
            return demo_data
        
        market_data = {}
        asset_mapping = {
            'kospi_index': 'KOSPI',
            'kosdaq_index': 'KOSDAQ',
            'nasdaq_index': 'NASDAQ',
            'bitcoin': 'BITCOIN'
        }
        
        for row in results:
            asset_name = asset_mapping.get(row[0], row[0].upper())
            market_data[asset_name] = {
                "price": float(row[1]),
                "change": 0.0,  # 계산 필요
                "rsi": float(row[2]),
                "signal": row[3]
            }
        
        return market_data if market_data else demo_data
        
    except Exception as e:
        st.warning(f"데이터 로드 실패: {e}")
        return demo_data

# AI 분석 리포트 가져오기
@st.cache_data(ttl=600)
def fetch_ai_report():
    """Databricks에서 최신 AI 분석 리포트 가져오기"""
    conn = get_databricks_connection()
    
    if conn is None:
        return "AI 분석 리포트를 불러올 수 없습니다."
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT report, date
            FROM default.investment_reports
            ORDER BY date DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return f"**{result[1]} AI 분석**\n\n{result[0]}"
        else:
            return "최신 AI 분석 리포트가 없습니다. Multi Agent 실행 버튼을 눌러주세요."
            
    except Exception as e:
        return f"리포트 로드 실패: {e}"

# 세션 스테이트 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# 헤더
st.markdown('<div class="big-title">💰 AI 투자 비서</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">당신만의 맞춤형 투자 전략을 찾아드립니다</div>', unsafe_allow_html=True)

# 로그인/회원가입 UI (간단한 버전)
if not st.session_state.authenticated:
    st.markdown("---")
    
    tab_login, tab_signup = st.tabs(["🔐 로그인", "📝 회원가입"])
    
    with tab_login:
        st.subheader("로그인")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("사용자 이름", key="login_username")
            password = st.text_input("비밀번호", type="password", key="login_password")
            
            if st.button("로그인", use_container_width=True):
                # 간단한 인증 (실제로는 DB 조회)
                if username == "demo" and password == "demo123":
                    st.session_state.authenticated = True
                    st.session_state.user_profile = credentials['usernames']['demo']
                    st.success("✅ 로그인 성공!")
                    st.rerun()
                else:
                    st.error("❌ 사용자 이름 또는 비밀번호가 틀렸습니다")
    
    with tab_signup:
        st.subheader("회원가입")
        st.info("💡 데모 버전: 현재는 로그인 기능만 제공됩니다. (ID: demo, PW: demo123)")
        
else:
    # 로그인 후 화면
    profile = st.session_state.user_profile
    
    # 사이드바
    with st.sidebar:
        st.header(f"👤 {profile['name']}님")
        st.write(f"**나이:** {profile['age']}세")
        st.write(f"**투자 성향:** {profile['investment_style']}")
        st.write(f"**투자 목적:** {profile['investment_goal']}")
        st.write(f"**예산:** {profile['budget']}")
        st.write(f"**경험:** {profile['experience']}")
        
        st.markdown("---")
        
        # Multi Agent 실행 버튼 추가! ⭐
        st.subheader("🤖 AI 분석 실행")
        if st.button("🚀 Multi Agent 실행", use_container_width=True, type="primary"):
            with st.spinner("Multi Agent 분석 실행 중..."):
                success, message = trigger_multi_agent()
                if success:
                    st.success(message)
                    st.info("💡 3-5분 후 새로고침하면 최신 분석을 볼 수 있습니다")
                    # 캐시 초기화
                    fetch_ai_report.clear()
                else:
                    st.error(message)
        
        st.markdown("---")
        
        if st.button("🚪 로그아웃"):
            st.session_state.authenticated = False
            st.session_state.user_profile = {}
            st.rerun()
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📊 시장 현황", "🎯 맞춤 분석", "📈 추천 전략"])
    
    # TAB 1: 시장 현황
    with tab1:
        st.header("📊 현재 시장 현황")
        st.info("💡 실시간 데이터는 Databricks에서 자동 업데이트됩니다 (매일 오전 9시)")
        
        market_data = fetch_market_data()
        
        cols = st.columns(4)
        for idx, (asset, data) in enumerate(market_data.items()):
            with cols[idx]:
                st.metric(
                    label=f"{asset}",
                    value=f"{data['price']:,.2f}",
                    delta=f"{data['change']:+.2f}%"
                )
                st.caption(f"RSI: {data['rsi']:.1f} {data['signal']}")
        
        st.markdown("---")
        
        st.subheader("🤖 AI 데일리 분석")
        ai_report = fetch_ai_report()
        st.success(ai_report)
        
        # 새로고침 버튼
        if st.button("🔄 최신 데이터 새로고침"):
            fetch_market_data.clear()
            fetch_ai_report.clear()
            st.rerun()
    
    # TAB 2 & 3: 기존 코드 유지 (간략화)
    with tab2:
        st.header(f"🎯 {profile['name']}님을 위한 맞춤 분석")
        st.info("사용자 프로필 기반 맞춤 분석을 제공합니다")
        
        # 파이 차트 예시
        allocation = {"국내 주식": 35, "해외 주식": 25, "채권": 20, "현금": 20}
        fig = go.Figure(data=[go.Pie(labels=list(allocation.keys()), values=list(allocation.values()))])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("📈 구체적 행동 전략")
        st.info("투자 성향에 맞는 추천 전략을 제공합니다")
        
        recommendations = pd.DataFrame({
            "종목": ["KODEX 200", "TIGER 미국S&P500", "삼성전자우", "KB금융"],
            "시장": ["ETF", "ETF", "KOSPI", "KOSPI"],
            "추천 이유": ["시장 평균 수익", "해외 분산", "안정 배당", "금융주 저평가"]
        })
        st.dataframe(recommendations, use_container_width=True, hide_index=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>💡 본 서비스는 투자 참고용이며, 투자 판단의 책임은 본인에게 있습니다.</p>
    <p>🤖 Powered by Databricks AI & Multi-Agent System</p>
</div>
""", unsafe_allow_html=True)
