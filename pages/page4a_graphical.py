import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import io
from utils.data_utils import classify_columns
from utils.plot_utils import create_histogram_with_kde, create_boxplot, create_pie_chart, create_bar_chart

def show():
    # Get data
    df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    if df is None:
        st.warning("No dataset found. Please upload a file first.")
        if st.button("Go to Upload"):
            st.session_state.page = 1
            st.rerun()
        st.stop()
    
    # Classify columns (if not already)
    if not st.session_state.column_categories:
        st.session_state.column_categories = classify_columns(df)
    categories = st.session_state.column_categories
    
    st.markdown("<h3 style='text-align:center;'>📊 Graphical Descriptive Statistics</h3>", unsafe_allow_html=True)
    st.write("Explore distributions of each variable. Continuous variables include histogram with KDE and boxplot; categorical variables use appropriate charts.")
    
    # Skip ID columns (by heuristic)
    id_cols = [col for col in df.columns if 'id' in col.lower()]
    vars_to_plot = [col for col in df.columns if col not in id_cols]
    
    # Allow user to select variables
    selected_vars = st.multiselect("Select variables to visualize", vars_to_plot, default=vars_to_plot[:5])
    
    if not selected_vars:
        st.info("Select at least one variable to see charts.")
    else:
        for var in selected_vars:
            st.markdown(f"### {var}")
            
            data = df[var].dropna()
            if len(data) == 0:
                st.warning(f"No data available for {var}.")
                continue
            
            cat = categories.get(var, "continuous")
            
            # Left column: text summary, right column: chart
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                with st.container():
                    if cat == "continuous":
                        # Compute summary stats and normality
                        mean = data.mean()
                        median = data.median()
                        std = data.std()
                        skewness = data.skew()
                        kurtosis = data.kurtosis()
                        
                        # Shapiro-Wilk test (only if n <= 5000, otherwise skip)
                        if len(data) <= 5000:
                            shapiro_stat, shapiro_p = stats.shapiro(data)
                            normal_msg = "Distribution is **normal**" if shapiro_p > 0.05 else "Distribution is **non-normal** (skewed)"
                            p_text = f"Shapiro-Wilk p = {shapiro_p:.4f}"
                        else:
                            normal_msg = "Normality test not performed (n > 5000)"
                            p_text = "Use graphical assessment"
                        
                        st.markdown(f"""
                        **Summary Statistics**  
                        - Mean: {mean:.3f}  
                        - Median: {median:.3f}  
                        - Std Dev: {std:.3f}  
                        - Skewness: {skewness:.3f}  
                        - Kurtosis: {kurtosis:.3f}  
                        
                        **Normality**  
                        {normal_msg}  
                        {p_text}
                        """)
                    
                    else:  # categorical
                        # For categorical, show frequency table
                        freq = data.value_counts()
                        st.markdown("**Frequency Table**")
                        st.dataframe(freq.reset_index().rename(columns={freq.index.name: var, var: "Count"}), use_container_width=True)
            
            with col_right:
                # Generate appropriate chart
                if cat == "continuous":
                    fig = create_histogram_with_kde(data, var)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Also show boxplot as a separate chart?
                    # We'll add a small boxplot below the histogram for better insight
                    fig_box = create_boxplot(data, var)
                    st.plotly_chart(fig_box, use_container_width=True)
                    
                else:
                    # Categorical: decide chart type based on number of categories
                    n_categories = len(data.unique())
                    if n_categories == 2:
                        fig = create_pie_chart(data, var)
                    elif 3 <= n_categories <= 5:
                        fig = create_bar_chart(data, var, orientation='v')
                    else:
                        fig = create_bar_chart(data, var, orientation='h')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Download button
                img_bytes = fig.to_image(format="png")
                st.download_button(
                    label="Download as PNG",
                    data=img_bytes,
                    file_name=f"{var}_distribution.png",
                    mime="image/png"
                )
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.page = 3
            st.rerun()
    with col2:
        if st.button("Proceed to Numerical Summary ➡️", use_container_width=True):
            st.session_state.page = 5
            st.rerun()