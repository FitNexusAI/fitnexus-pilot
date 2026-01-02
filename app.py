import streamlit as st
import os
import csv
from fit_engine import FitNexusAgent

st.set_page_config(page_title="FitNexus Pilot", page_icon="🛍️", layout="wide")

# --- STEP 1: FORCE LOG FILE CREATION ---
log_file_path = "fitnexus_usage_log.csv"
if not os.path.exists(log_file_path):
    with open(log_file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Height", "Size", "Preference", "Challenges", "User_Query", "Product_Recommended", "AI_Advice"])

# --- STEP 2: INITIALIZE AGENT (FORCE NEW VERSION) ---
# Renaming to 'agent_v2' forces the app to load the new code with logging!
if "agent_v2" not in st.session_state:
    st.session_state.agent_v2 = FitNexusAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STEP 3: SIDEBAR ---
with st.sidebar:
    st.image("https://placehold.co/200x100/png?text=YOUR+LOGO", width=150)
    st.title("My Fit Profile")
    st.markdown("Customize your AI recommendations:")
    
    # Inputs
    user_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"])
    user_size = st.selectbox("Usual Size", ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL"])
    user_challenges = st.multiselect("Fit Challenges", ["None", "Large Bust", "Small Bust", "Broad Shoulders", "Narrow Shoulders", "Long Torso", "Short Torso", "Wide Hips", "Narrow Hips", "Long Arms", "Thick Thighs", "Sensitive Skin"])
    user_pref = st.radio("I prefer clothes to fit:", ["Tight / Compression", "Standard / Regular", "Loose / Oversized"])
    
    user_profile = {"height": user_height, "size": user_size, "challenges": user_challenges, "preference": user_pref}
    
    st.markdown("---")
    
    # --- ADMIN SECTION ---
    st.markdown("### 📊 Admin Tools")
    
    if st.button("🔄 Refresh Logs"):
        st.rerun()

    if os.path.exists(log_file_path):
        with open(log_file_path, "rb") as file:
            file_data = file.read()
        
        line_count = len(file_data.decode('utf-8').split('\n'))
        interaction_count = max(0, line_count - 2)
        
        st.caption(f"Logged Interactions: {interaction_count}")
        st.download_button(label="Download Usage Data (CSV)", data=file_data, file_name="fitnexus_pilot_data.csv", mime="text/csv")

# --- STEP 4: CHAT ---
st.title("🛍️ Personal Fit Consultant")
challenges_text = f" and have **{', '.join(user_challenges)}**" if user_challenges and "None" not in user_challenges else ""
st.markdown(f"##### Hello! I see you usually wear a **{user_size}**{challenges_text}.")
st.markdown("Ask me about any item, and I'll tell you how it fits *you*.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: 'Will the hoodie fit me?'"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # Using the NEW agent_v2
            result = st.session_state.agent_v2.think(prompt, user_profile)
            
            if result["image"]:
                col1, col2 = st.columns([2, 1])
                with col1: st.markdown(result["text"])
                with col2: st.image(result["image"], caption=result["product_name"], width="stretch")
            else:
                st.markdown(result["text"])
            
    st.session_state.messages.append({"role": "assistant", "content": result["text"]})