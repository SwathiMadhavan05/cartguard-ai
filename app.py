import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =====================================================
# 1. UI CONFIGURATION & ANIMATIONS
# =====================================================
st.set_page_config(page_title="CartGuard AI | Enterprise", layout="wide")

LOGO_PATH = "logo.jpg" 

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 20px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    .stApp { 
        background: radial-gradient(circle at top right, #0a0e91, #050761); 
        color: white; 
        font-family: 'Satoshi', sans-serif !important;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.2rem;
        border-radius: 20px;
        text-align: center;
        animation: fadeInUp 0.8s ease-out;
    }

    /* Checkout Step Indicator */
    .step-active { color: #50FFB1; font-weight: 800; border-bottom: 2px solid #50FFB1; }
    .step-inactive { color: rgba(255,255,255,0.3); }

    div.stButton > button {
        background: linear-gradient(90deg, #50FFB1, #39d38d) !important;
        color: #050761 !important; 
        font-weight: 800 !important;
        border-radius: 50px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. APP STATE & ROUTING
# =====================================================
if "page" not in st.session_state: st.session_state.page = "landing"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if st.session_state.page == "landing":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_logo, _ = st.columns([1, 0.6, 1])
    with col_logo:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, use_container_width=True)
    st.markdown("<h1 style='text-align:center; font-size:4rem; font-weight:900; color:#50FFB1;'>CartGuardAI</h1>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1.2, 0.6, 1.2])
    with col_btn:
        if st.button("LAUNCH TERMINAL"):
            st.session_state.page = "login"
            st.rerun()

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

elif st.session_state.logged_in:
    @st.cache_resource
    def load_assets():
        try:
            rf = joblib.load("rf_abandonment_model.pkl")
            return rf
        except: return None

    rf_model = load_assets()

    with st.sidebar:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=100)
        st.markdown("<h3 style='color:#50FFB1;'>Command Center</h3>", unsafe_allow_html=True)
        menu = st.sidebar.selectbox("MODULE", ["Live Intelligence", "Journey Mapping"])
        if st.button("SHUTDOWN"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    if menu == "Live Intelligence":
        st.markdown("<h1>Live Intelligence</h1>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: items = st.number_input("Cart Items", 1, 100, 3)
        with c2: val = st.number_input("Cart Value ($)", 1.0, 50000.0, 450.0)
        with c3: dwell = st.number_input("Dwell Time (Min)", 0.1, 60.0, 5.0)
        with c4: step = st.selectbox("Current Step", ["Cart Review", "Shipping Info", "Payment Method", "Final Review"])

        if st.button("RUN NEURAL SCAN"):
            with st.spinner("Processing..."):
                time.sleep(1)
                risk = 15
                if rf_model:
                    risk = int(rf_model.predict_proba(np.array([[items, val, dwell, 0, 0, 0, 0, 0, 0, 0]]))[0][1] * 100)

            # --- JOURNEY MAP INDICATOR ---
            st.markdown("### 🗺️ Live Session Path")
            steps = ["Cart Review", "Shipping Info", "Payment Method", "Final Review"]
            cols = st.columns(len(steps))
            for i, s in enumerate(steps):
                if s == step:
                    cols[i].markdown(f"<p class='step-active'>● {s}</p>", unsafe_allow_html=True)
                else:
                    cols[i].markdown(f"<p class='step-inactive'>○ {s}</p>", unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f"<div class='stat-card'><p>ABANDON RISK</p><h2 style='color:#FF4B4B;'>{risk}%</h2></div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='stat-card'><p>FRICTION POINT</p><h2 style='color:#FFA500;'>{step}</h2></div>", unsafe_allow_html=True)
            with m3: 
                recovery = "High" if risk < 40 else "Medium" if risk < 75 else "Critical"
                st.markdown(f"<div class='stat-card'><p>RECOVERY STATUS</p><h2 style='color:#50FFB1;'>{recovery}</h2></div>", unsafe_allow_html=True)

    elif menu == "Journey Mapping":
        st.markdown("<h1>Customer Journey Analytics</h1>", unsafe_allow_html=True)
        
        # --- FEATURE 2: SANKEY / FUNNEL FLOW ---
        st.markdown("### Checkout Friction Funnel")
        
        funnel_data = pd.DataFrame(dict(
            number=[1000, 750, 400, 150],
            stage=["Cart Entry", "Shipping Details", "Payment Input", "Successful Purchase"]
        ))
        fig = px.funnel(funnel_data, x='number', y='stage', color_discrete_sequence=['#50FFB1'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.info("💡 **Insight:** 45% of users abandon at the 'Payment Input' stage. Suggests complex form fields or missing local payment methods.")
        with col_b:
            st.success("✅ **Optimization:** Moving 'Shipping Info' to step 1 increased progression by 12%.")
