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

    def analyze_fit(self, query, user_profile, forced_product_context=None):
        if self.catalog.empty: return {"error": "Catalog disconnected"}
        
        # 1. SEARCH LOGIC
        search_query = query
        if forced_product_context:
            search_query += f" {forced_product_context}"
            
        clean_query = search_query.lower().translate(str.maketrans('', '', string.punctuation))
        scored = []
        
        for _, row in self.catalog.iterrows():
            text = f"{row.get('name','')} {row.get('description','')} {row.get('fit_type','')}".lower()
            score = sum(1 for w in clean_query.split() if w in text)
            if score > 0: scored.append((score, row))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        if scored:
            target_product = scored[0][1]
            alternatives = [item[1] for item in scored[1:4]]
            if not alternatives: 
                alternatives = [r for _, r in self.catalog.iterrows() if r['name'] != target_product['name']][:3]
        else:
            target_product = self.catalog.iloc[0]
            alternatives = [self.catalog.iloc[i] for i in range(1, 4)]

        # 2. CONSTRUCT CONTEXT
        alt_text = "\n".join([f"- {p['name']}: {p['fit_type']} fit." for p in alternatives])
        
        context_block = (
            f"TARGET PRODUCT (User is looking at this):\n"
            f"Name: {target_product['name']}\n"
            f"Fit Type: {target_product['fit_type']}\n"
            f"Tech Specs: {target_product.get('fit_advice', '')}\n\n"
            f"AVAILABLE ALTERNATIVES (Recommend ONE of these ONLY if Target is bad):\n"
            f"{alt_text}"
        )
        
        # 3. AI PROMPT
        system_prompt = (
            "You are the FitNexus API. Your goal is to Save the Sale. "
            "1. Analyze the 'TARGET PRODUCT' against the User Profile. "
            "2. If the Target Product is a POOR fit (e.g., cropped item for long torso), "
            "you MUST recommend a specific item from the 'AVAILABLE ALTERNATIVES' list that solves the problem. "
            "3. If the Target Product is a GOOD fit, confirm it enthusiastically. "
            "Keep the output decisive."
        )
        
        user_msg = f"User Profile: {user_profile}\nQuery: {query}\n\n{context_block}"
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}]
        )
        
        return {
            "status": 200,
            "analysis": response.choices[0].message.content,
            "product": target_product.get('name')
        }

if "engine" not in st.session_state:
    st.session_state.engine = FitNexusEngine()

# --- 3. THE DEMO UI ---
with st.sidebar:
    st.header("FitNexus Engine")
    mode = st.radio("Select Demo Mode:", ["🛍️ Retail Storefront (Demo)", "👨‍💻 API Developer View"])
    st.divider()
    
    st.subheader("Simulated Shopper Context")
    sim_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"], index=2)
    sim_challenges = st.multiselect(
        "Fit Challenges (Select multiple)", 
        ["Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders", "Large Bust", "Small Bust", "Wide Hips", "Narrow Hips", "Thick Thighs", "Sensitive Skin"],
        default=[]
    )
    
    user_data = {
        "height": sim_height, 
        "challenges": sim_challenges if sim_challenges else ["None"]
    }
    st.info(f"**Active Biometrics:**\nHeight: {sim_height}\nIssues: {', '.join(sim_challenges) if sim_challenges else 'None'}")

# --- MODE 1: WHITE LABEL STOREFRONT ---
if mode == "🛍️ Retail Storefront (Demo)":
    st.markdown("### 🛒 Premium Activewear Co. (Integration Demo)")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    DISPLAYED_PRODUCT_NAME = "Oversized Fleece Half-Zip"
    
    with col1:
        st.image("https://images.lululemon.com/is/image/lululemon/LW3DM4S_032489_1?wid=750&op_usm=0.8,1,10,0&fmt=webp&qlt=80,1&fit=constrain,0&op_sharpen=0&resMode=sharp2&iccEmbed=0&printRes=72", caption="Product ID: SCUBA-HZ-001")
    
    with col2:
        st.subheader(DISPLAYED_PRODUCT_NAME)
        st.write("⭐⭐⭐⭐⭐ (4.8) | **$118.00**")
        st.write("The ultimate post-workout layer. Cotton-blend fleece fabric is naturally breathable.")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], horizontal=True, label_visibility="collapsed")
        st.button("Add to Bag", type="primary")
        
        st.markdown("---")
        st.markdown("""<style>.stExpander {border: 1px solid #e0e0e0; border-radius: 8px; background-color: #f9f9f9;}</style>""", unsafe_allow_html=True)
        
        with st.expander("📐 FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: **{sim_height}** | **{', '.join(sim_challenges)}**")
            q = st.text_input("Ask a question:", value="Will this fit my body type?")
            
            # --- FIXED LOGIC: SAVE TO SESSION STATE ---
            if st.button("Run Analysis"):
                with st.spinner("Processing technical specs..."):
                    st.session_state.last_result = st.session_state.engine.analyze_fit(q, user_data, forced_product_context=DISPLAYED_PRODUCT_NAME)
            
            # Display Result if it exists in memory
            if "last_result" in st.session_state:
                res = st.session_state.last_result
                
                # Check for Pivot
                is_pivot = "recommend" in res['analysis'].lower() and "instead" in res['analysis'].lower()
                
                if is_pivot:
                    st.warning(f"**Fit Alert:**\n\n{res['analysis']}")
                    # THE NEW LINK FEATURE
                    st.button("👉 Shop Recommended Alternative", type="primary", use_container_width=True)
                else:
                    st.success(f"**Fit Confirmation:**\n\n{res['analysis']}")

# --- MODE 2: API VIEW ---
else:
    st.title("⚡ FitNexus API Console")
    st.markdown("### Developer Documentation")
    
    if st.button("Send Mock Request"):
        st.code(json.dumps({
            "endpoint": "POST /v1/analyze_fit",
            "payload": {"user_profile": user_data, "product_sku": "SCUBA-HZ-001"}
        }, indent=2), language="json")
        
        with st.spinner("Computing..."):
            res = st.session_state.engine.analyze_fit("fit check", user_data, forced_product_context="Oversized Fleece Half-Zip")
            
        st.code(json.dumps({
            "status": "success",
            "cross_sell": True if "instead" in res['analysis'] else False,
            "message": res['analysis']
        }, indent=2), language="json")