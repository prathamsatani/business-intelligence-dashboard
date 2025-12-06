"""
This module provides functions for generating insights from data, such as identifying
top/bottom performers, detecting trends, and finding anomalies.
"""

import pandas as pd

def get_top_bottom_performers(
    df: pd.DataFrame, 
    column: str, 
    n: int = 5, 
    ascending: bool = False
) -> pd.DataFrame:
    """
    Identifies the top or bottom N performers in a given column.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column (str): The column to evaluate.
        n (int): The number of performers to return.
        ascending (bool): Whether to sort in ascending order (for bottom performers).

    Returns:
        pd.DataFrame: A DataFrame with the top/bottom performers.
    """
    return df.sort_values(by=column, ascending=ascending).head(n)

def detect_trends(
    df: pd.DataFrame, 
    date_col: str, 
    value_col: str
) -> str:
    """
    Detects basic seasonal trends in time series data.
    For stock data, this might show the average performance by month.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        date_col (str): The name of the date column.
        value_col (str): The name of the value column.

    Returns:
        str: A string describing the best and worst performing months on average.
    """
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])
    
    df['month'] = df[date_col].dt.month_name()
    monthly_avg = df.groupby('month')[value_col].mean().sort_values(ascending=False)
    return f"Best performing month on average: {monthly_avg.index[0]} with an average of {monthly_avg.iloc[0]:.2f}\\n" \
           f"Worst performing month on average: {monthly_avg.index[-1]} with an average of {monthly_avg.iloc[-1]:.2f}"

def detect_anomalies(
    df: pd.DataFrame, 
    value_col: str, 
    threshold: float = 2
) -> pd.DataFrame:
    """
    Detects anomalies (outliers) in a numerical column based on standard deviation.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        value_col (str): The name of the value column.
        threshold (float): The number of standard deviations to use as a threshold.

    Returns:
        pd.DataFrame: A DataFrame containing the anomalous rows.
    """
    mean = df[value_col].mean()
    std = df[value_col].std()
    anomalies = df[(df[value_col] > mean + threshold * std) | (df[value_col] < mean - threshold * std)]
    return anomalies
