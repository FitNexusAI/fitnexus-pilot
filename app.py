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

# --- 2. THE ENGINE ---
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
        if self.catalog.empty: return {"error": "Catalog disconnected"}
        
        # Search Logic
        clean_query = query.lower().translate(str.maketrans('', '', string.punctuation))
        scored = []
        for _, row in self.catalog.iterrows():
            text = f"{row.get('name','')} {row.get('description','')} {row.get('fit_type','')}".lower()
            score = sum(1 for w in clean_query.split() if w in text)
            if score > 0: scored.append((score, row))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        products = [item[1] for item in scored] if scored else [r for _, r in self.catalog.iterrows()][:4]

        # AI Analysis
        context = "\n".join([f"- {p['name']} ({p['fit_type']}): {p['fit_advice']}" for p in products[:4]])
        
        system_prompt = (
            "You are the FitNexus API. Analyze the User Profile vs Product Data. "
            "Output a short, decisive recommendation for the shopper. "
            "Focus on technical fit (stretch, cut, fabric). "
            "If the user has multiple challenges, explain how they interact."
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
    mode = st.radio("Select Demo Mode:", ["🛍️ Retail Storefront (Demo)", "👨‍💻 API Developer View"])
    st.divider()
    
    # --- GRANULAR CONTROLS ---
    st.subheader("Simulated Shopper Context")
    st.caption("Combine parameters to test complex edge cases.")
    
    # 1. Height
    sim_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"], index=2)
    
    # 2. Multi-Select Challenges (UPDATED)
    sim_challenges = st.multiselect(
        "Fit Challenges (Select multiple)", 
        ["Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders", "Large Bust", "Small Bust", "Wide Hips", "Narrow Hips", "Thick Thighs", "Sensitive Skin"],
        default=[]
    )
    
    # Construct Profile
    user_data = {
        "height": sim_height, 
        "challenges": sim_challenges if sim_challenges else ["None"]
    }
    
    st.info(f"**Active Biometrics:**\nHeight: {sim_height}\nIssues: {', '.join(sim_challenges) if sim_challenges else 'None'}")

# --- MODE 1: WHITE LABEL STOREFRONT ---
if mode == "🛍️ Retail Storefront (Demo)":
    st.markdown("### 🛒 Premium Activewear Co. (Integration Demo)")
    st.caption("This view simulates how FitNexus appears on a partner's product page.")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://images.lululemon.com/is/image/lululemon/LW3DM4S_032489_1?wid=750&op_usm=0.8,1,10,0&fmt=webp&qlt=80,1&fit=constrain,0&op_sharpen=0&resMode=sharp2&iccEmbed=0&printRes=72", caption="Product ID: SCUBA-HZ-001")
    
    with col2:
        st.subheader("Oversized Fleece Half-Zip")
        st.write("⭐⭐⭐⭐⭐ (4.8) | **$118.00**")
        st.write("The ultimate post-workout layer. Cotton-blend fleece fabric is naturally breathable.")
        
        st.markdown("#### Select Size")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], horizontal=True, label_visibility="collapsed")
        
        st.button("Add to Bag", type="primary")
        
        # --- THE INTEGRATION ---
        st.markdown("---")
        st.markdown("""
        <style>
        .stExpander {border: 1px solid #e0e0e0; border-radius: 8px; background-color: #f9f9f9;}
        </style>
        """, unsafe_allow_html=True)
        
        with st.expander("📐 FitNexus Intelligence (Check My Fit)"):
            # Dynamic display of current user context
            if sim_challenges:
                st.write(f"Analyzing for: **{sim_height}** with **{', '.join(sim_challenges)}**")
            else:
                st.write(f"Analyzing for: **{sim_height}** (Standard Fit)")
                
            q = st.text_input("Ask a question:", value="Will this fit my body type?")
            
            if st.button("Run Analysis"):
                with st.spinner("Processing biometrics..."):
                    res = st.session_state.engine.analyze_fit(q, user_data)
                    st.success(f"**Recommendation:**\n\n{res['analysis']}")

# --- MODE 2: API VIEW ---
else:
    st.title("⚡ FitNexus API Console")
    st.markdown("### Developer Documentation")
    st.markdown("Send us user biometrics + product SKUs, we return fit risk analysis.")
    
    if st.button("Send Mock Request"):
        # The JSON updates dynamically based on multi-select
        st.code(json.dumps({
            "endpoint": "POST /v1/analyze_fit",
            "header": {"Authorization": "Bearer sk_live_..."},
            "payload": {"user_profile": user_data, "product_sku": "SCUBA-HZ-001"}
        }, indent=2), language="json")
        
        with st.spinner("Computing..."):
            res = st.session_state.engine.analyze_fit("fit check", user_data)
            
        st.code(json.dumps({
            "status": "success",
            "fit_score": "High Risk" if "avoid" in res['analysis'].lower() else "Good Match",
            "message": res['analysis']
        }, indent=2), language="json")