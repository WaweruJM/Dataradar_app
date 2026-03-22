import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score, confusion_matrix
from utils.data_utils import classify_columns

def show():
    df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    if df is None:
        st.warning("No dataset found. Please upload a file first.")
        if st.button("Go to Upload"):
            st.session_state.page = 1
            st.rerun()
        st.stop()
    
    if not st.session_state.column_categories:
        st.session_state.column_categories = classify_columns(df)
    categories = st.session_state.column_categories
    
    st.markdown("<h3 style='text-align:center;'>📊 Statistical Tests & Modelling</h3>", unsafe_allow_html=True)
    
    # ----------------------------
    # Section 1: Two-Variable Tests
    # ----------------------------
    with st.container():
        st.subheader("🔍 Two-Variable Analysis")
        cols = df.columns.tolist()
        var1 = st.selectbox("Select Variable 1", cols, key="two_var1")
        var2 = st.selectbox("Select Variable 2", cols, key="two_var2")
        
        if st.button("Run Test", key="run_two"):
            with st.spinner("Performing test..."):
                x = df[var1].dropna()
                y = df[var2].dropna()
                
                # Determine test based on variable types
                cat1 = categories.get(var1)
                cat2 = categories.get(var2)
                
                result = ""
                p_value = None
                
                try:
                    if cat1 == "continuous" and cat2 == "continuous":
                        # Pearson or Spearman? Check normality
                        # For simplicity, use Pearson
                        corr, p = stats.pearsonr(x, y)
                        result = f"Pearson correlation: r = {corr:.3f}, p = {p:.4f}"
                        p_value = p
                    elif cat1 == "continuous" and cat2 != "continuous":
                        # Continuous vs Categorical: t-test / Mann-Whitney
                        groups = y.unique()
                        if len(groups) == 2:
                            # Two groups: t-test or Mann-Whitney
                            group0 = x[y == groups[0]]
                            group1 = x[y == groups[1]]
                            # Check normality for each group
                            if len(group0) > 3 and len(group1) > 3:
                                # Use t-test if both groups normal? We'll use Mann-Whitney as default
                                stat, p = stats.mannwhitneyu(group0, group1)
                                result = f"Mann-Whitney U: stat = {stat:.3f}, p = {p:.4f}"
                            else:
                                stat, p = stats.ttest_ind(group0, group1)
                                result = f"Independent t-test: t = {stat:.3f}, p = {p:.4f}"
                        else:
                            # More than 2 groups: ANOVA or Kruskal-Wallis
                            # For simplicity, use Kruskal-Wallis
                            groups_data = [x[y == g] for g in groups]
                            stat, p = stats.kruskal(*groups_data)
                            result = f"Kruskal-Wallis H-test: H = {stat:.3f}, p = {p:.4f}"
                        p_value = p
                    elif cat1 != "continuous" and cat2 != "continuous":
                        # Both categorical: Chi-square
                        contingency = pd.crosstab(df[var1], df[var2])
                        chi2, p, dof, expected = stats.chi2_contingency(contingency)
                        result = f"Chi-square test: χ² = {chi2:.3f}, df = {dof}, p = {p:.4f}"
                        p_value = p
                    else:
                        result = "Test type not supported for this combination."
                    
                    st.write(result)
                    if p_value is not None:
                        if p_value < 0.05:
                            st.success("Result: Statistically significant (p < 0.05)")
                        else:
                            st.info("Result: Not statistically significant (p ≥ 0.05)")
                except Exception as e:
                    st.error(f"Error performing test: {e}")
    
    # ----------------------------
    # Section 2: Multi-Variable (optional)
    # ----------------------------
    with st.expander("📐 Three or More Variables (ANOVA / MANOVA)"):
        st.write("Select one dependent variable and multiple independent variables.")
        dependent = st.selectbox("Dependent Variable", cols, key="multi_dep")
        independents = st.multiselect("Independent Variables", cols, key="multi_indep")
        if st.button("Run ANOVA", key="run_multi"):
            if len(independents) == 0:
                st.warning("Select at least one independent variable.")
            else:
                # For simplicity, we'll run a simple ANOVA using statsmodels
                # Combine independent variables into a formula
                formula = f"{dependent} ~ " + " + ".join(independents)
                try:
                    model = sm.formula.ols(formula, data=df).fit()
                    anova_table = sm.stats.anova_lm(model, typ=2)
                    st.dataframe(anova_table)
                    st.write("ANOVA Results (Type II)")
                except Exception as e:
                    st.error(f"Error in ANOVA: {e}")
    
    # ----------------------------
    # Section 3: Predictive Modelling
    # ----------------------------
    with st.expander("🤖 Predictive Modelling"):
        st.write("Build regression models to predict an outcome variable.")
        target = st.selectbox("Target Variable", cols, key="model_target")
        predictors = st.multiselect("Predictor Variables", cols, key="model_predictors")
        model_type = st.selectbox("Model Type", ["Linear Regression", "Logistic Regression"], key="model_type")
        
        if st.button("Train Model", key="run_model"):
            if not predictors:
                st.warning("Select at least one predictor.")
            else:
                with st.spinner("Training model..."):
                    X = df[predictors].dropna()
                    y = df[target].loc[X.index]
                    # Handle categorical predictors (one-hot encode)
                    X = pd.get_dummies(X, drop_first=True)
                    
                    # Train/test split
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    
                    if model_type == "Linear Regression":
                        model = LinearRegression()
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        r2 = r2_score(y_test, y_pred)
                        st.write(f"R² Score: {r2:.3f}")
                        st.write("Coefficients:")
                        coef_df = pd.DataFrame({"Feature": X.columns, "Coefficient": model.coef_})
                        st.dataframe(coef_df)
                    else:  # Logistic Regression
                        # Ensure target is binary
                        if len(y.unique()) != 2:
                            st.error("Logistic regression requires a binary target variable.")
                        else:
                            model = LogisticRegression(max_iter=1000)
                            model.fit(X_train, y_train)
                            y_pred = model.predict(X_test)
                            acc = accuracy_score(y_test, y_pred)
                            st.write(f"Accuracy: {acc:.3f}")
                            st.write("Confusion Matrix:")
                            cm = confusion_matrix(y_test, y_pred)
                            st.dataframe(pd.DataFrame(cm))
                            st.write("Coefficients:")
                            coef_df = pd.DataFrame({"Feature": X.columns, "Coefficient": model.coef_[0]})
                            st.dataframe(coef_df)
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.page = 5
            st.rerun()
    with col2:
        if st.button("Proceed to Documentation ➡️", use_container_width=True):
            st.session_state.page = 7
            st.rerun()