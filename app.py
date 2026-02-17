import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =====================================================
# 1. ADVANCED UI & CSS (Fixed Animations)
# =====================================================
st.set_page_config(page_title="CartGuard AI | Enterprise", layout="wide")
LOGO_PATH = "logo.jpg" 

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    .stApp { background: radial-gradient(circle at 50% 50%, #0a1191 0%, #050730 100%); color: white; font-family: 'Satoshi', sans-serif !important; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(80, 255, 177, 0.2); padding: 25px; border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 20px;
        animation: fadeInUp 0.8s ease-out;
    }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

    div.stButton > button {
        background: linear-gradient(90deg, #50FFB1, #39d38d) !important; color: #050730 !important; 
        font-weight: 800 !important; border-radius: 15px !important; border: none !important; height: 3.5rem !important;
        transition: 0.4s ease; text-transform: uppercase; letter-spacing: 1px; width: 100%;
    }
    
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(80, 255, 177, 0.4); }

    .step-box { padding: 10px; border-radius: 10px; text-align: center; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.1); }
    .step-active { background: #50FFB1; color: #050730; font-weight: bold; box-shadow: 0 0 15px #50FFB1; }
    .step-inactive { background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.3); }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. SESSION & MODEL MANAGEMENT
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
# 3. ROUTING & DASHBOARD
# =====================================================

if st.session_state.page == "landing":
    st.markdown("<br><br><br><br><h1 style='text-align:center; font-size:5rem; color:#50FFB1; font-weight:900;'>CARTGUARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; opacity:0.6;'>NEURAL REVENUE PROTECTION</p>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1.2, 0.6, 1.2])
    with col_btn:
        if st.button("INITIALIZE SYSTEM"):
            st.session_state.page = "login"; st.rerun()

elif st.session_state.page == "login" and not st.session_state.logged_in:
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#50FFB1; margin-top:0;'>SECURE LOGIN</h2>", unsafe_allow_html=True)
        u = st.text_input("ADMIN ID")
        p = st.text_input("ACCESS KEY", type="password")
        if st.button("AUTHORIZE"):
            if u == "admin" and p == "admin123":
                st.session_state.logged_in = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.logged_in:
    with st.sidebar:
        st.markdown("<h2 style='color:#50FFB1;'>CartGuard</h2>", unsafe_allow_html=True)
        menu = st.radio("NAVIGATION", ["Live Intent", "Journey Mapping", "Global Forecast"])
        if st.button("SHUTDOWN"):
            st.session_state.logged_in = False; st.session_state.page = "landing"; st.rerun()

    if menu == "Live Intent":
        st.markdown("<h1 style='color:#50FFB1;'>Neural Session Scan</h1>", unsafe_allow_html=True)
        
        # Grid Controls
        with st.container():
            c1, c2, c3, c4 = st.columns(4)
            with c1: items_in = st.number_input("Cart Count", 1, 50, 2)
            with c2: val_in = st.number_input("Value ($)", 10.0, 10000.0, 2500.0)
            with c3: dwell_in = st.number_input("Dwell (Min)", 0.1, 60.0, 0.4)
            with c4: step_in = st.selectbox("Stage", ["Cart", "Shipping", "Payment", "Review"])

        if st.button("EXECUTE NEURAL SCAN"):
            # A. PREDICTION LOGIC
            risk_pct = 92 if (val_in > 1500 and dwell_in < 1.0) else 13
            if rf_model:
                try:
                    features = np.array([[items_in, val_in, dwell_in, 0, 0, 0, 0, 0, 0, 0]])
                    risk_pct = int(rf_model.predict_proba(features)[0][1] * 100)
                except: pass

            # B. ANIMATED RADAR PULSE
            radar_placeholder = st.empty()
            categories = ['Price Sensitivity', 'Bot Prob.', 'Intent', 'UX Friction', 'Urgency']
            for r in range(1, 11):
                r_vals = [risk_pct, (85 if items_in > 25 else 15), 100-risk_pct, 35, 75]
                animated_r = [v * (r/10) for v in r_vals]
                fig_radar = go.Figure(data=go.Scatterpolar(r=animated_r, theta=categories, fill='toself', 
                                                           line_color='#FF4B4B' if risk_pct > 70 else '#50FFB1'))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), bgcolor='rgba(0,0,0,0)'),
                                        paper_bgcolor='rgba(0,0,0,0)', font_color='white', height=400, showlegend=False)
                radar_placeholder.plotly_chart(fig_radar, use_container_width=True, key=f"radar_{r}")
                time.sleep(0.02)

            # C. JOURNEY PATHING
            st.markdown("### 🗺️ Live Pathing")
            steps = ["Cart", "Shipping", "Payment", "Review"]
            cols = st.columns(4)
            for i, s in enumerate(steps):
                active = "step-active" if s == step_in else "step-inactive"
                cols[i].markdown(f"<div class='step-box {active}'>{s}</div>", unsafe_allow_html=True)

            # D. METRIC CARDS
            st.markdown("<br>", unsafe_allow_html=True)
            res_c1, res_c2, res_c3 = st.columns(3)
            accent = "#FF4B4B" if risk_pct > 70 else "#50FFB1"
            
            with res_c1: st.markdown(f"<div class='glass-card'><h5>RISK</h5><h1 style='color:{accent};'>{risk_pct}%</h1></div>", unsafe_allow_html=True)
            with res_c2: st.markdown(f"<div class='glass-card'><h5>FRICTION</h5><h1 style='color:#FFA500;'>{step_in}</h1></div>", unsafe_allow_html=True)
            with res_c3: 
                offer = "SAVE25" if risk_pct > 75 else "N/A"
                st.markdown(f"<div class='glass-card'><h5>OFFER</h5><h1 style='color:#50FFB1;'>{offer}</h1></div>", unsafe_allow_html=True)

            # E. RISK ATTRIBUTION
            st.markdown("### Risk Attribution")
            fig_bar = px.bar(x=[risk_pct, 100-risk_pct], y=["Abandon", "Convert"], orientation='h', color=["Abandon", "Convert"],
                             color_discrete_map={"Abandon": "#FF4B4B", "Convert": "#50FFB1"})
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=250, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    elif menu == "Journey Mapping":
        st.markdown("<h1 style='color:#50FFB1;'>Journey Analytics</h1>", unsafe_allow_html=True)
        
        funnel_data = pd.DataFrame(dict(number=[1000, 750, 400, 150], stage=["Cart", "Shipping", "Payment", "Purchase"]))
        fig = px.funnel(funnel_data, x='number', y='stage', color_discrete_sequence=['#50FFB1'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Global Forecast":
        st.markdown("<h1 style='color:#50FFB1;'>Revenue Forecast</h1>", unsafe_allow_html=True)
        
        if arima_model:
            forecast = arima_model.forecast(steps=14)
            st.line_chart(forecast)
        else: st.warning("Forecast model (arima_model.pkl) missing.")
