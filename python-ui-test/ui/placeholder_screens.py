"""
Placeholder screen widgets for the Data Visualization Dashboard.

These screens will be replaced with full implementations in subsequent tasks.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class PlaceholderScreen(QWidget):
    """Base class for placeholder screens."""

    def __init__(self, screen_name):
        super().__init__()
        self.screen_name = screen_name
        self.init_ui()

    def init_ui(self):
        """Initialize the placeholder UI."""
        layout = QVBoxLayout()

        title = QLabel(self.screen_name)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 32px; font-weight: bold; padding: 20px;')

        description = QLabel('This screen will be implemented in a future task.')
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet('font-size: 16px; color: #666; padding: 10px;')

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()

        self.setLayout(layout)


class DashboardScreen(PlaceholderScreen):
    """Placeholder for Dashboard screen."""

    def __init__(self):
        super().__init__('Dashboard')


class ImportScreen(PlaceholderScreen):
    """Placeholder for Import screen."""

    def __init__(self):
        super().__init__('Import Data')


class TableScreen(PlaceholderScreen):
    """Placeholder for Table View screen."""

    def __init__(self):
        super().__init__('Table View')


class VisualizeScreen(PlaceholderScreen):
    """Placeholder for Visualization screen."""

    def __init__(self):
        super().__init__('Visualize Data')


class SettingsScreen(PlaceholderScreen):
    """Placeholder for Settings screen."""

    def __init__(self):
        super().__init__('Settings')


class ExportScreen(PlaceholderScreen):
    """Placeholder for Export screen."""

    def __init__(self):
        super().__init__('Export Data')
