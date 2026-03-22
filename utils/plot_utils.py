import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_histogram_with_kde(data, title):
    """Create histogram with KDE overlay."""
    fig = px.histogram(data, nbins=30, marginal="violin", title=f"Distribution of {title}")
    fig.update_layout(barmode='overlay')
    return fig

def create_boxplot(data, title):
    """Create boxplot."""
    fig = px.box(data, y=data, title=f"Boxplot of {title}")
    return fig

def create_pie_chart(data, title):
    """Create pie chart for categorical data."""
    fig = px.pie(data, names=data, title=f"Distribution of {title}")
    return fig

def create_bar_chart(data, title, orientation='v'):
    """Create bar chart for categorical data."""
    freq = data.value_counts().reset_index()
    freq.columns = [title, "Count"]
    if orientation == 'v':
        fig = px.bar(freq, x=title, y="Count", title=f"Distribution of {title}")
    else:
        fig = px.bar(freq, y=title, x="Count", orientation='h', title=f"Distribution of {title}")
    return fig