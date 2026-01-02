import streamlit as st
import os
import csv
from datetime import datetime
from fit_engine import FitNexusAgent

st.set_page_config(page_title="FitNexus Pilot", page_icon="🛍️", layout="wide")

# --- 1. SETUP LOGGING (Runs silently in background) ---
log_file_path = "fitnexus_usage_log.csv"

# Ensure file exists with headers
if not os.path.exists(log_file_path):
    with open(log_file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Height", "Size", "Preference", "Challenges", "User_Query", "Product_Recommended", "AI_Advice"])

# --- 2. INITIALIZE BRAIN ---
if "agent_v4" not in st.session_state:
    st.session_state.agent_v4 = FitNexusAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://placehold.co/200x100/png?text=YOUR+LOGO", width=150)
    st.title("My Fit Profile")
    
    # Inputs
    user_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"])
    user_size = st.selectbox("Usual Size", ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL"])
    user_challenges = st.multiselect("Fit Challenges", ["None", "Large Bust", "Small Bust", "Broad Shoulders", "Narrow Shoulders", "Long Torso", "Short Torso", "Wide Hips", "Narrow Hips", "Long Arms", "Thick Thighs", "Sensitive Skin"])
    user_pref = st.radio("I prefer clothes to fit:", ["Tight / Compression", "Standard / Regular", "Loose / Oversized"])
    
    user_profile = {"height": user_height, "size": user_size, "challenges": user_challenges, "preference": user_pref}
    
    st.markdown("---")
    
    # Admin Tools (Only you need to click this)
    st.markdown("### 📊 Admin Tools")
    if st.button("🔄 Refresh Logs"):
        st.rerun()

    if os.path.exists(log_file_path):
        with open(log_file_path, "rb") as file:
            file_data = file.read()
        st.download_button(label="Download CSV", data=file_data, file_name="fitnexus_data.csv", mime="text/csv")

# --- 4. MAIN CHAT ---
st.title("🛍️ Personal Fit Consultant")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: 'Will the hoodie fit me?'"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            result = st.session_state.agent_v4.think(prompt, user_profile)
            
            if result["image"]:
                col1, col2 = st.columns([2, 1])
                with col1: st.markdown(result["text"])
                with col2: st.image(result["image"], caption=result["product_name"], width="stretch")
            else:
                st.markdown(result["text"])
            
            # --- SILENT LOGGING ---
            try:
                with open(log_file_path, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        user_height, user_size, user_pref, 
                        ", ".join(user_challenges), 
                        prompt, 
                        result.get("product_name", "None"), 
                        result["text"]
                    ])
                # Removed the "Success!" popup so it feels seamless to the user
            except Exception as e:
                # We still print errors to the console just in case
                print(f"Log Error: {e}")

    st.session_state.messages.append({"role": "assistant", "content": result["text"]})