# 🛡️ GTM Revenue Intelligence Engine
### Bridging Strategic Finance & Generative AI (Finance 4.0)

A high-performance Revenue Operations (RevOps) platform that transforms raw CRM data into actionable executive insights using Python, DuckDB, and the Gemini 2.0 AI model.

## 🚀 The Business Problem
Standard CRM reports are often static and lack qualitative context. This engine solves two core issues:
1. **Data Scalability:** Efficiently processes 50,000+ rows of pipeline data for "What-If" scenario planning.
2. **Qualitative Blindspots:** Uses Generative AI to audit sales notes and identify strategic risks (e.g., technical gaps or competitor threats) that traditional metrics miss.

## 🛠️ The Technical Stack
- **Dashboard:** `Streamlit` for an interactive, executive-ready UI.
- **Data Engine:** `Pandas` & `NumPy` for complex financial calculations and multi-segmented filtering.
- **AI Intelligence:** `Google Gemini 2.0 Flash` for automated deal auditing and board-level executive summaries.
- **Resilience:** Implemented custom **Strategic Fallback Logic** to ensure dashboard uptime even during API rate-limiting events.

## 💡 Key Features
- **Multidimensional Filtering:** Slice the entire pipeline by **Industry**, **Region**, and **Lead Source** for granular QBR analysis.
- **Weighted Revenue Bridge:** Dynamic Waterfall chart visualizing the "leakage" from Gross Pipeline to Forecasted Yield.
- **AI-Powered Audit:** Automated risk assessment on high-value deals with professional fallback triggers.
- **Scenario Planning:** Real-time impact analysis of win rates and discount buffers on H2 revenue targets.

## 🏃 Setup & Deployment
1. **Install dependencies:**
   ```powershell
   python -m pip install -r requirements.txt