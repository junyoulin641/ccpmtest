"""
Main window for the PyQt Data Visualization Dashboard.

Provides the application framework with navigation, menus, toolbar, and screen management.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QFrame, QAction,
    QMenuBar, QToolBar, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence

from .placeholder_screens import (
    DashboardScreen, SettingsScreen, ExportScreen
)
from .import_screen import ImportScreen
from .table_screen import TableScreen
from .viz_screen import VizScreen


class MainWindow(QMainWindow):
    """Main application window with navigation framework."""

    # Signal emitted when screen changes
    screenChanged = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.current_screen_index = 0
        self.nav_buttons = []
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('PyQt Data Visualization Dashboard')
        self.setGeometry(100, 100, 1280, 720)

        # Create central widget with layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create stacked widget for screens
        self.stacked_widget = QStackedWidget()
        self.init_screens()
        main_layout.addWidget(self.stacked_widget, 1)  # Stretch factor 1

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create menus, toolbar, statusbar
        self.create_menus()
        self.create_toolbar()
        self.create_statusbar()

        # Set initial screen
        self.switch_screen(0)

    def create_sidebar(self):
        """Create the navigation sidebar."""
        sidebar = QFrame()
        sidebar.setFrameStyle(QFrame.StyledPanel)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 1px solid #34495e;
            }
        """)
        sidebar.setMinimumWidth(180)
        sidebar.setMaximumWidth(180)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)

        # Navigation buttons
        nav_items = [
            ('Dashboard', 0, 'Ctrl+1'),
            ('Import', 1, 'Ctrl+2'),
            ('Table', 2, 'Ctrl+3'),
            ('Visualize', 3, 'Ctrl+4'),
            ('Settings', 4, 'Ctrl+5'),
            ('Export', 5, 'Ctrl+6')
        ]

        for name, index, shortcut in nav_items:
            button = self.create_nav_button(name, index)
            self.nav_buttons.append(button)
            layout.addWidget(button)

            # Add keyboard shortcut
            action = QAction(name, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(lambda checked, idx=index: self.switch_screen(idx))
            self.addAction(action)

        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar

    def create_nav_button(self, text, index):
        """Create a navigation button."""
        button = QPushButton(text)
        button.setMinimumHeight(50)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ecf0f1;
                border: none;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """)
        button.clicked.connect(lambda: self.switch_screen(index))
        return button

    def update_nav_button_styles(self):
        """Update navigation button styles to highlight active screen."""
        for i, button in enumerate(self.nav_buttons):
            if i == self.current_screen_index:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #1abc9c;
                        color: white;
                        border: none;
                        border-left: 4px solid #16a085;
                        text-align: left;
                        padding-left: 16px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #ecf0f1;
                        border: none;
                        text-align: left;
                        padding-left: 20px;
                        font-size: 14px;
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #34495e;
                    }
                    QPushButton:pressed {
                        background-color: #1abc9c;
                    }
                """)

    def init_screens(self):
        """Initialize application screens."""
        self.screens = [
            DashboardScreen(),
            ImportScreen(),
            TableScreen(),
            VizScreen(),
            SettingsScreen(),
            ExportScreen()
        ]

        for screen in self.screens:
            self.stacked_widget.addWidget(screen)

    def switch_screen(self, index):
        """Switch to the specified screen."""
        if 0 <= index < len(self.screens):
            self.current_screen_index = index
            self.stacked_widget.setCurrentIndex(index)
            self.update_nav_button_styles()

            screen_name = self.screens[index].screen_name
            self.statusbar.showMessage(f'Switched to {screen_name}')
            self.screenChanged.emit(index, screen_name)

    def create_menus(self):
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('&File')

        new_action = QAction('&New', self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setStatusTip('Create new project')
        file_menu.addAction(new_action)

        open_action = QAction('&Open...', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setStatusTip('Open existing file')
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = QAction('&Save', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setStatusTip('Save current file')
        file_menu.addAction(save_action)

        save_as_action = QAction('Save &As...', self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.setStatusTip('Save as new file')
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu('&Edit')

        prefs_action = QAction('&Preferences', self)
        prefs_action.setShortcut(QKeySequence.Preferences)
        prefs_action.setStatusTip('Open preferences')
        edit_menu.addAction(prefs_action)

        # View menu
        view_menu = menubar.addMenu('&View')

        fullscreen_action = QAction('&Full Screen', self)
        fullscreen_action.setShortcut(QKeySequence.FullScreen)
        fullscreen_action.setStatusTip('Toggle full screen')
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        view_menu.addSeparator()

        zoom_in_action = QAction('Zoom &In', self)
        zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction('Zoom &Out', self)
        zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        view_menu.addAction(zoom_out_action)

        # Tools menu
        tools_menu = menubar.addMenu('&Tools')

        refresh_action = QAction('&Refresh Data', self)
        refresh_action.setShortcut(QKeySequence.Refresh)
        refresh_action.setStatusTip('Refresh data from source')
        tools_menu.addAction(refresh_action)

        # Help menu
        help_menu = menubar.addMenu('&Help')

        about_action = QAction('&About', self)
        about_action.setStatusTip('About this application')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        doc_action = QAction('&Documentation', self)
        doc_action.setShortcut(QKeySequence.HelpContents)
        doc_action.setStatusTip('View documentation')
        help_menu.addAction(doc_action)

    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = QToolBar('Main Toolbar')
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Add quick navigation actions
        for i, (name, _, _) in enumerate([
            ('Dashboard', 0, 'Ctrl+1'),
            ('Import', 1, 'Ctrl+2'),
            ('Table', 2, 'Ctrl+3'),
            ('Visualize', 3, 'Ctrl+4'),
            ('Settings', 4, 'Ctrl+5'),
            ('Export', 5, 'Ctrl+6')
        ]):
            action = QAction(name, self)
            action.setStatusTip(f'Go to {name}')
            action.triggered.connect(lambda checked, idx=i: self.switch_screen(idx))
            toolbar.addAction(action)

    def create_statusbar(self):
        """Create the status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready')

    def toggle_fullscreen(self, checked):
        """Toggle full screen mode."""
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            'About PyQt Data Visualization Dashboard',
            '<h3>PyQt Data Visualization Dashboard</h3>'
            '<p>Version 0.1.0</p>'
            '<p>A desktop application for data visualization and analysis.</p>'
            '<p>Built with PyQt5, pandas, and matplotlib.</p>'
        )

    def get_current_screen(self):
        """Get the currently active screen widget."""
        return self.screens[self.current_screen_index]

    def get_screen_by_index(self, index):
        """Get screen by index."""
        if 0 <= index < len(self.screens):
            return self.screens[index]
        return None
