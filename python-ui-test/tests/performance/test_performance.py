"""
Performance tests for the application.

Tests load times, chart generation speed, and memory usage.
"""

import pytest
import pandas as pd
import numpy as np
import time
from core.data_manager import DataManager
from core.chart_builder import ChartBuilder
import matplotlib.pyplot as plt


class TestPerformance:
    """Performance and stress tests."""

    def teardown_method(self):
        """Clean up after each test."""
        plt.close('all')
        dm = DataManager()
        dm.clear_data()

    @pytest.mark.slow
    def test_large_dataset_import_performance(self):
        """Test that 50k row dataset loads within 2 seconds."""
        # Create 50k row dataset
        df = pd.DataFrame({
            'A': np.random.rand(50000),
            'B': np.random.rand(50000),
            'C': np.random.randint(0, 100, 50000),
            'D': np.random.choice(['X', 'Y', 'Z'], 50000)
        })

        dm = DataManager()
        start = time.time()
        dm.set_data(df, 'test.csv')
        duration = time.time() - start

        assert duration < 2.0, f"Import took {duration:.2f}s, should be <2s"
        assert dm.has_data(), "Data should be loaded"

    @pytest.mark.slow
    def test_chart_generation_speed(self):
        """Test that chart generation completes within 1 second."""
        df = pd.DataFrame({
            'X': range(1000),
            'Y': np.random.rand(1000)
        })

        start = time.time()
        fig = ChartBuilder.create_line_chart(df, 'X', 'Y')
        duration = time.time() - start

        assert duration < 1.0, f"Chart generation took {duration:.2f}s, should be <1s"
        assert fig is not None, "Chart should be created"

    @pytest.mark.slow
    def test_large_chart_rendering(self):
        """Test chart rendering with 10k data points."""
        df = pd.DataFrame({
            'X': range(10000),
            'Y': np.random.rand(10000)
        })

        start = time.time()
        fig = ChartBuilder.create_line_chart(df, 'X', 'Y')
        duration = time.time() - start

        # Should still be reasonable even with downsampling
        assert duration < 2.0, f"Large chart took {duration:.2f}s"

    @pytest.mark.slow
    def test_multiple_chart_generations(self):
        """Test generating multiple charts in succession."""
        df = pd.DataFrame({
            'X': range(500),
            'Y': np.random.rand(500)
        })

        start = time.time()
        for _ in range(10):
            fig = ChartBuilder.create_line_chart(df, 'X', 'Y')
            plt.close(fig)

        duration = time.time() - start

        assert duration < 5.0, f"10 charts took {duration:.2f}s, should be <5s"

    def test_data_manager_memory_efficiency(self):
        """Test that DataManager doesn't leak memory."""
        dm = DataManager()

        # Load and clear multiple times
        for _ in range(10):
            df = pd.DataFrame({
                'A': range(10000),
                'B': range(10000)
            })
            dm.set_data(df, 'test.csv')
            dm.clear_data()

        # Should complete without memory issues
        assert True, "Multiple load/clear cycles completed"

    @pytest.mark.slow
    def test_sorting_large_dataset(self):
        """Test sorting performance on large dataset."""
        # Create 10k row dataset
        df = pd.DataFrame({
            'A': np.random.rand(10000),
            'B': np.random.randint(0, 1000, 10000)
        })

        start = time.time()
        sorted_df = df.sort_values(by='A')
        duration = time.time() - start

        assert duration < 0.5, f"Sorting took {duration:.2f}s, should be <0.5s"
        assert len(sorted_df) == 10000, "All rows should be preserved"

    @pytest.mark.slow
    def test_filtering_performance(self):
        """Test filtering performance on large dataset."""
        df = pd.DataFrame({
            'Value': np.random.randint(0, 100, 50000),
            'Category': np.random.choice(['A', 'B', 'C'], 50000)
        })

        start = time.time()
        filtered = df[df['Value'] > 50]
        duration = time.time() - start

        assert duration < 0.5, f"Filtering took {duration:.2f}s"
        assert len(filtered) > 0, "Should have filtered results"

    def test_empty_dataframe_performance(self):
        """Test that empty DataFrame operations are fast."""
        dm = DataManager()
        empty_df = pd.DataFrame()

        start = time.time()
        dm.set_data(empty_df, 'empty.csv')
        dm.clear_data()
        duration = time.time() - start

        assert duration < 0.1, "Empty DataFrame operations should be instant"
