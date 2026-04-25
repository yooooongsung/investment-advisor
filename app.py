import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from databricks import sql

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

# 시장 데이터 가져오기
@st.cache_data(ttl=3600)  # 1시간 캐시
def fetch_market_data():
    """Databricks에서 시장 데이터 가져오기"""
    conn = get_databricks_connection()
    
    if conn is None:
        # 연결 실패 시 데모 데이터 반환
        return {
            "KOSPI": {"price": 6388.47, "change": 2.72, "rsi": 75.9, "signal": "⚠️ 과매수"},
            "KOSDAQ": {"price": 1179.03, "change": 0.36, "rsi": 61.9, "signal": "✅ 정상"},
            "NASDAQ": {"price": 24404.39, "change": -0.26, "rsi": 98.3, "signal": "⚠️ 과매수"},
            "BITCOIN": {"price": 76236.01, "change": 0.48, "rsi": 62.1, "signal": "✅ 정상"}
        }
    
    try:
        cursor = conn.cursor()
        
        # market_signals_summary 테이블에서 최신 데이터 가져오기
        query = """
        SELECT 
            asset,
            close as price,
            ((close - LAG(close) OVER (PARTITION BY asset ORDER BY date)) / LAG(close) OVER (PARTITION BY asset ORDER BY date)) * 100 as change,
            rsi,
            CASE 
                WHEN rsi > 70 THEN '⚠️ 과매수'
                WHEN rsi < 30 THEN '⚠️ 과매도'
                ELSE '✅ 정상'
            END as signal
        FROM default.market_signals_summary
        WHERE date = (SELECT MAX(date) FROM default.market_signals_summary)
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        # 자산 이름 매핑
        asset_mapping = {
            'kospi_index': 'KOSPI',
            'kosdaq_index': 'KOSDAQ',
            'nasdaq_index': 'NASDAQ',
            'bitcoin': 'BITCOIN'
        }
        
        market_data = {}
        for row in results:
            asset_name = asset_mapping.get(row[0], row[0].upper())
            market_data[asset_name] = {
                "price": float(row[1]) if row[1] else 0,
                "change": float(row[2]) if row[2] else 0,
                "rsi": float(row[3]) if row[3] else 50,
                "signal": row[4] if row[4] else "✅ 정상"
            }
        
        return market_data if market_data else {
            "KOSPI": {"price": 6388.47, "change": 2.72, "rsi": 75.9, "signal": "⚠️ 과매수"},
            "KOSDAQ": {"price": 1179.03, "change": 0.36, "rsi": 61.9, "signal": "✅ 정상"},
            "NASDAQ": {"price": 24404.39, "change": -0.26, "rsi": 98.3, "signal": "⚠️ 과매수"},
            "BITCOIN": {"price": 76236.01, "change": 0.48, "rsi": 62.1, "signal": "✅ 정상"}
        }
        
    except Exception as e:
        st.warning(f"⚠️ 데이터 로드 실패, 데모 데이터 사용 중: {e}")
        return {
            "KOSPI": {"price": 6388.47, "change": 2.72, "rsi": 75.9, "signal": "⚠️ 과매수"},
            "KOSDAQ": {"price": 1179.03, "change": 0.36, "rsi": 61.9, "signal": "✅ 정상"},
            "NASDAQ": {"price": 24404.39, "change": -0.26, "rsi": 98.3, "signal": "⚠️ 과매수"},
            "BITCOIN": {"price": 76236.01, "change": 0.48, "rsi": 62.1, "signal": "✅ 정상"}
        }

# AI 분석 리포트 가져오기
@st.cache_data(ttl=3600)
def fetch_ai_report():
    """Databricks에서 최신 AI 분석 리포트 가져오기"""
    conn = get_databricks_connection()
    
    if conn is None:
        return """**2026-04-21 시장 요약**
        
- KOSPI와 NASDAQ이 과매수 구간 진입
- 단기 조정 가능성 존재
- 변동성 확대 예상
- 안전 자산 비중 확대 권장
"""
    
    try:
        cursor = conn.cursor()
        
        # 최신 리포트 가져오기
        query = """
        SELECT report, date
        FROM default.investment_reports
        WHERE date = (SELECT MAX(date) FROM default.investment_reports)
        ORDER BY date DESC
        LIMIT 1
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return f"**{result[1]} AI 분석**\n\n{result[0]}"
        else:
            return """**최신 AI 분석**
        
- 시장 데이터 분석 중입니다
- 매일 오전 9시 업데이트됩니다
"""
            
    except Exception as e:
        st.warning(f"⚠️ AI 리포트 로드 실패: {e}")
        return """**데모 AI 분석**
        
- KOSPI와 NASDAQ이 과매수 구간 진입
- 단기 조정 가능성 존재
- 변동성 확대 예상
"""

# 세션 스테이트 초기화
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# 헤더
st.markdown('<div class="big-title">💰 AI 투자 비서</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">당신만의 맞춤형 투자 전략을 찾아드립니다</div>', unsafe_allow_html=True)

# 사용자 입력이 없으면 입력 폼 표시
if not st.session_state.analyzed:
    st.markdown("---")
    st.header("📝 투자 프로필 입력")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("이름", placeholder="홍길동")
        age = st.number_input("나이", min_value=19, max_value=100, value=30)
        investment_style = st.select_slider(
            "투자 성향",
            options=["매우 보수적", "보수적", "중립", "공격적", "매우 공격적"],
            value="중립"
        )
    
    with col2:
        investment_goal = st.selectbox(
            "투자 목적",
            ["단기 수익 (1년 이내)", "중기 성장 (1-3년)", "장기 자산 증식 (3년+)", "안정적 배당 수익", "은퇴 자금 마련"]
        )
        budget = st.selectbox(
            "투자 가능 금액",
            ["100만원 미만", "100만원 ~ 500만원", "500만원 ~ 1,000만원", "1,000만원 ~ 5,000만원", "5,000만원 이상"]
        )
        experience = st.selectbox(
            "투자 경험",
            ["없음 (처음)", "1년 미만", "1-3년", "3-5년", "5년 이상"]
        )
    
    st.markdown("---")
    
    if st.button("🚀 AI 분석 시작", type="primary", use_container_width=True):
        if name:
            st.session_state.user_profile = {
                "name": name,
                "age": age,
                "investment_style": investment_style,
                "investment_goal": investment_goal,
                "budget": budget,
                "experience": experience
            }
            st.session_state.analyzed = True
            st.rerun()
        else:
            st.error("이름을 입력해주세요!")

else:
    # 분석 결과 표시
    profile = st.session_state.user_profile
    
    # 사이드바에 프로필 요약
    with st.sidebar:
        st.header(f"👤 {profile['name']}님의 프로필")
        st.write(f"**나이:** {profile['age']}세")
        st.write(f"**투자 성향:** {profile['investment_style']}")
        st.write(f"**투자 목적:** {profile['investment_goal']}")
        st.write(f"**예산:** {profile['budget']}")
        st.write(f"**경험:** {profile['experience']}")
        
        if st.button("🔄 다시 입력"):
            st.session_state.analyzed = False
            st.rerun()
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📊 시장 현황", "🎯 맞춤 분석", "📈 추천 전략"])
    
    # TAB 1: 시장 현황 (제너럴 리포트)
    with tab1:
        st.header("📊 현재 시장 현황")
        st.info("💡 실시간 데이터는 Databricks에서 자동 업데이트됩니다 (매일 오전 9시)")
        
        # Databricks에서 실시간 데이터 가져오기
        with st.spinner("시장 데이터 로딩 중..."):
            market_data = fetch_market_data()
        
        cols = st.columns(4)
        for idx, (asset, data) in enumerate(market_data.items()):
            with cols[idx]:
                delta_color = "normal" if data['change'] >= 0 else "inverse"
                st.metric(
                    label=f"{asset}",
                    value=f"{data['price']:,.2f}",
                    delta=f"{data['change']:+.2f}%"
                )
                st.caption(f"RSI: {data['rsi']:.1f} {data['signal']}")
        
        st.markdown("---")
        
        # AI 데일리 분석
        st.subheader("🤖 AI 데일리 분석")
        with st.spinner("AI 분석 로딩 중..."):
            ai_report = fetch_ai_report()
        st.success(ai_report)
    
    # TAB 2: 맞춤 분석
    with tab2:
        st.header(f"🎯 {profile['name']}님을 위한 맞춤 분석")
        
        # 투자 성향 점수화
        style_score = {
            "매우 보수적": 1, "보수적": 2, "중립": 3, "공격적": 4, "매우 공격적": 5
        }[profile['investment_style']]
        
        # 연령대별 추천
        if profile['age'] < 30:
            age_advice = "젊은 나이에는 공격적 투자가 가능합니다. 장기 성장주 중심으로 포트폴리오를 구성하세요."
        elif profile['age'] < 40:
            age_advice = "경력을 쌓는 시기입니다. 중립적 포트폴리오로 안정성과 수익성을 균형있게 추구하세요."
        elif profile['age'] < 50:
            age_advice = "중년기에는 안정성을 중시하되, 성장 가능성도 고려하세요."
        else:
            age_advice = "은퇴를 앞둔 시기입니다. 안전 자산 비중을 높이고 배당주에 집중하세요."
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 투자 프로필 분석")
            st.write(f"**연령대 조언:** {age_advice}")
            st.write(f"**투자 성향 점수:** {style_score}/5")
            
            if style_score >= 4:
                risk_text = "고위험 고수익 전략이 적합합니다."
            elif style_score >= 3:
                risk_text = "중위험 중수익 전략이 적합합니다."
            else:
                risk_text = "저위험 안정 수익 전략이 적합합니다."
            
            st.write(f"**추천 전략:** {risk_text}")
        
        with col2:
            st.subheader("💼 추천 자산 배분")
            
            # 성향 기반 배분
            if style_score >= 4:
                allocation = {"국내 성장주": 40, "해외 주식": 30, "비트코인": 20, "현금": 10}
            elif style_score >= 3:
                allocation = {"국내 주식": 35, "해외 주식": 25, "채권": 20, "현금": 20}
            else:
                allocation = {"채권": 40, "배당주": 30, "현금": 20, "금": 10}
            
            # 파이 차트
            fig = go.Figure(data=[go.Pie(labels=list(allocation.keys()), values=list(allocation.values()))])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("⚠️ 리스크 경고")
        
        if style_score >= 4:
            st.warning("""
            - 고위험 투자는 큰 손실 가능성이 있습니다
            - 분산 투자를 필수적으로 실행하세요
            - 투자 금액의 50% 이상을 단일 자산에 집중하지 마세요
            """)
        else:
            st.info("""
            - 안정적 투자도 시장 변동성에 영향을 받습니다
            - 정기적으로 포트폴리오를 점검하세요
            - 장기 투자 관점을 유지하세요
            """)
    
    # TAB 3: 추천 전략
    with tab3:
        st.header("📈 구체적 행동 전략")
        
        st.subheader("🎯 이번 주 추천 액션")
        
        # 성향별 추천
        if style_score >= 4:
            st.success("""
            **공격적 투자자를 위한 전략:**
            
            1️⃣ **단기 매매 (30%)**
               - 기술주 중심 (반도체, AI)
               - 손절/익절 라인 명확히 설정
            
            2️⃣ **성장주 장기 보유 (40%)**
               - 미국 빅테크 (NASDAQ)
               - 국내 대형주 (삼성전자, SK하이닉스)
            
            3️⃣ **대체 투자 (20%)**
               - 비트코인 (변동성 주의)
            
            4️⃣ **현금 보유 (10%)**
               - 급락 시 매수 기회 대비
            """)
            
            st.subheader("📌 추천 종목 (참고용)")
            recommendations = pd.DataFrame({
                "종목": ["삼성전자", "SK하이닉스", "NVIDIA", "Bitcoin"],
                "시장": ["KOSPI", "KOSPI", "NASDAQ", "Crypto"],
                "추천 이유": ["AI 반도체 수요 증가", "메모리 반도체 회복", "AI 리더", "기관 자금 유입"],
                "리스크": ["중국 리스크", "수요 변동성", "고평가 우려", "높은 변동성"]
            })
            
        elif style_score >= 3:
            st.info("""
            **중립 투자자를 위한 전략:**
            
            1️⃣ **안정 성장주 (40%)**
               - 배당 + 성장 가능성 있는 대형주
               - 한국전력, 통신주
            
            2️⃣ **인덱스 펀드 (30%)**
               - KOSPI 200 ETF
               - S&P 500 ETF
            
            3️⃣ **채권 (20%)**
               - 국채, 회사채 혼합
            
            4️⃣ **현금 (10%)**
               - 안전 자산 확보
            """)
            
            recommendations = pd.DataFrame({
                "종목": ["KODEX 200", "TIGER 미국S&P500", "삼성전자우", "KB금융"],
                "시장": ["ETF", "ETF", "KOSPI", "KOSPI"],
                "추천 이유": ["시장 평균 수익", "해외 분산", "안정 배당", "금융주 저평가"],
                "리스크": ["시장 리스크", "환율 변동", "주가 정체", "경기 민감"]
            })
        
        else:
            st.success("""
            **보수적 투자자를 위한 전략:**
            
            1️⃣ **배당주 (40%)**
               - 안정적 배당 기업
               - 통신, 유틸리티
            
            2️⃣ **채권 (40%)**
               - 국채 중심
               - 안전 자산
            
            3️⃣ **금 ETF (10%)**
               - 안전 자산 분산
            
            4️⃣ **현금 (10%)**
               - 유동성 확보
            """)
            
            recommendations = pd.DataFrame({
                "종목": ["KT&G", "한국전력", "국채 3년", "KODEX 골드선물"],
                "시장": ["KOSPI", "KOSPI", "채권", "ETF"],
                "추천 이유": ["높은 배당률", "안정 배당", "안전 자산", "인플레 헤지"],
                "리스크": ["업종 리스크", "전기요금 이슈", "금리 변동", "가격 변동성"]
            })
        
        st.dataframe(recommendations, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.subheader("📅 실행 체크리스트")
        
        checklist = [
            "투자 목표 금액 설정",
            "포트폴리오 배분 결정",
            "종목별 매수 가격대 설정",
            "손절/익절 라인 설정",
            "월 1회 포트폴리오 리뷰 일정 등록",
            "뉴스 알림 설정 (주요 종목)"
        ]
        
        for item in checklist:
            st.checkbox(item, key=f"check_{item}")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>💡 본 서비스는 투자 참고용이며, 투자 판단의 책임은 본인에게 있습니다.</p>
    <p>🤖 Powered by Databricks AI & Multi-Agent System</p>
</div>
""", unsafe_allow_html=True)
