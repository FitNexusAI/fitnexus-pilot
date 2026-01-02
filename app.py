import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="FitNexus Enterprise Demo")

st.markdown(
    """
    <style>
    /* 1. Make the Multiselect Chips Red */
    span[data-baseweb="tag"] {
        background-color: #F74845 !important;
        color: white !important;
    }
    
    /* 2. Style the "Shop Recommended Alternative" / Primary Buttons Red */
    div.stButton > button:first-child {
        background-color: #F74845;
        color: white;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #D3322F;
        color: white;
    }

    /* 3. Custom font tweaks for headers */
    h1, h2, h3 {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    
    /* 4. Hide the "Deploy" button and main menu for a cleaner demo look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. FIT LOGIC HANDLER
# ---------------------------------------------------------
FIT_CHALLENGES = [
    "None",
    "Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders",
    "Long Arms", "Short Arms", "Full Bust", "Small Bust",
    "Round Stomach", "Soft Midsection", "Curvy Hips", "Wide Hips", 
    "Narrow Hips", "High Hip Shelf", "Athletic Thighs", "Long Legs", 
    "Short Legs", "Muscular Calves"
]

def handle_fit_challenge_change():
    current = st.session_state.fit_challenges_selector
    previous = st.session_state.get('previous_selection', ['None'])

    if not current:
        st.session_state.fit_challenges_selector = ["None"]
    elif "None" in current and "None" not in previous:
        st.session_state.fit_challenges_selector = ["None"]
    elif "None" in current and len(current) > 1:
        st.session_state.fit_challenges_selector = [x for x in current if x != "None"]

    st.session_state.previous_selection = st.session_state.fit_challenges_selector

if 'previous_selection' not in st.session_state:
    st.session_state.previous_selection = ['None']

# ---------------------------------------------------------
# 3. SIDEBAR (The Left Panel)
# ---------------------------------------------------------
with st.sidebar:
    st.header("FitNexus Engine")
    st.caption("v2.1.0 | Enterprise Retail Build")
    
    st.divider()
    
    st.subheader("Simulated Shopper Context")
    
    # --- Height ---
    height = st.selectbox("Height", ["Under 5'0", "5'0 - 5'2", "5'3 - 5'7", "5'8 - 5'11", "Over 6'0"], index=2)

    # --- Simplified Body Types ---
    body_type = st.selectbox(
        "Body Type", 
        ["Curvy", "Athletic / Muscular", "Straight / Slender", "Full Figured", "Petite Frame"],
        index=2
    )
    
    # --- Fit Challenge Selector ---
    st.write("Fit Challenges (Select multiple)")
    selected_challenges = st.multiselect(
        label="Fit Challenges",
        options=FIT_CHALLENGES,
        default=["Long Torso", "Broad Shoulders"], 
        key="fit_challenges_selector",
        on_change=handle_fit_challenge_change,
        label_visibility="collapsed"
    )
    
    # --- Blue Info Box (Dynamic) ---
    st.info(
        f"""
        **Active Biometrics:**
        Height: {height}
        Body Type: {body_type}
        
        **Issues:** {", ".join(selected_challenges)}
        """
    )

# ---------------------------------------------------------
# 4. MAIN CONTENT AREA (RETAIL STOREFRONT)
# ---------------------------------------------------------

st.subheader("🛒 Premium Activewear Co. (Integration Demo)")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    # --- UPDATED IMAGE: Woman in Grey Hoodie ---
    st.image(
        "https://images.unsplash.com/photo-1579913750778-60eb933f7460?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
        caption="Product ID: SCUBA-HZ-001 | Woman shown in oversized fit",
        use_container_width=True
    )

with col2:
    st.title("Oversized Fleece Half-Zip")
    st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$118.00**")
    
    st.write("The ultimate post-workout layer. Cotton-blend fleece fabric is naturally breathable and soft against your skin. Designed with a roomy fit that falls below the hip.")
    
    st.write("**Size**")
    size = st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True)
    
    st.button("Add to Bag")

    st.write("") 
    st.write("") 

    # --- INTELLIGENCE SECTION ---
    with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
        st.caption(f"Analyzing for: {height} | {body_type} | {', '.join(selected_challenges)}")
        
        question = st.text_input("Ask a question:", "Will this fit my body type?")
        
        if st.button("Run Analysis"):
            st.warning(
                f"""
                **Fit Alert:**
                
                Based on the user profile provided ({body_type}, {', '.join(selected_challenges)}), this specific product - Scuba Oversized Half-Zip Hoodie - 
                may not be an ideal fit for your preferences.
                
                **Analysis:**
                While the model image shows a longer fit, our returns data indicates this item sits at the high hip. For a user with a **Long Torso**, this often results in the item feeling like a "cropped" fit rather than the intended oversized look.
                
                **Recommendation:**
                As an alternative, I recommend the **Swiftly Tech Long Sleeve Shirt 2.0** for reliable extra length.
                """
            )
            
            st.button("👉 Shop Recommended Alternative")