"""
This module contains tests for the visualization functions, ensuring that plots
are created correctly using Plotly Express.
"""

import pandas as pd
import pytest
from visualizations import (
    create_time_series_plot,
    create_distribution_plot,
    create_bar_chart,
    create_scatter_plot,
)
import plotly.graph_objects as go


@pytest.fixture
def sample_df():
    """Returns a sample DataFrame for testing."""
    data = {
        "Date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03", "2023-02-01"]),
        "Category": ["A", "B", "A", "C"],
        "Value": [10, 20, 10, 30],
        "Value2": [1, 2, 1, 3],
    }
    return pd.DataFrame(data)


def test_create_time_series_plot(sample_df):
    """Tests the create_time_series_plot function."""
    fig = create_time_series_plot(sample_df, "Date", "Value")
    assert isinstance(fig, go.Figure)


def test_create_distribution_plot(sample_df):
    """Tests the create_distribution_plot function."""
    fig = create_distribution_plot(sample_df, "Value")
    assert isinstance(fig, go.Figure)


@pytest.mark.parametrize("agg_func", ["sum", "mean", "count", "median"])
def test_create_bar_chart(sample_df, agg_func):
    """Tests the create_bar_chart function with all aggregation methods."""
    fig = create_bar_chart(sample_df, "Category", "Value", agg_func)
    assert isinstance(fig, go.Figure)


def test_create_scatter_plot(sample_df):
    """Tests the create_scatter_plot function."""
    fig = create_scatter_plot(sample_df, "Value", "Value2")
    assert isinstance(fig, go.Figure)
