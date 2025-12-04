"""
FileHandler module for importing and exporting data files.

Supports CSV, Excel (XLSX), and JSON formats with validation and error handling.
"""

import pandas as pd
import os
from typing import Optional, Tuple
from pathlib import Path


class FileHandler:
    """
    Handles file import and export operations for various formats.

    Supports:
    - CSV files (.csv)
    - Excel files (.xlsx, .xls)
    - JSON files (.json)
    """

    # Supported file extensions
    SUPPORTED_IMPORT_FORMATS = {
        '.csv': 'CSV Files',
        '.xlsx': 'Excel Files',
        '.xls': 'Excel Files (Legacy)',
        '.json': 'JSON Files'
    }

    SUPPORTED_EXPORT_FORMATS = {
        '.csv': 'CSV Files',
        '.xlsx': 'Excel Files',
        '.json': 'JSON Files'
    }

    @staticmethod
    def get_import_filter() -> str:
        """
        Get file dialog filter string for import operations.

        Returns:
            Filter string for QFileDialog
        """
        filters = []
        filters.append("All Supported Files (*.csv *.xlsx *.xls *.json)")
        for ext, name in FileHandler.SUPPORTED_IMPORT_FORMATS.items():
            filters.append(f"{name} (*{ext})")
        filters.append("All Files (*.*)")
        return ";;".join(filters)

    @staticmethod
    def get_export_filter() -> str:
        """
        Get file dialog filter string for export operations.

        Returns:
            Filter string for QFileDialog
        """
        filters = []
        for ext, name in FileHandler.SUPPORTED_EXPORT_FORMATS.items():
            filters.append(f"{name} (*{ext})")
        return ";;".join(filters)

    @staticmethod
    def validate_file(filepath: str, for_import: bool = True) -> Tuple[bool, str]:
        """
        Validate file path and format.

        Args:
            filepath: Path to the file
            for_import: True for import validation, False for export

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filepath:
            return False, "No file path provided"

        path = Path(filepath)

        # For import, file must exist
        if for_import and not path.exists():
            return False, f"File does not exist: {filepath}"

        # For import, file must be readable
        if for_import and not os.access(filepath, os.R_OK):
            return False, f"File is not readable: {filepath}"

        # Check file extension
        ext = path.suffix.lower()
        supported = FileHandler.SUPPORTED_IMPORT_FORMATS if for_import else FileHandler.SUPPORTED_EXPORT_FORMATS

        if ext not in supported:
            return False, f"Unsupported file format: {ext}"

        # For import, check file is not empty
        if for_import and path.stat().st_size == 0:
            return False, "File is empty"

        return True, ""

    @staticmethod
    def import_file(filepath: str) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Import data from a file.

        Args:
            filepath: Path to the file to import

        Returns:
            Tuple of (DataFrame, error_message)
            DataFrame is None if import fails
        """
        # Validate file
        is_valid, error = FileHandler.validate_file(filepath, for_import=True)
        if not is_valid:
            return None, error

        path = Path(filepath)
        ext = path.suffix.lower()

        try:
            # Import based on file type
            if ext == '.csv':
                df = FileHandler._import_csv(filepath)
            elif ext in ['.xlsx', '.xls']:
                df = FileHandler._import_excel(filepath)
            elif ext == '.json':
                df = FileHandler._import_json(filepath)
            else:
                return None, f"Unsupported file format: {ext}"

            # Validate imported data
            if df is None or df.empty:
                return None, "File contains no data"

            return df, ""

        except pd.errors.EmptyDataError:
            return None, "File is empty or contains no valid data"
        except pd.errors.ParserError as e:
            return None, f"Failed to parse file: {str(e)}"
        except PermissionError:
            return None, f"Permission denied: {filepath}"
        except Exception as e:
            return None, f"Failed to import file: {str(e)}"

    @staticmethod
    def _import_csv(filepath: str) -> pd.DataFrame:
        """
        Import CSV file.

        Args:
            filepath: Path to CSV file

        Returns:
            DataFrame with imported data
        """
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

        for encoding in encodings:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                return df
            except UnicodeDecodeError:
                continue
            except Exception:
                raise

        raise UnicodeDecodeError(
            'utf-8', b'', 0, 1,
            'Unable to decode file with any supported encoding'
        )

    @staticmethod
    def _import_excel(filepath: str) -> pd.DataFrame:
        """
        Import Excel file.

        Args:
            filepath: Path to Excel file

        Returns:
            DataFrame with imported data
        """
        # Read the first sheet by default
        df = pd.read_excel(filepath, sheet_name=0, engine='openpyxl')
        return df

    @staticmethod
    def _import_json(filepath: str) -> pd.DataFrame:
        """
        Import JSON file.

        Args:
            filepath: Path to JSON file

        Returns:
            DataFrame with imported data
        """
        # Try different orientations
        try:
            df = pd.read_json(filepath, orient='records')
            return df
        except ValueError:
            try:
                df = pd.read_json(filepath, orient='columns')
                return df
            except ValueError:
                df = pd.read_json(filepath, orient='index')
                return df

    @staticmethod
    def export_file(df: pd.DataFrame, filepath: str) -> Tuple[bool, str]:
        """
        Export DataFrame to a file.

        Args:
            df: DataFrame to export
            filepath: Path where file should be saved

        Returns:
            Tuple of (success, error_message)
        """
        if df is None or df.empty:
            return False, "No data to export"

        # Validate file path
        is_valid, error = FileHandler.validate_file(filepath, for_import=False)
        if not is_valid:
            return False, error

        path = Path(filepath)
        ext = path.suffix.lower()

        try:
            # Create parent directory if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)

            # Export based on file type
            if ext == '.csv':
                success, error = FileHandler._export_csv(df, filepath)
            elif ext == '.xlsx':
                success, error = FileHandler._export_excel(df, filepath)
            elif ext == '.json':
                success, error = FileHandler._export_json(df, filepath)
            else:
                return False, f"Unsupported export format: {ext}"

            return success, error

        except PermissionError:
            return False, f"Permission denied: {filepath}"
        except Exception as e:
            return False, f"Failed to export file: {str(e)}"

    @staticmethod
    def _export_csv(df: pd.DataFrame, filepath: str) -> Tuple[bool, str]:
        """
        Export DataFrame to CSV.

        Args:
            df: DataFrame to export
            filepath: Destination file path

        Returns:
            Tuple of (success, error_message)
        """
        try:
            df.to_csv(filepath, index=False, encoding='utf-8')
            return True, ""
        except Exception as e:
            return False, f"CSV export failed: {str(e)}"

    @staticmethod
    def _export_excel(df: pd.DataFrame, filepath: str) -> Tuple[bool, str]:
        """
        Export DataFrame to Excel.

        Args:
            df: DataFrame to export
            filepath: Destination file path

        Returns:
            Tuple of (success, error_message)
        """
        try:
            df.to_excel(filepath, index=False, engine='openpyxl')
            return True, ""
        except Exception as e:
            return False, f"Excel export failed: {str(e)}"

    @staticmethod
    def _export_json(df: pd.DataFrame, filepath: str) -> Tuple[bool, str]:
        """
        Export DataFrame to JSON.

        Args:
            df: DataFrame to export
            filepath: Destination file path

        Returns:
            Tuple of (success, error_message)
        """
        try:
            df.to_json(filepath, orient='records', indent=2)
            return True, ""
        except Exception as e:
            return False, f"JSON export failed: {str(e)}"

    @staticmethod
    def get_file_info(filepath: str) -> Optional[dict]:
        """
        Get information about a file.

        Args:
            filepath: Path to the file

        Returns:
            Dictionary with file information, or None if file doesn't exist
        """
        path = Path(filepath)

        if not path.exists():
            return None

        stat = path.stat()

        return {
            'name': path.name,
            'extension': path.suffix,
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': stat.st_mtime,
            'is_readable': os.access(filepath, os.R_OK),
            'is_writable': os.access(filepath, os.W_OK)
        }
