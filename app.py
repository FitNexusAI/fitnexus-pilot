import streamlit as st

# ---------------------------------------------------------
# 1. CUSTOM CSS TO FIX THE "BROKEN" LOOK
# ---------------------------------------------------------
# This block injects CSS to style the default Streamlit widgets 
# to look more like your original red/white design.
st.markdown(
    """
    <style>
    /* 1. Style the MultiSelect Tags (Chips) to be Red */
    span[data-baseweb="tag"] {
        background-color: #E65149 !important; /* The red from your screenshot */
        color: white !important;
        border-radius: 6px;
    }
    
    /* 2. Hide the 'x' on the tag if it conflicts with text, 
       or style it white so it's visible on red */
    span[data-baseweb="tag"] svg {
        fill: white !important;
    }

    /* 3. Adjust the main container for a cleaner look */
    .stMultiSelect {
        max-width: 600px;
    }
    
    /* 4. Optional: Clean up the JSON output font */
    .stJson {
        font-family: 'Courier New', monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. DEFINE OPTIONS
# ---------------------------------------------------------
FIT_CHALLENGES = [
    "None",
    # Torso & Shoulders
    "Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders",
    "Long Arms", "Short Arms",
    # Bust
    "Full Bust", "Small Bust",
    # Stomach
    "Round Stomach", "Soft Midsection",
    # Hips
    "Curvy Hips", "Wide Hips", "Narrow Hips", "High Hip Shelf",
    # Legs
    "Athletic Thighs", "Long Legs", "Short Legs", "Muscular Calves"
]

# ---------------------------------------------------------
# 3. LOGIC HANDLER
# ---------------------------------------------------------
def handle_fit_challenge_change():
    current = st.session_state.fit_challenges_selector
    previous = st.session_state.get('previous_selection', ['None'])

    # 1. User deselected everything -> Default to None
    if not current:
        st.session_state.fit_challenges_selector = ["None"]
    
    # 2. User clicked "None" -> Clear everything else
    elif "None" in current and "None" not in previous:
        st.session_state.fit_challenges_selector = ["None"]
    
    # 3. User clicked a specific trait -> Remove "None"
    elif "None" in current and len(current) > 1:
        st.session_state.fit_challenges_selector = [x for x in current if x != "None"]

    # Update history
    st.session_state.previous_selection = st.session_state.fit_challenges_selector

# Initialize history if missing
if 'previous_selection' not in st.session_state:
    st.session_state.previous_selection = ['None']

# ---------------------------------------------------------
# 4. RENDER UI
# ---------------------------------------------------------
st.title("Fit Profile Setup")
st.write("Select any areas where you typically have fit challenges:")

# The Widget
st.multiselect(
    label="Fit Challenges",
    options=FIT_CHALLENGES,
    default=["None"],
    key="fit_challenges_selector",
    on_change=handle_fit_challenge_change,
    placeholder="Choose your fit challenges..."
)

# ---------------------------------------------------------
# 5. BACKEND SUMMARY
# ---------------------------------------------------------
st.divider()
st.subheader("Summary for Backend")
st.json({"user_fit_profile": st.session_state.fit_challenges_selector})