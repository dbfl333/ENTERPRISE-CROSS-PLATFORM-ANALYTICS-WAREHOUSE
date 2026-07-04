import streamlit as st

st.set_page_config(
    page_title="Enterprise Analytics Warehouse",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI CSS styling injection
st.markdown("""
    <style>
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
st.markdown("<p class='sub-text'>Centralized corporate data warehouse integrating live API extraction (Shopify & Binance) and pre-launch empty staging structures (Prompt Labs & Terrazas-home) inside a clean DuckDB star schema.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class='metric-card'>
        <h3>📁 Data Pipeline Overview</h3>
        <p>The pipeline has been migrated from synthetic data generators to real-time API extraction and staging architectures:</p>
        <ul>
            <li><b>Live API Extraction:</b> Shopify REST Admin API and Binance Public Candlestick endpoints extract raw JSON logs directly, saving them as CSV files inside <code>02_raw_data/</code>.</li>
            <li><b>Empty Staging Architecture:</b> Pre-launch systems (Agentic Prompt Labs and Terrazas-home) contain zero fake data. The warehouse provisions their clean relational staging target schemas, leaving them ready for Day 1 launch.</li>
        </ul>
        <p>Use the sidebar navigation to explore the live analytics pages and audit the staging schemas.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card' style='height: 100%;'>
        <h3>🛠️ Infrastructure Stack</h3>
        <ul>
            <li><b>Core SQL Engine:</b> DuckDB (PostgreSQL syntax)</li>
            <li><b>Business Logic:</b> Python 3.12</li>
            <li><b>API Clients:</b> <code>requests</code>, <code>json_normalize</code></li>
            <li><b>Web Presentation:</b> Streamlit (Wide Layout)</li>
            <li><b>Staging Tables:</b> Structured empty tables</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 Open the sidebar navigation menu to explore each tenant page and audit details.")
