import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# =====================================================
# 1. THE ULTIMATE UI CONFIGURATION (CSS OVERHAUL)
# =====================================================
st.set_page_config(page_title="CartGuard AI | Portal", layout="wide")

LOGO_PATH = "logo.jpg" 

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/satoshi');
    
    /* Global Styles */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #0a0e91 0%, #050761 100%);
        color: white; 
        font-family: 'Satoshi', sans-serif !important;
    }

    /* Animated Background Elements */
    .bg-glow {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        opacity: 0.1;
        z-index: -1;
    }

    /* Glassmorphism Login Container */
    .login-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(80, 255, 177, 0.2);
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        text-align: center;
        margin-top: 50px;
    }

    /* Typography & Effects */
    .hero-text {
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(to bottom, #50FFB1, #39d38d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -2px;
    }

    .sub-text {
        font-size: 1.1rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.6);
        margin-top: -10px;
    }

    /* Custom Input Styling (Forcing Dark Mode Look) */
    div[data-baseweb="input"] {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(80, 255, 177, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    input {
        color: white !important;
        font-weight: 500 !important;
    }

    label {
        color: #50FFB1 !important;
        text-transform: uppercase;
        font-size: 0.8rem !important;
        letter-spacing: 1px;
    }

    /* The "Power" Button */
    div.stButton > button {
        background: linear-gradient(90deg, #50FFB1, #39d38d) !important;
        color: #050761 !important; 
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-radius: 15px !important;
        border: none !important;
        height: 3rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 30px rgba(80, 255, 177, 0.5);
    }

    /* Animations */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in { animation: slideUp 1s ease-out; }
    </style>
    <div class="bg-glow"></div>
    """, unsafe_allow_html=True)

# =====================================================
# 2. APP STATE & ROUTING
# =====================================================
if "page" not in st.session_state: st.session_state.page = "landing"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- LANDING PAGE ---
if st.session_state.page == "landing":
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col_logo, _ = st.columns([1, 0.4, 1])
    with col_logo:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown("<div class='animate-in'><h1 class='hero-text' style='text-align:center;'>CARTGUARD</h1><p class='sub-text' style='text-align:center;'>AI Revenue Protection</p></div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1.2, 0.6, 1.2])
    with col_btn:
        if st.button("INITIALIZE TERMINAL"):
            st.session_state.page = "login"
            st.rerun()

# --- NEW IMPRESSIVE LOGIN PAGE ---
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.2, 1])
    
    with col_login:
        st.markdown("""
            <div class='login-card animate-in'>
                <h2 style='color: #50FFB1; margin-bottom: 5px;'>SECURITY CLEARANCE</h2>
                <p style='color: rgba(255,255,255,0.5); font-size: 0.9rem;'>Level 4 Encrypted Access Required</p>
            </div>
        """, unsafe_allow_html=True)
        
        # We wrap inputs in a container to maintain styling
        with st.container():
            st.markdown("<br>", unsafe_allow_html=True)
            u = st.text_input("ADMINISTRATOR ID", placeholder="Enter ID...")
            p = st.text_input("ACCESS KEY", type="password", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("AUTHORIZE ACCESS"):
                if u == "admin" and p == "admin123":
                    with st.spinner("Decrypting Dashboard..."):
                        time.sleep(1.5)
                        st.session_state.logged_in = True
                        st.rerun()
                else:
                    st.error("ACCESS DENIED: Invalid Credentials")

# --- DASHBOARD (保持原功能不变) ---
elif st.session_state.logged_in:
    # (Existing Dashboard Code stays here...)
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
            st.write("Scan Initiated...")
            # (Rest of the analysis logic from previous version goes here)
