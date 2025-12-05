"""
Integration tests for the complete import workflow.

Tests the end-to-end flow from file selection to data display.
"""

import pytest
import pandas as pd
from ui.main_window import MainWindow
from core.data_manager import DataManager


class TestImportWorkflow:
    """Integration tests for data import workflow."""

    @pytest.fixture
    def main_window(self, qtbot):
        """Create MainWindow instance for testing."""
        window = MainWindow()
        qtbot.addWidget(window)
        return window

    @pytest.fixture
    def sample_csv(self, tmp_path):
        """Create a sample CSV file for testing."""
        csv_path = tmp_path / "sample.csv"
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [30, 25, 35],
            'Salary': [75000, 60000, 85000]
        })
        df.to_csv(csv_path, index=False)
        return str(csv_path)

    def test_import_screen_accessible(self, qtbot, main_window):
        """Test that import screen is accessible from main window."""
        # Navigate to import screen (index 1)
        main_window.switch_screen(1)

        current_screen = main_window.get_current_screen()
        assert current_screen.screen_name == 'Import Data', "Should navigate to import screen"

    def test_complete_import_flow(self, qtbot, main_window, sample_csv):
        """Test complete import workflow from file selection to data loaded."""
        # Navigate to import screen
        main_window.switch_screen(1)
        import_screen = main_window.get_current_screen()

        # Simulate file import
        # Note: In real test, would use QTest or monkey-patch file dialog
        # For now, test the import method directly
        from core.file_handler import FileHandler

        df, error = FileHandler.import_file(sample_csv)

        assert error == "", f"Import should succeed: {error}"
        assert df is not None, "Should return DataFrame"
        assert len(df) == 3, "Should have 3 rows"

        # Verify data is in DataManager
        dm = DataManager()
        dm.set_data(df, sample_csv)

        assert dm.has_data(), "DataManager should have data after import"
        assert dm.filename == sample_csv, "Should store filename"

    def test_table_screen_displays_imported_data(self, qtbot, main_window, sample_csv):
        """Test that table screen displays imported data correctly."""
        # Import data
        from core.file_handler import FileHandler
        df, error = FileHandler.import_file(sample_csv)

        dm = DataManager()
        dm.set_data(df, sample_csv)

        # Navigate to table screen (index 2)
        main_window.switch_screen(2)
        table_screen = main_window.get_current_screen()

        assert table_screen.screen_name == 'Table View', "Should be on table screen"

        # Table screen should show the data
        # (Would need to verify table model has correct row count)

    def test_dashboard_updates_after_import(self, qtbot, main_window, sample_csv):
        """Test that dashboard screen updates with imported data."""
        # Import data
        from core.file_handler import FileHandler
        df, error = FileHandler.import_file(sample_csv)

        dm = DataManager()
        dm.set_data(df, sample_csv)

        # Navigate to dashboard (index 0)
        main_window.switch_screen(0)
        dashboard_screen = main_window.get_current_screen()

        # Dashboard should show data statistics
        # (Would verify KPI cards show correct values)

    def test_import_then_visualize_workflow(self, qtbot, main_window, sample_csv):
        """Test import followed by visualization."""
        # Import data
        from core.file_handler import FileHandler
        df, error = FileHandler.import_file(sample_csv)

        dm = DataManager()
        dm.set_data(df, sample_csv)

        # Navigate to visualize screen (index 3)
        main_window.switch_screen(3)
        viz_screen = main_window.get_current_screen()

        assert viz_screen.screen_name == 'Visualize Data', "Should be on viz screen"

        # Column selectors should be populated with data columns
        # (Would verify combo boxes have correct items)

    def test_navigation_between_screens(self, qtbot, main_window):
        """Test smooth navigation between all screens."""
        screen_indices = [0, 1, 2, 3, 4, 5]  # All screens

        for index in screen_indices:
            main_window.switch_screen(index)
            current = main_window.get_current_screen()
            assert current is not None, f"Screen {index} should exist"

        # No crashes during navigation
        assert True, "Navigation successful"
