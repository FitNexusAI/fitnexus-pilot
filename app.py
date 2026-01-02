import streamlit as st
import os
import csv
import string
import pandas as pd
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# --- CONFIG & SETUP ---
st.set_page_config(page_title="FitNexus Pilot", page_icon="🛍️", layout="wide")
load_dotenv()

# --- THE BRAIN (Now built directly into the app) ---
class FitNexusAgent:
    def __init__(self, data_file="fashion_products_mock.csv"):
        self.catalog = pd.DataFrame()
        try:
            # Try to load the data
            if os.path.exists(data_file):
                self.catalog = pd.read_csv(data_file)
                # Clean columns and data
                self.catalog.columns = self.catalog.columns.str.strip()
                self.catalog = self.catalog.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            else:
                st.error(f"⚠️ CRITICAL ERROR: Could not find '{data_file}'. Make sure it is uploaded to GitHub!")
        except Exception as e:
            st.error(f"⚠️ CRITICAL ERROR: CSV File is broken. {e}")

        # Initialize OpenAI
        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except:
            st.error("⚠️ API Key Error. Check your Secrets.")

    def retrieve_products(self, query):
        if self.catalog.empty: return []
        
        # 1. Clean Query
        clean_query = query.lower().translate(str.maketrans('', '', string.punctuation))
        
        # 2. Synonyms
        synonyms = {"sweatshirt": "hoodie", "pullover": "hoodie", "tshirt": "tee", "pants": "leggings", "tights": "leggings"}
        for word, target in synonyms.items():
            clean_query = clean_query.replace(word, target)

        query_words = clean_query.split()
        
        # 3. Score Products
        scored_results = []
        for index, row in self.catalog.iterrows():
            text = f"{row.get('name','')} {row.get('category','')} {row.get('description','')}".lower()
            score = sum(1 for word in query_words if word in text)
            if score > 0:
                scored_results.append((score, row))
        
        scored_results.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored_results]

        # 4. FAIL-SAFE: If no specific match, return Top 5 items for General Advice
        if not results:
            return [row for index, row in self.catalog.iterrows()][:5]

        return results

    def generate_response(self, user_input, product_data_list, user_profile):
        challenges = ", ".join(user_profile.get('challenges', ['None']))
        
        # Build Context
        products_context = ""
        for i, prod in enumerate(product_data_list[:5]):
            products_context += f"\nPRODUCT {i+1}: {prod.get('name')} | Fit: {prod.get('fit_type')} | Advice: {prod.get('fit_advice')}"

        system_prompt = (
            "You are FitNexus, an elite personal stylist. "
            "Use the PRODUCT DATA below to answer the User's Question. "
            "If they ask for a general recommendation (e.g. 'What do you suggest?'), "
            "look at their FIT CHALLENGES and pick the BEST item from the list. "
            "Explain WHY that item works for their body type."
        )
        
        user_message = (
            f"User Question: {user_input}\n\n"
            f"USER PROFILE: Height: {user_profile.get('height')}, Size: {user_profile.get('size')}, Challenges: {challenges}\n\n"
            f"AVAILABLE PRODUCTS:\n{products_context}"
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {e}"

    def think(self, user_input, user_profile):
        matches = self.retrieve_products(user_input)
        result = {"text": "", "image": None, "product_name": None}

        if not matches:
            result["text"] = "I can't access the product catalog right now. Is the CSV file empty?"
        else:
            result["text"] = self.generate_response(user_input, matches, user_profile)
            # Show image of the first product in the list
            best_match = matches[0]
            img_url = best_match.get("image_url", None)
            if pd.notna(img_url) and str(img_url).strip() != "":
                result["image"] = str(img_url).strip()
                result["product_name"] = best_match.get("name", "")
            
        return result

# --- INITIALIZE THE APP ---
# We force a fresh agent every time to avoid cache bugs
if "agent_final" not in st.session_state:
    st.session_state.agent_final = FitNexusAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("My Fit Profile")
    user_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"])
    user_size = st.selectbox("Usual Size", ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL"])
    user_challenges = st.multiselect("Fit Challenges", ["None", "Large Bust", "Small Bust", "Broad Shoulders", "Narrow Shoulders", "Long Torso", "Short Torso", "Wide Hips", "Narrow Hips", "Long Arms", "Thick Thighs", "Sensitive Skin"])
    user_pref = st.radio("Fit Preference:", ["Tight", "Standard", "Loose"])
    user_profile = {"height": user_height, "size": user_size, "challenges": user_challenges, "preference": user_pref}
    
    st.markdown("---")
    st.markdown("### 📊 Admin Tools")
    if st.button("🔄 Refresh Logs"): st.rerun()
    
    log_file = "fitnexus_usage_log.csv"
    if os.path.exists(log_file):
        with open(log_file, "rb") as f:
            st.download_button("Download Data (CSV)", f, "fitnexus_data.csv", "text/csv")

# --- MAIN CHAT ---
st.title("🛍️ Personal Fit Consultant")

# Debug Message: Check if catalog loaded
catalog_size = len(st.session_state.agent_final.catalog)
if catalog_size == 0:
    st.error("⚠️ ERROR: Product Catalog is Empty! Check 'fashion_products_mock.csv' on GitHub.")
