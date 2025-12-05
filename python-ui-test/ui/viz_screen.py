"""
Visualization Screen for creating charts from data.

Provides matplotlib integration with interactive chart generation and export.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QLineEdit, QGroupBox, QFileDialog, QMessageBox,
    QColorDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from core.data_manager import DataManager
from core.chart_builder import ChartBuilder


class VizScreen(QWidget):
    """
    Screen for data visualization with multiple chart types.

    Features:
    - Multiple chart types (Line, Bar, Scatter, Pie)
    - Interactive column selection
    - Chart customization (title, color)
    - Zoom/pan via NavigationToolbar
    - Export to PNG
    """

    screen_name = 'Visualize Data'

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.selected_color = '#3498db'  # Default blue color

        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.init_ui()
        self.connect_signals()

        # Load initial columns if data available
        if self.data_manager.has_data():
            self.update_column_selectors()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel('Data Visualization')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)

        # Controls panel
        controls_group = self.create_controls_panel()
        layout.addWidget(controls_group)

        # Customization panel
        custom_group = self.create_customization_panel()
        layout.addWidget(custom_group)

        # Matplotlib toolbar
        layout.addWidget(self.toolbar)

        # Canvas
        layout.addWidget(self.canvas, 1)

        self.setLayout(layout)

        # Show initial message
        self.show_welcome_message()

    def create_controls_panel(self):
        """Create the chart controls panel."""
        group = QGroupBox('Chart Configuration')
        layout = QHBoxLayout()

        # Chart type selector
        layout.addWidget(QLabel('Chart Type:'))
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(['Line', 'Bar', 'Scatter', 'Pie'])
        self.chart_type_combo.setMinimumWidth(120)
        layout.addWidget(self.chart_type_combo)

        layout.addSpacing(20)

        # X axis column selector
        layout.addWidget(QLabel('X Axis:'))
        self.x_column_combo = QComboBox()
        self.x_column_combo.setMinimumWidth(150)
        layout.addWidget(self.x_column_combo)

        layout.addSpacing(20)

        # Y axis column selector
        layout.addWidget(QLabel('Y Axis:'))
        self.y_column_combo = QComboBox()
        self.y_column_combo.setMinimumWidth(150)
        layout.addWidget(self.y_column_combo)

        layout.addStretch()

        # Generate button
        self.generate_btn = QPushButton('Generate Chart')
        self.generate_btn.setMinimumWidth(140)
        self.generate_btn.clicked.connect(self.generate_chart)
        self.generate_btn.setEnabled(False)
        self.generate_btn.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #a9dfbf;
            }
        """)
        layout.addWidget(self.generate_btn)

        group.setLayout(layout)
        return group

    def create_customization_panel(self):
        """Create the customization panel."""
        group = QGroupBox('Customization')
        layout = QHBoxLayout()

        # Title input
        layout.addWidget(QLabel('Title:'))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Enter custom chart title...')
        self.title_input.setMinimumWidth(300)
        layout.addWidget(self.title_input)

        layout.addSpacing(20)

        # Color picker
        layout.addWidget(QLabel('Color:'))
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(40, 30)
        self.color_btn.clicked.connect(self.choose_color)
        self.update_color_button()
        layout.addWidget(self.color_btn)

        layout.addStretch()

        # Export button
        self.export_btn = QPushButton('Export PNG')
        self.export_btn.setMinimumWidth(120)
        self.export_btn.clicked.connect(self.export_chart)
        self.export_btn.setEnabled(False)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        layout.addWidget(self.export_btn)

        # Clear button
        self.clear_btn = QPushButton('Clear Chart')
        self.clear_btn.setMinimumWidth(120)
        self.clear_btn.clicked.connect(self.clear_chart)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #d0d0d0;
            }
        """)
        layout.addWidget(self.clear_btn)

        group.setLayout(layout)
        return group

    def connect_signals(self):
        """Connect signals from DataManager."""
        self.data_manager.dataLoaded.connect(self.on_data_loaded)
        self.data_manager.dataCleared.connect(self.on_data_cleared)

    def on_data_loaded(self, filename):
        """Handle data loaded signal."""
        self.update_column_selectors()
        self.clear_chart()

    def on_data_cleared(self):
        """Handle data cleared signal."""
        self.x_column_combo.clear()
        self.y_column_combo.clear()
        self.generate_btn.setEnabled(False)
        self.clear_chart()

    def update_column_selectors(self):
        """Update column selector dropdowns with available columns."""
        df = self.data_manager.get_data()

        if df is None or df.empty:
            self.x_column_combo.clear()
            self.y_column_combo.clear()
            self.generate_btn.setEnabled(False)
            return

        columns = df.columns.tolist()

        # Update X column selector
        self.x_column_combo.clear()
        self.x_column_combo.addItems(columns)

        # Update Y column selector
        self.y_column_combo.clear()
        self.y_column_combo.addItems(columns)

        # Set default selections
        if len(columns) > 1:
            self.x_column_combo.setCurrentIndex(0)
            self.y_column_combo.setCurrentIndex(1)
        elif len(columns) == 1:
            self.x_column_combo.setCurrentIndex(0)
            self.y_column_combo.setCurrentIndex(0)

        self.generate_btn.setEnabled(True)

    def choose_color(self):
        """Open color picker dialog."""
        color = QColorDialog.getColor(
            QColor(self.selected_color),
            self,
            'Select Chart Color'
        )

        if color.isValid():
            self.selected_color = color.name()
            self.update_color_button()

    def update_color_button(self):
        """Update color button appearance."""
        self.color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.selected_color};
                border: 2px solid #333;
                border-radius: 4px;
            }}
        """)

    def generate_chart(self):
        """Generate chart based on current selections."""
        # Get selections
        chart_type = self.chart_type_combo.currentText()
        x_col = self.x_column_combo.currentText()
        y_col = self.y_column_combo.currentText()

        if not x_col or not y_col:
            QMessageBox.warning(self, 'Invalid Selection', 'Please select both X and Y columns')
            return

        # Get data
        df = self.data_manager.get_data()

        if df is None or df.empty:
            QMessageBox.warning(self, 'No Data', 'No data available to visualize')
            return

        # Validate data
        is_valid, error_msg = ChartBuilder.validate_chart_data(df, chart_type, x_col, y_col)

        if not is_valid:
            QMessageBox.warning(self, 'Invalid Data', error_msg)
            return

        try:
            # Get custom title
            title = self.title_input.text().strip() or None

            # Clear previous chart
            self.figure.clear()
            plt.close('all')  # Free memory

            # Generate chart
            if chart_type == 'Line':
                fig = ChartBuilder.create_line_chart(
                    df, x_col, y_col,
                    title=title,
                    color=self.selected_color
                )
            elif chart_type == 'Bar':
                fig = ChartBuilder.create_bar_chart(
                    df, x_col, y_col,
                    title=title,
                    color=self.selected_color
                )
            elif chart_type == 'Scatter':
                fig = ChartBuilder.create_scatter_chart(
                    df, x_col, y_col,
                    title=title,
                    color=self.selected_color
                )
            elif chart_type == 'Pie':
                fig = ChartBuilder.create_pie_chart(
                    df, x_col, y_col,
                    title=title
                )
            else:
                QMessageBox.warning(self, 'Error', f'Unsupported chart type: {chart_type}')
                return

            # Transfer chart to canvas
            self.figure = fig
            self.canvas.figure = self.figure
            self.canvas.draw()

            # Enable export and clear buttons
            self.export_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(
                self,
                'Chart Generation Error',
                f'Failed to generate chart:\n{str(e)}'
            )

    def clear_chart(self):
        """Clear the current chart."""
        self.figure.clear()
        plt.close('all')
        self.canvas.draw()
        self.export_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.show_welcome_message()

    def show_welcome_message(self):
        """Show welcome message on empty canvas."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5, 0.5,
            'Load data and select chart options to visualize',
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=16,
            color='#999'
        )
        ax.axis('off')
        self.canvas.draw()

    def export_chart(self):
        """Export current chart to PNG file."""
        if not self.figure.get_axes():
            QMessageBox.warning(self, 'No Chart', 'Generate a chart first before exporting')
            return

        # Get file path
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            'Export Chart',
            '',
            'PNG Image (*.png);;PDF Document (*.pdf);;SVG Vector (*.svg)'
        )

        if not filepath:
            return

        try:
            # Export with high DPI
            self.figure.savefig(filepath, dpi=300, bbox_inches='tight')
            QMessageBox.information(
                self,
                'Export Successful',
                f'Chart saved to:\n{filepath}'
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                'Export Failed',
                f'Failed to export chart:\n{str(e)}'
            )
