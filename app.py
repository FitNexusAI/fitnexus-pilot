import streamlit as st
import streamlit.components.v1 as components

# 1. PAGE CONFIG
st.set_page_config(layout="wide", page_title="FitNexus | Retail Integration Demo")

# --- THE FIX: TOP-LEVEL SCROLL TRIGGER ---
# This executes BEFORE the rest of the UI renders, ensuring the snap to top.
if st.session_state.get('view_mode') == 'alternative':
    components.html(
        """
        <script>
            window.parent.document.querySelector('section.main').scrollTo({ top: 0, behavior: 'instant' });
        </script>
        """,
        height=0,
    )

# 2. STATE MANAGEMENT & TAG SYNC
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'
if 'challenges_selection' not in st.session_state:
    st.session_state.challenges_selection = ["None"]

def sync_logic():
    """CLEARS 'NONE' INSTANTLY: Refactored to force a visual refresh."""
    current = st.session_state.challenge_widget
    previous = st.session_state.challenges_selection
    if not current:
        new_selection = ["None"]
    elif "None" in current and len(current) > 1:
        if "None" in previous:
            new_selection = [x for x in current if x != "None"]
        else:
            new_selection = ["None"]
    else:
        new_selection = current
    
    st.session_state.challenges_selection = new_selection
    # This line forces the widget to visually update
    st.session_state.challenge_widget = new_selection

# [Rest of your UI/Sidebar code here...]