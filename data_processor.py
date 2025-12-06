"""
This module provides functions for data processing, including downloading stock data,
loading data from files, and calculating summary statistics.
"""

import yfinance as yf
import pandas as pd
import os

def download_stock_data(
    ticker: str, 
    start_date: str, 
    end_date: str, 
    filepath: str
) -> None:
    """
    Downloads stock data from Yahoo Finance and saves it to a CSV file.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
        filepath (str): The path to save the CSV file.
    Returns:
        None
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        data.to_csv(filepath)
        print(f"Successfully downloaded data for {ticker} to {filepath}")
    except Exception as e:
        print(f"Failed to download data for {ticker}: {e}")

def get_sample_files():
    """
    Get list of sample CSV/Excel files from data/ directory.
    Assumes files are stored in 'data/' directory.
    Returns:
        list: A list of sample file names.
    """
    data_dir = "data"
    if not os.path.exists(data_dir):
        return []
    
    files = []
    for f in os.listdir(data_dir):
        if f.endswith(('.csv', '.xlsx', '.xls')):
            files.append(f)
    return sorted(files)

def load_data(file:str):
    """
    Loads data from a CSV or Excel file and returns a pandas DataFrame.

    Args:
        file (str): The path to the uploaded file.

    Returns:
        pandas.DataFrame: The loaded data.
    """
    try:
        if file.endswith('.csv'):
            df = pd.read_csv(file)    
        elif file.endswith(('.xls', '.xlsx')):
            df_xlsx = pd.read_excel(file)
            df = df_xlsx.to_csv(index=False)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
        unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
        if unnamed_cols:
            df = df.drop(columns=unnamed_cols)
            
        return df
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def get_summary_statistics(df:pd.DataFrame) -> pd.DataFrame:
    """
    Returns summary statistics for numerical columns.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.DataFrame: Summary statistics for numerical columns.
    """
    return df.describe()

def get_categorical_summary(df:pd.DataFrame) -> dict:
    """
    Returns a summary for categorical columns.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        dict: A dictionary containing unique values, value counts, and mode for each categorical column.
    """
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    summary = {}
    for col in categorical_cols:
        summary[col] = {
            'unique_values': df[col].nunique(),
            'value_counts': df[col].value_counts().to_dict(),
            'mode': df[col].mode().iloc[0]
        }
    return summary

def get_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Returns a report of missing values.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A series containing the count of missing values for each column.
    """
    return df.isnull().sum()

def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the correlation matrix for numerical features.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.DataFrame: The correlation matrix.
    """
    numerical_cols = df.select_dtypes(include=['number']).columns
    return df[numerical_cols].corr()

def filter_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Filters the DataFrame based on the provided filter criteria.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        filters (dict): A dictionary of filters to apply.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    if not filters:
        return df

    filtered_df = df.copy()
    for col, value in filters.items():
        if isinstance(value, list):
            if pd.api.types.is_datetime64_any_dtype(filtered_df[col]):
                filtered_df = filtered_df[filtered_df[col].between(pd.to_datetime(value[0]), pd.to_datetime(value[1]))]
            else:
                filtered_df = filtered_df[filtered_df[col].isin(value)]
        elif isinstance(value, tuple):
            filtered_df = filtered_df[filtered_df[col].between(value[0], value[1])]
    return filtered_df

if __name__ == '__main__':
    # Create the data directory if it doesn't exist
    if not os.path.exists('project/data'):
        os.makedirs('project/data')

    # Download data for AAPL and GOOG
    # download_stock_data('AAPL', '2020-01-01', '2023-12-31', 'project/data/sample1.csv')
    # download_stock_data('GOOG', '2020-01-01', '2023-12-31', 'project/data/sample2.csv')
