import streamlit as st
import os

# Set page configuration
st.set_page_config(
    page_title="Enterprise Analytics Warehouse",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI CSS styling injection
st.markdown("""
    <style>
    /* Dark glassmorphism card design */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
        transition: transform 0.2s, border-color 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 224, 255, 0.3);
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00E5FF, #7D2AE8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .sub-text {
        color: #B2B2B2;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Landing Page Content
st.markdown("<h1 class='main-header'>Enterprise Analytics Warehouse & BI Suite</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>A high-performance local corporate data warehouse consolidating multi-tenant metrics across E-Commerce, SaaS telemetry, Property bookings, and Quantitative strategies into a unified DuckDB analytical store.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class='metric-card'>
        <h3>📁 Data Pipeline Overview</h3>
        <p>The warehouse ingests raw, disconnected, and malformed files from four distinct business channels, processes them through isolated PostgreSQL transformation scripts, and merges them into a clean dimensional warehouse model.</p>
        <p>Select any tenant module in the sidebar to review detailed performance analytics, or visit the <b>Data Quality ETL</b> showcase to inspect raw vs. clean database tables.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("https://raw.githubusercontent.com/duckdb/duckdb/master/images/logo-horizontal.png", width=200)

with col2:
    st.markdown("""
    <div class='metric-card' style='height: 100%;'>
        <h3>🛠️ Architecture Stack</h3>
        <ul>
            <li><b>Core SQL Engine:</b> DuckDB</li>
            <li><b>Business Logic:</b> Python 3.12</li>
            <li><b>Web Presentation:</b> Streamlit Wide Layout</li>
            <li><b>Orchestration:</b> Local Pipeline Scripts</li>
            <li><b>Data Store:</b> Star Schema Dimensions/Facts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 Open the sidebar navigation menu to explore each tenant page and audit details.")
