import streamlit as st

# 1. PAGE CONFIG & CUSTOM CSS
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
    """STRICT MUTUAL EXCLUSION: Ensures 'None' and challenges never coexist."""
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

def reset_demo():
    """FULL FACTORY RESET: Clears images, logic, and dropdowns."""
    st.session_state.view_mode = 'original'
    st.session_state.challenges_selection = ["None"]
    if 'h_key' in st.session_state: st.session_state.h_key = ""
    if 'b_key' in st.session_state: st.session_state.b_key = ""
    st.rerun()

# 3. SIDEBAR
with st.sidebar:
    st.header("FitNexus Engine")
    st.caption("v2.1.0 | Enterprise Retail Build")
    st.divider()
    st.subheader("Simulated Shopper Context")
    
    h_val = st.selectbox("Height", ["", "Under 5'0", "5'0-5'2", "5'3-5'7", "5'8-5'11", "Over 6'0"], index=0, key="h_key")
    b_val = st.selectbox("Body Type", ["", "Curvy", "Athletic", "Slender", "Full Figured", "Petite"], index=0, key="b_key")
    
    st.multiselect("Fit Challenges", options=FIT_OPTIONS, key="challenge_widget", 
                   default=st.session_state.challenges_selection, on_change=sync_logic)
    
    active = st.session_state.challenges_selection
    real_issues = [c for c in active if c != "None"]
    
    st.info(f"**Biometrics:** {h_val if h_val else 'Not Set'}, {b_val if b_val else 'Not Set'}\n\n"
            f"**Issues:** {', '.join(real_issues) if real_issues else 'None Selected'}")
    
    st.divider()
    st.button("🔄 Reset Demo", on_click=reset_demo)

# 4. MAIN CONTENT
st.subheader("🛒 Premium Activewear Co. (Integration Demo)")
st.divider()

col1, col2 = st.columns([1, 1])

if st.session_state.view_mode == 'original':
    with col1:
        st.image("https://images.pexels.com/photos/7242947/pexels-photo-7242947.jpeg?auto=compress&cs=tinysrgb&w=800",
                 caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up", use_container_width=True)
    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00**")
        
        if not real_issues and h_val and b_val:
            st.success("🎯 FitNexus Confidence: 94% Match")

        st.write("A versatile layer for seasonal transitions. Features a smooth full-length zipper and soft, insulating fabric.")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True)
        st.button("Add to Bag")

        with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: {h_val if h_val else 'Not Set'} | {b_val if b_val else 'Not Set'} | {', '.join(active)}")
            st.text_input("Ask a question:", "Will this fit my body type?", key="q_box")
            
            if st.button("Run Analysis"):
                if not real_issues:
                    st.success("Analysis complete: High-confidence match for your standard profile.")
                else:
                    analysis_points = []
                    if "Long Torso" in real_issues:
                        analysis_points.append("- **Torso Length:** This jacket has a standard 22\" cut. On a **Long Torso**, the hem will sit above the hip, potentially causing it to ride up.")
                    if "Broad Shoulders" in real_issues:
                        analysis_points.append("- **Shoulder Width:** The high-collar construction has reinforced seams. For **Broad Shoulders**, this may cause pulling across the upper back.")
                    if "Short Torso" in real_issues:
                        analysis_points.append("- **Proportions:** The mid-section may bunch at the zipper line for a **Short Torso** profile.")
                    if "Curvy Hips" in real_issues or "Wide Hips" in real_issues:
                        analysis_points.append("- **Hem Opening:** This jacket features a tapered hem. On **Curvy Hips**, the fabric may feel restrictive when fully zipped.")
                    
                    if not analysis_points:
                        analysis_points.append(f"- The specific combination of {', '.join(real_issues)} suggests this standard cut may not provide the optimal comfort you are looking for.")

                    st.warning("**Fit Analysis Results:**\n\n" + "\n".join(analysis_points))
                    st.button("👉 Shop Recommended Alternative", on_click=lambda: st.session_state.update({"view_mode": "alternative"}))

else:
    with col1:
        st.image("https://images.pexels.com/photos/6311613/pexels-photo-6311613.jpeg?auto=compress&cs=tinysrgb&w=800",
                 caption="Product ID: LNG-ZIP-009 | CloudSoft Longline", use_container_width=True)
    with col2:
        st.success("🏆 FitNexus Confidence: 98% Match for your profile")
        st.title("CloudSoft Longline Zip-Up")
        st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$138.00**")
        st.write(f"Designed with an extended hemline and full-length zipper specifically to accommodate {', '.join(real_issues) if real_issues else 'your fit profile'}.")
        
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_alt")
        if st.button("Add to Bag"): st.balloons()
        st.button("← Back to Original Item", on_click=lambda: st.session_state.update({"view_mode": "original"}))