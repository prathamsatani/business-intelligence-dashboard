"""
This module provides functions for creating various types of plots using Plotly Express.
"""

import plotly.express as px
import pandas as pd

def create_time_series_plot(df, date_col, value_col, color_col=None):
    """Create a time series plot with optional color grouping."""
    if df is None or date_col is None or value_col is None:
        return None
    
    if color_col and color_col in df.columns:
        fig = px.line(
            df, 
            x=date_col, 
            y=value_col, 
            color=color_col,
            title=f"{value_col} over {date_col} (by {color_col})"
        )
    else:
        fig = px.line(
            df, 
            x=date_col, 
            y=value_col,
            title=f"{value_col} over {date_col}"
        )
    
    fig.update_layout(
        xaxis_title=date_col,
        yaxis_title=value_col,
        legend_title=color_col if color_col else None
    )
    
    return fig

def create_distribution_plot(df, col):
    """
    Creates a distribution plot (histogram).

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        col (str): The name of the column to visualize.

    Returns:
        plotly.graph_objects.Figure: The generated distribution plot.
    """
    fig = px.histogram(df, x=col, title=f'Distribution of {col}')
    return fig

def create_bar_chart(df, cat_col, num_col, agg_func):
    """
    Creates a bar chart with aggregation.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        cat_col (str): The name of the categorical column for the x-axis.
        num_col (str): The name of the numerical column for the y-axis.
        agg_func (str): The aggregation function to apply ('sum', 'mean', 'count', 'median').

    Returns:
        plotly.graph_objects.Figure: The generated bar chart.
    """
    agg_map = {'sum': pd.Series.sum, 'mean': pd.Series.mean, 'count': pd.Series.count, 'median': pd.Series.median}
    agg_df = df.groupby(cat_col)[num_col].agg(agg_map[agg_func]).reset_index()
    fig = px.bar(agg_df, x=cat_col, y=num_col, title=f'{agg_func.capitalize()} of {num_col} by {cat_col}')
    return fig

def create_scatter_plot(df, x_col, y_col, color_col=None):
    """Create a scatter plot with optional color grouping."""
    if df is None or x_col is None or y_col is None:
        return None
    
    if color_col and color_col in df.columns:
        fig = px.scatter(
            df, 
            x=x_col, 
            y=y_col, 
            color=color_col,
            title=f"{y_col} vs {x_col} (by {color_col})"
        )
    else:
        fig = px.scatter(
            df, 
            x=x_col, 
            y=y_col,
            title=f"{y_col} vs {x_col}"
        )
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        legend_title=color_col if color_col else None
    )
    
    return fig