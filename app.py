import streamlit as st
from fit_engine import FitNexusAgent

st.set_page_config(page_title="FitNexus Pilot", page_icon="🛍️", layout="wide")

# --- NEW: SIDEBAR PROFILE INPUTS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/ab/Android_O_Preview_Logo.png", width=50)
    st.title("My Fit Profile")
    st.markdown("Customize your AI recommendations:")
    
    # Collect User Stats
    user_height = st.selectbox("Height", ["< 5'3", "5'3 - 5'7", "5'8 - 6'0", "> 6'0"])
    user_size = st.selectbox("Usual Size", ["XS", "S", "M", "L", "XL"])
    user_pref = st.radio("I prefer clothes to fit:", ["Tight / Compression", "Standard / Regular", "Loose / Oversized"])
    
    # Store this in a dictionary
    user_profile = {
        "height": user_height,
        "size": user_size,
        "preference": user_pref
    }
    
    st.markdown("---")
    st.info("FitNexus uses these stats to compare against garment technical data.")
    st.caption("© 2026 FitNexus Thesis Project")

# --- MAIN CHAT INTERFACE ---
st.title("🛍️ Personal Fit Consultant")
st.markdown(f"##### Hello! I see you usually wear a **{user_size}** and like a **{user_pref.split('/')[0]}** fit.")
st.markdown("Ask me about any item, and I'll tell you how it fits *you*.")

if "agent" not in st.session_state:
    st.session_state.agent = FitNexusAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: 'Will the leggings fit me?'"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your profile against product specs..."):
            # PASS THE PROFILE TO THE BRAIN
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