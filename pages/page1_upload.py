import streamlit as st
import time
import pandas as pd

def show():
    st.subheader("🤗 Welcome to Data Radar")
    st.write("Your ultimate companion in research projects.")
    
    uploaded = st.file_uploader(
        "📁 Upload your file here (CSV or Excel)",
        type=["csv", "xlsx"],
        key="file_uploader"
    )
    
    if uploaded is not None:
        with st.spinner("Uploading in progress, please wait..."):
            time.sleep(1)
            try:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded)
                
                # Store in session state
                st.session_state.df = df
                st.session_state.filename = uploaded.name
                st.session_state.page = 2
                st.rerun()
            except Exception as e:
                st.error(f"Error reading file: {e}. Please check file format.")
    
    st.info("Awaiting data file upload.....")
    st.write("👨🏾‍💻 Note: Uploaded data is analysed centrally and displayed only to your device.")
    st.write("📊 You may download charts and analytical outputs during your session.")
    st.write("🗑 Automatic deletion of all cached files is carried out at end of your session.")