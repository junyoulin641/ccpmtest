"""
Unit tests for ChartBuilder class.

Tests chart generation for different types (line, bar, scatter, pie).
"""

import pytest
import pandas as pd
import matplotlib.pyplot as plt
from core.chart_builder import ChartBuilder


class TestChartBuilder:
    """Test suite for ChartBuilder chart generation."""

    def teardown_method(self):
        """Clean up matplotlib figures after each test."""
        plt.close('all')

    def test_create_line_chart(self):
        """Test creating a line chart."""
        df = pd.DataFrame({
            'X': [1, 2, 3, 4, 5],
            'Y': [2, 4, 6, 8, 10]
        })

        fig = ChartBuilder.create_line_chart(df, 'X', 'Y')

        assert fig is not None, "Should return a Figure object"
        assert len(fig.axes) == 1, "Should have one axis"

        ax = fig.axes[0]
        assert ax.get_xlabel() == 'X', "X-axis label should match column name"
        assert ax.get_ylabel() == 'Y', "Y-axis label should match column name"

    def test_create_bar_chart(self):
        """Test creating a bar chart."""
        df = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Value': [10, 20, 15, 25]
        })

        fig = ChartBuilder.create_bar_chart(df, 'Category', 'Value')

        assert fig is not None, "Should return a Figure object"
        assert len(fig.axes) == 1, "Should have one axis"

    def test_create_scatter_chart(self):
        """Test creating a scatter chart."""
        df = pd.DataFrame({
            'X': [1, 2, 3, 4, 5],
            'Y': [2, 4, 3, 7, 6]
        })

        fig = ChartBuilder.create_scatter_chart(df, 'X', 'Y')

        assert fig is not None, "Should return a Figure object"
        assert len(fig.axes) == 1, "Should have one axis"

    def test_create_pie_chart(self):
        """Test creating a pie chart."""
        df = pd.DataFrame({
            'Category': ['A', 'B', 'C'],
            'Value': [30, 40, 30]
        })

        fig = ChartBuilder.create_pie_chart(df, 'Category', 'Value')

        assert fig is not None, "Should return a Figure object"
        assert len(fig.axes) == 1, "Should have one axis"

    def test_chart_with_custom_title(self):
        """Test chart creation with custom title."""
        df = pd.DataFrame({'X': [1, 2, 3], 'Y': [1, 2, 3]})

        fig = ChartBuilder.create_line_chart(df, 'X', 'Y', title='Custom Title')

        ax = fig.axes[0]
        assert ax.get_title() == 'Custom Title', "Should set custom title"

    def test_chart_with_custom_color(self):
        """Test chart creation with custom color."""
        df = pd.DataFrame({'X': [1, 2, 3], 'Y': [1, 2, 3]})

        fig = ChartBuilder.create_line_chart(df, 'X', 'Y', color='red')

        assert fig is not None, "Should handle custom colors"
        # Note: Actual color verification would require inspecting line properties

    def test_validate_chart_data_valid(self):
        """Test data validation for valid data."""
        df = pd.DataFrame({'X': [1, 2, 3], 'Y': [4, 5, 6]})

        is_valid, error_msg = ChartBuilder.validate_chart_data(df, 'Line', 'X', 'Y')

        assert is_valid, "Valid data should pass validation"
        assert error_msg == "", "Should have no error message"

    def test_validate_chart_data_missing_column(self):
        """Test data validation with missing column."""
        df = pd.DataFrame({'X': [1, 2, 3], 'Y': [4, 5, 6]})

        is_valid, error_msg = ChartBuilder.validate_chart_data(df, 'Line', 'Z', 'Y')

        assert not is_valid, "Should fail validation for missing column"
        assert 'Z' in error_msg, "Error message should mention missing column"

    def test_validate_chart_data_non_numeric(self):
        """Test data validation with non-numeric Y column for line chart."""
        df = pd.DataFrame({'X': [1, 2, 3], 'Y': ['a', 'b', 'c']})

        is_valid, error_msg = ChartBuilder.validate_chart_data(df, 'Line', 'X', 'Y')

        assert not is_valid, "Should fail validation for non-numeric Y"
        assert 'numeric' in error_msg.lower(), "Error should mention numeric requirement"

    def test_empty_dataframe(self):
        """Test chart creation with empty DataFrame."""
        empty_df = pd.DataFrame()

        with pytest.raises(Exception):
            ChartBuilder.create_line_chart(empty_df, 'X', 'Y')

    def test_large_dataset_downsampling(self):
        """Test that large datasets are handled efficiently."""
        # Create large dataset
        large_df = pd.DataFrame({
            'X': range(50000),
            'Y': range(50000)
        })

        fig = ChartBuilder.create_line_chart(large_df, 'X', 'Y')

        assert fig is not None, "Should handle large datasets"
        # ChartBuilder should implement downsampling for performance

    def test_chart_with_nan_values(self):
        """Test chart creation with NaN values in data."""
        df = pd.DataFrame({
            'X': [1, 2, 3, 4, 5],
            'Y': [1, None, 3, None, 5]
        })

        # Should handle NaN values gracefully
        fig = ChartBuilder.create_line_chart(df, 'X', 'Y')

        assert fig is not None, "Should handle NaN values"

    def test_bar_chart_aggregation(self):
        """Test bar chart with duplicate categories (should aggregate)."""
        df = pd.DataFrame({
            'Category': ['A', 'B', 'A', 'B'],
            'Value': [10, 20, 15, 25]
        })

        fig = ChartBuilder.create_bar_chart(df, 'Category', 'Value')

        assert fig is not None, "Should handle duplicate categories"
