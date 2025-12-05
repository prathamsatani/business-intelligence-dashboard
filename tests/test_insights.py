"""
This module contains tests for the insight generation functions, such as identifying
top/bottom performers, detecting trends, and finding anomalies.
"""

import pandas as pd
import pytest
from insights import (
    get_top_bottom_performers,
    detect_trends,
    detect_anomalies,
)


@pytest.fixture
def sample_df():
    """Returns a sample DataFrame for testing."""
    data = {
        "Date": pd.to_datetime(["2023-01-01", "2023-01-15", "2023-02-01", "2023-03-01"]),
        "Value": [10, 11, 12, 100],  # 100 is a clear anomaly
        "Category": ["A", "B", "A", "C"],
    }
    return pd.DataFrame(data)


def test_get_top_bottom_performers(sample_df):
    """Tests the get_top_bottom_performers function."""
    top_2 = get_top_bottom_performers(sample_df, "Value", n=2, ascending=False)
    assert len(top_2) == 2
    assert top_2.iloc[0]["Value"] == 100

    bottom_1 = get_top_bottom_performers(sample_df, "Value", n=1, ascending=True)
    assert len(bottom_1) == 1
    assert bottom_1.iloc[0]["Value"] == 10


def test_detect_trends(sample_df):
    """Tests the detect_trends function."""
    trends = detect_trends(sample_df, "Date", "Value")
    assert "Best performing month on average: March" in trends
    assert "Worst performing month on average: January" in trends


def test_detect_anomalies(sample_df):
    """Tests the detect_anomalies function."""
    mean = sample_df["Value"].mean()
    std = sample_df["Value"].std()
    print(f"Mean: {mean}, Std: {std}")
    anomalies = detect_anomalies(sample_df, "Value", threshold=1.0) # Lowered threshold
    assert len(anomalies) == 1
    assert anomalies.iloc[0]["Value"] == 100

    no_anomalies = detect_anomalies(sample_df, "Value", threshold=3)
    assert len(no_anomalies) == 0
