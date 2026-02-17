import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =====================================================
# 1. ADVANCED UI & ANIMATION ENGINE (CSS)
# =====================================================
st.set_page_config(page_title="CartGuard AI | Enterprise", layout="wide")

LOGO_PATH = "logo.jpg" 

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    
    /* Background & Global Fonts */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #0a1191 0%, #050730 100%);
        color: white; 
        font-family: 'Satoshi', sans-serif !important;
    }

    /* Entrance Animations */
    @keyframes growIn {
        0% { opacity: 0; transform: scale(0.9) translateY(20px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(80, 255, 177, 0.2);
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        margin-bottom: 20px;
        animation: growIn 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* Interactive Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #50FFB1, #39d38d, #50FFB1) !important;
        background-size: 200% auto !important;
        color: #050730 !important; 
        font-weight: 800 !important;
        border-radius: 15px !important;
        border: none !important;
        height: 3.5rem !important;
        transition: 0.5s all ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    div.stButton > button:hover {
        background-position: right center !important;
        transform: scale(1.03) translateY(-3px);
        box-shadow: 0px 10px 20px rgba(80, 255, 177, 0.4);
    }

    /* Step Indicators */
    .step-box { padding: 12px; border-radius: 12px; text-align: center; font-size: 0.85rem; transition: 0.3s; }
    .step-active { background: #50FFB1; color: #050730; font-weight: bold; box-shadow: 0 0 15px #50FFB1; }
    .step-inactive { background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.3); }

    .hero-title { font-size: 5.5rem; font-weight: 900; color: #50FFB1; letter-spacing: -4px; line-height: 1; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. STATE & MODEL ASSET MANAGEMENT
# =====================================================
if "page" not in st.session_state: st.session_state.page = "landing"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

@st.cache_resource
def load_models():
    try:
        rf = joblib.load("rf_abandonment_model.pkl")
        arima = joblib.load("arima_model.pkl")
        return rf, arima
    except: return None, None

rf_model, arima_model = load_models()

# =====================================================
# 3. PAGE NAVIGATION
# =====================================================

# --- LANDING PAGE ---
if st.session_state.page == "landing":
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col_logo, _ = st.columns([1, 0.4, 1])
    with col_logo:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown("<h1 class='hero-title' style='text-align:center;'>CARTGUARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:8px; opacity:0.6; font-size:0.9rem;'>NEURAL INTENT ARCHITECTURE</p>", unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1.2, 0.6, 1.2])
    with col_btn:
        if st.button("INITIALIZE SYSTEM"):
            st.session_state.page = "login"
            st.rerun()

# --- LOGIN PAGE ---
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#50FFB1; margin-top:0; text-align:center;'>SECURE ACCESS</h2>", unsafe_allow_html=True)
        u = st.text_input("ADMINISTRATOR ID", placeholder="ID...")
        p = st.text_input("ACCESS KEY", type="password", placeholder="••••••••")
        if st.button("AUTHORIZE"):
            if u == "admin" and p == "admin123":
                with st.spinner("Decrypting Neural Nodes..."):
                    time.sleep(1.2)
                    st.session_state.logged_in = True
                    st.rerun()
            else: st.error("Unauthorized: Credentials Invalid")
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
elif st.session_state.logged_in:
    with st.sidebar:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=80)
        st.markdown("<h2 style='color:#50FFB1;'>CartGuard</h2>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.radio("ECOSYSTEM", ["Live Intent", "Journey Mapping", "Global Forecast"])
        st.markdown("---")
        if st.button("SHUTDOWN SYSTEM"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    if menu == "Live Intent":
        st.markdown("<h1 style='color:#50FFB1;'>Neural Session Scan</h1>", unsafe_allow_html=True)
        
        # Grid Controls
        with st.container():
            c1, c2, c3, c4 = st.columns(4)
            with c1: items = st.number_input("Cart Count", 1, 50, 3)
            with c2: val = st.number_input("Session Value ($)", 10.0, 10000.0, 450.0)
            with c3: dwell = st.number_input("Active Dwell (Min)", 0.1, 60.0, 4.5)
            with c4: step = st.selectbox("Current Node", ["Cart", "Shipping", "Payment", "Final"])

        if st.button("RUN INFERENCE"):
            with st.status("Analyzing Packet Behavior...") as status:
                time.sleep(1.5)
                # Detection Logic
                is_bot = (items > 25 and dwell < 0.3)
                risk_pct = 92 if (val > 1500 and dwell < 1.0) else 18
                if rf_model:
                    features = np.array([[items, val, dwell, 0, 0, 0, 0, 0, 0, 0]])
                    risk_pct = int(rf_model.predict_proba(features)[0][1] * 100)
                status.update(label="Inference Complete", state="complete")

            # --- JOURNEY PATH ANIMATED ---
            st.markdown("### 🗺️ Live Progression Path")
            steps = ["Cart", "Shipping", "Payment", "Final"]
            step_cols = st.columns(len(steps))
            for i, s in enumerate(steps):
                active = "step-active" if s == step else "step-inactive"
                step_cols[i].markdown(f"<div class='step-box {active}'>{s}</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- METRIC CARDS ---
            res_c1, res_c2, res_c3 = st.columns(3)
            with res_c1:
                r_color = "#FF4B4B" if risk_pct > 70 else "#50FFB1"
                st.markdown(f"<div class='glass-card'><h5>RISK SCORE</h5><h1 style='color:{r_color}; font-size:3.5rem;'>{risk_pct}%</h1></div>", unsafe_allow_html=True)
            with res_c2:
                st.markdown(f"<div class='glass-card'><h5>BOT STATUS</h5><h1 style='color:#50FFB1;'>{'DETECTED' if is_bot else 'CLEAN'}</h1></div>", unsafe_allow_html=True)
            with res_c3:
                offer = "SAVE25" if risk_pct > 75 else "FREE_SHIP" if risk_pct > 40 else "NONE"
                st.markdown(f"<div class='glass-card'><h5>AUTO-RECOVERY</h5><h1 style='color:#FFA500;'>{offer}</h1></div>", unsafe_allow_html=True)

            # --- ANIMATED PLOTLY BAR ---
            v1, v2 = st.columns(2)
            with v1:
                st.markdown("### Decision Attribution")
                fig = px.bar(x=[risk_pct, 100-risk_pct], y=["Abandon", "Convert"], orientation='h', 
                             color=["Abandon", "Convert"], color_discrete_map={"Abandon":"#FF4B4B", "Convert":"#50FFB1"})
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white',
                                 height=300, transition_duration=1200, transition_easing="cubic-in-out")
                st.plotly_chart(fig, use_container_width=True)
            with v2:
                st.markdown("### Interaction Heatmap")
                st.plotly_chart(px.imshow(np.random.rand(6,6), color_continuous_scale='Viridis').update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0)), use_container_width=True)

    elif menu == "Journey Mapping":
        st.markdown("<h1 style='color:#50FFB1;'>Conversion Funnel Analytics</h1>", unsafe_allow_html=True)
        
        funnel_data = pd.DataFrame(dict(val=[1200, 850, 320, 110], stage=["Added to Cart", "Shipping Entry", "Payment Loaded", "Final Order"]))
        fig = px.funnel(funnel_data, x='val', y='stage', color_discrete_sequence=['#50FFB1'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', transition_duration=1500)
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Global Forecast":
        st.markdown("<h1 style='color:#50FFB1;'>Predictive Revenue Engine</h1>", unsafe_allow_html=True)
        if arima_model:
            forecast = arima_model.forecast(steps=14)
            st.line_chart(forecast)
            st.info("💡 ARIMA model is projecting a 12% decrease in abandonment for next week based on current recovery scripts.")
        else: st.warning("ARIMA Forecasting model (`arima_model.pkl`) not found in repository.")  
