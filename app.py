import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google import genai
import os
from dotenv import load_dotenv

# 1. SETUP & CONFIG
load_dotenv()
st.set_page_config(page_title="GTM Revenue Intelligence", layout="wide")

# Standard format function for a professional Finance look
def format_currency(value):
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    else:
        return f"${value:,.0f}"

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# 2. DATA LOADING & HEALTH CHECK
st.title("🛡️ Revenue Intelligence Engine")

data_loaded = False
audit_loaded = False

if os.path.exists('crm_data.csv'):
    df = pd.read_csv('crm_data.csv')
    data_loaded = True
else:
    st.error("❌ 'crm_data.csv' missing. Run 'python 1_data_generation.py' first.")
    st.stop()

if os.path.exists('ai_audit_results.csv'):
    audit_df = pd.read_csv('ai_audit_results.csv')
    audit_loaded = True
else:
    audit_df = pd.DataFrame()

# 3. SIDEBAR & FILTERS
st.sidebar.header("🕹️ Strategic Planning")

# Customer Segment Filters
st.sidebar.subheader("🔍 Segment Filters")

def create_filter(label, column_name):
    options = ["All"] + sorted(df[column_name].unique().tolist())
    return st.sidebar.selectbox(label, options)

selected_industry = create_filter("Industry", "Industry")
selected_region = create_filter("Region", "Region")
selected_source = create_filter("Lead Source", "Lead_Source")

# Planning Sliders
st.sidebar.subheader("📈 Forecast Inputs")
target_rev = st.sidebar.number_input("H2 Revenue Target ($)", value=50000000)
win_rate = st.sidebar.slider("Assumed Win Rate (%)", 5, 50, 25) / 100
avg_discount = st.sidebar.slider("Max Discount Buffer (%)", 0, 30, 10) / 100

# 4. GLOBAL FILTERING LOGIC
filtered_df = df.copy()

if selected_industry != "All":
    filtered_df = filtered_df[filtered_df['Industry'] == selected_industry]
if selected_region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_source != "All":
    filtered_df = filtered_df[filtered_df['Lead_Source'] == selected_source]

# 5. CALCULATIONS
total_pipe = filtered_df['Amount'].sum()
weighted_pipe = total_pipe * win_rate * (1 - avg_discount)
gap_to_target = target_rev - weighted_pipe

# 6. KPI ROW
c1, c2, c3, c4 = st.columns(4)
c1.metric("Gross Pipeline", format_currency(total_pipe))
c2.metric("Weighted Forecast", format_currency(weighted_pipe))
c3.metric("Gap to Target", format_currency(gap_to_target), delta_color="inverse")
c4.metric("Audited Deals", len(audit_df))

st.markdown("---")

# 7. VISUALS (Using Filtered Data)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("#### 🚀 Sales Velocity: Deal Size vs. Age")
    # Generate Days_in_Stage for plotting
    filtered_df['Days_in_Stage'] = (filtered_df['Amount'] % 100) + 10
    # Dynamic sampling to prevent crashes on small segments
    sample_size = min(len(filtered_df), 1000)
    if sample_size > 0:
        fig = px.scatter(filtered_df.sample(sample_size), x="Days_in_Stage", y="Amount", color="Stage", size="Amount")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected segments.")

with col_right:
    st.markdown("#### 📊 Weighted Revenue Bridge")
    fig_bridge = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["relative", "relative", "relative", "total"],
        x = ["Gross Pipe", "Win Rate", "Discounting", "Forecast"],
        y = [total_pipe/1e6, -(total_pipe*(1-win_rate)/1e6), -(weighted_pipe*avg_discount/1e6), weighted_pipe/1e6],
        textposition = "outside",
        text = [f"{total_pipe/1e6:.1f}M", "", "", f"{weighted_pipe/1e6:.1f}M"]
    ))
    fig_bridge.update_layout(yaxis_title="USD (Millions)", showlegend=False)
    st.plotly_chart(fig_bridge, use_container_width=True)

# 8. AI EXECUTIVE SUMMARY (With Professional Error Handling)
st.markdown("---")
st.markdown("#### 📝 AI Executive Summary")

if st.button("Generate Board Briefing"):
    if client:
        with st.spinner(f"Analyzing {selected_industry} pipeline..."):
            try:
                # Prepare risks for the prompt
                risks = audit_df['AI_Risk_Assessment'].head(3).tolist() if not audit_df.empty else ["No specific risks found."]
                
                prompt = f"""
                Act as a Strategic Finance Director. Provide a 3-sentence executive summary for the {selected_industry} sector in {selected_region}.
                - Current Segment Pipeline: {format_currency(total_pipe)}
                - Forecasted Revenue: {format_currency(weighted_pipe)}
                - Strategic Risks: {risks}
                Analyze if the target of {format_currency(target_rev)} is achievable.
                """
                
                response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
                st.info(response.text)

            except Exception as e:
                # PROFESSIONAL FALLBACK
                st.warning("⚖️ **Strategic Summary (Automated Fallback)**")
                
                # Logic-based professional insight
                status = "ON TRACK" if gap_to_target <= 0 else "AT RISK"
                priority = "Volume" if win_rate < 0.2 else "Yield/Discounting"
                
                st.markdown(f"""
                **Current Status:** {status}  
                **Analysis:** The {selected_industry} pipeline currently stands at {format_currency(total_pipe)}. 
                With a {win_rate*100:.0f}% win rate, the weighted forecast is {format_currency(weighted_pipe)}.
                
                **Director's Recommendation:** To bridge the {format_currency(abs(gap_to_target))} gap, 
                management should focus on **{priority}** optimization within the {selected_region} region.
                """)
    else:
        st.error("API Key missing. Check your .env file.")

# 9. AUDIT DETAIL TABLE
st.markdown("---")
st.markdown("#### 🎯 Audit Detail")
if not audit_df.empty:
    display_df = audit_df.copy()
    display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(display_df, use_container_width=True)
else:
    st.write("Run 'ai_audit.py' to populate the risk assessments.")