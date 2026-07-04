# Skill 4: Local Web App Presentation Interface (Streamlit)

## Objective
Design and build a multi-page interactive local business intelligence panel that showcases both analytical business metrics and data engineering pipeline quality.

## Framework Constraints
- **Core Technology:** Python, Streamlit.
- **Layout Design:** Modern dark theme styling, cohesive color scheme, readable typography, and sidebar-driven multi-page navigation matching the specification.

## Multi-Page Structure
1. **Executive Overview (`01_executive_overview.py`):** Consolidated operational metrics across all 4 tenants in a single page.
2. **Data Quality Showcase (`02_data_quality_etl.py`):** Split-screen layout displaying raw vs. clean datasets side-by-side. Highlight specific parsed fields, handled nulls, and anomaly cleanups to demonstrate pipeline effectiveness.
3. **Shop Analytics (`03_shop_analytics.py`):** Conversion funnels, customer geography charts, and pricing trends.
4. **Prompt Analytics (`04_prompt_analytics.py`):** Latency tracking, rate limits, token usage, and performance breakdowns.
5. **Terrazas Analytics (`05_terrazas_analytics.py`):** Venue calendar schedules, double-booking alerts, and corrected reservations.
6. **GTrend Screener (`06_gtrend_analytics.py`):** Quantitative metrics including Win-Rate, Maximum Drawdowns, and Profit Factor distributions.
