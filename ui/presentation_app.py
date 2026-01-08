import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mock_data import (
    get_mock_priority_list, get_mock_portfolio, get_mock_risk_exposure, get_mock_insights,
    get_overseas_stock_briefing, get_market_one_liners, get_market_briefing_tabs,
    get_house_asset_allocation, get_product_recommendations, get_seeking_alpha_list,
    get_trade_review
)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Streamlit Presentation | Antigravity",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [data-testid="stSidebarContent"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Gradient Background for Headers */
    .main-title {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }

    .sub-title {
        color: #555;
        font-size: 1.5rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }

    /* Card Styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        backdrop-filter: blur(4px);
        margin-bottom: 20px;
    }

    .highlight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* Big Text for Conclusion */
    .conclusion-text {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        line-height: 1.2;
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 50px 0;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 2rem;
        background-color: #4facfe;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00f2fe;
        transform: translateY(-2px);
    }
    
    /* Navigation Simulation */
    .nav-hint {
        position: fixed;
        bottom: 20px;
        right: 20px;
        color: #888;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
if "current_slide" not in st.session_state:
    st.session_state.current_slide = 1

def update_radio_from_slide():
    st.session_state.nav_radio = f"Slide {st.session_state.current_slide}"

def on_radio_change():
    st.session_state.current_slide = int(st.session_state.nav_radio.split(" ")[1])

def next_slide():
    if st.session_state.current_slide < 8:
        st.session_state.current_slide += 1
        update_radio_from_slide()

def prev_slide():
    if st.session_state.current_slide > 1:
        st.session_state.current_slide -= 1
        update_radio_from_slide()

# Sidebar Navigation
with st.sidebar:
    st.title("🗂 Slides")
    # Initialize nav_radio if not present to avoid KeyError
    if "nav_radio" not in st.session_state:
        update_radio_from_slide()
        
    st.radio("Go to Slide", 
        [f"Slide {i}" for i in range(1, 9)],
        key="nav_radio",
        on_change=on_radio_change
    )
    
    st.divider()
    st.info("Use Sidebar to navigate or Sidebar handles below.")

# ==============================================================================
# SLIDE 1: LIVE APP ENTRY
# ==============================================================================
if st.session_state.current_slide == 1:
    st.markdown('<h1 class="main-title">AI PB Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">This is a live Streamlit app</p>', unsafe_allow_html=True)
    
    # Render a preview of the actual dashboard logic here
    st.info("🚀 Presenter Message: \"지금 보고 계신 화면이 오늘 강의의 결과물입니다. PPT가 아니라, 이미 배포된 웹 앱에서 발표를 시작합니다.\"")
    
    # Dashboard Preview (Simplified from streamlit_app.py)
    tabs = st.tabs(["📈 Investment Info", "👥 Client Management", "👤 Client Detail"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Overseas Stock Briefing")
            st.dataframe(get_overseas_stock_briefing().head(5), use_container_width=True, hide_index=True)
        with c2:
            st.subheader("Market One-Liners")
            for item in get_market_one_liners()[:2]:
                st.caption(f"**{item['Symbol']}**: {item['Reason']}")
    
    with tabs[1]:
        st.subheader("Priority Client List")
        st.dataframe(get_mock_priority_list().head(5), use_container_width=True, hide_index=True)

    with tabs[2]:
        st.subheader("Client Portfolio View")
        st.plotly_chart(px.pie(get_mock_portfolio(101), values='Allocation', names='Asset Class', hole=0.4, height=300), use_container_width=True)

# ==============================================================================
# SLIDE 2: INTRO & AUDIENCE
# ==============================================================================
elif st.session_state.current_slide == 2:
    st.markdown('<h1>Slide 2. antigravity, Streamlit 소개 & 강의 대상</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>🛠️ Tool Summary</h3>
            <p><b>antigravity</b>: 디자인 선택지를 줄여 레이아웃을 코드로 강제하는 설계 철학</p>
            <p><b>Streamlit</b>: Python 스크립트를 즉시 웹 앱으로 변환하는 프레임워크</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🎯 누구를 위한 강의인가?</h3>
            <p>✅ <b>대상:</b> Python 결과물을 멋지게 보여주고 싶은 데이터 분석가/엔지니어</p>
            <p>❌ <b>비대상:</b> 전문적인 프론트엔드 개발자가 되고 싶은 분</p>
        </div>
        """, unsafe_allow_html=True)

    st.warning("🎤 \"이 강의는 웹 개발 강의가 아닙니다. Python 결과를 화면으로 보여주고 싶은 사람을 위한 강의입니다.\"")

# ==============================================================================
# SLIDE 3: ANTIGRAVITY INNOVATION
# ==============================================================================
elif st.session_state.current_slide == 3:
    st.markdown('<h1>Slide 3. antigravity의 혁신</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 50vh;">
        <div class="highlight-card" style="width: 80%;">
            <h2 style="font-size: 3rem;">"antigravity는 디자인 도구가 아니다"</h2>
            <hr style="border: 0.5px solid rgba(255,255,255,0.3);">
            <h3>레이아웃 규칙을 코드로 강제한다</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🎤 \"디자인이 망가지는 이유는 감각 부족이 아니라 선택지가 너무 많기 때문입니다. antigravity는 선택지를 줄입니다.\"")

# ==============================================================================
# SLIDE 4: STREAMLIT INNOVATION
# ==============================================================================
elif st.session_state.current_slide == 4:
    st.markdown('<h1>Slide 4. Streamlit의 혁신</h1>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Python script = Web App</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #888;'>웹을 배운다 ❌, 웹을 사용한다 ⭕</h3>", unsafe_allow_html=True)
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### 기존 웹 개발
        - HTML/CSS/JS/React...
        - API 서버 구축 (FastAPI/Django)
        - 비동기 통신 (Axios/Fetch)
        - 서버-클라이언트 분리
        """)
    with c2:
        st.markdown("""
        ### Streamlit 방식
        - **Python Script 하나로 끝**
        - UI가 변수 값에 따라 자동 재렌더링
        - 위젯 = 변수
        - 백엔드 로직이 곧 프론트엔드
        """)

    st.info("🎤 \"Streamlit의 혁신은 기술이 아니라 관점입니다. 웹을 '만드는 것'에서 '출력하는 것'으로 바꿨습니다.\"")

# ==============================================================================
# SLIDE 5: ROLES
# ==============================================================================
elif st.session_state.current_slide == 5:
    st.markdown('<h1>Slide 5. 역할 분담</h1>', unsafe_allow_html=True)
    
    col_st, col_ag = st.columns(2)
    
    with col_st:
        st.markdown("""
        <div class="glass-card" style="border-top: 5px solid #ff4b4b;">
            <h2>Streamlit</h2>
            <p><b>실행 · 렌더링 · 배포</b></p>
            <ul>
                <li>Python 코드 실행</li>
                <li>데이터 시각화 (Plotly/Altair)</li>
                <li>Cloud 배포 (Share)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ag:
        st.markdown("""
        <div class="glass-card" style="border-top: 5px solid #4facfe;">
            <h2>antigravity</h2>
            <p><b>정렬 · 간격 · 구조</b></p>
            <ul>
                <li>화면 구성 (Grid/Container)</li>
                <li>디자인 일관성 유지</li>
                <li>사용자 경험(UX) 최적화</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.info("🎤 \"하나가 배를 띄우면(Streamlit), 하나는 짐을 정리합니다(antigravity). 역할이 겹치지 않아 강력합니다.\"")

# ==============================================================================
# SLIDE 6: WHY STRONG IN PRACTICE
# ==============================================================================
elif st.session_state.current_slide == 6:
    st.markdown('<h1>Slide 6. 실무에서 강한 이유</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-bottom: 20px;">✅ Checklist</h3>
        <p>🚀 <b>빠르게 만든다</b>: 기획에서 데모까지 단 몇 시간</p>
        <p>🗣️ <b>설명하기 쉽다</b>: 코드가 곧 구조라 협업이 직관적</p>
        <p>🛠️ <b>유지보수 가능하다</b>: 복잡한 프론트엔드 코드 없이 Python만 관리</p>
        <p>🌐 <b>공유가 즉시 된다</b>: URL 하나로 전 세계 어디서든 확인</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🎤 \"이 방식은 예쁘기 때문이 아니라, 업무에서 실제로 쓰이기 때문에 강력합니다.\"")

# ==============================================================================
# SLIDE 7: NEXT STEPS
# ==============================================================================
elif st.session_state.current_slide == 7:
    st.markdown('<h1>Slide 7. 강의 이후 해볼 수 있는 예시</h1>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("### [Streamlit Gallery](https://streamlit.io/gallery)")
        st.write("다양한 대시보드 및 도구 영감 얻기")
    with c2:
        st.success("### [Official Docs](https://docs.streamlit.io)")
        st.write("Streamlit의 모든 기능을 마스터하기")
    with c3:
        st.warning("### [Recommend Books](https://example.com)")
        st.write("추천 서적 및 관련 워크숍")
        
    st.divider()
    st.markdown("""
    ### 확장 가능성
    - 사내 데이터 대시보드
    - LLM 기반 AI Agent 인터페이스
    - 고객 제안용 인터랙티브 리포트
    """)

    st.info("🎤 \"오늘 배운 건 시작점입니다. 대시보드, 내부 도구, 고객 설명 페이지로 확장하세요.\"")

# ==============================================================================
# SLIDE 8: CONCLUSION
# ==============================================================================
elif st.session_state.current_slide == 8:
    st.markdown('<div class="conclusion-text">', unsafe_allow_html=True)
    st.markdown('웹은 목적이 아니라,<br>여러분의 Python 결과물을<br>보여주기 위한 수단이다.', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("🎤 \"웹을 배운다는 부담은 내려놓으세요. 오늘 가져가야 할 건 이 관점 하나입니다.\"")

# --- FOOTER NAVIGATION BUTTONS ---
st.divider()
col_prev, col_center, col_next = st.columns([1, 4, 1])

with col_prev:
    if st.button("⬅️ Prev", use_container_width=True):
        prev_slide()
        st.rerun()

with col_next:
    if st.button("Next ➡️", use_container_width=True):
        next_slide()
        st.rerun()

st.markdown('<p class="nav-hint">Slide {} / 8</p>'.format(st.session_state.current_slide), unsafe_allow_html=True)
