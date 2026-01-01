import streamlit as st
from fit_engine import FitNexusAgent

# 1. Page Configuration
st.set_page_config(page_title="FitNexus Pilot", page_icon="🛍️", layout="wide")

# 2. Sidebar Branding
with st.sidebar:
    # Using a generic placeholder logo URL
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/ab/Android_O_Preview_Logo.png", width=50) 
    st.title("FitNexus")
    st.markdown("**Pilot Environment**")
    st.info("This agent is connected to the live inventory pilot database.")
    st.markdown("---")
    st.caption("© 2026 FitNexus Thesis Project")

# 3. Main Header
st.title("🛍️ Personal Fit Assistant")
st.markdown("##### Ask me about sizing, materials, or specific products.")

# 4. Initialize Agent & History
if "agent" not in st.session_state:
    st.session_state.agent = FitNexusAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input & Processing
if prompt := st.chat_input("Ex: 'How do the leggings fit?'"):
    
    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get Response
    with st.chat_message("assistant"):
        with st.spinner("Checking inventory & fit specs..."):
            result = st.session_state.agent.think(prompt)
            
            # Layout: Text on Left, Image on Right (if image exists)
            if result["image"]:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(result["text"])
                with col2:
                    # FIX: Updated for 2026 Streamlit compliance
                    st.image(result["image"], caption=result["product_name"], width="stretch")
            else:
                st.markdown(result["text"])
            
    # Save text response to history
    st.session_state.messages.append({"role": "assistant", "content": result["text"]})