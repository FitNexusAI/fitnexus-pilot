import streamlit as st

# 1. PAGE CONFIG & CUSTOM CSS
st.set_page_config(layout="wide", page_title="FitNexus | Retail Integration Demo")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    span[data-baseweb="tag"] { background-color: #F74845 !important; color: white !important; }
    div.stButton > button:first-child { background-color: #F74845; color: white; border: none; width: 100%; }
    div.stButton > button:hover { background-color: #D3322F; color: white; }
    h1, h2, h3 { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .logo-text { font-weight: bold; font-size: 24px; color: #333; margin-bottom: 0px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. STATE MANAGEMENT & EXCLUSIVE LOGIC
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'

if 'challenges_selection' not in st.session_state:
    st.session_state.challenges_selection = ["None"]

FIT_OPTIONS = [
    "None", "Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders",
    "Long Arms", "Short Arms", "Full Bust", "Small Bust", "Round Stomach", 
    "Soft Midsection", "Curvy Hips", "Wide Hips", "Narrow Hips", "High Hip Shelf", 
    "Athletic Thighs", "Long Legs", "Short Legs", "Muscular Calves"
]

def sync_logic():
    """STRICT MUTUAL EXCLUSION: If 'None' is chosen, remove others. If challenges added, remove 'None'."""
    current = st.session_state.challenge_widget
    previous = st.session_state.challenges_selection
    if not current:
        st.session_state.challenges_selection = ["None"]
    elif "None" in current and len(current) > 1:
        if "None" not in previous:
            st.session_state.challenges_selection = ["None"]
        else:
            st.session_state.challenges_selection = [x for x in current if x != "None"]
    else:
        st.session_state.challenges_selection = current

def reset_demo_state():
    """FACTORY RESET: Returns everything to a blank, original state."""
    st.session_state.view_mode = 'original'
    st.session_state.challenges_selection = ["None"]
    st.session_state.h_key = ""
    st.session_state.b_key = ""
    if 'challenge_widget' in st.session_state:
        st.session_state.challenge_widget = ["None"]

# 3. SIDEBAR (FitNexus Branded)
with st.sidebar:
    # Matches the 'logo.png' in your local directory and GitHub root
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown('<p class="logo-text">⚡ FitNexusAI</p>', unsafe_allow_html=True)
    
    st.caption("AI-Powered Fit Intelligence | v2.1.0")
    st.divider()
    
    st.subheader("Shopper Profile")
    h_val = st.selectbox("Height", ["", "Under 5'0", "5'0-5'2", "5'3-5'7", "5'8-5'11", "Over 6'0"], index=0, key="h_key")
    b_val = st.selectbox("Body Type", ["", "Curvy", "Athletic", "Slender", "Full Figured", "Petite"], index=0, key="b_key")
    
    st.multiselect("Fit Challenges", options=FIT_OPTIONS, key="challenge_widget", 
                   default=st.session_state.challenges_selection, on_change=sync_logic)
    
    active = st.session_state.challenges_selection
    real_issues = [c for c in active if c != "None"]
    
    # Unified Shopper Context Summary
    st.info(f"**Biometrics:** {h_val if h_val else 'Not Set'}, {b_val if b_val else 'Not Set'}\n\n"
            f"**Issues:** {', '.join(real_issues) if real_issues else 'None Selected'}")
    
    st.divider()
    st.button("🔄 Reset Demo", on_click=reset_demo_state)

# 4. MAIN CONTENT (Retailer Branded)
st.subheader("🛒 Premium Activewear Co.")
st.caption("Official Retail Partner Integration")
st.divider()

col1, col2 = st.columns([1, 1])

if st.session_state.view_mode == 'original':
    with col1:
        # Original Product Image
        st.image("https://images.pexels.com/photos/7242947/pexels-photo-7242947.jpeg?auto=compress&cs=tinysrgb&w=800",
                 caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up Jacket", use_container_width=True)
    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00