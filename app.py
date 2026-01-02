import streamlit as st
import os
import string
import pandas as pd
import json
from dotenv import load_dotenv
from openai import OpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="FitNexus Enterprise Demo", page_icon="⚡", layout="wide")
load_dotenv()

# --- 2. THE ENGINE (Your Logic) ---
class FitNexusEngine:
    def __init__(self, data_file="fashion_products_mock.csv"):
        self.catalog = pd.DataFrame()
        try:
            if os.path.exists(data_file):
                self.catalog = pd.read_csv(data_file)
                self.catalog.columns = self.catalog.columns.str.strip()
                self.catalog = self.catalog.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        except Exception:
            pass

        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except:
            st.error("SYSTEM ERROR: Check API Key.")

    def analyze_fit(self, query, user_profile):
        # A. Search Logic
        if self.catalog.empty: return {"error": "Catalog disconnected"}
        
        clean_query = query.lower().translate(str.maketrans('', '', string.punctuation))
        scored = []
        for _, row in self.catalog.iterrows():
            text = f"{row.get('name','')} {row.get('description','')} {row.get('fit_type','')}".lower()
            score = sum(1 for w in clean_query.split() if w in text)
            if score > 0: scored.append((score, row))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        products = [item[1] for item in scored] if scored else [r for _, r in self.catalog.iterrows()][:4]

        # B. AI Analysis
        context = "\n".join([f"- {p['name']} ({p['fit_type']}): {p['fit_advice']}" for p in products[:4]])
        
        system_prompt = (
            "You are the FitNexus API. Analyze the User Profile vs Product Data. "
            "Output a short, decisive recommendation for the shopper."
        )
        user_msg = f"Profile: {user_profile}\nQuery: {query}\nInventory:\n{context}"
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}]
        )
        
        return {
            "status": 200,
            "analysis": response.choices[0].message.content,
            "product": products[0].get('name')
        }

if "engine" not in st.session_state:
    st.session_state.engine = FitNexusEngine()

# --- 3. THE DEMO UI ---
with st.sidebar:
    st.header("FitNexus Engine")
    mode = st.radio("Select Demo Mode:", ["🛍️ Nike/Lulu Simulation", "👨‍💻 API Developer View"])
    st.divider()
    st.subheader("Simulated User")
    profile = st.selectbox("Load Profile", ["Long Torso / Tall", "Petite / Curves", "Standard"])
    
    if profile == "Long Torso / Tall":
        user_data = {"height": "> 6'0", "challenges": ["Long Torso", "Broad Shoulders"]}
    elif profile == "Petite / Curves":
        user_data = {"height": "< 5'3", "challenges": ["Large Bust", "Short Torso"]}
    else:
        user_data = {"height": "5'7", "challenges": ["None"]}
    
    st.info(f"**Active Context:**\n{user_data}")

# --- MODE 1: THE WIDGET SIMULATION ---
if mode == "🛍️ Nike/Lulu Simulation":
    # Header mimics a top-tier retail site
    st.markdown("### 🛒 Lululemon / Nike Storefront Simulator")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Placeholder for a product image
        st.image("https://images.lululemon.com/is/image/lululemon/LW3DM4S_032489_1?wid=750&op_usm=0.8,1,10,0&fmt=webp&qlt=80,1&fit=constrain,0&op_sharpen=0&resMode=sharp2&iccEmbed=0&printRes=72", caption="Scuba Oversized Half-Zip Hoodie")
    
    with col2:
        st.subheader("Scuba Oversized Half-Zip Hoodie")
        st.write("⭐⭐⭐⭐⭐ (4.8) | **$118.00**")
        st.write("The ultimate post-workout layer. Oversized, cozy, and breathable.")
        
        st.markdown("#### Select Size")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], horizontal=True, label_visibility="collapsed")
        
        st.button("Add to Bag", type="primary")
        
        # --- THE FITNEXUS INTEGRATION ---
        st.markdown("---")
        with st.expander("✨ FitNexus Intelligence (Click to Test)"):
            st.caption(f"Analyzing for user with: **{profile}**")
            q = st.text_input("Ask a question:", value="How will this fit my body type?")
            if st.button("Analyze Fit"):
                with st.spinner("Processing Biometrics..."):
                    res = st.session_state.engine.analyze_fit(q, user_data)
                    st.success(f"**FitNexus Recommendation:**\n\n{res['analysis']}")

# --- MODE 2: THE API VIEW ---
else:
    st.title("⚡ FitNexus API Console")
    st.markdown("This view shows the raw JSON data exchanged between the Retailer and FitNexus.")
    
    if st.button("Send Test Request"):
        st.code(json.dumps({
            "endpoint": "POST /v1/recommend",
            "payload": {"user": user_data, "product_sku": "scuba-001"}
        }, indent=2), language="json")
        
        with st.spinner("Computing..."):
            res = st.session_state.engine.analyze_fit("fit check", user_data)
            
        st.code(json.dumps({
            "status": "success",
            "fit_score": 88,
            "message": res['analysis']
        }, indent=2), language="json")