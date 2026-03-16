import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
n = 50000

print(f"Generating {n} rows of synthetic GTM data...")

# This generates realistic, messy data for a GTM professional to clean
data = {
    'Opp_ID': [f'OPP-{i:05d}' for i in range(n)],
    'Account_Name': [fake.company() for _ in range(n)],
    'Industry': [random.choice(['SaaS', 'FinTech', 'HealthTech', 'Logistics', 'Retail', 'AI']) for _ in range(n)],
    'Region': [random.choice(['EMEA', 'AMER', 'APAC']) for _ in range(n)],
    'Amount': [random.randint(15000, 250000) for _ in range(n)],
    'Stage': [random.choice(['Discovery', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']) for _ in range(n)],
    'Lead_Source': [random.choice(['LinkedIn', 'Cold Outbound', 'G2 Review', 'Webinar', 'Partner']) for _ in range(n)],
    'Sales_Notes': [random.choice([
        "Decision maker is hesitant about the pricing structure.",
        "They are comparing us to a local competitor in Berlin.",
        "Budget is approved, but they need an API integration for Python.",
        "Highly motivated, looking to close by the end of Q3.",
        "Customer requested a 15% discount; Finance approval pending.",
        "Technical gap: missing multi-currency support in the dashboard.",
        "Great call, but internal restructuring might delay the sign-off."
    ]) for _ in range(n)],
    'Created_Date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(n)]
}

df = pd.DataFrame(data)

# Save to CSV - this will act as your "Database"
df.to_csv('crm_data.csv', index=False)

print("✅ Success! 'crm_data.csv' has been created in your project folder.")