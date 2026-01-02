import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="FitNexus Enterprise Demo")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    span[data-baseweb="tag"] {
        background-color: #F74845 !important;
        color: white !important;
    }
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
# 2. STATE MANAGEMENT & LOGIC
# ---------------------------------------------------------
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'

# Logic to ensure "None" is mutually exclusive
if 'fit_challenges' not in st.session_state:
    st.session_state.fit_challenges = ["None"]

def update_challenges():
    current = st.session_state.temp_challenges
    # If "None" was just added, make it the only selection
    if len(current) > 1 and "None" == current[-1]:
        st.session_state.fit_challenges = ["None"]
    # If other items exist and "None" is present, remove "None"
    elif len(current) > 1 and "None" in current:
        st.session_state.fit_challenges = [x for x in current if x != "None"]
    else:
        st.session_state.fit_challenges = current

def switch_to_alternative():
    st.session_state.view_mode = 'alternative'

def switch_to_original():
    st.session_state.view_mode = 'original'

# ---------------------------------------------------------
# 3. SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.header("FitNexus Engine")
    st.caption("v2.1.0 | Enterprise Retail Build")
    st.divider()
    
    st.subheader("Simulated Shopper Context")
    height = st.selectbox("Height", ["Under 5'0", "5'0 - 5'2", "5'3 - 5'7", "5'8 - 5'11", "Over 6'0"], index=2)
    body_type = st.selectbox("Body Type", ["Curvy", "Athletic", "Slender", "Full Figured", "Petite"], index=0)
    
    # Mutually exclusive multiselect
    st.multiselect(
        "Fit Challenges",
        ["None", "Short Torso", "Long Torso", "Broad Shoulders", "Curvy Hips", "Long Arms"],
        key="temp_challenges",
        default=st.session_state.fit_challenges,
        on_change=update_challenges
    )
    
    # Use the cleaned state for display
    challenges_display = st.session_state.fit_challenges
    st.info(f"**Biometrics:** {height}, {body_type}\n\n**Issues:** {', '.join(challenges_display)}")
    
    st.divider()
    if st.button("🔄 Reset Demo"):
        st.session_state.view_mode = 'original'
        st.session_state.fit_challenges = ["None"]
        st.rerun()

# ---------------------------------------------------------
# 4. MAIN CONTENT
# ---------------------------------------------------------
st.subheader("🛒 Premium Activewear Co. (Integration Demo)")
st.divider()

col1, col2 = st.columns([1, 1])

if st.session_state.view_mode == 'original':
    with col1:
        st.image(
            "https://images.pexels.com/photos/7242947/pexels-photo-7242947.jpeg?auto=compress&cs=tinysrgb&w=800",
            caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up",
            use_container_width=True
        )
    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00**")
        
        if "None" in challenges_display:
            st.success("🎯 FitNexus: 92% Match (High Confidence)")
        
        st.write("A versatile layer for seasonal transitions. This textured fleece features a smooth full-length zipper and a tailored, athletic fit.")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_orig")
        st.button("Add to Bag")

        with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: {height} | {body_type} | {', '.join(challenges_display)}")
            st.text_input("Ask a question:", "Will this fit my body type?")
            
            if st.button("Run Analysis"):
                if "None" in challenges_display:
                    st.success("Fit Confirmation: High-confidence match for your standard profile.")
                else:
                    st.warning(f"**Fit Alert:** Based on your biometrics ({body_type}), the standard zipper track may pull. We recommend our Longline version.")
                    st.button("👉 Shop Recommended Alternative", on_click=switch_to_alternative)

else:
    with col1:
        st.image(
            "https://images.pexels.com/photos/6311613/pexels-photo-6311613.jpeg?auto=compress&cs=tinysrgb&w=800",
            caption="Product ID: LNG-ZIP-009 | Longline Performance",
            use_container_width=True
        )
    with col2:
        st.success(f"🏆 FitNexus: 98% Match for: {', '.join(challenges_display)}")
        st.title("CloudSoft Longline Zip-Up")
        st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$138.00**")
        st.write("**Why this fits you:** Designed with an extended hemline and high-stretch zipper track to provide coverage for long torsos and broad shoulders.")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_alt")
        if st.button("Add to Bag"):
            st.balloons()
        st.button("← Back to Original Item", on_click=switch_to_original)