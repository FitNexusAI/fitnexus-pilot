import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="FitNexus Enterprise Demo")

st.markdown(
    """
    <style>
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
# 2. STATE MANAGEMENT & CALLBACKS
# ---------------------------------------------------------
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'

def switch_to_alternative():
    st.session_state.view_mode = 'alternative'

def switch_to_original():
    st.session_state.view_mode = 'original'

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
    
    selected_challenges = st.multiselect(
        "Fit Challenges",
        ["Short Torso", "Long Torso", "Broad Shoulders", "Curvy Hips", "Long Arms"],
        default=["Short Torso", "Broad Shoulders"]
    )
    
    st.info(f"**Biometrics:** {height}, {body_type}\n\n**Issues:** {', '.join(selected_challenges)}")
    
    if st.session_state.view_mode == 'alternative':
        st.button("🔄 Reset to Original", on_click=switch_to_original)

# ---------------------------------------------------------
# 4. MAIN CONTENT AREA
# ---------------------------------------------------------
st.subheader("🛒 Premium Activewear Co. (Integration Demo)")
st.divider()

col1, col2 = st.columns([1, 1])

if st.session_state.view_mode == 'original':
    with col1:
        # Verified: Woman of Color in Grey Zip-Up Fleece
        st.image(
            "https://images.unsplash.com/photo-1548690312-e3b507d8c110?auto=format&fit=crop&w=800&q=80",
            caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up Jacket",
            use_container_width=True
        )

    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00**")
        st.write("A versatile layer with a full-length zipper closure and zippered hand pockets. Features a high-collar design for wind protection and a tailored, athletic fit.")
        
        st.write("**Size**")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_orig")
        st.button("Add to Bag")

        with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: {height} | {body_type} | {', '.join(selected_challenges)}")
            st.text_input("Ask a question:", "Will this fit my body type?")
            
            if st.button("Run Analysis"):
                st.warning(
                    f"""
                    **Fit Alert:** Based on your profile ({body_type}, Broad Shoulders), the zipper on this specific jacket may pull at the chest and shoulders.
                    
                    **Recommendation:** We recommend our Longline version which features a dropped shoulder to accommodate your biometrics.
                    """
                )
                st.button("👉 Shop Recommended Alternative", on_click=switch_to_alternative)

else:
    with col1:
        # Verified: Woman of Color in Longline Zip-Up Performance Wear
        st.image(
            "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=800&q=80",
            caption="Product ID: LNG-ZIP-009 | CloudSoft Longline Zip-Up",
            use_container_width=True
        )

    with col2:
        st.success(f"✅ Perfect Match for: {', '.join(selected_challenges)}")
        st.title("CloudSoft Longline Zip-Up")
        st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$138.00**")
        st.write("Designed with an extended hemline and a full-length front zipper. The CloudSoft fabric provides extra stretch at the shoulders and hips to prevent riding up.")
        
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_alt")
        if st.button("Add to Bag"):
            st.balloons()
        
        st.button("← Back to Original Item", on_click=switch_to_original)