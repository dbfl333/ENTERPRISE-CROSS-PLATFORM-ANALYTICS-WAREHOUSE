import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Agentic Prompt Labs Analytics", layout="wide")

st.title("⚡ Agentic Prompt Labs Infrastructure Metrics")
st.markdown("API latency, LLM model tokens usage, and error rate monitoring panel.")

db_path = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(db_path):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()

conn = duckdb.connect(db_path, read_only=True)

# Main Stats
stats = conn.execute("""
    SELECT 
        COUNT(*) as total_requests,
        AVG(latency_ms) as avg_latency,
        SUM(prompt_token_count) as prompt_tokens,
        SUM(completion_token_count) as completion_tokens
    FROM fact_prompt_telemetry
""").fetchone()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total API Requests", f"{stats[0]:,}")
col2.metric("Average Latency (Clean)", f"{stats[1]:,.1f} ms")
col3.metric("Prompt Tokens", f"{stats[2]:,}")
col4.metric("Completion Tokens", f"{stats[3]:,}")

st.write("---")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Sub-routine Latency Performance")
    latency_df = conn.execute("""
        SELECT 
            agent_sub_routine, 
            AVG(latency_ms) as avg_latency,
            MAX(latency_ms) as max_latency
        FROM fact_prompt_telemetry
        GROUP BY 1
        ORDER BY avg_latency DESC
    """).df()
    
    latency_chart = alt.Chart(latency_df).mark_bar(color="#7D2AE8").encode(
        y=alt.Y("agent_sub_routine:N", sort="-x", title="Agent Subroutine"),
        x=alt.X("avg_latency:Q", title="Average Latency (ms)"),
        tooltip=["agent_sub_routine", "avg_latency", "max_latency"]
    ).properties(height=300)
    st.altair_chart(latency_chart, use_container_width=True)

with c2:
    st.subheader("Rate Limit (HTTP 429) Distribution")
    limits_df = conn.execute("""
        SELECT 
            agent_sub_routine, 
            COUNT(*) as error_count
        FROM fact_prompt_telemetry
        WHERE http_status_code = 429
        GROUP BY 1
        ORDER BY error_count DESC
    """).df()
    
    if len(limits_df) > 0:
        limits_chart = alt.Chart(limits_df).mark_bar(color="#FF3333").encode(
            y=alt.Y("agent_sub_routine:N", sort="-x", title="Agent Subroutine"),
            x=alt.X("error_count:Q", title="HTTP 429 Hits"),
            tooltip=["agent_sub_routine", "error_count"]
        ).properties(height=300)
        st.altair_chart(limits_chart, use_container_width=True)
    else:
        st.info("No rate limit errors found in the analytical database.")

st.write("---")

# Model Token Metrics
st.subheader("LLM Token Usage by Model")
model_df = conn.execute("""
    SELECT 
        model, 
        SUM(prompt_token_count) as prompt_tokens,
        SUM(completion_token_count) as completion_tokens,
        AVG(temperature) as avg_temperature
    FROM fact_prompt_telemetry
    GROUP BY 1
""").df()

st.dataframe(model_df, use_container_width=True)

conn.close()
