import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mock_data import get_mock_priority_list, get_mock_portfolio, get_mock_risk_exposure, get_mock_insights

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI PB Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4e8cff;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

# --- CUSTOM CLIENT GROUPS STATE ---
if "client_groups" not in st.session_state:
    st.session_state.client_groups = {
        "All Clients": [],
        "High Net Worth": ["Arthur Pendragon", "Lancelot du Lac"],
        "ELS Buyers": ["Guinevere Leodegrance", "Morgan le Fay"],
        "Risk Focused": ["Merlin Ambrosius"]
    }

# --- SIDEBAR ---
st.sidebar.title("🏦 PB Advisor AI")
page = st.sidebar.radio("Navigate", ["📊 Command Center", "👤 Client 360", "📝 Recommendation"])
st.sidebar.divider()

# Group Management in Sidebar
st.sidebar.subheader("👥 Client Groups")
selected_group = st.sidebar.selectbox("Filter View by Group", list(st.session_state.client_groups.keys()))

with st.sidebar.expander("Manage Groups"):
    new_group = st.text_input("New Group Name")
    if st.button("Create Group"):
        if new_group and new_group not in st.session_state.client_groups:
            st.session_state.client_groups[new_group] = []
            st.success(f"Created {new_group}")
            st.rerun()
            
    group_to_delete = st.selectbox("Delete Group", [k for k in st.session_state.client_groups.keys() if k != "All Clients"])
    if st.button("Delete Selected Group"):
        del st.session_state.client_groups[group_to_delete]
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("Logged in as: **John Doe (PB)**")
st.sidebar.caption(f"Last Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")

# --- PAGE 1: COMMAND CENTER ---
if "Command Center" in page:
    st.title("📊 PB Command Center")
    
    # --- WIDGET LOGIC ---
    from mock_data import (
        get_market_heatmap_data, get_aggregated_aum_data, get_risk_distribution_data,
        get_cashflow_data, get_high_cash_clients, get_churn_risk_data, 
        get_client_events, get_market_movers
    )

    # 1. Priority List Widget (Filtered by Group)
    def widget_priority_list():
        st.subheader(f"🚀 Priority List - {selected_group}")
        df_priority = get_mock_priority_list()
        
        # Filter by Group
        if selected_group != "All Clients":
            target_names = st.session_state.client_groups[selected_group]
            if target_names:
                df_priority = df_priority[df_priority['client_name'].isin(target_names)]
            else:
                st.warning(f"No clients in group '{selected_group}'")
                return

        def highlight_score(val):
            color = '#ffcccb' if val > 90 else '#ffe5cc' if val > 70 else ''
            return f'background-color: {color}'

        styled_df = df_priority.style.map(highlight_score, subset=['priority_score'])
        st.dataframe(
            styled_df,
            column_config={
                "priority_score": st.column_config.ProgressColumn("Score", format="%d", min_value=0, max_value=100),
                "aum_usd": st.column_config.NumberColumn("AUM ($)", format="$%.2f")
            },
            use_container_width=True,
            hide_index=True
        )

    # 2. Market Heatmap Widget
    def widget_market_heatmap():
        st.subheader("🌍 Market Sector Heatmap")
        df = get_market_heatmap_data()
        fig = px.treemap(
            df, path=['Sector'], values='Market Weight', color='Color Score',
            color_continuous_scale='RdYlGn', color_continuous_midpoint=0,
            custom_data=['Return (%)']
        )
        fig.update_traces(textinfo="label+value+percent entry", hovertemplate='Sector: %{label}<br>Return: %{customdata[0]}%')
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    # 3. Asset Allocation Widget
    def widget_asset_allocation():
        st.subheader("💰 Total Book Assets")
        df = get_aggregated_aum_data()
        fig = px.pie(df, values='AUM (M)', names='Asset Class', hole=0.5)
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    # 4. Risk Distribution Widget
    def widget_risk_distribution():
        st.subheader("⚠️ Client Risk Distribution")
        df = get_risk_distribution_data()
        fig = px.bar(
            df, x='Risk Category', y='Client Count', color='Risk Category', 
            color_discrete_map={'High': 'red', 'Medium-High': 'orange', 'Medium': 'gold', 'Medium-Low': 'lightblue', 'Low': 'lightgreen'}
        )
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # 5. Client Cashflow Widget
    def widget_cashflow():
        st.subheader("💸 Net Cash Flows (MTD)")
        df = get_cashflow_data()
        if not df.empty:
            fig = px.bar(df, x='Net Flow', y='Client', color='Type', orientation='h', text='Net Flow')
            fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cash flow data available.")

    # 6. Available Cash List
    def widget_cash_list():
        st.subheader("💰 High Cash Balances (Action Required)")
        df = get_high_cash_clients()
        st.dataframe(
            df, 
            column_config={
                "Cash ($)": st.column_config.NumberColumn("Cash ($)", format="$%.2f"),
                "Cash %": st.column_config.ProgressColumn("Liquidity %", min_value=0, max_value=100)
            },
            hide_index=True,
            use_container_width=True
        )

    # 7. Churn Risk / Quitting Clients
    def widget_churn_risk():
        st.subheader("🚨 Leaving Risk (Churn Prediction)")
        df = get_churn_risk_data()
        for _, row in df.iterrows():
            col_color = "red" if row['Risk Score'] == "High" else "orange"
            st.markdown(f":{col_color}[**{row['Client']}**] - {row['Prob']}% Probability")
            st.caption(f"Reason: {row['Reason']}")
            st.progress(row['Prob'] / 100, text=f"{row['Prob']}% Risk")

    # 8. Client Events
    def widget_client_events():
        st.subheader("📅 Customer Events")
        df = get_client_events()
        st.dataframe(df, hide_index=True, use_container_width=True)

    # 9. Market Movers (Stock Explainability)
    def widget_market_movers():
        st.subheader("📈 Why is it moving?")
        movers = get_market_movers()
        for m in movers:
            delta_color = "normal" if m['Move'].startswith('+') else "inverse"
            st.metric(label=m['Ticker'], value=m['Move'])
            st.info(f"**AI Reason**: {m['Reason']}")


    # Dictionary of available widgets
    WIDGETS = {
        "Priority List": widget_priority_list,
        "Market Heatmap": widget_market_heatmap,
        "Customer Cashflow": widget_cashflow,        # NEW
        "Available Cash List": widget_cash_list,     # NEW
        "Churn/Leaving Risk": widget_churn_risk,     # NEW
        "Customer Events": widget_client_events,     # NEW
        "Stock Insights": widget_market_movers,      # NEW
        "Book Assets": widget_asset_allocation,
        "Risk Clients": widget_risk_distribution
    }

    # --- CUSTOMIZE LAYOUT ---
    with st.expander("🛠️ Customize Dashboard Layout", expanded=False):
        st.caption("Select which widgets to display on your command center.")
        selected_widgets = st.multiselect(
            "Active Widgets", 
            list(WIDGETS.keys()), 
            default=["Priority List", "Customer Cashflow", "Available Cash List", "Churn/Leaving Risk"]
        )

    # --- RENDER DASHBOARD ---
    # Top Actions Metrics (Fixed Header)
    st.markdown(f"### 🎯 Daily Snapshot ({selected_group})")
    c1, c2, c3, c4 = st.columns(4)
    df_priority = get_mock_priority_list() # For metric calculation, use full list or filtered? Let's use full for global view
    
    with c1: st.metric("Actions Today", len(df_priority[df_priority['priority_score'] > 80]))
    with c2: st.metric("Portfolio Alerts", "3", delta="1 New", delta_color="inverse")
    with c3: st.metric("Meetings", "4")
    with c4: st.metric("Unique Login", "John Doe")
    st.divider()

    # Dynamic Grid Layout
    # Priority List always full width if selected
    if "Priority List" in selected_widgets:
        WIDGETS["Priority List"]() 
    
    # Filter remaining widgets
    remaining = [w for w in selected_widgets if w != "Priority List"]
    
    # Create rows of 2
    for i in range(0, len(remaining), 2):
        row_widgets = remaining[i:i+2]
        cols = st.columns(len(row_widgets))
        for col, widget_name in zip(cols, row_widgets):
            with col:
                with st.container(border=True):
                    WIDGETS[widget_name]()

# --- PAGE 2: CLIENT 360 ---
elif "Client 360" in page:
    st.title("👤 Client 360")
    
    # Selector
    client_list = get_mock_priority_list()
    selected_client_name = st.selectbox("Select Client", client_list['client_name'])
    client_id = client_list[client_list['client_name'] == selected_client_name]['client_id'].values[0]
    
    # Profile Header
    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.markdown(f"## {selected_client_name}")
        st.caption(f"Client ID: {client_id} | Risk Profile: Aggressive | Tenancy: 5 Years")
        tags = ["Tech-Founder", "ESG-Focused", "High-Liquidity-Needs"]
        st.markdown(" ".join([f"`{t}`" for t in tags]))
    with col_r:
        st.metric("YTD Performance", "+12.4%", "+2.1%")
    
    st.divider()
    
    # Dashboard Grid
    c1, c2 = st.columns(2)
    
    # Portfolio Pie Chart
    with c1:
        st.subheader("Portfolio Composition")
        df_port = get_mock_portfolio(client_id)
        fig_pie = px.pie(df_port, values='Allocation', names='Asset Class', hole=0.4)
        fig_pie.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    # Risk Bar Chart
    with c2:
        st.subheader("Risk Factor Exposure")
        df_risk = get_mock_risk_exposure(client_id)
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df_risk['Factor'], y=df_risk['Current Exposure'], name='Current',
            marker_color='#4e8cff'
        ))
        fig_bar.add_trace(go.Scatter(
            x=df_risk['Factor'], y=df_risk['Target Exposure'], name='Target',
            mode='markers', marker=dict(color='red', size=10, symbol='line-ew-open')
        ))
        fig_bar.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    # AI Insights
    st.subheader("✨ AI Insights & Alerts")
    insights = get_mock_insights(client_id)
    for i, txt in enumerate(insights):
        with st.expander(f"Insight #{i+1}", expanded=True):
            st.markdown(txt)

# --- PAGE 3: RECOMMENDATION ---
elif "Recommendation" in page:
    st.title("📝 AI Recommendation Draft")
    
    st.info("Drafting Recommendation for: **Arthur Pendragon** (generated 2 mins ago)")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Proposed Rebalancing")
        with st.container(border=True):
            st.markdown("""
            **Action**: REBALANCE
            
            **Rationale**: 
            1. Reduce US Tech exposure (Overweight by 5%) to lock in recent gains.
            2. Reallocate to Investment Grade Bonds to improve yield stability.
            
            **Trades**:
            - **SELL**: $500k NASDAQ ETF (QQQ)
            - **BUY**: $500k USD Corp Bond ETF (LQD)
            """)
        
        st.subheader("Compliance Check")
        st.success("✅ Suitability Check Passed (Policy v2024.1)")
        st.markdown("- **Concentration Risk**: Within limits (<15% single issuer)")
        st.markdown("- **Risk Profile**: Aligned (Aggressive)")
        
    with c2:
        st.subheader("Actions")
        st.button("✍️ Edit Draft", type="secondary", use_container_width=True)
        st.button("📩 Send for Approval", type="primary", use_container_width=True)
        st.button("🔍 View Audit Log", type="secondary", use_container_width=True)
