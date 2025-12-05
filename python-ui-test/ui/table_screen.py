"""
Table View Screen for displaying and manipulating data.

Provides a comprehensive table view with sorting, filtering, pagination,
and export functionality.
"""

import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTableView, QHeaderView, QFileDialog,
    QMessageBox, QAbstractItemView
)
from PyQt5.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, QVariant, QTimer, pyqtSignal
)
from PyQt5.QtGui import QFont

from core.data_manager import DataManager
from core.file_handler import FileHandler


class PandasTableModel(QAbstractTableModel):
    """
    Custom table model for displaying pandas DataFrames in QTableView.

    Supports sorting, filtering, and pagination for large datasets.
    """

    def __init__(self, data=None):
        super().__init__()
        self._data = data if data is not None else pd.DataFrame()
        self._filtered_data = self._data.copy()
        self._display_data = self._filtered_data.copy()

        # Pagination settings
        self.page_size = 10000
        self.current_page = 0
        self.pagination_enabled = False

        # Sort settings
        self._sort_column = None
        self._sort_order = Qt.AscendingOrder

    def rowCount(self, parent=QModelIndex()):
        """Return number of rows in current display data."""
        if parent.isValid():
            return 0
        return len(self._display_data)

    def columnCount(self, parent=QModelIndex()):
        """Return number of columns."""
        if parent.isValid():
            return 0
        return len(self._display_data.columns) if not self._display_data.empty else 0

    def data(self, index, role=Qt.DisplayRole):
        """Return data for a specific cell."""
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            try:
                value = self._display_data.iloc[index.row(), index.column()]
                # Handle NaN and None
                if pd.isna(value):
                    return ""
                return str(value)
            except (IndexError, KeyError):
                return QVariant()

        elif role == Qt.TextAlignmentRole:
            # Right-align numeric columns
            try:
                value = self._display_data.iloc[index.row(), index.column()]
                if isinstance(value, (int, float)) and not pd.isna(value):
                    return Qt.AlignRight | Qt.AlignVCenter
            except (IndexError, KeyError):
                pass
            return Qt.AlignLeft | Qt.AlignVCenter

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Return header data."""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self._display_data.columns):
                    return str(self._display_data.columns[section])
            else:
                # Show actual row numbers from filtered data
                if section < len(self._display_data):
                    return str(self._display_data.index[section] + 1)
        return QVariant()

    def sort(self, column, order=Qt.AscendingOrder):
        """Sort data by column."""
        if self._filtered_data.empty or column >= len(self._filtered_data.columns):
            return

        self.layoutAboutToBeChanged.emit()

        try:
            col_name = self._filtered_data.columns[column]
            ascending = (order == Qt.AscendingOrder)

            self._filtered_data = self._filtered_data.sort_values(
                by=col_name,
                ascending=ascending
            )

            self._sort_column = column
            self._sort_order = order

            # Update display data for current page
            self._update_display_data()

        except Exception as e:
            print(f"Sort error: {e}")

        self.layoutChanged.emit()

    def set_data(self, dataframe):
        """Set new DataFrame data."""
        self.beginResetModel()

        self._data = dataframe.copy() if dataframe is not None else pd.DataFrame()
        self._filtered_data = self._data.copy()

        # Reset pagination
        self.current_page = 0
        self.pagination_enabled = len(self._filtered_data) > self.page_size

        # Reset sort
        self._sort_column = None
        self._sort_order = Qt.AscendingOrder

        self._update_display_data()
        self.endResetModel()

    def filter_data(self, search_text):
        """Filter data based on search text."""
        self.beginResetModel()

        if not search_text or self._data.empty:
            self._filtered_data = self._data.copy()
        else:
            try:
                # Search across all columns (case-insensitive)
                mask = self._data.astype(str).apply(
                    lambda x: x.str.contains(search_text, case=False, na=False)
                ).any(axis=1)
                self._filtered_data = self._data[mask].copy()
            except Exception as e:
                print(f"Filter error: {e}")
                self._filtered_data = self._data.copy()

        # Reset to first page after filtering
        self.current_page = 0
        self.pagination_enabled = len(self._filtered_data) > self.page_size

        # Reapply sort if there was one
        if self._sort_column is not None:
            try:
                col_name = self._filtered_data.columns[self._sort_column]
                ascending = (self._sort_order == Qt.AscendingOrder)
                self._filtered_data = self._filtered_data.sort_values(
                    by=col_name,
                    ascending=ascending
                )
            except Exception:
                pass

        self._update_display_data()
        self.endResetModel()

    def _update_display_data(self):
        """Update display data based on current page."""
        if self.pagination_enabled:
            start_idx = self.current_page * self.page_size
            end_idx = start_idx + self.page_size
            self._display_data = self._filtered_data.iloc[start_idx:end_idx].copy()
        else:
            self._display_data = self._filtered_data.copy()

    def get_page_count(self):
        """Return total number of pages."""
        if not self.pagination_enabled or self._filtered_data.empty:
            return 1
        return (len(self._filtered_data) - 1) // self.page_size + 1

    def go_to_page(self, page_number):
        """Navigate to a specific page."""
        if 0 <= page_number < self.get_page_count():
            self.beginResetModel()
            self.current_page = page_number
            self._update_display_data()
            self.endResetModel()
            return True
        return False

    def get_filtered_data(self):
        """Return the complete filtered DataFrame."""
        return self._filtered_data.copy()

    def get_total_rows(self):
        """Return total rows in original data."""
        return len(self._data)

    def get_filtered_rows(self):
        """Return number of filtered rows."""
        return len(self._filtered_data)


class TableScreen(QWidget):
    """
    Screen for displaying data in a table view.

    Features:
    - Sortable columns
    - Search/filter functionality
    - Pagination for large datasets
    - Row selection
    - Export filtered data
    """

    screen_name = 'Table View'

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.model = PandasTableModel()
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)

        self.init_ui()
        self.connect_signals()

        # Load initial data if available
        if self.data_manager.has_data():
            self.refresh_table()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel('Table View')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)

        # Top bar with search and export
        top_bar = self.create_top_bar()
        layout.addLayout(top_bar)

        # Table view
        self.table_view = self.create_table_view()
        layout.addWidget(self.table_view, 1)

        # Pagination bar
        self.pagination_bar = self.create_pagination_bar()
        layout.addLayout(self.pagination_bar)
        self.update_pagination_visibility()

        self.setLayout(layout)

    def create_top_bar(self):
        """Create top bar with search and controls."""
        layout = QHBoxLayout()

        # Search box
        search_label = QLabel('Search:')
        layout.addWidget(search_label)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Type to filter data...')
        self.search_box.setMinimumWidth(300)
        self.search_box.textChanged.connect(self.on_search_text_changed)
        layout.addWidget(self.search_box)

        layout.addStretch()

        # Row count label
        self.row_count_label = QLabel('Rows: 0 / 0')
        self.row_count_label.setStyleSheet('color: #666; font-size: 14px;')
        layout.addWidget(self.row_count_label)

        # Export button
        self.export_btn = QPushButton('Export Data')
        self.export_btn.setMinimumWidth(120)
        self.export_btn.clicked.connect(self.export_data)
        self.export_btn.setEnabled(False)
        self.export_btn.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        layout.addWidget(self.export_btn)

        return layout

    def create_table_view(self):
        """Create and configure the table view."""
        table = QTableView()
        table.setModel(self.model)

        # Appearance
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableView {
                gridline-color: #d0d0d0;
                background-color: white;
            }
            QTableView::item {
                padding: 5px;
            }
            QTableView::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        # Selection
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Sorting
        table.setSortingEnabled(True)

        # Headers
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        table.verticalHeader().setVisible(True)
        table.verticalHeader().setDefaultSectionSize(30)

        return table

    def create_pagination_bar(self):
        """Create pagination controls."""
        layout = QHBoxLayout()
        layout.addStretch()

        # First page button
        self.first_page_btn = QPushButton('⏮ First')
        self.first_page_btn.clicked.connect(self.go_first_page)
        layout.addWidget(self.first_page_btn)

        # Previous button
        self.prev_page_btn = QPushButton('⏪ Previous')
        self.prev_page_btn.clicked.connect(self.go_previous_page)
        layout.addWidget(self.prev_page_btn)

        # Page label
        self.page_label = QLabel('Page 1 of 1')
        self.page_label.setMinimumWidth(100)
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(self.page_label)

        # Next button
        self.next_page_btn = QPushButton('Next ⏩')
        self.next_page_btn.clicked.connect(self.go_next_page)
        layout.addWidget(self.next_page_btn)

        # Last page button
        self.last_page_btn = QPushButton('Last ⏭')
        self.last_page_btn.clicked.connect(self.go_last_page)
        layout.addWidget(self.last_page_btn)

        layout.addStretch()

        # Style buttons
        button_style = """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:disabled {
                background-color: #d0d0d0;
            }
        """
        for btn in [self.first_page_btn, self.prev_page_btn,
                    self.next_page_btn, self.last_page_btn]:
            btn.setStyleSheet(button_style)

        return layout

    def connect_signals(self):
        """Connect signals from DataManager."""
        self.data_manager.dataLoaded.connect(self.on_data_loaded)
        self.data_manager.dataCleared.connect(self.on_data_cleared)
        self.data_manager.dataModified.connect(self.refresh_table)

    def on_data_loaded(self, filename):
        """Handle data loaded signal."""
        self.refresh_table()

    def on_data_cleared(self):
        """Handle data cleared signal."""
        self.model.set_data(pd.DataFrame())
        self.update_row_count_label()
        self.update_pagination_buttons()
        self.export_btn.setEnabled(False)

    def refresh_table(self):
        """Refresh table with current data from DataManager."""
        df = self.data_manager.get_data()
        if df is not None:
            self.model.set_data(df)
            self.update_row_count_label()
            self.update_pagination_visibility()
            self.update_pagination_buttons()
            self.export_btn.setEnabled(True)

            # Clear search box
            self.search_box.clear()

    def on_search_text_changed(self, text):
        """Handle search text changes with debouncing."""
        # Debounce: wait 300ms after user stops typing
        self.search_timer.stop()
        self.search_timer.start(300)

    def _perform_search(self):
        """Perform the actual search operation."""
        search_text = self.search_box.text().strip()
        self.model.filter_data(search_text)
        self.update_row_count_label()
        self.update_pagination_buttons()

    def update_row_count_label(self):
        """Update the row count label."""
        total = self.model.get_total_rows()
        filtered = self.model.get_filtered_rows()

        if total == filtered:
            self.row_count_label.setText(f'Rows: {total:,}')
        else:
            self.row_count_label.setText(f'Rows: {filtered:,} / {total:,}')

    def update_pagination_visibility(self):
        """Show/hide pagination controls based on data size."""
        visible = self.model.pagination_enabled

        for widget in [self.first_page_btn, self.prev_page_btn, self.page_label,
                       self.next_page_btn, self.last_page_btn]:
            widget.setVisible(visible)

    def update_pagination_buttons(self):
        """Update pagination button states."""
        if not self.model.pagination_enabled:
            return

        current_page = self.model.current_page
        total_pages = self.model.get_page_count()

        self.page_label.setText(f'Page {current_page + 1} of {total_pages}')

        self.first_page_btn.setEnabled(current_page > 0)
        self.prev_page_btn.setEnabled(current_page > 0)
        self.next_page_btn.setEnabled(current_page < total_pages - 1)
        self.last_page_btn.setEnabled(current_page < total_pages - 1)

    def go_first_page(self):
        """Navigate to first page."""
        if self.model.go_to_page(0):
            self.update_pagination_buttons()

    def go_previous_page(self):
        """Navigate to previous page."""
        if self.model.go_to_page(self.model.current_page - 1):
            self.update_pagination_buttons()

    def go_next_page(self):
        """Navigate to next page."""
        if self.model.go_to_page(self.model.current_page + 1):
            self.update_pagination_buttons()

    def go_last_page(self):
        """Navigate to last page."""
        last_page = self.model.get_page_count() - 1
        if self.model.go_to_page(last_page):
            self.update_pagination_buttons()

    def export_data(self):
        """Export filtered data to file."""
        df = self.model.get_filtered_data()

        if df.empty:
            QMessageBox.warning(self, 'No Data', 'No data to export')
            return

        # Get file path from user
        file_filter = FileHandler.get_export_filter()
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            'Export Data',
            '',
            file_filter
        )

        if not filepath:
            return

        # Export data
        success, error = FileHandler.export_file(df, filepath)

        if success:
            QMessageBox.information(
                self,
                'Export Successful',
                f'Exported {len(df)} rows to:\n{filepath}'
            )
        else:
            QMessageBox.critical(
                self,
                'Export Failed',
                f'Failed to export data:\n{error}'
            )
