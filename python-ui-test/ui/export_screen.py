"""
Export Screen for exporting data and visualizations.

Provides multi-format export for datasets and charts.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QRadioButton, QFileDialog, QMessageBox,
    QCheckBox, QListWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.data_manager import DataManager
from core.file_handler import FileHandler


class ExportScreen(QWidget):
    """
    Export screen for data and chart export.

    Features:
    - Multi-format data export (CSV, Excel, JSON)
    - Chart export (PNG, PDF, SVG)
    - Export all or filtered data
    """

    screen_name = 'Export Data'

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        title = QLabel('Export Data')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)

        # Data export section
        data_group = self.create_data_export_section()
        layout.addWidget(data_group)

        # Chart export section
        chart_group = self.create_chart_export_section()
        layout.addWidget(chart_group)

        # Batch operations section
        batch_group = self.create_batch_export_section()
        layout.addWidget(batch_group)

        layout.addStretch()
        self.setLayout(layout)

    def create_data_export_section(self):
        """Create data export section."""
        group = QGroupBox('Data Export')
        layout = QVBoxLayout()

        # Description
        desc = QLabel('Export your dataset to various formats')
        desc.setStyleSheet('color: #666; font-size: 13px;')
        layout.addWidget(desc)

        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel('Format:'))

        self.csv_radio = QRadioButton('CSV')
        self.csv_radio.setChecked(True)
        format_layout.addWidget(self.csv_radio)

        self.excel_radio = QRadioButton('Excel (.xlsx)')
        format_layout.addWidget(self.excel_radio)

        self.json_radio = QRadioButton('JSON')
        format_layout.addWidget(self.json_radio)

        format_layout.addStretch()
        layout.addLayout(format_layout)

        # Options
        self.include_index_check = QCheckBox('Include row index')
        layout.addWidget(self.include_index_check)

        # Export button
        export_btn = QPushButton('Export Data')
        export_btn.setMinimumWidth(150)
        export_btn.clicked.connect(self.export_data)
        export_btn.setStyleSheet("""
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
        """)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(export_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        group.setLayout(layout)
        return group

    def create_chart_export_section(self):
        """Create chart export section."""
        group = QGroupBox('Chart Export')
        layout = QVBoxLayout()

        # Description
        desc = QLabel('Export charts from the Visualization screen')
        desc.setStyleSheet('color: #666; font-size: 13px;')
        layout.addWidget(desc)

        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel('Format:'))

        self.png_radio = QRadioButton('PNG Image')
        self.png_radio.setChecked(True)
        format_layout.addWidget(self.png_radio)

        self.pdf_radio = QRadioButton('PDF Document')
        format_layout.addWidget(self.pdf_radio)

        self.svg_radio = QRadioButton('SVG Vector')
        format_layout.addWidget(self.svg_radio)

        format_layout.addStretch()
        layout.addLayout(format_layout)

        # DPI selection for PNG
        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(QLabel('Quality (DPI):'))

        self.dpi_low_radio = QRadioButton('150')
        dpi_layout.addWidget(self.dpi_low_radio)

        self.dpi_medium_radio = QRadioButton('300')
        self.dpi_medium_radio.setChecked(True)
        dpi_layout.addWidget(self.dpi_medium_radio)

        self.dpi_high_radio = QRadioButton('600')
        dpi_layout.addWidget(self.dpi_high_radio)

        dpi_layout.addStretch()
        layout.addLayout(dpi_layout)

        # Note
        note = QLabel('Note: Go to the Visualize screen to generate and export charts')
        note.setStyleSheet('color: #999; font-size: 12px; font-style: italic;')
        layout.addWidget(note)

        group.setLayout(layout)
        return group

    def create_batch_export_section(self):
        """Create batch export section."""
        group = QGroupBox('Batch Export')
        layout = QVBoxLayout()

        # Description
        desc = QLabel('Export multiple formats at once')
        desc.setStyleSheet('color: #666; font-size: 13px;')
        layout.addWidget(desc)

        # Format checklist
        self.batch_csv = QCheckBox('CSV')
        self.batch_excel = QCheckBox('Excel')
        self.batch_json = QCheckBox('JSON')

        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.batch_csv)
        checkboxes_layout.addWidget(self.batch_excel)
        checkboxes_layout.addWidget(self.batch_json)
        checkboxes_layout.addStretch()
        layout.addLayout(checkboxes_layout)

        # Batch export button
        batch_btn = QPushButton('Batch Export')
        batch_btn.setMinimumWidth(150)
        batch_btn.clicked.connect(self.batch_export)
        batch_btn.setStyleSheet("""
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

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(batch_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        group.setLayout(layout)
        return group

    def export_data(self):
        """Export data in selected format."""
        # Check if data is available
        df = self.data_manager.get_data()

        if df is None or df.empty:
            QMessageBox.warning(self, 'No Data', 'No data available to export')
            return

        # Determine format
        if self.csv_radio.isChecked():
            file_filter = 'CSV Files (*.csv)'
            default_ext = '.csv'
        elif self.excel_radio.isChecked():
            file_filter = 'Excel Files (*.xlsx)'
            default_ext = '.xlsx'
        else:
            file_filter = 'JSON Files (*.json)'
            default_ext = '.json'

        # Get file path
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            'Export Data',
            '',
            file_filter
        )

        if not filepath:
            return

        # Ensure file has correct extension
        if not filepath.endswith(default_ext):
            filepath += default_ext

        # Export data
        try:
            if self.csv_radio.isChecked():
                df.to_csv(filepath, index=self.include_index_check.isChecked())
            elif self.excel_radio.isChecked():
                df.to_excel(filepath, index=self.include_index_check.isChecked(), engine='openpyxl')
            else:
                df.to_json(filepath, orient='records', indent=2)

            QMessageBox.information(
                self,
                'Export Successful',
                f'Data exported successfully to:\n{filepath}\n\n'
                f'Exported {len(df)} rows and {len(df.columns)} columns.'
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                'Export Failed',
                f'Failed to export data:\n{str(e)}'
            )

    def batch_export(self):
        """Batch export data to multiple formats."""
        # Check if data is available
        df = self.data_manager.get_data()

        if df is None or df.empty:
            QMessageBox.warning(self, 'No Data', 'No data available to export')
            return

        # Check if any format is selected
        if not (self.batch_csv.isChecked() or self.batch_excel.isChecked() or self.batch_json.isChecked()):
            QMessageBox.warning(self, 'No Format Selected', 'Please select at least one format for batch export')
            return

        # Get directory
        directory = QFileDialog.getExistingDirectory(self, 'Select Export Directory')

        if not directory:
            return

        # Determine base filename
        base_name = self.data_manager.filename or 'export'
        if '.' in base_name:
            base_name = base_name.rsplit('.', 1)[0]

        export_count = 0
        errors = []

        # Export CSV
        if self.batch_csv.isChecked():
            try:
                csv_path = f'{directory}/{base_name}.csv'
                df.to_csv(csv_path, index=False)
                export_count += 1
            except Exception as e:
                errors.append(f'CSV: {str(e)}')

        # Export Excel
        if self.batch_excel.isChecked():
            try:
                excel_path = f'{directory}/{base_name}.xlsx'
                df.to_excel(excel_path, index=False, engine='openpyxl')
                export_count += 1
            except Exception as e:
                errors.append(f'Excel: {str(e)}')

        # Export JSON
        if self.batch_json.isChecked():
            try:
                json_path = f'{directory}/{base_name}.json'
                df.to_json(json_path, orient='records', indent=2)
                export_count += 1
            except Exception as e:
                errors.append(f'JSON: {str(e)}')

        # Show results
        if errors:
            error_msg = '\n'.join(errors)
            QMessageBox.warning(
                self,
                'Batch Export Partial',
                f'Exported {export_count} file(s) successfully.\n\n'
                f'Errors:\n{error_msg}'
            )
        else:
            QMessageBox.information(
                self,
                'Batch Export Successful',
                f'Successfully exported {export_count} file(s) to:\n{directory}'
            )
