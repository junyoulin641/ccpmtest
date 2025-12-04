"""
PyQt Data Visualization Dashboard

A desktop application for data visualization and analysis built with PyQt5.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt


class DataVizDashboard(QMainWindow):
    """Main application window for the data visualization dashboard."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('PyQt Data Visualization Dashboard')
        self.setGeometry(100, 100, 1280, 720)

        # Placeholder central widget
        label = QLabel('Data Visualization Dashboard\n\nProject structure initialized.', self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 24px; padding: 20px;')
        self.setCentralWidget(label)


def main():
    """Application entry point."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName('PyQt Data Visualization Dashboard')

        window = DataVizDashboard()
        window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
