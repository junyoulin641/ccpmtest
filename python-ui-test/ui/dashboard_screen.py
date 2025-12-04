"""
Dashboard Screen showing data overview and summary statistics.

Provides at-a-glance insights with KPI cards, statistics tables, and mini charts.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from core.data_manager import DataManager


class KPICard(QFrame):
    """
    KPI Card widget for displaying key metrics.

    Shows a title and large value with professional styling.
    """

    def __init__(self, title, value="--", icon=None):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet("""
            KPICard {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            font-size: 12px;
            color: #666;
            font-weight: 500;
            border: none;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            border: none;
        """)
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)

        self.setLayout(layout)
        self.setMinimumHeight(100)

    def update_value(self, new_value):
        """Update the displayed value."""
        self.value_label.setText(str(new_value))


class DashboardScreen(QWidget):
    """
    Dashboard overview screen with summary statistics and KPIs.

    Features:
    - KPI cards (rows, columns, memory, missing values)
    - Summary statistics table
    - Data preview (top 5 rows)
    - Data types distribution chart
    - File information panel
    """

    screen_name = 'Dashboard'

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.init_ui()
        self.connect_signals()

        # Load initial data if available
        if self.data_manager.has_data():
            self.refresh_dashboard()
        else:
            self.show_empty_state()

    def init_ui(self):
        """Initialize the user interface."""
        # Main scroll area to handle large content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        # Container widget for scroll area
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        header = self.create_header()
        main_layout.addLayout(header)

        # KPI Cards
        kpi_layout = self.create_kpi_cards()
        main_layout.addLayout(kpi_layout)

        # Middle section: Statistics and Charts
        middle_layout = QHBoxLayout()

        # Left panel (60%)
        left_panel = self.create_left_panel()
        middle_layout.addWidget(left_panel, 6)

        # Right panel (40%)
        right_panel = self.create_right_panel()
        middle_layout.addWidget(right_panel, 4)

        main_layout.addLayout(middle_layout)

        # Push content to top
        main_layout.addStretch()

        scroll.setWidget(container)

        # Set main layout
        final_layout = QVBoxLayout()
        final_layout.setContentsMargins(0, 0, 0, 0)
        final_layout.addWidget(scroll)
        self.setLayout(final_layout)

    def create_header(self):
        """Create header with title and timestamp."""
        layout = QHBoxLayout()

        # Title
        title = QLabel('Dashboard Overview')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)

        layout.addStretch()

        # Timestamp
        self.timestamp_label = QLabel('Last Updated: --')
        self.timestamp_label.setStyleSheet('color: #666; font-size: 12px;')
        layout.addWidget(self.timestamp_label)

        return layout

    def create_kpi_cards(self):
        """Create KPI cards row."""
        layout = QHBoxLayout()
        layout.setSpacing(15)

        # Create KPI cards
        self.rows_card = KPICard('Total Rows', '--')
        self.cols_card = KPICard('Columns', '--')
        self.memory_card = KPICard('Memory Usage', '--')
        self.missing_card = KPICard('Missing Values', '--')

        layout.addWidget(self.rows_card)
        layout.addWidget(self.cols_card)
        layout.addWidget(self.memory_card)
        layout.addWidget(self.missing_card)

        return layout

    def create_left_panel(self):
        """Create left panel with statistics and preview."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        # Summary Statistics
        stats_group = QGroupBox('Summary Statistics')
        stats_layout = QVBoxLayout()
        self.stats_table = QTableWidget()
        self.stats_table.setMaximumHeight(250)
        self.stats_table.setAlternatingRowColors(True)
        stats_layout.addWidget(self.stats_table)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Data Preview
        preview_group = QGroupBox('Data Preview (Top 5 Rows)')
        preview_layout = QVBoxLayout()
        self.preview_table = QTableWidget()
        self.preview_table.setMaximumHeight(200)
        self.preview_table.setAlternatingRowColors(True)
        preview_layout.addWidget(self.preview_table)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        return panel

    def create_right_panel(self):
        """Create right panel with charts and file info."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        # Data Types Chart
        chart_group = QGroupBox('Data Types Distribution')
        chart_layout = QVBoxLayout()
        self.chart_widget = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_widget)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.addWidget(self.chart_widget)
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)

        # File Info
        info_group = QGroupBox('File Information')
        info_layout = QVBoxLayout()
        self.file_info_label = QLabel('No file loaded')
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setStyleSheet('padding: 10px; font-family: monospace;')
        info_layout.addWidget(self.file_info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Missing Values Info
        missing_group = QGroupBox('Missing Values Details')
        missing_layout = QVBoxLayout()
        self.missing_info_label = QLabel('No missing values')
        self.missing_info_label.setWordWrap(True)
        self.missing_info_label.setStyleSheet('padding: 10px; font-size: 12px;')
        missing_layout.addWidget(self.missing_info_label)
        missing_group.setLayout(missing_layout)
        layout.addWidget(missing_group)

        layout.addStretch()

        return panel

    def connect_signals(self):
        """Connect signals from DataManager."""
        self.data_manager.dataLoaded.connect(self.on_data_loaded)
        self.data_manager.dataCleared.connect(self.on_data_cleared)
        self.data_manager.dataModified.connect(self.refresh_dashboard)

    def on_data_loaded(self, filename):
        """Handle data loaded signal."""
        self.refresh_dashboard()

    def on_data_cleared(self):
        """Handle data cleared signal."""
        self.show_empty_state()

    def refresh_dashboard(self):
        """Refresh all dashboard components."""
        df = self.data_manager.get_data()

        if df is None or df.empty:
            self.show_empty_state()
            return

        # Update timestamp
        self.timestamp_label.setText(
            f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )

        # Update all components
        self.update_kpis(df)
        self.update_statistics_table(df)
        self.update_data_preview(df)
        self.update_datatypes_chart(df)
        self.update_file_info()
        self.update_missing_values_info(df)

    def update_kpis(self, df):
        """Update KPI cards."""
        # Row count
        row_count = len(df)
        self.rows_card.update_value(f'{row_count:,}')

        # Column count
        col_count = len(df.columns)
        self.cols_card.update_value(col_count)

        # Memory usage
        memory_bytes = df.memory_usage(deep=True).sum()
        memory_mb = memory_bytes / (1024 ** 2)
        if memory_mb < 1:
            memory_str = f'{memory_bytes / 1024:.1f} KB'
        else:
            memory_str = f'{memory_mb:.2f} MB'
        self.memory_card.update_value(memory_str)

        # Missing values
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            total_cells = df.size
            missing_pct = (missing_count / total_cells) * 100
            missing_str = f'{missing_count:,} ({missing_pct:.1f}%)'
        else:
            missing_str = '0'
        self.missing_card.update_value(missing_str)

    def update_statistics_table(self, df):
        """Update summary statistics table."""
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if not numeric_cols:
            self.stats_table.clear()
            self.stats_table.setRowCount(1)
            self.stats_table.setColumnCount(1)
            self.stats_table.setItem(0, 0, QTableWidgetItem('No numeric columns'))
            return

        # Calculate statistics
        stats_df = df[numeric_cols].describe()

        # Set table dimensions
        self.stats_table.setRowCount(len(stats_df))
        self.stats_table.setColumnCount(len(numeric_cols))
        self.stats_table.setHorizontalHeaderLabels(numeric_cols)
        self.stats_table.setVerticalHeaderLabels(stats_df.index.tolist())

        # Populate table
        for i, row_name in enumerate(stats_df.index):
            for j, col_name in enumerate(numeric_cols):
                value = stats_df.loc[row_name, col_name]
                # Format based on row type
                if row_name == 'count':
                    formatted = f'{int(value):,}'
                else:
                    formatted = f'{value:.2f}'

                item = QTableWidgetItem(formatted)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.stats_table.setItem(i, j, item)

        # Adjust column widths
        self.stats_table.resizeColumnsToContents()

    def update_data_preview(self, df):
        """Update data preview table."""
        preview_df = df.head(5)

        # Set table dimensions
        self.preview_table.setRowCount(min(5, len(df)))
        self.preview_table.setColumnCount(len(df.columns))
        self.preview_table.setHorizontalHeaderLabels(df.columns.tolist())

        # Populate table
        for i in range(len(preview_df)):
            for j, col in enumerate(df.columns):
                value = preview_df.iloc[i, j]
                # Handle NaN
                if pd.isna(value):
                    display_value = 'NaN'
                else:
                    display_value = str(value)

                item = QTableWidgetItem(display_value)
                self.preview_table.setItem(i, j, item)

        # Adjust column widths
        self.preview_table.resizeColumnsToContents()

    def update_datatypes_chart(self, df):
        """Update data types distribution chart."""
        # Clear previous chart
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Count data types
        type_counts = df.dtypes.value_counts()

        # Create matplotlib figure
        fig = Figure(figsize=(4, 4))
        ax = fig.add_subplot(111)

        # Create pie chart
        colors = plt.cm.Set3(range(len(type_counts)))
        wedges, texts, autotexts = ax.pie(
            type_counts.values,
            labels=[str(t) for t in type_counts.index],
            autopct='%1.0f%%',
            startangle=90,
            colors=colors
        )

        # Style text
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        ax.set_title('Data Types', fontsize=12, fontweight='bold')
        fig.tight_layout()

        # Add to widget
        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)

    def update_file_info(self):
        """Update file information display."""
        filename = self.data_manager.filename

        if filename:
            info_text = f"""
<b>File:</b> {filename}

<b>Loaded:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """.strip()
        else:
            info_text = 'No file information available'

        self.file_info_label.setText(info_text)

    def update_missing_values_info(self, df):
        """Update missing values information."""
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]

        if len(missing_cols) > 0:
            info_lines = ['<b>Columns with missing values:</b>']
            for col, count in missing_cols.items():
                pct = (count / len(df)) * 100
                info_lines.append(f'• {col}: {count:,} ({pct:.1f}%)')
            info_text = '<br>'.join(info_lines)
        else:
            info_text = '<b>No missing values detected</b>'

        self.missing_info_label.setText(info_text)

    def show_empty_state(self):
        """Show empty state when no data is loaded."""
        # Clear KPI cards
        self.rows_card.update_value('--')
        self.cols_card.update_value('--')
        self.memory_card.update_value('--')
        self.missing_card.update_value('--')

        # Clear tables
        self.stats_table.clear()
        self.stats_table.setRowCount(0)
        self.stats_table.setColumnCount(0)

        self.preview_table.clear()
        self.preview_table.setRowCount(0)
        self.preview_table.setColumnCount(0)

        # Clear chart
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Show empty message in chart area
        empty_label = QLabel('No data to display')
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet('color: #999; font-size: 14px; padding: 50px;')
        self.chart_layout.addWidget(empty_label)

        # Update info labels
        self.file_info_label.setText('No file loaded')
        self.missing_info_label.setText('Load data to see missing value analysis')
        self.timestamp_label.setText('Last Updated: --')
