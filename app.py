import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="FitNexus Enterprise Demo")

st.markdown(
    """
    <style>
    /* Change Sidebar Background Color */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }

    /* Make the Multiselect Chips Red */
    span[data-baseweb="tag"] {
        background-color: #F74845 !important;
        color: white !important;
    }
    
    /* Style Primary Buttons Red */
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

    h1, h2, h3 {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. STATE MANAGEMENT & EXCLUSIVE LOGIC
# ---------------------------------------------------------
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'

if 'fit_challenges' not in st.session_state:
    st.session_state.fit_challenges = ["None"]

# Full list of challenges restored
FIT_CHALLENGE_OPTIONS = [
    "None", "Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders",
    "Long Arms", "Short Arms", "Full Bust", "Small Bust", "Round Stomach", 
    "Soft Midsection", "Curvy Hips", "Wide Hips", "Narrow Hips", "High Hip Shelf", 
    "Athletic Thighs", "Long Legs", "Short Legs", "Muscular Calves"
]

def handle_challenge_logic():
    current = st.session_state.challenge_input
    
    # If "None" is selected along with others, prioritize the NEWEST selection
    if len(current) > 1:
        if current[-1] == "None":
            # User just clicked "None", clear everything else
            st.session_state.fit_challenges = ["None"]
        elif "None" in current:
            # User clicked a specific challenge, remove "None"
            st.session_state.fit_challenges = [x for x in current if x != "None"]
        else:
            st.session_state.fit_challenges = current
    elif not current:
        # Fallback to "None" if empty
        st.session_state.fit_challenges = ["None"]
    else:
        st.session_state.fit_challenges = current

def switch_to_alternative():
    st.session_state.view_mode = 'alternative'

def switch_to_original():
    st.session_state.view_mode = 'original'
    st.session_state.fit_challenges = ["None"]

# ---------------------------------------------------------
# 3. SIDEBAR (The Left Panel)
# ---------------------------------------------------------
with st.sidebar:
    st.header("FitNexus Engine")
    st.caption("v2.1.0 | Enterprise Retail Build")
    st.divider()
    
    st.subheader("Simulated Shopper Context")
    height = st.selectbox("Height", ["Under 5'0", "5'0 - 5'2", "5'3 - 5'7", "5'8 - 5'11", "Over 6'0"], index=2)
    body_type = st.selectbox("Body Type", ["Curvy", "Athletic", "Slender", "Full Figured", "Petite"], index=0)
    
    # Restored Multiselect with logic
    st.multiselect(
        "Fit Challenges",
        options=FIT_CHALLENGE_OPTIONS,
        key="challenge_input",
        default=st.session_state.fit_challenges,
        on_change=handle_challenge_logic
    )
    
    active_challenges = st.session_state.fit_challenges
    st.info(f"**Biometrics:** {height}, {body_type}\n\n**Issues:** {', '.join(active_challenges)}")
    
    st.divider()
    if st.button("🔄 Reset Demo"):
        switch_to_original()
        st.rerun()

# ---------------------------------------------------------
# 4. MAIN CONTENT AREA
# ---------------------------------------------------------
st.subheader("🛒 Premium Activewear Co. (Integration Demo)")
st.divider()

col1, col2 = st.columns([1, 1])

if st.session_state.view_mode == 'original':
    with col1:
        # Verified Hero Image
        st.image(
            "https://images.pexels.com/photos/7242947/pexels-photo-7242947.jpeg?auto=compress&cs=tinysrgb&w=800",
            caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up Jacket",
            use_container_width=True
        )

    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00**")
        
        if "None" in active_challenges:
            st.success("🎯 FitNexus: 92% Match (High Confidence)")
        
        st.write("A versatile layer for seasonal transitions. This textured fleece jacket features a smooth full-length zipper and a tailored, athletic fit.")
        
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_orig")
        st.button("Add to Bag")

        with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: {height} | {body_type} | {', '.join(active_challenges)}")
            st.text_input("Ask a question:", "Will this fit my body type?")
            
            if st.button("Run Analysis"):
                if "None" in active_challenges:
                    st.success("Analysis complete: High-confidence match for your standard profile.")
                else:
                    st.warning(f"**Fit Alert:** Based on your biometrics ({body_type}), the standard zipper track may pull. We recommend our Longline version.")
                    st.button("👉 Shop Recommended Alternative", on_click=switch_to_alternative)

else:
    with col1:
        # Verified Secondary Image: Zip-Up Fleece
        st.image(
            "https://images.pexels.com/photos/6311613/pexels-photo-6311613.jpeg?auto=compress&cs=tinysrgb&w=800",
            caption="Product ID: LNG-ZIP-009 | CloudSoft Longline Zip-Up",
            use_container_width=True
        )

    with col2:
        st.success(f"🏆 FitNexus: 98% Match for: {', '.join(active_challenges)}")
        st.title("CloudSoft Longline Zip-Up")
        st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$138.00**")
        st.write("Designed with an extended hemline and a full-length zipper specifically for profiles with " + ", ".join(active_challenges) + ".")
        
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_alt")
        if st.button("Add to Bag"):
            st.balloons()
        
        st.button("← Back to Original Item", on_click=switch_to_original)