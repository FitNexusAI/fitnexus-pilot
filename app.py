import streamlit as st

# Page Configuration
st.set_page_config(layout="wide", page_title="Premium Activewear Co.")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("Fit Profile")
    
    # Separate Dropdown for Height
    height_options = ["< 5'0\"", "5'0\" - 5'3\"", "5'4\" - 5'7\"", "5'8\" - 5'11\"", "6'0\" - 6'3\"", "> 6'3\""]
    selected_height = st.selectbox("Height", height_options, index=3)

    # Separate Dropdown for Fit Challenges
    # Using multiselect allows for multiple challenges, but standard selectbox works if only one is needed.
    # Based on "dropdowns", a multiselect is often preferred for "challenges".
    fit_challenges_options = ["None", "Broad Shoulders", "Long Torso", "Short Torso", "Athletic Thighs", "Petite Frame", "Curvy Hips"]
    selected_challenges = st.multiselect("Fit Challenges", fit_challenges_options, default=["None"])

# --- MAIN CONTENT ---

# Header
st.markdown("### 🛒 Premium Activewear Co. (Integration Demo)")
st.markdown("---")

# Layout: Two columns for Product Image and Product Details
col1, col2 = st.columns([1, 1])

with col1:
    # Placeholder for the product image
    # Replace 'path/to/image.png' with your actual image file or URL
    st.image("https://via.placeholder.com/500x400?text=Oversized+Cotton+Hoodie", use_column_width=True)
    st.caption("Product ID: SCUBA-CT-001")

with col2:
    st.title("Oversized Cotton Hoodie")
    st.markdown("⭐⭐⭐⭐⭐ (4.9) | **$118.00**")
    
    st.write("""
    The ultimate post-workout layer. Naturally breathable soft cotton fabric with a cozy hood and kangaroo pocket.
    """)
    
    st.markdown("**Size:**")
    size_selection = st.radio("Size", ["XS/S", "M/L", "XL/XXL"], index=1, horizontal=True, label_visibility="collapsed")
    
    st.button("Add to Bag", type="primary")

# --- FITNEXUS INTELLIGENCE SECTION ---
st.write("")
st.write("")

with st.expander("📐 FitNexus Intelligence (Check My Fit)", expanded=True):
    # Displaying the context from the sidebar inputs
    challenges_str = ", ".join(selected_challenges) if selected_challenges else "None"
    st.info(f"Analyzing for: **{selected_height}** | **{challenges_str}**")
    
    user_question = st.text_input("Ask a question:", value="Will this fit my body type?")
    
    if st.button("Run Analysis"):
        st.write("Running analysis based on your fit profile...")
        # Add your backend analysis logic here