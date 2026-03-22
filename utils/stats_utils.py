import scipy.stats as stats
import pandas as pd

def normality_test(data, alpha=0.05):
    """Perform Shapiro-Wilk test and return result."""
    if len(data) < 3 or len(data) > 5000:
        return "Not computed (sample size outside range)"
    stat, p = stats.shapiro(data)
    result = f"Shapiro-Wilk: statistic={stat:.3f}, p={p:.4f}"
    if p < alpha:
        result += " → Not normally distributed"
    else:
        result += " → Normally distributed"
    return result