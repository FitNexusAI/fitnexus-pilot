import streamlit as st
import os
from fit_engine import FitNexusAgent

st.set_page_config(page_title="FitNexus Pilot", page_icon="🛍️", layout="wide")

# --- SIDEBAR PROFILE INPUTS ---
with st.sidebar:
    # 1. Logo
    st.image("https://placehold.co/200x100/png?text=YOUR+LOGO", width=150)
    st.title("My Fit Profile")
    st.markdown("Customize your AI recommendations:")
    
    # 2. Height
    user_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"])
    
    # 3. Usual Size
    user_size = st.selectbox("Usual Size", ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL"])
    
    # 4. Fit Challenges (Includes Bust Options)
    user_challenges = st.multiselect(
        "Fit Challenges", 
        [
            "None", 
            "Large Bust", "Small Bust",
            "Broad Shoulders", "Narrow Shoulders", 
            "Long Torso", "Short Torso", 
            "Wide Hips", "Narrow Hips", 
            "Long Arms", "Thick Thighs", 
            "Sensitive Skin"
        ]
    )
    
    # 5. Fit Preference
    user_pref = st.radio("I prefer clothes to fit:", ["Tight / Compression", "Standard / Regular", "Loose / Oversized"])
    
    # Store all this in the profile dictionary
    user_profile = {
        "height": user_height,
        "size": user_size,
        "challenges": user_challenges,
        "preference": user_pref
    }
    
    st.markdown("---")
    st.caption("© 2026 FitNexus Thesis Project")
    
    # --- ADMIN SECTION (With Refresh Fix) ---
    st.markdown("### 📊 Admin Tools")
    
    # Force Refresh Button (Updates the download data)
    if st.button("🔄 Refresh Logs"):
        st.rerun()

    log_file_path = "fitnexus_usage_log.csv"
    
    # Only show download if file exists
    if os.path.exists(log_file_path):
        with open(log_file_path, "rb") as file:
            file_data = file.read()
        
        # Show count of interactions
        num_lines = len(file_data.decode('utf-8').split('\n')) - 2 
        st.caption(f"Logged Interactions: {max(0, num_lines)}")
        
        st.download_button(
            label="Download Usage Data (CSV)",
            data=file_data,
            file_name="fitnexus_pilot_data.csv",
            mime="text/csv"
        )
    else:
        st.info("No logs yet. Ask a question to start logging.")

# --- MAIN CHAT INTERFACE ---
st.title("🛍️ Personal Fit Consultant")

# Dynamic Welcome Message
challenges_text = f" and have **{', '.join(user_challenges)}**" if user_challenges and "None" not in user_challenges else ""
st.markdown(f"##### Hello! I see you usually wear a **{user_size}**{challenges_text}.")
st.markdown("Ask me about any item, and I'll tell you how it fits *you*.")

if "agent" not in st.session_state:
    st.session_state.agent = FitNexusAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: 'Will the hoodie fit me?'"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your profile & logging request..."):
            result = st.session_state.agent.think(prompt, user_profile)
            
            if result["image"]:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(result["text"])
                with col2:
                    st.image(result["image"], caption=result["product_name"], width="stretch")
            else:
                st.markdown(result["text"])
            
    st.session_state.messages.append({"role": "assistant", "content": result["text"]})