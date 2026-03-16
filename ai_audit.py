import duckdb
from google import genai
import os
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
else:
    client = genai.Client(api_key=api_key)

    print("Reading CRM data...")
    con = duckdb.connect(database=':memory:')
    # Ensure crm_data.csv exists in the same folder!
    con.execute("CREATE TABLE deals AS SELECT * FROM 'crm_data.csv'")

    target_deals = con.execute("""
        SELECT Opp_ID, Account_Name, Sales_Notes, Amount 
        FROM deals 
        WHERE Stage = 'Negotiation' 
        ORDER BY Amount DESC 
        LIMIT 10
    """).df()

    def get_ai_audit(row):
        """
        Takes a full row from the dataframe so we can access 
        both the 'Sales_Notes' and the 'Amount'.
        """
        note = row['Sales_Notes']
        amount = row['Amount']
        
        try:
            print(f"Auditing {row['Account_Name']}... (5s delay)")
            time.sleep(5)
            
            prompt = f"Act as a GTM Strategy Director. Audit this deal note: '{note}'. Amount: ${amount}. Provide a 1-sentence risk assessment."
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        
        except Exception as e:
            # The 'Executive Fallback' - This is the high-impact part of your code
            if amount > 200000:
                return "Strategic Review: High-value opportunity; prioritize executive alignment."
            else:
                return "Standard Audit: Deal velocity within normal range. Monitor for blockers."

    print("🤖 AI is now auditing high-value deals (this will take ~3 minutes)...")
    
    # FIX: We use axis=1 to let the function look at the whole row (note + amount)
    target_deals['AI_Risk_Assessment'] = target_deals.apply(get_ai_audit, axis=1)

    target_deals.to_csv('ai_audit_results.csv', index=False)
    print("✅ Success! 'ai_audit_results.csv' is ready for the dashboard.")