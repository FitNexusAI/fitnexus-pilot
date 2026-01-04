import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import os

# 1. PAGE CONFIG
st.set_page_config(layout="wide", page_title="FitNexusAI | Retail Integration Demo")

# 2. THE LOGO FIX
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, 'logo.png')
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
except Exception as e:
    st.sidebar.title("FitNexus Ai")
    st.sidebar.error("Branding logo not found.")

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

# 4. CLEAN UI CSS
st.markdown("""
<style>
    .stAppDeployButton { display: none !important; visibility: hidden !important; }
    [data-testid="stStatusWidget"] { display: none !important; visibility: hidden !important; }
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
    # --- RESTORED PRODUCT DETAILS ---
    st.image("https://i.imgur.com/898989.jpg", caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up Jacket", use_container_width=True) 
    
    st.title("Textured Fleece Zip-Up Jacket")
    st.write("⭐⭐⭐⭐⭐ (4.8) | $128.00")
    st.write("A versatile layer with a smooth full-length zipper and soft fabric.")
    
    st.write("**Size**")
    st.radio("Size Selection", ["XS/S", "M/L", "XL/XXL"], horizontal=True, label_visibility="collapsed")
    
    st.button("Add to Bag", type="primary")
    
    st.write("---")
    st.subheader("FitNexus Intelligence (Check My Fit)")
    st.write("Analyzing for: || None")
    st.text_input("Ask a question:")

# 6. POWERED BY TAG
st.markdown('<div class="powered-by">Powered by FitNexus AI v2.1.0</div>', unsafe_allow_html=True)