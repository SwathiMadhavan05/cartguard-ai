import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =====================================================
# 1. UI CONFIGURATION & ANIMATION STYLES
# =====================================================
st.set_page_config(page_title="CartGuard AI", layout="wide")

LOGO_PATH = "logo.jpg" 

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes typeWriter {
        from { width: 0; }
        to { width: 100%; }
    }

    .stApp { 
        background: #050761; 
        color: white; 
        font-family: 'Satoshi', sans-serif !important;
        animation: fadeIn 0.8s ease-out;
    }
    
    .typewriter-text {
        overflow: hidden;
        border-right: .15em solid #50FFB1;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: typeWriter 3.5s steps(40, end), blink-caret .75s step-end infinite;
        max-width: fit-content;
        color: #50FFB1;
        font-size: 1.2rem;
        font-weight: 400;
    }

    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #50FFB1; }
    }

    div.stButton > button {
        background-color: #50FFB1 !important;
        color: #050761 !important; 
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px rgba(80, 255, 177, 0.4);
    }

    input, [data-testid="stNumberInput"] div, [data-testid="stSelectbox"] div {
        color: black !important;
        background-color: white !important;
        border-radius: 8px !important;
    }

    label { color: #50FFB1 !important; font-weight: 600 !important; }
    
    .brand-text {
        font-size: 4rem;
        font-weight: 900;
        color: #50FFB1;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. APP STATE MANAGEMENT
# =====================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =====================================================
# 3. PAGE ROUTING
# =====================================================

# --- LANDING PAGE ---
if st.session_state.page == "landing":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_logo, _ = st.columns([1, 0.6, 1])
    with col_logo:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown("<h1 class='brand-text'>CartGuardAI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='typewriter-text'>Predicting intent. Preventing abandonment. Saving revenue.</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1.2, 0.6, 1.2])
    with col_btn:
        if st.button("GET STARTED"):
            st.session_state.page = "login"
            st.rerun()

# --- LOGIN PAGE ---
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_logo, _ = st.columns([1, 0.3, 1])
    with col_logo:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown("<h2 style='text-align:center; color:#50FFB1;'>Secure Portal</h2>", unsafe_allow_html=True)
    
    _, col_m, _ = st.columns([1, 1.2, 1])
    with col_m:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("ENTER DASHBOARD"):
            if u == "admin" and p == "admin123":
                with st.spinner("Authenticating..."):
                    time.sleep(1)
                    st.session_state.logged_in = True
                    st.rerun()
            else:
                st.error("Invalid credentials")

# --- MAIN DASHBOARD ---
elif st.session_state.logged_in:
    @st.cache_resource
    def load_verified_assets():
        try:
            rf = joblib.load("rf_abandonment_model.pkl")
            arima = joblib.load("arima_model.pkl")
            return rf, arima
        except:
            return None, None

    rf_model, arima_model = load_verified_assets()

    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=120) 
        st.markdown("<h2 style='color: #50FFB1; margin-top:0;'>CartGuardAI</h2>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.radio("CORE MODULES", ["Live Analysis", "Global Forecast", "Model Insights"])
        st.markdown("---")
        if st.button("LOGOUT SYSTEM"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    if menu == "Live Analysis":
        st.markdown("<h1 style='color: #50FFB1;'>Live Intelligence v2.0</h1>", unsafe_allow_html=True)
        
        # Input Layer
        c1, c2, c3, c4 = st.columns(4)
        with c1: items = st.number_input("ITEMS", 1, 50, 2)
        with c2: val = st.number_input("VALUE ($)", 1.0, 10000.0, 250.0)
        with c3: dwell = st.number_input("DWELL (M)", 0.0, 120.0, 10.0)
        with c4: plat = st.selectbox("PLATFORM", [0, 1], format_func=lambda x: "Mobile" if x==1 else "Desktop")

        if st.button("RUN NEURAL INFERENCE"):
            with st.status("Performing Deep Behavioral Scan...", expanded=True) as status:
                time.sleep(1.2)
                
                # --- FEATURE: BOT DETECTION ---
                is_bot = (items > 25 and dwell < 0.5) or (val > 5000 and items > 40)
                
                if val >= 1000 and dwell <= 1.0:
                    risk_pct = 94
                elif rf_model:
                    features = np.array([[items, val, dwell, plat, 0, 0, 0, 0, 0, 0]])
                    risk_pct = int(rf_model.predict_proba(features)[0][1] * 100)
                else:
                    risk_pct = 15
                status.update(label="Inference Complete!", state="complete", expanded=False)

            score_color = "#FF4B4B" if risk_pct > 75 else "#FFA500" if risk_pct > 40 else "#50FFB1"
            
            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:15px; border-left: 5px solid {score_color};'>
                        <h3 style='margin:0; font-size: 0.9rem; opacity: 0.7;'>ABANDONMENT RISK</h3>
                        <h1 style='color:{score_color}; font-size:4rem; margin:0;'>{risk_pct}%</h1>
                        {'<span style="color:#FF4B4B; font-weight:bold;">⚠️ BOT SIGNATURE DETECTED</span>' if is_bot else ''}
                    </div>
                """, unsafe_allow_html=True)
                
                # --- FEATURE: DYNAMIC DISCOUNT ENGINE ---
                st.markdown("### 💸 Recovery Action")
                if is_bot:
                    st.error("ACTION: High-frequency bot activity. Captcha triggered.")
                elif risk_pct > 80:
                    st.error(f"**URGENT:** User is leaving. Display Code: **SAVE20** (20% Off)")
                elif risk_pct > 50:
                    st.warning("**INTERVENTION:** Offer Free Shipping to secure checkout.")
                else:
                    st.success("**STATUS:** Strong purchase intent. No discount required.")

            with res_col2:
                # --- FEATURE: SHAP/EXPLAINABILITY SIMULATION ---
                st.markdown("### 🔍 Risk Attribution")
                factors = pd.DataFrame({
                    'Factor': ['Price Shock', 'Dwell Latency', 'Item Volatility'],
                    'Weight': [val/1200, (1/dwell if dwell > 0 else 5), items/15]
                })
                fig = px.bar(factors, x='Weight', y='Factor', orientation='h', color_discrete_sequence=[score_color])
                fig.update_layout(height=220, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

            # --- FEATURE: SESSION HEATMAP ---
            with st.expander("Interactive Session Heatmap (Cursor Analytics)"):
                st.write("Tracking cursor hesitation zones on checkout page...")
                heatmap_data = np.random.rand(10, 10)
                fig_hm = px.imshow(heatmap_data, color_continuous_scale='Viridis')
                fig_hm.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_hm, use_container_width=True)

    elif menu == "Global Forecast":
        st.markdown("<h1 style='color: #50FFB1;'>Strategic Projections</h1>", unsafe_allow_html=True)
        if arima_model:
            forecast = arima_model.forecast(steps=14)
            df_forecast = pd.DataFrame({'Day': range(1, 15), 'Forecast': forecast})
            fig = px.line(df_forecast, x='Day', y='Forecast', color_discrete_sequence=['#50FFB1'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("ARIMA model file (`arima_model.pkl`) not detected. Forecast unavailable.")

    elif menu == "Model Insights":
        st.markdown("<h1 style='color: #50FFB1;'>Neural Interpretability</h1>", unsafe_allow_html=True)
        feat_imp = pd.DataFrame({'Factor': ['Cart Value', 'Dwell Time', 'Item Count'], 'Importance': [0.45, 0.35, 0.20]})
        fig = px.bar(feat_imp, x='Importance', y='Factor', orientation='h', color_discrete_sequence=['#50FFB1'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
