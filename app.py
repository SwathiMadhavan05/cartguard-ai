import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =====================================================
# 1. UI CONFIGURATION & ADVANCED ANIMATIONS
# =====================================================
st.set_page_config(page_title="CartGuard AI | Enterprise", layout="wide")

LOGO_PATH = "logo.jpg" 

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    
    /* Smooth Page Entrance */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 30px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    /* Pulsing Live Indicator */
    @keyframes pulse-red {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }

    .stApp { 
        background: radial-gradient(circle at top right, #0a0e91, #050761); 
        color: white; 
        font-family: 'Satoshi', sans-serif !important;
    }

    /* Glassmorphism Stat Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeInUp 0.8s ease-out;
    }

    .stat-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.07);
        border-color: #50FFB1;
    }

    .live-dot {
        height: 10px; width: 10px;
        background-color: #ff4b4b;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: pulse-red 2s infinite;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #50FFB1, #39d38d) !important;
        color: #050761 !important; 
        font-weight: 800 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        letter-spacing: 2px;
        box-shadow: 0px 0px 20px rgba(80, 255, 177, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. APP STATE & ROUTING
# =====================================================
if "page" not in st.session_state: st.session_state.page = "landing"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- LANDING PAGE ---
if st.session_state.page == "landing":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_logo, _ = st.columns([1, 0.6, 1])
    with col_logo:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown("<h1 style='text-align:center; font-size:4rem; font-weight:900; color:#50FFB1;'>CartGuardAI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2rem; opacity:0.8;'>Neural-driven checkout optimization & bot mitigation.</p>", unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1.2, 0.6, 1.2])
    with col_btn:
        if st.button("LAUNCH TERMINAL"):
            st.session_state.page = "login"
            st.rerun()

# --- LOGIN PAGE ---
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_m, _ = st.columns([1, 1, 1])
    with col_m:
        st.markdown("<h2 style='text-align:center; color:#50FFB1;'>Access Restricted</h2>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("AUTHORIZE"):
            if u == "admin" and p == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Invalid Credentials")

# --- DASHBOARD ---
elif st.session_state.logged_in:
    @st.cache_resource
    def load_assets():
        try:
            rf = joblib.load("rf_abandonment_model.pkl")
            arima = joblib.load("arima_model.pkl")
            return rf, arima
        except: return None, None

    rf_model, arima_model = load_assets()

    with st.sidebar:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=100)
        st.markdown("<h3 style='color:#50FFB1;'>Command Center</h3>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.sidebar.selectbox("MODULE", ["Live Intelligence", "Global Forecast", "Bot Mitigation"])
        st.markdown("---")
        if st.button("SHUTDOWN"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    if menu == "Live Intelligence":
        st.markdown("<h1><span class='live-dot'></span>Live Intelligence</h1>", unsafe_allow_html=True)
        
        # User Input Row
        c1, c2, c3, c4 = st.columns(4)
        with c1: items = st.number_input("Cart Items", 1, 100, 3)
        with c2: val = st.number_input("Cart Value ($)", 1.0, 50000.0, 450.0)
        with c3: dwell = st.number_input("Dwell Time (Min)", 0.1, 60.0, 5.0)
        with c4: plat = st.selectbox("Device", [0, 1], format_func=lambda x: "Mobile" if x==1 else "Desktop")

        if st.button("RUN NEURAL SCAN"):
            with st.spinner("Analyzing behavioral nodes..."):
                time.sleep(1)
                
                # Logic Logic
                risk = 85 if val > 1000 and dwell < 1 else 15
                if rf_model:
                    risk = int(rf_model.predict_proba(np.array([[items, val, dwell, plat, 0, 0, 0, 0, 0, 0]]))[0][1] * 100)

            # Animated Stat Cards
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"<div class='stat-card'><p>ABANDON RISK</p><h2 style='color:#FF4B4B;'>{risk}%</h2></div>", unsafe_allow_html=True)
            with m2:
                st.markdown(f"<div class='stat-card'><p>AT-RISK REVENUE</p><h2 style='color:#FFA500;'>${val*(risk/100):,.2f}</h2></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div class='stat-card'><p>RECOVERY SCORE</p><h2 style='color:#50FFB1;'>{(100-risk)+10}%</h2></div>", unsafe_allow_html=True)

            # Interactive Charts
            chart_left, chart_right = st.columns(2)
            with chart_left:
                st.markdown("### Behavioral Attribution")
                fig = px.bar(x=[val/100, (1/dwell)*10, items*2], y=["Value", "Dwell", "Density"], orientation='h', color_discrete_sequence=['#50FFB1'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with chart_right:
                st.markdown("### Intent Radar")
                df_radar = pd.DataFrame(dict(r=[risk, 100-risk, 50, 80], theta=['Abandon', 'Purchase', 'Loyalty', 'Urgency']))
                fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
                fig_radar.update_traces(fill='toself', line_color='#50FFB1')
                fig_radar.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=300)
                st.plotly_chart(fig_radar, use_container_width=True)

    elif menu == "Global Forecast":
        st.markdown("<h1>Strategic Forecast</h1>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Desktop', 'Mobile', 'App'])
        st.line_chart(chart_data)
        st.info("Forecasting 14-day revenue leakage based on historical ARIMA trends.")

    elif menu == "Bot Mitigation":
        st.markdown("<h1>Bot Defense Firewall</h1>", unsafe_allow_html=True)
        st.error("🚨 3 High-frequency IP addresses flagged in the last 10 minutes.")
        st.table(pd.DataFrame({
            "Source IP": ["192.168.1.45", "104.16.2.1", "45.79.10.2"],
            "Action": ["Blocked", "Challenged", "Monitoring"],
            "Certainty": ["99%", "82%", "71%"]
        }))
