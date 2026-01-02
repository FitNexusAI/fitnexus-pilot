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
    
    /* 4. Hide standard Streamlit chrome for a clean demo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. STATE MANAGEMENT
# ---------------------------------------------------------

if 'previous_selection' not in st.session_state:
    st.session_state.previous_selection = ['None']

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'

# ---------------------------------------------------------
# 3. FIT LOGIC HANDLER
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
    """
    Ensures 'None' is mutually exclusive from other options.
    """
    current = st.session_state.fit_challenges_selector
    previous = st.session_state.get('previous_selection', ['None'])

    # 1. If selection is empty, force default to "None"
    if not current:
        st.session_state.fit_challenges_selector = ["None"]
        
    # 2. If "None" was just selected, clear everything else
    elif "None" in current and "None" not in previous:
        st.session_state.fit_challenges_selector = ["None"]
        
    # 3. If a specific trait was selected, remove "None"
    elif "None" in current and len(current) > 1:
        st.session_state.fit_challenges_selector = [x for x in current if x != "None"]

    # Update history tracking
    st.session_state.previous_selection = st.session_state.fit_challenges_selector

# ---------------------------------------------------------
# 4. SIDEBAR (The Left Panel)
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
        index=0
    )
    
    # --- Fit Challenge Selector ---
    st.write("Fit Challenges (Select multiple)")
    selected_challenges = st.multiselect(
        label="Fit Challenges",
        options=FIT_CHALLENGES,
        default=["None"],
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
    
    # Reset button for demo purposes
    if st.session_state.view_mode == 'alternative':
        st.divider()
        if st.button("🔄 Reset Demo to Start"):
            st.session_state.view_mode = 'original'
            st.rerun()

# ---------------------------------------------------------
# 5. MAIN CONTENT AREA (DYNAMIC)
# ---------------------------------------------------------

st.subheader("🛒 Premium Activewear Co. (Integration Demo)")
st.divider()

col1, col2 = st.columns([1, 1])

# =========================================================
# VIEW A: THE ORIGINAL PRODUCT
# =========================================================
if st.session_state.view_mode == 'original':
    with col1:
        st.image(
            "https://images.pexels.com/photos/7242947/pexels-photo-7242947.jpeg?auto=compress&cs=tinysrgb&w=800",
            caption="Product ID: FLCE-ZIP-001 | Woman shown in relaxed fit",
            use_container_width=True
        )

    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00**")
        
        st.write("A versatile layer for seasonal transitions. This textured fleece jacket features a smooth full-length zipper, a relaxed silhouette, and soft, insulating fabric.")
        
        st.write("**Size**")
        size = st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True)
        
        st.button("Add to Bag")

        st.write("") 
        st.write("") 

        # --- INTELLIGENCE SECTION (Logic: Dynamic Warnings) ---
        with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: {height} | {body_type} | {', '.join(selected_challenges)}")
            
            question = st.text_input("Ask a question:", "Will this fit my body type and address my fit challenges?")
            
            if st.button("Run Analysis"):
                if "None" in selected_challenges:
                     st.success(f"Fit Confirmation: Great Match! The relaxed fit aligns with your {body_type} body type.")
                else:
                    # --- DYNAMIC TEXT GENERATION ---
                    # This block builds the sentences based on what is actually selected
                    analysis_points = []
                    
                    if "Long Torso" in selected_challenges:
                        analysis_points.append("This jacket sits just below the waist (22\" length). For a **Long Torso**, this often feels like a 'cropped' fit rather than the intended length.")
                    
                    if "Broad Shoulders" in selected_challenges:
                        analysis_points.append("The shoulder seams are structured and true-to-size. For **Broad Shoulders**, this may feel restrictive, especially when layering over other clothes.")
                        
                    if "Curvy Hips" in selected_challenges or "Wide Hips" in selected_challenges:
                        analysis_points.append("The hemline features a non-stretch binding. For **Curvy Hips**, this often causes the jacket to ride up when walking rather than sitting flat.")
                    
                    if "Full Bust" in selected_challenges:
                        analysis_points.append("The chest measurement is fitted. For a **Full Bust**, the zipper may pull across the chest line.")

                    # Fallback for other tags
                    if not analysis_points:
                        analysis_points.append(f"The specific combination of {', '.join(selected_challenges)} suggests the standard cut of this jacket may not provide the optimal comfort you are looking for.")

                    # Join the points into a single string
                    final_analysis = " ".join(analysis_points)

                    st.warning(
                        f"""
                        **Fit Alert:**
                        
                        Based on the user profile ({body_type}, {', '.join(selected_challenges)}), this specific product may not be an ideal fit.
                        
                        **Analysis:**
                        {final_analysis}
                        
                        **Recommendation:**
                        As an alternative, I recommend the **CloudSoft Longline Zip-Up**. It features a dropped shoulder and extended hem that accommodates these specific fit needs.
                        """
                    )
                    
                    if st.button("👉 Shop Recommended Alternative"):
                        st.session_state.view_mode = 'alternative'
                        st.rerun()

# =========================================================
# VIEW B: THE RECOMMENDED ALTERNATIVE
# =========================================================
else:
    with col1:
        st.image(
            "https://images.pexels.com/photos/6311392/pexels-photo-6311392.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            caption="Product ID: LNG-ZIP-009 | Model wearing Longline Fit",
            use_container_width=True
        )

    with col2:
        st.success(f"✅ Perfect Match for: {', '.join(selected_challenges)}")
        
        st.title("CloudSoft Longline Zip-Up")
        st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$138.00**")
        
        st.write("**Why this fits you:** Designed with an extended hemline (3 inches longer) and relaxed drop-shoulders. specifically engineered to provide coverage without riding up or pulling at the shoulders.")
        
        st.write("**Size**")
        size = st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True)
        
        if st.button("Add to Bag"):
            st.balloons()
            st.toast("Added to Bag!", icon="🛍️")

        st.write("")
        st.divider()
        
        if st.button("← Back to Original Item"):
            st.session_state.view_mode = 'original'
            st.rerun()