import streamlit as st

# ---------------------------------------------------------
# 1. DEFINE THE EXTENSIVE LIST OF OPTIONS
# ---------------------------------------------------------
FIT_CHALLENGES = [
    "None",
    
    # Torso & Shoulders
    "Long Torso",
    "Short Torso",
    "Broad Shoulders",
    "Narrow Shoulders",
    "Long Arms",
    "Short Arms",

    # Bust
    "Full Bust",
    "Small Bust",

    # Stomach
    "Round Stomach",
    "Soft Midsection",

    # Hips
    "Curvy Hips",
    "Wide Hips",
    "Narrow Hips",
    "High Hip Shelf",

    # Legs
    "Athletic Thighs",
    "Long Legs",
    "Short Legs",
    "Muscular Calves"
]

# ---------------------------------------------------------
# 2. DEFINE THE LOGIC (CALLBACK HANDLER)
# ---------------------------------------------------------
def handle_fit_challenge_change():
    """
    Manages the mutual exclusivity logic between 'None' 
    and specific fit attributes.
    """
    # Get the current list selected by the user
    current_selection = st.session_state.fit_challenges_selector
    
    # Get what was selected previously (to detect changes)
    previous_selection = st.session_state.get('previous_selection', ['None'])

    # SCENARIO A: The list is empty (User deselected everything)
    # -> Force default back to "None"
    if not current_selection:
        st.session_state.fit_challenges_selector = ["None"]

    # SCENARIO B: User just clicked "None" (It wasn't there before, now it is)
    # -> Clear all other options
    elif "None" in current_selection and "None" not in previous_selection:
        st.session_state.fit_challenges_selector = ["None"]

    # SCENARIO C: "None" is present, but the user added a specific trait
    # -> Remove "None" so only the specific traits remain
    elif "None" in current_selection and len(current_selection) > 1:
        st.session_state.fit_challenges_selector = [
            x for x in current_selection if x != "None"
        ]

    # Update the history tracker for the next interaction
    st.session_state.previous_selection = st.session_state.fit_challenges_selector


# ---------------------------------------------------------
# 3. INITIALIZE STATE
# ---------------------------------------------------------
# Ensure our history tracker exists on first load
if 'previous_selection' not in st.session_state:
    st.session_state.previous_selection = ['None']

# ---------------------------------------------------------
# 4. RENDER THE UI
# ---------------------------------------------------------
st.title("Fit Profile Setup")

st.write("Select any areas where you typically have fit challenges:")

# The Multiselect Widget
selected_challenges = st.multiselect(
    label="Fit Challenges",
    options=FIT_CHALLENGES,
    default=["None"],
    key="fit_challenges_selector", # This key binds the widget to session_state
    on_change=handle_fit_challenge_change # Triggers our logic function above
)

# ---------------------------------------------------------
# 5. DISPLAY RESULTS (For debugging/verification)
# ---------------------------------------------------------
st.divider()
st.write("### Summary for Backend:")
st.json({
    "user_fit_profile": selected_challenges
})