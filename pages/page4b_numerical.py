import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from utils.data_utils import classify_columns

def show():
    df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    if df is None:
        st.warning("No dataset found. Please upload a file first.")
        if st.button("Go to Upload"):
            st.session_state.page = 1
            st.rerun()
        st.stop()
    
    # Ensure categories are available
    if not st.session_state.column_categories:
        st.session_state.column_categories = classify_columns(df)
    categories = st.session_state.column_categories
    
    st.markdown("<h3 style='text-align:center;'>📈 Numerical Summary Statistics</h3>", unsafe_allow_html=True)
    
    # Separate continuous and categorical
    cont_cols = [col for col in df.columns if categories.get(col) == "continuous"]
    cat_cols = [col for col in df.columns if categories.get(col) != "continuous"]
    
    # 1. Continuous variables summary
    st.subheader("Continuous Variables")
    if cont_cols:
        desc = df[cont_cols].describe().T
        # Add skewness and kurtosis
        desc['skewness'] = df[cont_cols].skew()
        desc['kurtosis'] = df[cont_cols].kurtosis()
        st.dataframe(desc, use_container_width=True)
    else:
        st.info("No continuous variables found.")
    
    # 2. Normality tests for continuous variables
    if cont_cols:
        st.subheader("Normality Tests (Shapiro-Wilk)")
        normality_results = []
        for col in cont_cols:
            data = df[col].dropna()
            if len(data) <= 5000 and len(data) >= 3:
                stat, p = stats.shapiro(data)
                normality_results.append({
                    "Variable": col,
                    "Statistic": stat,
                    "p-value": p,
                    "Normal (p>0.05)": p > 0.05
                })
            else:
                normality_results.append({
                    "Variable": col,
                    "Statistic": "N/A",
                    "p-value": "N/A",
                    "Normal (p>0.05)": "Not computed"
                })
        st.dataframe(pd.DataFrame(normality_results), use_container_width=True)
    
    # 3. Categorical variables summary (frequency tables)
    if cat_cols:
        st.subheader("Categorical Variables")
        for col in cat_cols:
            with st.expander(f"Frequency table for {col}"):
                freq = df[col].value_counts().reset_index()
                freq.columns = [col, "Count"]
                st.dataframe(freq, use_container_width=True)
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Graphical", use_container_width=True):
            st.session_state.page = 4
            st.rerun()
    with col2:
        if st.button("Proceed to Statistical Tests ➡️", use_container_width=True):
            st.session_state.page = 6
            st.rerun()