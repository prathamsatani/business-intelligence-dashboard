"""
This module contains tests for the data processing functions, including data loading,
summary statistics calculation, and data filtering.
"""

import pandas as pd
import pytest
from data_processor import (
    load_data,
    get_summary_statistics,
    get_categorical_summary,
    get_missing_values,
    get_correlation_matrix,
    filter_data,
)
import os


@pytest.fixture
def sample_df():
    """Returns a sample DataFrame for testing."""
    data = {
        "Date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03", "2023-02-01"]),
        "Category": ["A", "B", "A", "C"],
        "Value": [10, 20, 10, 30],
        "Value2": [1, 2, 1, 3],
        "WithNaN": [1, None, 3, 4]
    }
    return pd.DataFrame(data)


def test_load_data():
    """Tests the load_data function."""
    # Create a dummy CSV file
    dummy_data = "col1,col2\n1,2\n3,4"
    with open("dummy.csv", "w") as f:
        f.write(dummy_data)

    # Create a mock file object to pass to load_data
    class MockFile:
        def __init__(self, name):
            self.name = name
    
    mock_file = MockFile("dummy.csv")
    df = load_data(mock_file)
    print(df)
    assert df.shape == (2, 2)
    assert "col1" in df.columns
    os.remove("dummy.csv")


def test_get_summary_statistics(sample_df):
    """Tests the get_summary_statistics function."""
    summary = get_summary_statistics(sample_df.drop(columns=['Date']))
    assert summary.loc["mean", "Value"] == 17.5
    assert summary.shape[1] == 3


def test_get_categorical_summary(sample_df):
    """Tests the get_categorical_summary function."""
    summary = get_categorical_summary(sample_df)
    assert "Category" in summary
    assert summary["Category"]["unique_values"] == 3
    assert summary["Category"]["mode"] == "A"


def test_get_missing_values(sample_df):
    """Tests the get_missing_values function."""
    missing = get_missing_values(sample_df)
    assert missing["WithNaN"] == 1
    assert missing["Value"] == 0


def test_get_correlation_matrix(sample_df):
    """Tests the get_correlation_matrix function."""
    corr = get_correlation_matrix(sample_df)
    assert corr.loc["Value", "Value2"] == pytest.approx(1.0)


def test_filter_data_numerical(sample_df):
    """Tests numerical filtering."""
    filters = {"Value": (15, 25)}
    filtered_df = filter_data(sample_df, filters)
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]["Value"] == 20


def test_filter_data_categorical(sample_df):
    """Tests categorical filtering."""
    filters = {"Category": ["A", "C"]}
    filtered_df = filter_data(sample_df, filters)
    assert len(filtered_df) == 3
    assert "B" not in filtered_df["Category"].tolist()


def test_filter_data_date(sample_df):
    """Tests date range filtering."""
    filters = {"Date": ["2023-01-01", "2023-01-02"]}
    filtered_df = filter_data(sample_df, filters)
    assert len(filtered_df) == 2


def test_filter_data_combined(sample_df):
    """Tests combined filtering."""
    filters = {"Value": (5, 15), "Category": ["A"]}
    filtered_df = filter_data(sample_df, filters)
    assert len(filtered_df) == 2
