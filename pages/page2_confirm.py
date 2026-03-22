import streamlit as st
import pandas as pd

def show():
    # Safety check
    if st.session_state.df is None:
        st.error("No dataset found. Please upload a file first.")
        if st.button("⬅️ Back to Upload"):
            st.session_state.page = 1
            st.rerun()
        st.stop()
    
    df = st.session_state.df
    
    # Centered confirmation
    st.markdown("""
    <div style="text-align:center; padding:15px; background:#f0f6fb; border-radius:10px; margin-bottom:20px;">
        <h3>✅ Dataset Successfully Uploaded</h3>
        <p style="font-size:14px; color:gray;">Review dataset structure and confirm to proceed</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset overview
    rows, cols = df.shape
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    
    overview_df = pd.DataFrame({
        "Metric": ["Number of Rows", "Number of Columns", "Missing Values", "Duplicate Rows"],
        "Value": [f"{rows:,}", cols, f"{missing:,}", duplicates]
    })
    st.markdown("### 𝄜 Dataset Overview")
    st.table(overview_df)
    
    # Data preview
    st.markdown(f"### 🔍 Data Preview <span style='font-size:13px; color:gray;'>({rows:,} rows × {cols} columns)</span>", unsafe_allow_html=True)
    st.caption("Displaying first 6 rows")
    st.dataframe(df.head(6), use_container_width=True)
    
    # Variable structure expander
    with st.expander("🧬 Variable Structure"):
        dtype_df = df.dtypes.astype(str).reset_index()
        dtype_df.columns = ["Variable", "Data Type"]
        st.dataframe(dtype_df, use_container_width=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm & Proceed", use_container_width=True):
            st.session_state.page = 3
            st.rerun()
    with col2:
        if st.button("🗑️ Replace Dataset", use_container_width=True):
            st.session_state.df = None
            st.session_state.filename = None
            st.session_state.page = 1
            st.rerun()