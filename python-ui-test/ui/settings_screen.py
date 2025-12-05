"""
Settings Screen for application configuration.

Provides user preferences management with QSettings persistence.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QGroupBox, QComboBox, QSpinBox, QCheckBox,
    QFileDialog, QLineEdit, QMessageBox, QColorDialog
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont, QColor


class SettingsScreen(QWidget):
    """
    Settings screen for application preferences.

    Features:
    - General settings (theme, directories)
    - Chart defaults
    - Preferences persistence with QSettings
    """

    screen_name = 'Settings'

    def __init__(self):
        super().__init__()
        self.settings = QSettings('PyQtDashboard', 'DataViz')
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        title = QLabel('Application Settings')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_general_tab(), 'General')
        self.tabs.addTab(self.create_chart_defaults_tab(), 'Chart Defaults')
        self.tabs.addTab(self.create_advanced_tab(), 'Advanced')
        layout.addWidget(self.tabs, 1)

        # Buttons
        button_layout = self.create_buttons()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_general_tab(self):
        """Create general settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Theme selection
        theme_group = QGroupBox('Appearance')
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel('Theme:'))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Light', 'Dark'])
        self.theme_combo.setMinimumWidth(150)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Directories
        dir_group = QGroupBox('Default Directories')
        dir_layout = QVBoxLayout()

        # Import directory
        import_layout = QHBoxLayout()
        import_layout.addWidget(QLabel('Import Directory:'))
        self.import_dir_edit = QLineEdit()
        self.import_dir_edit.setReadOnly(True)
        import_layout.addWidget(self.import_dir_edit, 1)
        import_btn = QPushButton('Browse...')
        import_btn.clicked.connect(self.browse_import_dir)
        import_layout.addWidget(import_btn)
        dir_layout.addLayout(import_layout)

        # Export directory
        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel('Export Directory:'))
        self.export_dir_edit = QLineEdit()
        self.export_dir_edit.setReadOnly(True)
        export_layout.addWidget(self.export_dir_edit, 1)
        export_btn = QPushButton('Browse...')
        export_btn.clicked.connect(self.browse_export_dir)
        export_layout.addWidget(export_btn)
        dir_layout.addLayout(export_layout)

        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)

        # Auto-save
        auto_group = QGroupBox('Auto-Save')
        auto_layout = QHBoxLayout()
        auto_layout.addWidget(QLabel('Save interval (minutes):'))
        self.autosave_spin = QSpinBox()
        self.autosave_spin.setRange(0, 60)
        self.autosave_spin.setSpecialValueText('Disabled')
        auto_layout.addWidget(self.autosave_spin)
        auto_layout.addStretch()
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_chart_defaults_tab(self):
        """Create chart defaults tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Default chart type
        type_group = QGroupBox('Default Chart Type')
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel('Chart Type:'))
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(['Line', 'Bar', 'Scatter', 'Pie'])
        type_layout.addWidget(self.chart_type_combo)
        type_layout.addStretch()
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # Colors
        color_group = QGroupBox('Default Colors')
        color_layout = QVBoxLayout()

        # Line color
        line_layout = QHBoxLayout()
        line_layout.addWidget(QLabel('Line Color:'))
        self.line_color_btn = QPushButton()
        self.line_color_btn.setFixedSize(80, 30)
        self.line_color_btn.clicked.connect(lambda: self.choose_color('line'))
        line_layout.addWidget(self.line_color_btn)
        line_layout.addStretch()
        color_layout.addLayout(line_layout)

        # Bar color
        bar_layout = QHBoxLayout()
        bar_layout.addWidget(QLabel('Bar Color:'))
        self.bar_color_btn = QPushButton()
        self.bar_color_btn.setFixedSize(80, 30)
        self.bar_color_btn.clicked.connect(lambda: self.choose_color('bar'))
        bar_layout.addWidget(self.bar_color_btn)
        bar_layout.addStretch()
        color_layout.addLayout(bar_layout)

        color_group.setLayout(color_layout)
        layout.addWidget(color_group)

        # Grid and legend
        display_group = QGroupBox('Display Options')
        display_layout = QVBoxLayout()

        self.grid_check = QCheckBox('Show grid lines by default')
        display_layout.addWidget(self.grid_check)

        legend_layout = QHBoxLayout()
        legend_layout.addWidget(QLabel('Legend Position:'))
        self.legend_combo = QComboBox()
        self.legend_combo.addItems(['Best', 'Upper Right', 'Upper Left', 'Lower Right', 'Lower Left'])
        legend_layout.addWidget(self.legend_combo)
        legend_layout.addStretch()
        display_layout.addLayout(legend_layout)

        display_group.setLayout(display_layout)
        layout.addWidget(display_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_advanced_tab(self):
        """Create advanced settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Performance
        perf_group = QGroupBox('Performance')
        perf_layout = QVBoxLayout()

        # Max rows for charts
        rows_layout = QHBoxLayout()
        rows_layout.addWidget(QLabel('Max rows for charts:'))
        self.max_rows_spin = QSpinBox()
        self.max_rows_spin.setRange(1000, 100000)
        self.max_rows_spin.setSingleStep(1000)
        rows_layout.addWidget(self.max_rows_spin)
        rows_layout.addStretch()
        perf_layout.addLayout(rows_layout)

        # Pagination threshold
        page_layout = QHBoxLayout()
        page_layout.addWidget(QLabel('Pagination threshold:'))
        self.page_threshold_spin = QSpinBox()
        self.page_threshold_spin.setRange(1000, 50000)
        self.page_threshold_spin.setSingleStep(1000)
        page_layout.addWidget(self.page_threshold_spin)
        page_layout.addStretch()
        perf_layout.addLayout(page_layout)

        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)

        # Debug
        debug_group = QGroupBox('Developer Options')
        debug_layout = QVBoxLayout()
        self.debug_check = QCheckBox('Enable debug mode')
        debug_layout.addWidget(self.debug_check)
        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_buttons(self):
        """Create action buttons."""
        layout = QHBoxLayout()
        layout.addStretch()

        # Reset button
        reset_btn = QPushButton('Reset to Defaults')
        reset_btn.setMinimumWidth(150)
        reset_btn.clicked.connect(self.reset_to_defaults)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        layout.addWidget(reset_btn)

        # Save button
        save_btn = QPushButton('Save Settings')
        save_btn.setMinimumWidth(150)
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        layout.addWidget(save_btn)

        return layout

    def browse_import_dir(self):
        """Browse for import directory."""
        directory = QFileDialog.getExistingDirectory(self, 'Select Import Directory')
        if directory:
            self.import_dir_edit.setText(directory)

    def browse_export_dir(self):
        """Browse for export directory."""
        directory = QFileDialog.getExistingDirectory(self, 'Select Export Directory')
        if directory:
            self.export_dir_edit.setText(directory)

    def choose_color(self, color_type):
        """Open color picker dialog."""
        if color_type == 'line':
            current_color = self.line_color_btn.styleSheet()
            btn = self.line_color_btn
        else:
            current_color = self.bar_color_btn.styleSheet()
            btn = self.bar_color_btn

        color = QColorDialog.getColor(QColor('#3498db'), self, 'Select Color')
        if color.isValid():
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color.name()};
                    border: 2px solid #333;
                    border-radius: 4px;
                }}
            """)
            btn.setProperty('color_value', color.name())

    def load_settings(self):
        """Load settings from QSettings."""
        # General
        theme = self.settings.value('theme', 'Light')
        self.theme_combo.setCurrentText(theme)

        import_dir = self.settings.value('import_dir', '')
        self.import_dir_edit.setText(import_dir)

        export_dir = self.settings.value('export_dir', '')
        self.export_dir_edit.setText(export_dir)

        autosave = self.settings.value('autosave_interval', 0, type=int)
        self.autosave_spin.setValue(autosave)

        # Chart defaults
        chart_type = self.settings.value('default_chart_type', 'Line')
        self.chart_type_combo.setCurrentText(chart_type)

        line_color = self.settings.value('line_color', '#3498db')
        self.line_color_btn.setStyleSheet(f'background-color: {line_color}; border: 2px solid #333; border-radius: 4px;')
        self.line_color_btn.setProperty('color_value', line_color)

        bar_color = self.settings.value('bar_color', '#e74c3c')
        self.bar_color_btn.setStyleSheet(f'background-color: {bar_color}; border: 2px solid #333; border-radius: 4px;')
        self.bar_color_btn.setProperty('color_value', bar_color)

        show_grid = self.settings.value('show_grid', True, type=bool)
        self.grid_check.setChecked(show_grid)

        legend_pos = self.settings.value('legend_position', 'Best')
        self.legend_combo.setCurrentText(legend_pos)

        # Advanced
        max_rows = self.settings.value('max_chart_rows', 10000, type=int)
        self.max_rows_spin.setValue(max_rows)

        page_threshold = self.settings.value('pagination_threshold', 10000, type=int)
        self.page_threshold_spin.setValue(page_threshold)

        debug = self.settings.value('debug_mode', False, type=bool)
        self.debug_check.setChecked(debug)

    def save_settings(self):
        """Save settings to QSettings."""
        # General
        self.settings.setValue('theme', self.theme_combo.currentText())
        self.settings.setValue('import_dir', self.import_dir_edit.text())
        self.settings.setValue('export_dir', self.export_dir_edit.text())
        self.settings.setValue('autosave_interval', self.autosave_spin.value())

        # Chart defaults
        self.settings.setValue('default_chart_type', self.chart_type_combo.currentText())
        self.settings.setValue('line_color', self.line_color_btn.property('color_value') or '#3498db')
        self.settings.setValue('bar_color', self.bar_color_btn.property('color_value') or '#e74c3c')
        self.settings.setValue('show_grid', self.grid_check.isChecked())
        self.settings.setValue('legend_position', self.legend_combo.currentText())

        # Advanced
        self.settings.setValue('max_chart_rows', self.max_rows_spin.value())
        self.settings.setValue('pagination_threshold', self.page_threshold_spin.value())
        self.settings.setValue('debug_mode', self.debug_check.isChecked())

        QMessageBox.information(self, 'Settings Saved', 'Your settings have been saved successfully.')

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        reply = QMessageBox.question(
            self,
            'Reset Settings',
            'Are you sure you want to reset all settings to defaults?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.settings.clear()

            # Set defaults
            self.settings.setValue('theme', 'Light')
            self.settings.setValue('autosave_interval', 0)
            self.settings.setValue('default_chart_type', 'Line')
            self.settings.setValue('line_color', '#3498db')
            self.settings.setValue('bar_color', '#e74c3c')
            self.settings.setValue('show_grid', True)
            self.settings.setValue('legend_position', 'Best')
            self.settings.setValue('max_chart_rows', 10000)
            self.settings.setValue('pagination_threshold', 10000)
            self.settings.setValue('debug_mode', False)

            # Reload UI
            self.load_settings()

            QMessageBox.information(self, 'Reset Complete', 'Settings have been reset to defaults.')
