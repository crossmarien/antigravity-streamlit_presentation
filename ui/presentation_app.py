import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
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
    initial_sidebar_state="expanded"
)

# --- CACHE IMAGES ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Note: Assets moved to local project directory to avoid MediaFileStorageError
AG_LOGO_PATH = "ui/assets/ag_logo.png"
PS_ICON_PATH = "ui/assets/ps_icon.png"

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap');

    html, body, [data-testid="stSidebarContent"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Section Styling */
    .slide-section {
        padding: 80px 5%;
        border-bottom: 1px solid #f0f0f0;
        min-height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* Gradient Background for Headers */
    .main-title {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 4.5rem;
        margin-bottom: 0.5rem;
    }

    .sub-title {
        color: #555;
        font-size: 1.8rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }

    /* Card Styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(8px);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
    }

    .highlight-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
        border-radius: 25px;
        padding: 50px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(30, 58, 138, 0.2);
    }

    /* Big Text for Conclusion */
    .conclusion-text {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        line-height: 1.1;
        background: linear-gradient(90deg, #6366f1 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 120px 0;
    }
    
    /* Code blocks */
    code {
        font-family: 'JetBrains Mono', monospace;
        background: #f1f5f9;
        padding: 2px 6px;
        border-radius: 4px;
        color: #e11d48;
    }

    /* Sidebar Navigation Labels */
    .sidebar-nav-item {
        padding: 12px 15px;
        border-radius: 10px;
        margin-bottom: 8px;
        transition: all 0.2s;
        text-decoration: none;
        color: #444;
        display: flex;
        align-items: center;
        font-weight: 500;
    }
    .sidebar-nav-item:hover {
        background: #e2e8f0;
        color: #1e293b;
    }
    
    /* Floating Effect */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image(AG_LOGO_PATH, use_container_width=True)
    st.title("🗂 Navigation")
    st.markdown("""
    <a href="#slide-1-live" class="sidebar-nav-item">🚀 1. Live App Entry</a>
    <a href="#slide-2-intro" class="sidebar-nav-item">🎯 2. Intro & Audience</a>
    <a href="#slide-3-ag" class="sidebar-nav-item">🧠 3. Antigravity Innovation</a>
    <a href="#slide-4-st" class="sidebar-nav-item">⚡ 4. Streamlit Innovation</a>
    <a href="#slide-5-roles" class="sidebar-nav-item">🤝 5. Roles & Synergy</a>
    <a href="#slide-6-practice" class="sidebar-nav-item">🛠️ 6. Why Strong in Practice</a>
    <a href="#slide-7-next" class="sidebar-nav-item">📈 7. Next Steps</a>
    <a href="#slide-8-conclusion" class="sidebar-nav-item">💎 8. Conclusion</a>
    """, unsafe_allow_html=True)
    st.divider()
    st.image(PS_ICON_PATH, width=100)
    st.caption("Empowering Pythonists")

# ==============================================================================
# SLIDE 1: LIVE APP ENTRY
# ==============================================================================
st.markdown('<div id="slide-1-live" class="slide-section">', unsafe_allow_html=True)
c_title, c_logo = st.columns([2, 1])
with c_title:
    st.markdown('<h1 class="main-title">AI PB Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">"The Power of Python, Visualized Instantly"</p>', unsafe_allow_html=True)
with c_logo:
    st.markdown('<div class="floating">', unsafe_allow_html=True)
    st.image(AG_LOGO_PATH, width=250)
    st.markdown('</div>', unsafe_allow_html=True)

st.info("🎤 Presenter Message: \"지금 보고 계신 화면이 오늘 강의의 결과물입니다. PPT가 아니라, 이미 배포된 웹 앱에서 발표를 시작합니다.\"")

# Dashboard Preview logic
cols = st.columns(3)
with cols[0]:
    with st.container(border=True):
        st.subheader("Global Market")
        st.dataframe(get_overseas_stock_briefing().head(3), use_container_width=True, hide_index=True)
with cols[1]:
    with st.container(border=True):
        st.subheader("Client Priority")
        st.dataframe(get_mock_priority_list().head(3)[['client_name', 'priority_score']], use_container_width=True, hide_index=True)
with cols[2]:
    with st.container(border=True):
        st.subheader("Asset Allocation")
        st.plotly_chart(px.pie(get_house_asset_allocation(), values='Current', names='Asset Class', hole=0.5, height=200), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SLIDE 2: INTRO & AUDIENCE
# ==============================================================================
st.markdown('<div id="slide-2-intro" class="slide-section">', unsafe_allow_html=True)
st.markdown('<h1>🎯 Lecture Target & Scope</h1>', unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: #4facfe;">Who is this for?</h2>
        <ul style="font-size: 1.2rem; line-height: 2;">
            <li>✅ <b>Data Scientists</b> wanting to share interactive results</li>
            <li>✅ <b>Internal Tool Builders</b> who need speed over complexity</li>
            <li>✅ <b>Analysts préparant</b> des pitchs clients dynamiques</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Visualization: Skill Cloud
    df_skills = pd.DataFrame({
        "Skill": ["Python", "Streamlit", "Data Logic", "UI Design", "Deployment", "Frontend JS"],
        "Importance": [100, 90, 80, 50, 40, 10]
    })
    fig = px.bar(df_skills, x="Skill", y="Importance", color="Skill", title="Focus Areas for Today")
    st.plotly_chart(fig, use_container_width=True)

st.warning("⚠️ \"이 강의는 웹 개발 강의가 아닙니다. Python 결과를 화면으로 보여주고 싶은 사람을 위한 강의입니다.\"")
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SLIDE 3: ANTIGRAVITY INNOVATION
# ==============================================================================
st.markdown('<div id="slide-3-ag" class="slide-section">', unsafe_allow_html=True)
st.markdown('<h1>🧠 Antigravity: Structure Over Aesthetics</h1>', unsafe_allow_html=True)

col_text, col_vis = st.columns([1, 1])
with col_text:
    st.markdown("""
    ### Why Design Fails?
    Too many choices. Padding, Margin, Colors, Fonts, Breakpoints...
    
    ### The Antigravity Solution:
    1. **Constraint is Freedom**: Reduce options to force consistency.
    2. **Grid-First**: Layout rules are encoded, not guessed.
    3. **Primitive Components**: Reuse high-quality atomic elements.
    """)
    st.info("🎤 \"디자인이 망가지는 이유는 감각 부족이 아니라 선택지가 너무 많기 때문입니다.\"")

with col_vis:
    # Conceptual Visualization: Chaos vs Order
    import random
    n = 20
    x0, y0 = [random.random() for _ in range(n)], [random.random() for _ in range(n)]
    x1, y1 = [i%5 for i in range(n)], [i//5 for i in range(n)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x0, y=y0, mode='markers', name='Ad-hoc UI', marker=dict(size=12, color='red')))
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', name='AG Structured', marker=dict(size=12, color='green')))
    fig.update_layout(title="Free Design vs Structured Rules", showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SLIDE 4: STREAMLIT INNOVATION
# ==============================================================================
st.markdown('<div id="slide-4-st" class="slide-section">', unsafe_allow_html=True)
st.markdown('<h1>⚡ Streamlit: The End of Web Development?</h1>', unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; justify-content: center; margin-bottom: 40px;">
    <div style="text-align: center; border: 2px dashed #ccc; padding: 20px; border-radius: 15px; background: white;">
        <p style="font-size: 1.5rem; font-family: 'JetBrains Mono'; margin: 0;">
        name = st.text_input("Brand", "Antigravity") <br>
        st.write(f"Hello {name}")
        </p>
    </div>
    <div style="font-size: 3rem; margin: 0 30px;">➡️</div>
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 20px; border-radius: 15px; background: #fff1f1;">
        <span style="font-weight: 800; color: #ff4b4b;">Functional Web App</span>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Dev Time (React)", "Weeks", "-80%")
    st.caption("Complex boilerplate required.")
with c2:
    st.metric("Dev Time (Streamlit)", "Hours", "FAST")
    st.caption("Focus on logic, not syntax.")
with c3:
    st.metric("Accessibility", "Global URL", "Instant")
    st.caption("Cloud deployment in one click.")

st.info("🎤 \"Streamlit의 혁신은 기술이 아니라 관점입니다. 웹을 '만드는 것'에서 '출력하는 것'으로 바꿨습니다.\"")
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SLIDE 5: ROLES & SYNERGY
# ==============================================================================
st.markdown('<div id="slide-5-roles" class="slide-section">', unsafe_allow_html=True)
st.markdown('<h1>🤝 The Power Couple</h1>', unsafe_allow_html=True)

# Comparison Table
df_roles = pd.DataFrame({
    "Feature": ["Engine", "Alignment", "Data Fetching", "Visual Polish", "Responsive Grid", "Hosting"],
    "Streamlit": ["✅ (State)", "⚠️ (Limited)", "✅ (Native)", "⚠️ (Default)", "⚠️ (Columns)", "✅ (Share)"],
    "Antigravity": ["❌", "✅ (Strict)", "❌", "✅ (Premium)", "✅ (Auto)", "❌"]
})
st.table(df_roles)

col_img, col_txt = st.columns([1, 1.5])
with col_img:
    st.image(PS_ICON_PATH, use_container_width=True)
with col_txt:
    st.markdown("""
    ### Why they work together:
    - **Streamlit** provides the **Pipeline** (the logic and interactivity).
    - **Antigravity** provides the **Frame** (the aesthetics and organization).
    
    > "Streamlit draws the pixels, Antigravity tells them where to sit."
    """)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SLIDE 6: WHY STRONG IN PRACTICE
# ==============================================================================
st.markdown('<div id="slide-6-practice" class="slide-section">', unsafe_allow_html=True)
st.markdown('<h1>🛠️ Practical Strength: "Demo to Prod"</h1>', unsafe_allow_html=True)

c1, c2 = st.columns([1, 1])
with c1:
    st.markdown("""
    ### 1. Unified Language
    Collaboration between Data Scientists and Engineers is easier when everything is `python`.
    
    ### 2. Immediate Feedback
    Stakeholders see progress every hour, not every month.
    
    ### 3. Maintainability
    No "code rot" from forgotten CSS files or JS dependencies.
    """)
with c2:
    # Radar Chart: Practice vs Theory
    categories = ['Speed', 'Aesthetics', 'Maintainability', 'Customizability', 'Ease of Use']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=[5, 4, 5, 2, 5],
          theta=categories,
          fill='toself',
          name='Modern Python Stack'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, title="Why it wins in practice")
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SLIDE 7: NEXT STEPS
# ==============================================================================
st.markdown('<div id="slide-7-next" class="slide-section">', unsafe_allow_html=True)
st.markdown('<h1>📈 Roadmap for You</h1>', unsafe_allow_html=True)

step_cols = st.columns(4)
steps = [
    ("Step 1", "Master **Streamlit Basics** (`st.write`, `st.columns`)"),
    ("Step 2", "Adopt **AG Structure** (Grouping widgets, spacing)"),
    ("Step 3", "Integrate **AI Agents** (Chat interfaces, RAG)"),
    ("Step 4", "Deploy & **Scale** (Share Cloud, Enterprise)")
]

for i, col in enumerate(step_cols):
    with col:
        st.markdown(f"### {steps[i][0]}")
        st.write(steps[i][1])
        st.button(f"Resource {i+1}", key=f"btn_res_{i}")

st.divider()
st.image(PS_ICON_PATH, width=50) 
st.markdown("*\"The journey of a thousand miles begins with a single `streamlit run`\"*")
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SLIDE 8: CONCLUSION
# ==============================================================================
st.markdown('<div id="slide-8-conclusion" class="slide-section" style="border-bottom: none;">', unsafe_allow_html=True)
st.markdown('<div class="conclusion-text">', unsafe_allow_html=True)
st.markdown('웹은 목적이 아니라,<br>여러분의 Python 결과물을<br>보여주기 위한 수단이다.', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.image(AG_LOGO_PATH, width=150)
st.info("🎤 \"웹을 배운다는 부담은 내려놓으세요. 오늘 가져가야 할 건 이 관점 하나입니다.\"")
st.markdown('</div>', unsafe_allow_html=True)
