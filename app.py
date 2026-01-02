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

# --- 2. SESSION STATE SETUP (The "Router") ---
# This tracks which product is currently on screen
if "current_product_key" not in st.session_state:
    st.session_state.current_product_key = "scuba_hoodie"

# Define the "Database" of products we can show
PRODUCT_DB = {
    "scuba_hoodie": {
        "name": "Oversized Fleece Half-Zip",
        "price": "$118.00",
        "desc": "The ultimate post-workout layer. Cotton-blend fleece fabric is naturally breathable.",
        "image": "https://images.lululemon.com/is/image/lululemon/LW3DM4S_032489_1?wid=750&op_usm=0.8,1,10,0&fmt=webp&qlt=80,1&fit=constrain,0&op_sharpen=0&resMode=sharp2&iccEmbed=0&printRes=72",
        "id": "SCUBA-HZ-001"
    },
    "define_jacket": {
        "name": "Define Jacket Luon",
        "price": "$118.00",
        "desc": "Cottony-soft Luon™ fabric is sweat-wicking and four-way stretch. Added Lycra™ fibre for shape retention.",
        "image": "https://images.lululemon.com/is/image/lululemon/LW4AWLS_0001_1?wid=750&op_usm=0.8,1,10,0&fmt=webp&qlt=80,1&fit=constrain,0&op_sharpen=0&resMode=sharp2&iccEmbed=0&printRes=72",
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
with