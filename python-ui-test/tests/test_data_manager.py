"""
Unit tests for DataManager class.

Tests the singleton pattern, data loading, clearing, and signal emissions.
"""

import pytest
import pandas as pd
from core.data_manager import DataManager


class TestDataManager:
    """Test suite for DataManager singleton class."""

    def test_singleton_pattern(self):
        """Test that DataManager follows singleton pattern."""
        dm1 = DataManager()
        dm2 = DataManager()
        assert dm1 is dm2, "DataManager should be a singleton"

    def test_set_data(self):
        """Test setting data in DataManager."""
        dm = DataManager()
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

        dm.set_data(df, 'test.csv')

        assert dm.has_data(), "DataManager should have data after set_data"
        assert dm.filename == 'test.csv', "Filename should be set correctly"

        retrieved_df = dm.get_data()
        assert retrieved_df is not None, "get_data should return DataFrame"
        assert len(retrieved_df) == 3, "DataFrame should have 3 rows"
        assert len(retrieved_df.columns) == 2, "DataFrame should have 2 columns"

    def test_clear_data(self):
        """Test clearing data from DataManager."""
        dm = DataManager()
        df = pd.DataFrame({'A': [1, 2, 3]})
        dm.set_data(df, 'test.csv')

        dm.clear_data()

        assert not dm.has_data(), "DataManager should not have data after clear"
        assert dm.filename is None, "Filename should be None after clear"

    def test_get_data_when_empty(self):
        """Test get_data returns None when no data loaded."""
        dm = DataManager()
        dm.clear_data()  # Ensure empty

        result = dm.get_data()
        assert result is None, "get_data should return None when empty"

    def test_data_independence(self):
        """Test that DataManager stores a copy of data."""
        dm = DataManager()
        original_df = pd.DataFrame({'A': [1, 2, 3]})

        dm.set_data(original_df, 'test.csv')

        # Modify original
        original_df.loc[0, 'A'] = 999

        # Retrieved data should not be affected
        retrieved_df = dm.get_data()
        assert retrieved_df.loc[0, 'A'] == 1, "DataManager should store a copy"

    def test_signals_emitted(self, qtbot):
        """Test that DataManager emits signals correctly."""
        dm = DataManager()
        df = pd.DataFrame({'A': [1, 2, 3]})

        # Test dataLoaded signal
        with qtbot.waitSignal(dm.dataLoaded, timeout=1000):
            dm.set_data(df, 'test.csv')

        # Test dataCleared signal
        with qtbot.waitSignal(dm.dataCleared, timeout=1000):
            dm.clear_data()

    def test_has_data(self):
        """Test has_data method."""
        dm = DataManager()
        dm.clear_data()

        assert not dm.has_data(), "has_data should return False when empty"

        df = pd.DataFrame({'A': [1]})
        dm.set_data(df)

        assert dm.has_data(), "has_data should return True when data loaded"

    def test_empty_dataframe(self):
        """Test loading empty DataFrame."""
        dm = DataManager()
        empty_df = pd.DataFrame()

        dm.set_data(empty_df, 'empty.csv')

        # DataManager should handle empty DataFrames
        assert dm.has_data(), "Empty DataFrame is still considered as 'having data'"
        retrieved = dm.get_data()
        assert retrieved is not None, "Should return empty DataFrame"
        assert len(retrieved) == 0, "Should be empty"

    def test_large_dataframe(self):
        """Test DataManager with large DataFrame."""
        dm = DataManager()
        # Create 10k row DataFrame
        large_df = pd.DataFrame({
            'A': range(10000),
            'B': range(10000, 20000)
        })

        dm.set_data(large_df, 'large.csv')

        assert dm.has_data(), "Should handle large DataFrames"
        retrieved = dm.get_data()
        assert len(retrieved) == 10000, "Should preserve all rows"
