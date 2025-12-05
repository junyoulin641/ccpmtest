"""
DataManager module for managing application data state.

Implements a singleton pattern to maintain a single source of truth for all data
throughout the application lifecycle.
"""

import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal
from typing import Optional, Dict, Any


class DataManager(QObject):
    """
    Singleton class for managing application data.

    Provides centralized data storage and emits signals when data changes.
    All screens and components should access data through this manager.
    """

    # Singleton instance
    _instance = None

    # Signals
    dataLoaded = pyqtSignal(str)  # Emits filename when data is loaded
    dataCleared = pyqtSignal()  # Emits when data is cleared
    dataModified = pyqtSignal()  # Emits when data is modified
    errorOccurred = pyqtSignal(str)  # Emits error messages

    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the DataManager."""
        if self._initialized:
            return

        super().__init__()
        self._data: Optional[pd.DataFrame] = None
        self._filename: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
        self._initialized = True

    @property
    def data(self) -> Optional[pd.DataFrame]:
        """Get the current DataFrame."""
        return self._data

    @property
    def filename(self) -> Optional[str]:
        """Get the current filename."""
        return self._filename

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get metadata about the current dataset."""
        return self._metadata

    def has_data(self) -> bool:
        """Check if data is currently loaded."""
        return self._data is not None and not self._data.empty

    def set_data(self, df: pd.DataFrame, filename: str = None) -> None:
        """
        Set the current DataFrame.

        Args:
            df: The pandas DataFrame to store
            filename: Optional filename associated with this data
        """
        if df is None:
            self.errorOccurred.emit("Cannot set None as data")
            return

        self._data = df.copy()  # Create a copy to prevent external modifications
        self._filename = filename
        self._update_metadata()

        if filename:
            self.dataLoaded.emit(filename)
        else:
            self.dataModified.emit()

    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Get a copy of the current DataFrame.

        Returns:
            A copy of the DataFrame, or None if no data is loaded
        """
        if self._data is None:
            return None
        return self._data.copy()

    def clear_data(self) -> None:
        """Clear the current data."""
        self._data = None
        self._filename = None
        self._metadata = {}
        self.dataCleared.emit()

    def update_cell(self, row: int, column: str, value: Any) -> bool:
        """
        Update a single cell in the DataFrame.

        Args:
            row: Row index
            column: Column name
            value: New value

        Returns:
            True if successful, False otherwise
        """
        if not self.has_data():
            self.errorOccurred.emit("No data loaded")
            return False

        try:
            self._data.at[row, column] = value
            self.dataModified.emit()
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Failed to update cell: {str(e)}")
            return False

    def add_column(self, column_name: str, default_value: Any = None) -> bool:
        """
        Add a new column to the DataFrame.

        Args:
            column_name: Name of the new column
            default_value: Default value for all rows

        Returns:
            True if successful, False otherwise
        """
        if not self.has_data():
            self.errorOccurred.emit("No data loaded")
            return False

        if column_name in self._data.columns:
            self.errorOccurred.emit(f"Column '{column_name}' already exists")
            return False

        try:
            self._data[column_name] = default_value
            self._update_metadata()
            self.dataModified.emit()
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Failed to add column: {str(e)}")
            return False

    def delete_column(self, column_name: str) -> bool:
        """
        Delete a column from the DataFrame.

        Args:
            column_name: Name of the column to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.has_data():
            self.errorOccurred.emit("No data loaded")
            return False

        if column_name not in self._data.columns:
            self.errorOccurred.emit(f"Column '{column_name}' does not exist")
            return False

        try:
            self._data = self._data.drop(columns=[column_name])
            self._update_metadata()
            self.dataModified.emit()
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Failed to delete column: {str(e)}")
            return False

    def delete_rows(self, indices: list) -> bool:
        """
        Delete rows from the DataFrame.

        Args:
            indices: List of row indices to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.has_data():
            self.errorOccurred.emit("No data loaded")
            return False

        try:
            self._data = self._data.drop(indices)
            self._data = self._data.reset_index(drop=True)
            self._update_metadata()
            self.dataModified.emit()
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Failed to delete rows: {str(e)}")
            return False

    def filter_data(self, condition) -> Optional[pd.DataFrame]:
        """
        Filter the DataFrame based on a condition.

        Args:
            condition: Boolean condition for filtering

        Returns:
            Filtered DataFrame copy, or None if error
        """
        if not self.has_data():
            self.errorOccurred.emit("No data loaded")
            return None

        try:
            return self._data[condition].copy()
        except Exception as e:
            self.errorOccurred.emit(f"Failed to filter data: {str(e)}")
            return None

    def sort_data(self, by: str, ascending: bool = True) -> Optional[pd.DataFrame]:
        """
        Sort the DataFrame by a column.

        Args:
            by: Column name to sort by
            ascending: Sort order

        Returns:
            Sorted DataFrame copy, or None if error
        """
        if not self.has_data():
            self.errorOccurred.emit("No data loaded")
            return None

        try:
            return self._data.sort_values(by=by, ascending=ascending).copy()
        except Exception as e:
            self.errorOccurred.emit(f"Failed to sort data: {str(e)}")
            return None

    def get_statistics(self) -> Optional[Dict[str, Any]]:
        """
        Get basic statistics about the current dataset.

        Returns:
            Dictionary with statistics, or None if no data
        """
        if not self.has_data():
            return None

        return {
            'rows': len(self._data),
            'columns': len(self._data.columns),
            'numeric_columns': len(self._data.select_dtypes(include='number').columns),
            'memory_usage': self._data.memory_usage(deep=True).sum(),
            'column_names': list(self._data.columns),
            'dtypes': {col: str(dtype) for col, dtype in self._data.dtypes.items()}
        }

    def _update_metadata(self) -> None:
        """Update internal metadata about the dataset."""
        if not self.has_data():
            self._metadata = {}
            return

        self._metadata = {
            'rows': len(self._data),
            'columns': len(self._data.columns),
            'column_names': list(self._data.columns),
            'dtypes': {col: str(dtype) for col, dtype in self._data.dtypes.items()},
            'memory_usage_mb': self._data.memory_usage(deep=True).sum() / (1024 * 1024),
            'has_missing': self._data.isnull().any().any(),
            'missing_counts': self._data.isnull().sum().to_dict()
        }
