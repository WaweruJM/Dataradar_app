import streamlit as st
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import time

def show():
    # Check data
    if st.session_state.df is None:
        st.warning("No dataset found. Please upload a file first.")
        if st.button("Go to Upload"):
            st.session_state.page = 1
            st.rerun()
        st.stop()
    
    df = st.session_state.df.copy()
    
    # Header
    st.markdown("""
    <div style='text-align:center; padding:10px; border-radius:10px; background:#f5f7fa; margin-bottom:20px;'>
        <h2>Data Cleaning & Preprocessing</h2>
        <p style='font-size:13px; color:gray;'>Stepwise workflow</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show data preview
    st.subheader("Data Preview (first 10 rows)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Missing values summary
    st.subheader("Missing Values Summary")
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_percent
    })
    st.dataframe(missing_df[missing_df["Missing Count"] > 0], use_container_width=True)
    
    # Cleaning options
    st.subheader("Cleaning Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        missing_strategy = st.selectbox(
            "Missing Values Strategy",
            ["None", "Drop rows", "Mean", "Median", "Mode", "MICE (Multivariate Imputation)"]
        )
    
    with col2:
        outlier_strategy = st.selectbox(
            "Outlier Handling",
            ["None", "Remove (IQR)", "Cap (Winsorize)"]
        )
    
    with col3:
        transform_strategy = st.selectbox(
            "Transformation",
            ["None", "Log", "Z-score"]
        )
    
    # Additional option for fixed value (if needed)
    if missing_strategy == "Mean" or missing_strategy == "Median" or missing_strategy == "Mode":
        st.info("Imputation will be applied only to numeric columns for mean/median, and to all columns for mode.")
    
    # Run cleaning button
    if st.button("Apply Cleaning", type="primary"):
        with st.spinner("Cleaning data, please wait..."):
            time.sleep(1)  # Simulate work
            df_clean = df.copy()
            log_entries = []
            
            # Handle missing values
            if missing_strategy != "None":
                if missing_strategy == "Drop rows":
                    original_rows = len(df_clean)
                    df_clean = df_clean.dropna()
                    log_entries.append(f"Dropped {original_rows - len(df_clean)} rows with missing values.")
                
                elif missing_strategy == "Mean":
                    numeric_cols = df_clean.select_dtypes(include=np.number).columns
                    for col in numeric_cols:
                        df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                    log_entries.append("Imputed missing values with column means (numeric columns only).")
                
                elif missing_strategy == "Median":
                    numeric_cols = df_clean.select_dtypes(include=np.number).columns
                    for col in numeric_cols:
                        df_clean[col].fillna(df_clean[col].median(), inplace=True)
                    log_entries.append("Imputed missing values with column medians (numeric columns only).")
                
                elif missing_strategy == "Mode":
                    for col in df_clean.columns:
                        mode_val = df_clean[col].mode()
                        if not mode_val.empty:
                            df_clean[col].fillna(mode_val[0], inplace=True)
                    log_entries.append("Imputed missing values with column mode (all columns).")
                
                elif missing_strategy == "MICE (Multivariate Imputation)":
                    numeric_cols = df_clean.select_dtypes(include=np.number).columns
                    if len(numeric_cols) > 0:
                        imputer = IterativeImputer(max_iter=10, random_state=42)
                        df_clean[numeric_cols] = imputer.fit_transform(df_clean[numeric_cols])
                        log_entries.append("Applied MICE imputation to numeric columns.")
                    else:
                        st.warning("No numeric columns found for MICE imputation. Skipping.")
            
            # Handle outliers (simplified)
            if outlier_strategy != "None":
                numeric_cols = df_clean.select_dtypes(include=np.number).columns
                for col in numeric_cols:
                    Q1 = df_clean[col].quantile(0.25)
                    Q3 = df_clean[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    if outlier_strategy == "Remove (IQR)":
                        original = len(df_clean)
                        df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
                        log_entries.append(f"Removed {original - len(df_clean)} rows based on IQR for {col}.")
                    elif outlier_strategy == "Cap (Winsorize)":
                        df_clean[col] = df_clean[col].clip(lower, upper)
                        log_entries.append(f"Capped outliers for {col} at IQR bounds.")
            
            # Handle transformation
            if transform_strategy != "None":
                numeric_cols = df_clean.select_dtypes(include=np.number).columns
                for col in numeric_cols:
                    if transform_strategy == "Log":
                        # Avoid log of non-positive values
                        min_val = df_clean[col].min()
                        if min_val > 0:
                            df_clean[col] = np.log(df_clean[col])
                            log_entries.append(f"Applied log transformation to {col}.")
                        else:
                            st.warning(f"Column {col} contains non-positive values; log transformation skipped.")
                    elif transform_strategy == "Z-score":
                        mean = df_clean[col].mean()
                        std = df_clean[col].std()
                        if std != 0:
                            df_clean[col] = (df_clean[col] - mean) / std
                            log_entries.append(f"Applied Z-score standardization to {col}.")
                        else:
                            st.warning(f"Column {col} has zero standard deviation; Z-score skipped.")
            
            # Store cleaned data and log
            st.session_state.cleaned_df = df_clean
            st.session_state.cleaning_log = log_entries
            
            st.success("Cleaning completed successfully!")
            st.balloons()
    
    # Show cleaned data preview if exists
    if st.session_state.cleaned_df is not None:
        st.subheader("Cleaned Data Preview (first 10 rows)")
        st.dataframe(st.session_state.cleaned_df.head(10), use_container_width=True)
        
        # Show cleaning log
        if st.session_state.cleaning_log:
            with st.expander("View Cleaning Log"):
                for entry in st.session_state.cleaning_log:
                    st.write(f"- {entry}")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.page = 2
            st.rerun()
    with col2:
        if st.button("Proceed ➡️", use_container_width=True):
            # If cleaning hasn't been applied, still proceed with original data
            if st.session_state.cleaned_df is None:
                st.session_state.cleaned_df = st.session_state.df
                st.session_state.cleaning_log.append("No cleaning applied.")
            st.session_state.page = 4
            st.rerun()