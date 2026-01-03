import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import os

# 1. PAGE CONFIG (Must be the very first Streamlit command)
st.set_page_config(layout="wide", page_title="FitNexusAI | Retail Integration Demo")

 # 2. THE LOGO FIX
st.sidebar.image("logo.png", use_container_width=True)

# 3. THE STABLE SCROLL FIX
if st.session_state.get('view_mode') == 'alternative':
    components.html(
        """
        <script>
        window.parent.document.querySelector('section.main').scrollTo({ top: 0, behavior: 'instant' });
        </script>
        """,
        height=0,
    )

# 4. CLEAN UI CSS (Hides 'Manage app', Footer, and Menu)
st.markdown("""
    <style>
    /* Hides the 'Manage app' button */
    .stAppDeployButton {
        display: none !important;
        visibility: hidden !important;
    }
    /* Hides the status widget/arrow */
    [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }
    /* Hides the Streamlit menu and footer */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    .powered-by { text-align: center; color: #999; font-size: 12px; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# 5. PRODUCT AND SHOPPER LOGIC
st.title("Shopper Profile")

col1, col2 = st.columns([1, 2])

with col1:
    st.selectbox("Height", ["5'4\"", "5'5\"", "5'6\"", "5'7\"", "5'8\""])
    st.selectbox("Body Type", ["Athletic", "Slim", "Average", "Curvy"])
    st.multiselect("Fit Challenges", ["None", "Long Arms", "Broad Shoulders", "Short Torso"], default="None")

    st.info("**Biometrics:** Not Set, Not Set  \n**Issues:** None Selected")
    
    if st.button("Reset Demo", type="primary"):
        st.session_state.clear()
        st.rerun()

with col2:
    # Placeholder for Product Analysis
    st.write("---")
    st.subheader("FitNexus Intelligence (Check My Fit)")
    st.write("Analyzing for: || None")
    st.text_input("Ask a question:")

# 6. POWERED BY TAG
st.markdown('<div class="powered-by">Powered by FitNexusAI v2.1.0</div>', unsafe_allow_html=True)
