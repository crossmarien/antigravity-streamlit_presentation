from datetime import datetime
import pandas as pd
import numpy as np
import random

# --- MOCK DATA GENERATORS ---

def get_mock_priority_list():
    """Generates the PB Command Center priority list."""
    clients = [
        {"id": "c101", "name": "Arthur Pendragon", "score": 95, "aum": 15000000},
        {"id": "c102", "name": "Guinevere Leodegrance", "score": 88, "aum": 8500000},
        {"id": "c103", "name": "Lancelot du Lac", "score": 75, "aum": 22000000},
        {"id": "c104", "name": "Merlin Ambrosius", "score": 40, "aum": 5000000},
        {"id": "c105", "name": "Morgan le Fay", "score": 30, "aum": 12000000},
    ]
    
    reasons = [
        {"code": "RISK_DRIFT", "label": "Risk Drift > 5%", "severity": "high"},
        {"code": "LIQUIDITY", "label": "Cash Drag (15%)", "severity": "medium"},
        {"code": "MATURITY", "label": "Bond Maturity (30d)", "severity": "medium"},
        {"code": "NEWS", "label": "Tech Sector Volatility", "severity": "low"},
    ]
    
    data = []
    for c in clients:
        # Assign random reasons based on score
        c_reasons = []
        if c['score'] > 80:
            c_reasons = [reasons[0]]
        elif c['score'] > 60:
            c_reasons = [reasons[1], reasons[2]]
        
        data.append({
            "client_id": c["id"],
            "client_name": c["name"],
            "priority_score": c["score"],
            "aum_usd": c["aum"],
            "reason_tags": [r["label"] for r in c_reasons],
            "last_contact": f"{random.randint(2, 30)} days ago",
            "next_action": "Call" if c['score'] > 80 else "Email"
        })
    
    return pd.DataFrame(data).sort_values("priority_score", ascending=False)

def get_mock_portfolio(client_id):
    """Generates a mock portfolio composition."""
    # Fixed seed for consistency per client
    random.seed(client_id)
    
    asset_classes = ["Equities", "Fixed Income", "Alternatives", "Cash"]
    weights = [0.4, 0.4, 0.15, 0.05]
    
    # Add some noise
    adj = np.random.normal(0, 0.05, 4)
    weights = [max(0, w + a) for w, a in zip(weights, adj)]
    weights = [w / sum(weights) for w in weights] # normalize
    
    df = pd.DataFrame({
        "Asset Class": asset_classes,
        "Allocation": weights,
        "Value USD": [w * 10000000 for w in weights]  # Assume 10m portfolio
    })
    return df

def get_mock_risk_exposure(client_id):
    """Generates mock risk factor exposures."""
    factors = ["Growth", "Value", "Momentum", "Volatility", "Liquidity", "Size"]
    
    current_exposure = np.random.normal(0.5, 0.3, len(factors))
    target_exposure = np.array([0.5, 0.5, 0.5, 0.0, 0.8, 0.2])
    
    df = pd.DataFrame({
        "Factor": factors,
        "Current Exposure": current_exposure,
        "Target Exposure": target_exposure,
        "Drift": current_exposure - target_exposure
    })
    return df

def get_market_heatmap_data():
    """Generates mock market sector performance for a heatmap."""
    sectors = [
        "Technology", "Financials", "Healthcare", "Consumer Disc", 
        "Energy", "Materials", "Industrials", "Utilities"
    ]
    # Generate random returns between -3% and +3%
    returns = np.random.uniform(-3, 3, len(sectors))
    weights = np.random.uniform(5, 25, len(sectors)) # Sizes for treemap
    
    return pd.DataFrame({
        "Sector": sectors,
        "Return (%)": np.round(returns, 2),
        "Market Weight": weights,
        "Color Score": returns # Used for color scale
    })

def get_aggregated_aum_data():
    """Generates mock aggregated AUM data for the whole book."""
    assets = ["Equities", "Fixed Income", "Alts", "Cash", "Real Estate"]
    values = [450, 350, 150, 50, 200] # In Millions
    return pd.DataFrame({
        "Asset Class": assets,
        "AUM (M)": values
    })

def get_risk_distribution_data():
    """Generates mock client count by risk category."""
    categories = ["Low", "Medium-Low", "Medium", "Medium-High", "High"]
    counts = [5, 12, 45, 28, 10]
    return pd.DataFrame({
        "Risk Category": categories,
        "Client Count": counts
    })

def get_cashflow_data():
    """Generates mock cashflow data for net deposits/outflows."""
    data = [
        {"Client": "Arthur Pendragon", "Type": "Pension", "Net Flow": 500000, "Direction": "Inflow"},
        {"Client": "Lancelot du Lac", "Type": "ISA", "Net Flow": -20000, "Direction": "Outflow"},
        {"Client": "Guinevere Leodegrance", "Type": "General", "Net Flow": 150000, "Direction": "Inflow"},
        {"Client": "Merlin Ambrosius", "Type": "Pension", "Net Flow": -500000, "Direction": "Outflow"},
        {"Client": "Gawain Orkney", "Type": "General", "Net Flow": 25000, "Direction": "Inflow"},
    ]
    return pd.DataFrame(data)

def get_high_cash_clients():
    """Generates list of clients with high cash balances."""
    return pd.DataFrame([
        {"Client": "Galahad Pure", "Cash ($)": 2500000, "Cash %": 35, "Reason": "Recent Business Sale"},
        {"Client": "Percival Grail", "Cash ($)": 800000, "Cash %": 22, "Reason": "Waiting for Dip"},
        {"Client": "Bors de Ganis", "Cash ($)": 450000, "Cash %": 18, "Reason": "Risk Averse"},
    ])

def get_churn_risk_data():
    """Generates clients at risk of leaving."""
    return pd.DataFrame([
        {"Client": "Mordred", "Risk Score": "High", "Prob": 85, "Reason": "Performance & Low Contact"},
        {"Client": "Morgan le Fay", "Risk Score": "Medium", "Prob": 60, "Reason": "Competitor Offer"},
        {"Client": "Kay Steward", "Risk Score": "Medium", "Prob": 45, "Reason": "Fee Sensitivity"},
    ])

def get_client_events():
    """Generates upcoming client life/portfolio events."""
    return pd.DataFrame([
        {"Client": "Arthur Pendragon", "Event": "Birthday (60th)", "Date": "2026-01-10", "Action": "Send Gift"},
        {"Client": "Guinevere Leodegrance", "Event": "Bond Maturity ($1M)", "Date": "2026-01-12", "Action": "Reinvest Proposal"},
        {"Client": "Lancelot du Lac", "Event": "Retirement Age", "Date": "2026-02-01", "Action": "Financial Plan Review"},
    ])

def get_market_movers():
    """Generates 'Why is it moving' market explanations."""
    return [
        {"Ticker": "NVDA", "Move": "+4.2%", "Reason": "AI Chip demand forecast raised by analyst consensus."},
        {"Ticker": "TSLA", "Move": "-3.1%", "Reason": "production figures missed quarterly estimates slightly."},
        {"Ticker": "US 10Y", "Move": "+5bps", "Reason": "Stronger than expected CPI print dampening rate cut hopes."}
    ]

# --- NEW DATA FOR INVESTMENT INFO MENU ---

def get_overseas_stock_briefing():
    """3.1 Daily Excess Return Overseas Stock Briefing"""
    return pd.DataFrame([
        {"Ticker": "NVDA", "Name": "NVIDIA", "Buy(Pre/Wk)": "120M / 500M", "Sell(Pre/Wk)": "80M / 400M", "NetBuy": 40, "Chg%": "+3.2%", "Reason": "Earnings Surprise"},
        {"Ticker": "TSLA", "Name": "Tesla", "Buy(Pre/Wk)": "90M / 350M", "Sell(Pre/Wk)": "110M / 450M", "NetBuy": -20, "Chg%": "-1.5%", "Reason": "Production Miss"},
        {"Ticker": "AAPL", "Name": "Apple", "Buy(Pre/Wk)": "200M / 800M", "Sell(Pre/Wk)": "50M / 200M", "NetBuy": 150, "Chg%": "+0.5%", "Reason": "Safe Haven Flow"},
        {"Ticker": "AMZN", "Name": "Amazon", "Buy(Pre/Wk)": "150M / 600M", "Sell(Pre/Wk)": "140M / 550M", "NetBuy": 10, "Chg%": "+1.1%", "Reason": "Cloud Growth"},
        {"Ticker": "MSFT", "Name": "Microsoft", "Buy(Pre/Wk)": "180M / 700M", "Sell(Pre/Wk)": "100M / 400M", "NetBuy": 80, "Chg%": "+0.8%", "Reason": "AI Integration"},
    ]).sort_values("NetBuy", ascending=False)

def get_market_one_liners():
    """3.2 Market One-Liner + Related Clients"""
    return [
        {"Symbol": "TSLA", "Reason": "Price cut announced in China region", "Clients": ["Arthur Pendragon", "Merlin Ambrosius"]},
        {"Symbol": "XOM", "Reason": "Oil prices surge due to geopolitical tension", "Clients": ["Guinevere Leodegrance"]},
        {"Symbol": "AAPL", "Reason": "Vision Pro sales exceeding expectations", "Clients": []},
    ]

def get_market_briefing_tabs():
    """3.3 Market Briefing Tabs"""
    return {
        "Macro": "🇺🇸 **Fed Policy**: Powell hints at maintaining rates. CPI expected to be sticky.\n🇨🇳 **China**: Stimulus package rumors driving Hang Seng index.",
        "Overseas": "Tech sector showing fatigue. Rotation into Healthcare and Industrials observed in last 3 trading sessions.",
        "Insight": "⚠️ **Risk Alert**: Yen carry trade unwinding could cause short-term volatility. Reduce leverage recommended."
    }

def get_house_asset_allocation():
    """3.4 House View Allocation History"""
    return pd.DataFrame({
        "Asset Class": ["Equities", "Bonds", "Cash", "Alts"],
        "1 Mo Ago": [50, 30, 10, 10],
        "1 Wk Ago": [45, 35, 10, 10],
        "Current": [40, 40, 10, 10],
        "Change": ["-5% (Bearish)", "+5% (Bullish)", "-", "-"]
    })

def get_product_recommendations():
    """3.5 Product & Client Matching"""
    return pd.DataFrame([
        {"Product": "Global Tech ETF", "Type": "ETF", "Rec Clients": 12, "Reason": "Growth Potential"},
        {"Product": "US Treasury 5Y", "Type": "Bond", "Rec Clients": 8, "Reason": "Yield Stability"},
        {"Product": "Green Energy Fund", "Type": "Fund", "Rec Clients": 5, "Reason": "ESG Mandate"},
    ])

def get_seeking_alpha_list():
    """3.6 Seeking Alpha (Internal Sources)"""
    return pd.DataFrame([
        {"Type": "Quant", "Asset": "Small Cap Value", "Idea": "Low P/E screening shows deep value in Russell 2000", "Valid Until": "2026-02-01"},
        {"Type": "Event", "Asset": "BioTech", "Idea": "FDA approval cycle heating up in Q1", "Valid Until": "2026-03-01"},
        {"Type": "Supply/Demand", "Asset": "Copper", "Idea": "Supply shortage due to strike in Chile", "Valid Until": "2026-01-20"},
    ])

def get_trade_review():
    """3.7 Buy/Sell Review & Outlook"""
    return pd.DataFrame([
        {"Ticker": "NVDA", "Action": "Buy", "Post-Move": "+2.1%", "Outlook": "Positive (Momentum)"},
        {"Ticker": "TSLA", "Action": "Sell", "Post-Move": "-1.5%", "Outlook": "Neutral (Wait)"},
        {"Ticker": "LQD", "Action": "Buy", "Post-Move": "+0.3%", "Outlook": "Positive (Income)"},
    ])

def get_mock_insights(client_id):
    return [
        "**Portfolio Drift**: Equity allocation is **5% Overweight** vs Target due to recent Tech rally.",
        "**Tax Opportunity**: Client has **$45k** in realized losses in Fixed Income that can offset gains.",
        "**Macro**: Fed rate pause expected; suggest checking duration exposure."
    ]
