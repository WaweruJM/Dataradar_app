import pandas as pd
import numpy as np

def classify_columns(df):
    """
    Classify columns as 'continuous' or 'categorical'.
    Simple heuristic: numeric with more than 10 unique values => continuous,
    else categorical. For non-numeric, categorical.
    """
    categories = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            if df[col].nunique() > 10:
                categories[col] = "continuous"
            else:
                categories[col] = "categorical"  # could be binary or multinomial
        else:
            categories[col] = "categorical"
    return categories

def detect_binary_columns(df):
    """Return list of columns with exactly two unique values."""
    return [col for col in df.columns if df[col].nunique() == 2]