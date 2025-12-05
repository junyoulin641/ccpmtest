"""
PyQt Data Visualization Dashboard

A desktop application for data visualization and analysis built with PyQt5.
"""

import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    """Application entry point."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName('PyQt Data Visualization Dashboard')
        app.setOrganizationName('PyQt Dashboard')

        window = MainWindow()
        window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
