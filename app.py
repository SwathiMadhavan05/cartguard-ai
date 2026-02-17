import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =====================================================
# 1. CORE THEME & ANIMATION ENGINE
# =====================================================
st.set_page_config(page_title="CartGuard AI | Enterprise", layout="wide")

LOGO_PATH = "logo.jpg" 

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #0a1191 0%, #050730 100%);
        color: white; 
        font-family: 'Satoshi', sans-serif !important;
    }

    /* Glassmorphism Effect */
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

    @keyframes growIn {
        0% { opacity: 0; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1); }
    }

    /* Professional Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #50FFB1, #39d38d) !important;
        color: #050730 !important; 
        font-weight: 800 !important;
        border-radius: 15px !important;
        border: none !important;
        height: 3.5rem !important;
        transition: 0.4s all ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 10px 20px rgba(80, 255, 177, 0.3);
    }

    .step-box { padding: 12px; border-radius: 12px; text-align: center; font-size: 0.85rem; }
    .step-active { background: #50FFB1; color: #050730; font-weight: bold; box-shadow: 0 0 15px #50FFB1; }
    .step-inactive { background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.3); }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. DATA & MODEL LOADING
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
# 3. APP ROUTING
# =====================================================

# --- LANDING ---
if st.session_state.page == "landing":
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:5.5rem; color:#50FFB1; font-weight:900;'>CARTGUARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6; letter-spacing:5px;'>NEURAL REVENUE PROTECTION</p>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 0.6, 1])
    with col_btn:
        if st.button("INITIALIZE"):
            st.session_state.page = "login"
            st.rerun()

# --- LOGIN ---
elif st.session_state.page == "login" and not st.session_state.logged_in:
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        st.markdown("<br><br><div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#50FFB1; text-align:center;'>SECURE ACCESS</h3>", unsafe_allow_html=True)
        u = st.text_input("ADMIN ID")
        p = st.text_input("PASSWORD", type="password")
        if st.button("AUTHORIZE"):
            if u == "admin" and p == "admin123":
                st.session_state.logged_in = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- DASHBOARD ---
elif st.session_state.logged_in:
    with st.sidebar:
        st.markdown("<h2 style='color:#50FFB1;'>CartGuard</h2>", unsafe_allow_html=True)
        menu = st.radio("NAVIGATION", ["Live Intent", "Journey Mapping", "Forecast"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    if menu == "Live Intent":
        st.markdown("<h2 style='color:#50FFB1;'>Inference Engine</h2>", unsafe_allow_html=True)
        
        # User Inputs
        c1, c2, c3, c4 = st.columns(4)
        with c1: items = st.number_input("Items", 1, 50, 3)
        with c2: val = st.number_input("Value ($)", 10.0, 5000.0, 450.0)
        with c3: dwell = st.number_input("Dwell (Min)", 0.1, 60.0, 4.5)
        with c4: step = st.selectbox("Stage", ["Cart", "Shipping", "Payment", "Final"])

        if st.button("RUN NEURAL SCAN"):
            # Calculate Risk
            risk_target = 90 if (val > 1500 and dwell < 1.0) else 20
            if rf_model:
                features = np.array([[items, val, dwell, 0, 0, 0, 0, 0, 0, 0]])
                risk_target = int(rf_model.predict_proba(features)[0][1] * 100)
            
            # ANIMATED RADAR CHART
            radar_placeholder = st.empty()
            categories = ['Price Sensitivity', 'Bot Prob.', 'Purchase Intent', 'UX Friction', 'Urgency']
            
            for r in range(1, 11):
                r_vals = [risk_target*0.8, (items*2 if items > 20 else 10), 100-risk_target, 30, 70]
                animated_r = [v * (r/10) for v in r_vals]
                
                fig = go.Figure(data=go.Scatterpolar(r=animated_r, theta=categories, fill='toself', line_color='#50FFB1', fillcolor='rgba(80, 255, 177, 0.3)'))
                fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), bgcolor='rgba(0,0,0,0)'),
                                  paper_bgcolor='rgba(0,0,0,0)', font_color='white', height=400, showlegend=False)
                radar_placeholder.plotly_chart(fig, use_container_width=True, key=f"radar_{r}")
                time.sleep(0.03)

            # Results
            st.markdown("### Decision Matrix")
            r1, r2, r3 = st.columns(3)
            with r1: st.markdown(f"<div class='glass-card'><h6>RISK</h6><h2 style='color:#FF4B4B;'>{risk_target}%</h2></div>", unsafe_allow_html=True)
            with r2: st.markdown(f"<div class='glass-card'><h6>BOT SCAN</h6><h2 style='color:#50FFB1;'>{'BOT' if items > 25 else 'HUMAN'}</h2></div>", unsafe_allow_html=True)
            with r3: st.markdown(f"<div class='glass-card'><h6>ACTION</h6><h2 style='color:#FFA500;'>SAVE20</h2></div>", unsafe_allow_html=True)

    elif menu == "Journey Mapping":
        st.markdown("<h2 style='color:#50FFB1;'>Conversion Funnel</h2>", unsafe_allow_html=True)
        
        f_data = pd.DataFrame(dict(val=[1200, 800, 400, 150], stage=["Cart", "Shipping", "Payment", "Order"]))
        st.plotly_chart(px.funnel(f_data, x='val', y='stage', color_discrete_sequence=['#50FFB1']).update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white'))
