import streamlit as st
import streamlit.components.v1 as components

# 1. PAGE CONFIG & CUSTOM CSS
st.set_page_config(layout="wide", page_title="FitNexus | Retail Integration Demo")

# Helper function to force browser scroll to top via JS
def scroll_to_top():
    components.html(
        """
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
        """,
        height=0,
    )

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
    .logo-text { font-weight: bold; font-size: 24px; color: #333; margin-bottom: 0px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. STATE MANAGEMENT
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'original'

if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

if 'challenges_selection' not in st.session_state:
    st.session_state.challenges_selection = ["None"]

def sync_logic():
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

def reset_demo_state():
    st.session_state.view_mode = 'original'
    st.session_state.analysis_run = False
    st.session_state.challenges_selection = ["None"]
    st.session_state.h_key = ""
    st.session_state.b_key = ""
    if 'challenge_widget' in st.session_state:
        st.session_state.challenge_widget = ["None"]

# 3. SIDEBAR
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown('<p class="logo-text">Fitnexus Ai</p>', unsafe_allow_html=True)
    
    st.caption("AI-Powered Fit Intelligence | v2.1.0")
    st.divider()
    
    st.subheader("Shopper Profile")
    h_val = st.selectbox("Height", ["", "Under 5'0", "5'0-5'2", "5'3-5'7", "5'8-5'11", "Over 6'0"], index=0, key="h_key")
    b_val = st.selectbox("Body Type", ["", "Curvy", "Athletic", "Slender", "Full Figured", "Petite"], index=0, key="b_key")
    
    FIT_OPTIONS = ["None", "Long Torso", "Short Torso", "Broad Shoulders", "Narrow Shoulders", "Long Arms", "Short Arms", "Full Bust", "Small Bust", "Round Stomach", "Soft Midsection", "Curvy Hips", "Wide Hips", "Narrow Hips", "High Hip Shelf", "Athletic Thighs", "Long Legs", "Short Legs", "Muscular Calves"]
    
    st.multiselect("Fit Challenges", options=FIT_OPTIONS, key="challenge_widget", 
                   default=st.session_state.challenges_selection, on_change=sync_logic)
    
    active = st.session_state.challenges_selection
    real_issues = [c for c in active if c != "None"]
    
    st.info(f"**Biometrics:** {h_val if h_val else 'Not Set'}, {b_val if b_val else 'Not Set'}\n\n"
            f"**Issues:** {', '.join(real_issues) if real_issues else 'None Selected'}")
    
    st.divider()
    st.button("🔄 Reset Demo", on_click=reset_demo_state)

# 4. MAIN CONTENT
st.subheader("🛒 Premium Activewear Co.")
st.caption("Official Retail Partner Integration")
st.divider()

col1, col2 = st.columns([1, 1])

if st.session_state.view_mode == 'original':
    with col1:
        st.image("https://images.pexels.com/photos/7242947/pexels-photo-7242947.jpeg?auto=compress&cs=tinysrgb&w=800",
                 caption="Product ID: FLCE-ZIP-001 | Textured Zip-Up Jacket", use_container_width=True)
    with col2:
        st.title("Textured Fleece Zip-Up Jacket")
        st.markdown("⭐⭐⭐⭐⭐ (4.8) | **$128.00**")
        
        if h_val and b_val and not real_issues:
             st.success("🎯 FitNexus Confidence: 94% Match")
        elif real_issues:
             st.error("⚠️ Fit Alert: Low Confidence Match")

        st.write("A versatile layer with a smooth full-length zipper and soft fabric.")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True)
        st.button("Add to Bag")

        with st.expander("FitNexus Intelligence (Check My Fit)", expanded=True):
            st.caption(f"Analyzing for: {h_val if h_val else 'Not Set'} | {b_val if b_val else 'Not Set'} | {', '.join(active)}")
            st.text_input("Ask a question:", "Will this fit my body type?", key="q_box")
            
            if st.button("Run Analysis"):
                st.session_state.analysis_run = True
            
            if st.session_state.analysis_run:
                if not real_issues:
                    st.success("Analysis complete: This item is a high-confidence match for your profile.")
                else:
                    st.warning("### Fit Alert:")
                    st.write(f"It seems like the Textured Fleece Zip-Up Jacket may not be the best fit for your body type. The jacket is designed to be short in the body which could be a problem due to your **{', '.join(real_issues)}**, as it may sit higher on your waist than is comfortable.")
                    st.write("As an alternative, I recommend instead the **CloudSoft Longline Zip-Up**. This jacket provides a smoother line and doesn't increase in width when sized up.")
                    
                    # Stable CTA Button
                    if st.button("👉 Shop Recommended Alternative"):
                        st.session_state.view_mode = 'alternative'
                        st.rerun()

else:
    scroll_to_top()
    with col1:
        st.image("https://images.pexels.com/photos/15759560/pexels-photo-15759560.jpeg?auto=compress&cs=tinysrgb&w=800",
                 caption="Product ID: LNG-ZIP-009 | CloudSoft Longline Zip-Up", use_container_width=True)
    with col2:
        st.success("🏆 FitNexus Confidence: 98% Match for your profile")
        st.title("CloudSoft Longline Zip-Up")
        st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$138.00**")
        st.write(f"Designed with a longer profile specifically to accommodate **{', '.join(real_issues)}**. This style ensures comfort and coverage that moves with you.")
        st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, key="size_alt")
        if st.button("Add to Bag"): st.balloons()
        
        if st.button("← Back to Original Item"):
            st.session_state.view_mode = 'original'
            st.session_state.analysis_run = False
            st.rerun()

# 5. RESTORED FULL ENTERPRISE FAQ SECTION
st.divider()
st.subheader("Enterprise Integration FAQ")

with st.expander("How long does a standard integration take?"):
    st.write("Our lightweight API-first architecture allows for a basic 'Powered by FitNexus' integration in as little as 2 weeks. Custom enterprise styling and full CRM data syncing typically takes 4–6 weeks.")

with st.expander("Does this require shoppers to create a FitNexus account?"):
    st.write("No. The demo you see here uses 'Guest Mode.' We can capture biometrics anonymously to provide immediate value, or sync with your existing loyalty program to save shopper profiles for future visits.")

with st.expander("How does this impact the Return Rate (RTO)?"):
    st.write("Retail partners using FitNexusAI typically see a meaningful reduction in size-related returns. By proactively flagging fit conflicts, we prevent the purchase of items destined to be returned.")

with st.expander("Is shopper data secure and GDPR/CCPA compliant?"):
    st.write("Absolutely. FitNexusAI does not store Personally Identifiable Information (PII) unless authorized. All biometric data is encrypted and used solely for providing fit recommendations.")