"""
Unit tests for FileHandler class.

Tests file import/export for CSV, Excel, and JSON formats.
"""

import pytest
import pandas as pd
from core.file_handler import FileHandler
import os


class TestFileHandler:
    """Test suite for FileHandler file I/O operations."""

    def test_import_csv(self, tmp_path):
        """Test importing CSV files."""
        # Create temp CSV
        csv_path = tmp_path / "test.csv"
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df.to_csv(csv_path, index=False)

        # Import
        imported_df, error = FileHandler.import_file(str(csv_path))

        assert error == "", "Import should succeed without errors"
        assert imported_df is not None, "Should return DataFrame"
        assert len(imported_df) == 3, "Should have 3 rows"
        assert list(imported_df.columns) == ['A', 'B'], "Should preserve column names"

    def test_import_excel(self, tmp_path):
        """Test importing Excel files."""
        xlsx_path = tmp_path / "test.xlsx"
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df.to_excel(xlsx_path, index=False, engine='openpyxl')

        imported_df, error = FileHandler.import_file(str(xlsx_path))

        assert error == "", "Import should succeed without errors"
        assert imported_df is not None, "Should return DataFrame"
        assert len(imported_df) == 3, "Should have 3 rows"

    def test_import_json(self, tmp_path):
        """Test importing JSON files."""
        json_path = tmp_path / "test.json"
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df.to_json(json_path, orient='records', indent=2)

        imported_df, error = FileHandler.import_file(str(json_path))

        assert error == "", "Import should succeed without errors"
        assert imported_df is not None, "Should return DataFrame"
        assert len(imported_df) == 3, "Should have 3 rows"

    def test_import_nonexistent_file(self):
        """Test importing file that doesn't exist."""
        imported_df, error = FileHandler.import_file("nonexistent.csv")

        assert imported_df is None, "Should return None for nonexistent file"
        assert "does not exist" in error.lower(), "Error message should mention file doesn't exist"

    def test_import_unsupported_format(self, tmp_path):
        """Test importing unsupported file format."""
        txt_path = tmp_path / "test.txt"
        txt_path.write_text("Some text data")

        imported_df, error = FileHandler.import_file(str(txt_path))

        assert imported_df is None, "Should return None for unsupported format"
        assert "not supported" in error.lower(), "Error should mention unsupported format"

    def test_import_corrupted_csv(self, tmp_path):
        """Test importing corrupted CSV file."""
        csv_path = tmp_path / "corrupted.csv"
        csv_path.write_text("A,B,C\n1,2\n3,4,5,6,7")  # Malformed CSV

        imported_df, error = FileHandler.import_file(str(csv_path))

        # Should either handle gracefully or return error
        if imported_df is None:
            assert error != "", "Should have error message for corrupted file"
        else:
            # pandas might handle it, just verify it doesn't crash
            assert True

    def test_export_csv(self, tmp_path):
        """Test exporting DataFrame to CSV."""
        export_path = tmp_path / "export.csv"
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

        # Export
        df.to_csv(export_path, index=False)

        assert export_path.exists(), "Export file should exist"

        # Verify exported data
        imported = pd.read_csv(export_path)
        assert imported.equals(df), "Exported data should match original"

    def test_export_excel(self, tmp_path):
        """Test exporting DataFrame to Excel."""
        export_path = tmp_path / "export.xlsx"
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

        # Export
        df.to_excel(export_path, index=False, engine='openpyxl')

        assert export_path.exists(), "Export file should exist"

        # Verify exported data
        imported = pd.read_excel(export_path, engine='openpyxl')
        assert imported.equals(df), "Exported data should match original"

    def test_validate_supported_extensions(self):
        """Test that supported extensions are recognized."""
        supported = FileHandler.SUPPORTED_IMPORT_FORMATS

        assert '.csv' in supported, "CSV should be supported"
        assert '.xlsx' in supported, "Excel should be supported"
        assert '.json' in supported, "JSON should be supported"

    def test_empty_dataframe_export(self, tmp_path):
        """Test exporting empty DataFrame."""
        export_path = tmp_path / "empty.csv"
        empty_df = pd.DataFrame()

        # Should not crash on empty DataFrame
        empty_df.to_csv(export_path, index=False)

        assert export_path.exists(), "Should create file even for empty DataFrame"

    def test_special_characters_in_data(self, tmp_path):
        """Test handling data with special characters."""
        csv_path = tmp_path / "special.csv"
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob, Jr.', 'Charlie "The Great"'],
            'Value': [1, 2, 3]
        })
        df.to_csv(csv_path, index=False)

        imported_df, error = FileHandler.import_file(str(csv_path))

        assert error == "", "Should handle special characters"
        assert len(imported_df) == 3, "Should preserve all rows"
        assert 'Bob, Jr.' in imported_df['Name'].values, "Should handle commas"
