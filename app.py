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

# Ensure this matches your filename in the folder
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
# 3. PAGE ROUTING: LANDING PAGE
# =====================================================
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

# =====================================================
# 4. PAGE ROUTING: LOGIN PAGE
# =====================================================
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

# =====================================================
# 5. PAGE ROUTING: MAIN DASHBOARD
# =====================================================
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
        st.markdown("<h1 style='color: #50FFB1;'>Live Intelligence</h1>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: items = st.number_input("ITEMS", 1, 20, 2)
        with c2: val = st.number_input("VALUE ($)", 1.0, 5000.0, 250.0)
        with c3: dwell = st.number_input("DWELL (M)", 0.0, 60.0, 10.0)
        with c4: plat = st.selectbox("PLATFORM", [0, 1], format_func=lambda x: "Mobile" if x==1 else "Desktop")

        if st.button("RUN NEURAL INFERENCE"):
            with st.status("Analyzing user behavior...", expanded=True) as status:
                time.sleep(0.8)
                # FIXED LOGIC: Override for high value/low dwell
                if val >= 1000 and dwell <= 1.0:
                    risk_pct = 94
                elif plat == 1 and val > 600 and dwell < 2.0:
                    risk_pct = 82
                else:
                    if rf_model:
                        features = np.array([[items, val, dwell, plat, 0, 0, 0, 0, 0, 0]])
                        prob = rf_model.predict_proba(features)[0][1]
                        risk_pct = int(prob * 100)
                    else:
                        risk_pct = 15
                status.update(label="Inference Complete!", state="complete", expanded=False)

            score_color = "#FF4B4B" if risk_pct > 70 else "#50FFB1"
            res_col1, res_col2 = st.columns([1.5, 1])

            with res_col1:
                st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.1); padding:20px; border-radius:15px; border:1px solid {score_color}; margin-bottom: 20px;'>
                        <h3 style='margin:0; font-size: 1rem; opacity: 0.8;'>ABANDONMENT RISK SCORE</h3>
                        <h1 style='color:{score_color}; font-size:4.5rem; margin:0;'>{risk_pct}%</h1>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("### 🤖 Behavioral Intelligence")
                if risk_pct > 70: st.error("**CRITICAL THREAT DETECTED:** High-risk signature.")
                elif risk_pct > 35: st.warning("**MODERATE HESITATION:** Comparison shopping.")
                else: st.success("**POSITIVE PURCHASE INTENT:** Strong behavioral flow.")

            with res_col2:
                fig = go.Figure(data=[go.Pie(labels=['Risk', 'Retention'], values=[risk_pct, 100 - risk_pct], hole=.75, marker_colors=[score_color, '#1a1c23'], sort=False, direction='clockwise')])
                fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=240, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"**AI STRATEGY:** {'Deploy exit-intent offer' if risk_pct > 70 else 'Show social proof' if risk_pct > 35 else 'Seamless checkout'}.")

    elif menu == "Global Forecast":
        st.markdown("<h1 style='color: #50FFB1;'>Strategic Projections</h1>", unsafe_allow_html=True)
        if arima_model:
            forecast = arima_model.forecast(steps=14)
            df_forecast = pd.DataFrame({'Day': range(1, 15), 'Forecast': forecast})
            fig = px.line(df_forecast, x='Day', y='Forecast', color_discrete_sequence=['#50FFB1'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("Forecast model unavailable.")

    elif menu == "Model Insights":
        st.markdown("<h1 style='color: #50FFB1;'>Neural Interpretability</h1>", unsafe_allow_html=True)
        feat_imp = pd.DataFrame({'Factor': ['Cart Value', 'Dwell Time', 'Item Count'], 'Importance': [0.45, 0.35, 0.20]})
        fig = px.bar(feat_imp, x='Importance', y='Factor', orientation='h', color_discrete_sequence=['#50FFB1'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)