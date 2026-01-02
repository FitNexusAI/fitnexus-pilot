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

# --- 2. SESSION STATE SETUP ---
if "current_product_key" not in st.session_state:
    st.session_state.current_product_key = "scuba_hoodie"

# --- UPDATED DATABASE (Manually Verified Images) ---
PRODUCT_DB = {
    "scuba_hoodie": {
        "name": "Oversized Cotton Hoodie",
        "price": "$118.00",
        "desc": "The ultimate post-workout layer. Naturally breathable soft cotton fabric with a cozy hood and kangaroo pocket.",
        # VERIFIED IMAGE: Black woman in beige oversized hoodie/sweatsuit
        "image": "https://images.pexels.com/photos/6311237/pexels-photo-6311237.jpeg?auto=compress&cs=tinysrgb&w=800",
        "id": "SCUBA-CT-001"
    },
    "define_jacket": {
        "name": "Define Jacket Luon",
        "price": "$118.00",
        "desc": "Cottony-soft Luon™ fabric is sweat-wicking and four-way stretch. Added Lycra™ fibre for shape retention.",
        # VERIFIED IMAGE: Woman in Black Athletic Jacket
        "image": "https://images.pexels.com/photos/4132651/pexels-photo-4132651.jpeg?auto=compress&cs=tinysrgb&w=800",
        "id": "DEFINE-JKT-009"
    }
}

# --- 3. THE ENGINE ---
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
        
        # SEARCH LOGIC
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
        
        # SMART ALTERNATIVES LOGIC
        if scored:
            target_product = scored[0][1]
        else:
            target_product = self.catalog.iloc[0]

        target_name = target_product['name'].lower()
        target_desc = str(target_product.get('description', '')).lower()
        layer_keywords = ["hoodie", "jacket", "pullover", "sweatshirt", "fleece", "coat", "zip"]
        is_layer = any(k in target_name or k in target_desc for k in layer_keywords)
        
        alternatives = []
        for _, row in self.catalog.iterrows():
            if row['name'] == target_product['name']: continue
            item_name = row['name'].lower()
            item_desc = str(row.get('description', '')).lower()
            
            if is_layer:
                if any(k in item_name or k in item_desc for k in layer_keywords):
                    alternatives.append(row)
            else:
                alternatives.append(row)
        
        if not alternatives:
             alternatives = [item[1] for item in scored[1:4]] if len(scored) > 1 else []
        alternatives = alternatives[:3]

        # CONSTRUCT CONTEXT
        alt_text = "\n".join([f"- {p['name']}: {p['fit_type']} fit." for p in alternatives])
        context_block = (
            f"TARGET PRODUCT (User is looking at this):\n"
            f"Name: {target_product['name']}\n"
            f"Fit Type: {target_product['fit_type']}\n"
            f"Tech Specs: {target_product.get('fit_advice', '')}\n\n"
            f"AVAILABLE ALTERNATIVES:\n{alt_text}"
        )
        
        # AI PROMPT
        system_prompt = (
            "You are the FitNexus API. Goal: Save the Sale.\n"
            "1. Analyze Target Product vs User Profile.\n"
            "2. If Target is POOR fit, recommend a specific alternative using 'As an alternative' or 'recommend instead'.\n"
            "3. Explain WHY the alternative is better (e.g. 'This jacket is longer...').\n"
            "4. If Target is GOOD fit, confirm enthusiastically."
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

# --- 4. THE DEMO UI ---
with st.sidebar:
    st.header("FitNexus Engine")
    mode = st.radio("Select Demo Mode:", ["🛍️ Retail Storefront (Demo)", "👨‍💻 API Developer View"])
    st.divider()
    
    st.subheader("Simulated Shopper Context")
    sim_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"], index=2)
    sim_challenges = st.multiselect(
        "Fit Challenges", 
        ["Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders", "Large Bust", "Small Bust", "Wide Hips"],
        default=[]
    )
    user_data = {"height": sim_height, "challenges": sim_challenges if sim_challenges else ["None"]}
    st.info(f"**Active Biometrics:**\nHeight: {sim_height}\nIssues: {', '.join(sim_challenges) if sim_challenges else 'None'}")
    
    # RESET BUTTON
    if st.button("Reset Demo"):
        st.session_state.current_product_key = "scuba_hoodie"
        if "last_result" in st.session_state: del st.session_state.last_result
        st.rerun()

# --- MODE 1: WHITE LABEL STOREFRONT ---
if mode == "🛍️ Retail Storefront (Demo)":
    st.markdown("### 🛒 Premium Activewear Co. (Integration Demo)")
    st.markdown("---")
    
    # LOAD CURRENT PRODUCT FROM "DB"
    current_item = PRODUCT_DB[st.session_state.current_product_key]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(current_item["image"], caption=f"Product ID: {current_item['id']}")
    
    with col2:
        st.subheader(current_item["name"])
        st.write(f"⭐⭐⭐⭐⭐ (4.8) | **{current_item['price']}**")
        st.write(current_item["desc"])
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], horizontal=True, label_visibility="collapsed")
        st.button("Add to Bag", type="primary")
        
        st.markdown("---")
        
        # THE WIDGET
        with st.expander("📐 FitNexus Intelligence (Check My Fit)", expanded=True):
            challenges_text = ", ".join(sim_challenges) if sim_challenges else "None"
            st.caption(f"Analyzing for: **{sim_height}** | **{challenges_text}**")
            
            q = st.text_input("Ask a question:", value="Will this fit my body type?")
            
            if st.button("Run Analysis"):
                with st.spinner("Processing technical specs..."):
                    st.session_state.last_result = st.session_state.engine.analyze_fit(q, user_data, forced_product_context=current_item["name"])
            
            if "last_result" in st.session_state:
                res = st.session_state.last_result
                text_lower = res['analysis'].lower()
                
                # Pivot Logic
                is_pivot = (
                    "alternative" in text_lower or 
                    "instead" in text_lower or 
                    ("not a good fit" in text_lower and "recommend" in text_lower)
                )
                
                if is_pivot:
                    st.warning(f"**Fit Alert:**\n\n{res['analysis']}")
                    
                    # --- THE MAGIC BUTTON ---
                    if st.session_state.current_product_key != "define_jacket":
                        if st.button("👉 Shop Recommended Alternative (Define Jacket)", type="primary", use_container_width=True):
                            st.session_state.current_product_key = "define_jacket"
                            del st.session_state.last_result 
                            st.rerun()
                else:
                    st.success(f"**Fit Confirmation:**\n\n{res['analysis']}")

# --- MODE 2: API VIEW ---
else:
    st.title("⚡ FitNexus API Console")
    st.markdown("### Developer Documentation")
    if st.button("Send Mock Request"):
        st.code(json.dumps({
            "endpoint": "POST /v1/analyze_fit",
            "payload": {"user_profile": user_data, "product_sku": "SCUBA-CT-001"}
        }, indent=2), language="json")
        st.code(json.dumps({"status": "success", "message": "High Risk: Torso Length Mismatch"}, indent=2), language="json")