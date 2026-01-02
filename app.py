import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="FitNexus Enterprise Demo")

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
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. STATE MANAGEMENT & EXCLUSIVE LOGIC
# ---------------------------------------------------------

# Initializing Session States
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'

# We track the 'selection' separately from the UI component to enforce logic
if 'challenges_selection' not in st.session_state:
    st.session_state.challenges_selection = ["None"]

# Full list of challenges
FIT_CHALLENGE_OPTIONS = [
    "None", "Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders",
    "Long Arms", "Short Arms", "Full Bust", "Small Bust", "Round Stomach", 
    "Soft Midsection", "Curvy Hips", "Wide Hips", "Narrow Hips", "High Hip Shelf", 
    "Athletic Thighs", "Long Legs", "Short Legs", "Muscular Calves"
]

def sync_challenges():
    """ 
    Enforces strict mutual exclusivity.
    Logic: If user adds a challenge, remove 'None'. 
    If user adds 'None', remove everything else.
    """
    current = st.session_state.challenge_widget
    previous = st.session_state.challenges_selection
    
    if not current:
        st.session_state.challenges_selection = ["None"]
    elif "None" in current and len(current) > 1:
        # Check if 'None' was just added or if it was already there
        if "None" not in previous:
            # User just selected 'None' while other items existed
            st.session_state.challenges_selection = ["None"]
        else:
            # User added a new challenge while 'None' was already there
            st.session_state.challenges_selection = [x for x in current if x != "None"]
    else:
        st.session_state.challenges_selection = current

def reset_demo_action():
    """Wipes all selections and restores original product view."""
    st.session_state.view_mode = 'original'
    st.session_state.challenges_selection = ["None"]
    # Clearing the widget keys forces the dropdowns to reset to index 0
    if 'height_key' in st.session_state: st.session_state.height_key = ""
    if 'body_key' in st.session_state: st.session_state.body_key = ""
    st.rerun()

# ---------------------------------------------------------
# 3. SIDEBAR (The Left Panel)
# ---------------------------------------------------------
with st.sidebar:
    st.header("FitNexus Engine")
    st.caption("v2.1.0 | Enterprise Retail Build")
    st.divider()
    
    st.subheader("Simulated Shopper Context")
    
    # Using keys for selectboxes allows the reset button to wipe them
    height = st.selectbox(
        "Height", 
        ["", "Under 5'0", "5'0 - 5'2", "5'3 - 5'7", "5'8 - 5'11", "Over 6'0"], 
        index=0,
        key="height_key"
    )
    
    body_type = st.selectbox(
        "Body Type", 
        ["", "Curvy", "Athletic", "Slender", "Full Figured", "Petite"], 
        index=0,
        key="body_key"
    )
    
    # THE WIDGET: Logic is handled via on_change
    st.multiselect(
        "Fit Challenges",
        options=FIT_CHALLENGES,
        key="challenge_widget",
        default=st.session_state.challenges_selection,
        on_change=sync_challenges
    )
    
    # Use the synced selection for the display logic
    current_challenges = st.session_state.challenges_selection
    display_issues = [c for c in current_challenges if c != "None"]
    
    st.info(
        f"**Biometrics:** {height if height else 'Not Set'}, {body_type if body_type else 'Not Set'}\n\n"
        f"**Issues:** {', '.join(display_issues) if display_issues else 'None Selected'}"
    )
    
    st.divider()
    st.button("🔄 Reset Demo", on_click=reset_demo_action)

# ---------------------------------------------------------
# 4. MAIN CONTENT AREA
# ---------------------------------------------------------
st.subheader("🛒 Premium Activewear Co. (Integration Demo)")
st.divider()

col1, col2 = st.columns([1, 1])

if st.session_state.view_mode == 'original':
    with col1:
        # Verified Hero Image (Woman in grey fleece)
        st.image(
            "https://images.pexels.com/photos/7242947/pexels-photo-7242947.jpeg?auto=compress&cs=tinysrgb&w=800",
            caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up Jacket",
            use_container_width=True
        )

    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00**")
        
        # Data-driven Confidence Score
        if "None" in current_challenges:
            st.success("🎯 FitNexus: 92% Match (High Confidence)")
        
        st.write("A versatile layer for seasonal transitions. This textured fleece features a smooth full-length zipper and a tailored, athletic fit.")
        
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_orig")
        st.button("Add to Bag")

        with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: {height} | {body_type} | {', '.join(current_challenges)}")
            st.text_input("Ask a question:", "Will this fit my body type?", key="question_box")
            
            if st.button("Run Analysis"):
                if "None" in current_challenges or not display_issues:
                    st.success("Analysis complete: High-confidence match for your standard profile.")
                else:
                    st.warning(f"**Fit Alert:** Based on your biometrics ({body_type}), the standard zipper track may pull. We recommend our Longline version.")
                    st.button("👉 Shop Recommended Alternative", on_click=lambda: st.session_state.update({"view_mode": "alternative"}))

else:
    with col1:
        # Verified Secondary Image (Grey zip-up fleece)
        st.image(
            "https://images.pexels.com/photos/6311613/pexels-photo-6311613.jpeg?auto=compress&cs=tinysrgb&w=800",
            caption="Product ID: LNG-ZIP-009 | CloudSoft Longline Zip-Up",
            use_container_width=True
        )

    with col2:
        st.success(f"🏆 FitNexus: 98% Match for your profile")
        st.title("CloudSoft Longline Zip-Up")
        st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$138.00**")
        st.write(f"Designed with an extended hemline and full-length zipper specifically to accommodate {', '.join(display_issues) if display_issues else 'your fit profile'}.")
        
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_alt")
        if st.button("Add to Bag"):
            st.balloons()
        
        st.button("← Back to Original Item", on_click=lambda: st.session_state.update({"view_mode": "original"}))