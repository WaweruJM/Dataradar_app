import streamlit as st
import pandas as pd

def show():
    st.markdown("<h3 style='text-align:center;'>📄 Analysis Documentation</h3>", unsafe_allow_html=True)
    
    # Gather summary
    fname = st.session_state.filename if st.session_state.filename else "uploaded_file"
    df_original = st.session_state.df
    df_cleaned = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else df_original
    
    # Data overview
    overview = f"""
    **Dataset:** {fname}  
    - Original rows: {df_original.shape[0]}  
    - Original columns: {df_original.shape[1]}  
    - Cleaned rows: {df_cleaned.shape[0]}  
    - Cleaned columns: {df_cleaned.shape[1]}  
    """
    
    # Cleaning steps
    cleaning_log = st.session_state.cleaning_log if st.session_state.cleaning_log else ["No cleaning steps recorded."]
    
    # Statistical tests results (placeholder, we could store them in session state)
    test_log = st.session_state.test_results if st.session_state.test_results else ["No statistical tests performed."]
    
    # Combine
    report = f"""
    ## Data Summary
    {overview}
    
    ## Data Cleaning
    {"\n".join([f"- {entry}" for entry in cleaning_log])}
    
    ## Statistical Tests
    {"\n".join([f"- {entry}" for entry in test_log])}
    
    ## Session Information
    - Analysis performed using Data Radar assistant.
    - All outputs are for research purposes.
    """
    
    st.text_area("Generated Report", report, height=400)
    
    # Option to download report
    st.download_button(
        label="Download Report as Text",
        data=report,
        file_name="analysis_report.txt",
        mime="text/plain"
    )
    
    # Exit button
    st.markdown("---")
    if st.button("Exit Session", type="primary"):
        st.session_state.clear()
        st.success("Session ended. Thank you for using Data Radar.")
        st.session_state.page = 1
        st.rerun()
    
    # Navigation back (optional)
    if st.button("⬅️ Back to Statistical Tests"):
        st.session_state.page = 6
        st.rerun()