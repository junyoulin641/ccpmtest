"""
Import Screen for loading data files.

Provides UI for selecting and importing CSV, Excel, and JSON files.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit, QGroupBox, QMessageBox,
    QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont

from core.data_manager import DataManager
from core.file_handler import FileHandler


class FileImportThread(QThread):
    """Background thread for file import operations."""

    # Signals
    importComplete = pyqtSignal(object, str)  # DataFrame, filename
    importFailed = pyqtSignal(str)  # error message
    progressUpdate = pyqtSignal(int)  # progress percentage

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        """Run the import operation in background."""
        try:
            self.progressUpdate.emit(30)

            # Import the file
            df, error = FileHandler.import_file(self.filepath)

            self.progressUpdate.emit(70)

            if df is not None:
                self.progressUpdate.emit(100)
                self.importComplete.emit(df, self.filepath)
            else:
                self.importFailed.emit(error)

        except Exception as e:
            self.importFailed.emit(f"Unexpected error: {str(e)}")


class ImportScreen(QWidget):
    """
    Screen for importing data files.

    Supports CSV, Excel, and JSON formats with drag-and-drop
    and file dialog selection.
    """

    screen_name = 'Import Data'

    # Signals
    dataImported = pyqtSignal(str)  # Emitted when data is successfully imported

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.import_thread = None
        self.current_file = None
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel('Import Data')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)

        # Description
        description = QLabel(
            'Import data from CSV, Excel, or JSON files. '
            'Supported formats: .csv, .xlsx, .xls, .json'
        )
        description.setWordWrap(True)
        description.setStyleSheet('color: #666; font-size: 14px;')
        layout.addWidget(description)

        # File selection group
        file_group = self.create_file_selection_group()
        layout.addWidget(file_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        # File info group
        info_group = self.create_file_info_group()
        layout.addWidget(info_group)

        # Preview group
        preview_group = self.create_preview_group()
        layout.addWidget(preview_group, 1)  # Stretch to fill space

        # Action buttons
        button_layout = self.create_action_buttons()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_file_selection_group(self):
        """Create the file selection UI group."""
        group = QGroupBox('Select File')
        layout = QVBoxLayout()

        # File path display
        path_layout = QHBoxLayout()

        self.file_path_label = QLabel('No file selected')
        self.file_path_label.setStyleSheet(
            'padding: 8px; background-color: #f5f5f5; '
            'border: 1px solid #ddd; border-radius: 4px;'
        )
        path_layout.addWidget(self.file_path_label, 1)

        # Browse button
        browse_btn = QPushButton('Browse...')
        browse_btn.setMinimumWidth(100)
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        path_layout.addWidget(browse_btn)

        layout.addLayout(path_layout)
        group.setLayout(layout)
        return group

    def create_file_info_group(self):
        """Create the file information display group."""
        group = QGroupBox('File Information')
        layout = QVBoxLayout()

        self.file_info_text = QTextEdit()
        self.file_info_text.setReadOnly(True)
        self.file_info_text.setMaximumHeight(120)
        self.file_info_text.setStyleSheet(
            'background-color: #fafafa; border: 1px solid #ddd;'
        )
        self.file_info_text.setText('No file information available')

        layout.addWidget(self.file_info_text)
        group.setLayout(layout)
        return group

    def create_preview_group(self):
        """Create the data preview group."""
        group = QGroupBox('Data Preview')
        layout = QVBoxLayout()

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet(
            'background-color: #fafafa; border: 1px solid #ddd; '
            'font-family: Consolas, monospace; font-size: 12px;'
        )
        self.preview_text.setText('No data to preview')

        layout.addWidget(self.preview_text)
        group.setLayout(layout)
        return group

    def create_action_buttons(self):
        """Create action buttons layout."""
        layout = QHBoxLayout()
        layout.addStretch()

        # Clear button
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.setMinimumWidth(120)
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self.clear_selection)
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
                background-color: #bdc3c7;
            }
        """)
        layout.addWidget(self.clear_btn)

        # Import button
        self.import_btn = QPushButton('Import Data')
        self.import_btn.setMinimumWidth(120)
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self.import_file)
        self.import_btn.setStyleSheet("""
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
        layout.addWidget(self.import_btn)

        return layout

    def connect_signals(self):
        """Connect DataManager signals."""
        self.data_manager.dataLoaded.connect(self.on_data_loaded)
        self.data_manager.errorOccurred.connect(self.on_error)

    def browse_file(self):
        """Open file dialog to select a file."""
        file_filter = FileHandler.get_import_filter()

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            'Select Data File',
            '',
            file_filter
        )

        if filepath:
            self.load_file_info(filepath)

    def load_file_info(self, filepath):
        """Load and display file information."""
        self.current_file = filepath

        # Update UI
        self.file_path_label.setText(filepath)

        # Get file info
        file_info = FileHandler.get_file_info(filepath)

        if file_info:
            info_text = f"""
File Name: {file_info['name']}
File Type: {file_info['extension']}
File Size: {file_info['size_mb']:.2f} MB
Readable: {'Yes' if file_info['is_readable'] else 'No'}
            """.strip()

            self.file_info_text.setText(info_text)

            # Try to load preview
            self.load_preview(filepath)

            # Enable buttons
            self.import_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)
        else:
            self.file_info_text.setText('Could not read file information')
            self.import_btn.setEnabled(False)

    def load_preview(self, filepath):
        """Load a preview of the file data."""
        try:
            # Quick validation
            is_valid, error = FileHandler.validate_file(filepath)

            if not is_valid:
                self.preview_text.setText(f'Cannot preview: {error}')
                return

            # Import file (limited preview)
            df, error = FileHandler.import_file(filepath)

            if df is not None:
                # Show first 10 rows
                preview = df.head(10).to_string()
                row_count = len(df)
                col_count = len(df.columns)

                preview_text = f"""
Dataset: {row_count} rows × {col_count} columns

First 10 rows:
{preview}
                """.strip()

                self.preview_text.setText(preview_text)
            else:
                self.preview_text.setText(f'Preview error: {error}')

        except Exception as e:
            self.preview_text.setText(f'Could not generate preview: {str(e)}')

    def import_file(self):
        """Import the selected file."""
        if not self.current_file:
            QMessageBox.warning(self, 'No File', 'Please select a file to import')
            return

        # Disable buttons during import
        self.import_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Start import thread
        self.import_thread = FileImportThread(self.current_file)
        self.import_thread.importComplete.connect(self.on_import_complete)
        self.import_thread.importFailed.connect(self.on_import_failed)
        self.import_thread.progressUpdate.connect(self.progress_bar.setValue)
        self.import_thread.start()

    def on_import_complete(self, df, filename):
        """Handle successful import."""
        # Update data manager
        self.data_manager.set_data(df, filename)

        # Hide progress bar
        self.progress_bar.setVisible(False)

        # Show success message
        QMessageBox.information(
            self,
            'Import Successful',
            f'Successfully imported {len(df)} rows from:\n{filename}'
        )

        # Emit signal
        self.dataImported.emit(filename)

        # Reset UI
        self.clear_selection()

    def on_import_failed(self, error):
        """Handle import failure."""
        self.progress_bar.setVisible(False)
        self.import_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)

        QMessageBox.critical(
            self,
            'Import Failed',
            f'Failed to import file:\n{error}'
        )

    def on_data_loaded(self, filename):
        """Handle data loaded signal from DataManager."""
        pass  # Already handled in on_import_complete

    def on_error(self, error):
        """Handle error signal from DataManager."""
        QMessageBox.warning(self, 'Error', error)

    def clear_selection(self):
        """Clear current selection and reset UI."""
        self.current_file = None
        self.file_path_label.setText('No file selected')
        self.file_info_text.setText('No file information available')
        self.preview_text.setText('No data to preview')
        self.import_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
