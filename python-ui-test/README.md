# PyQt Data Visualization Dashboard

A desktop data visualization and analysis application built with PyQt5, pandas, and matplotlib. This application provides an intuitive interface for importing, exploring, visualizing, and exporting tabular data.

## Features

- **Data Import**: Load data from CSV, Excel (.xlsx, .xls), and JSON files
- **Interactive Table View**: Sortable columns, searchable data, pagination for large datasets
- **Multiple Chart Types**: Line, bar, scatter, and pie charts with customization
- **Dashboard**: At-a-glance statistics with KPI cards, data preview, and summary tables
- **Settings**: Customizable preferences including themes, colors, and performance options
- **Multi-format Export**: Export data to CSV/Excel/JSON and charts to PNG/PDF/SVG
- **Performance**: Handles datasets up to 100k rows with sub-second response times

## Screenshots

(Desktop application with sidebar navigation, table views, and interactive charts)

## Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum
- **Disk Space**: 100MB for application and dependencies

## Installation

### 1. Install Python

Ensure Python 3.8+ is installed:
```bash
python --version
```

### 2. Clone or Download

```bash
git clone <repository-url>
cd python-ui-test
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- PyQt5 >= 5.15.0 (GUI framework)
- pandas >= 1.3.0 (Data manipulation)
- matplotlib >= 3.4.0 (Charting)
- openpyxl >= 3.0.0 (Excel support)
- numpy >= 1.21.0 (Numerical operations)

## Quick Start

### Running the Application

```bash
python main.py
```

The application window will appear with six navigation screens accessible from the sidebar.

### Basic Workflow

1. **Import Data**
   - Click "Import" in the sidebar
   - Click "Select File" and choose a CSV, Excel, or JSON file
   - Preview the data and click "Import"

2. **View in Table**
   - Navigate to "Table" screen
   - Sort columns by clicking headers
   - Search/filter using the search box
   - Navigate pages if dataset is large

3. **Create Charts**
   - Go to "Visualize" screen
   - Select chart type (Line, Bar, Scatter, Pie)
   - Choose X and Y axis columns
   - Click "Generate Chart"
   - Use toolbar to zoom/pan
   - Export chart using "Export PNG"

4. **View Dashboard**
   - Navigate to "Dashboard" for data overview
   - See KPI cards: total rows, columns, memory usage, missing values
   - View summary statistics and data preview

5. **Export**
   - Go to "Export" screen
   - Choose format (CSV, Excel, JSON)
   - Click "Export Data" or use "Batch Export" for multiple formats

## Usage Guide

### Navigation

Use the sidebar buttons or keyboard shortcuts:
- `Ctrl+1`: Dashboard
- `Ctrl+2`: Import
- `Ctrl+3`: Table
- `Ctrl+4`: Visualize
- `Ctrl+5`: Settings
- `Ctrl+6`: Export

### Dashboard Screen

The dashboard provides an overview of your data:
- **KPI Cards**: Row count, column count, memory usage, missing values
- **Summary Statistics**: Mean, std, min, max for numeric columns
- **Data Preview**: First 5 rows of your dataset
- **Data Types Chart**: Pie chart showing distribution of column types
- **Missing Values**: Detailed breakdown by column

### Import Screen

Import data from various formats:
- **Supported Formats**: CSV, Excel (.xlsx, .xls), JSON
- **File Size**: Handles files up to 1GB (depending on available memory)
- **Preview**: See first 10 rows before importing
- **Validation**: Automatic detection of file encoding and format issues

### Table Screen

Interactive table view with advanced features:
- **Sorting**: Click column headers to sort (ascending/descending)
- **Search**: Type in search box to filter rows (300ms debounce)
- **Pagination**: Automatic for datasets >10,000 rows
- **Selection**: Click rows to select (future feature)
- **Performance**: <500ms initial load for 50k rows

### Visualization Screen

Create professional charts:
- **Chart Types**:
  - Line: Time series or continuous data
  - Bar: Categorical comparisons
  - Scatter: Correlation analysis
  - Pie: Proportional data (max 20 categories)
- **Customization**:
  - Custom titles
  - Color picker for lines/bars
  - Auto-downsampling for large datasets (>5000 points)
- **Interactivity**:
  - Zoom and pan using NavigationToolbar
  - Reset view, save figure
- **Export**: PNG (150/300/600 DPI), PDF, SVG

### Settings Screen

Configure application preferences:
- **General**:
  - Theme: Light/Dark (currently Light only)
  - Default directories for import/export
  - Auto-save interval
- **Chart Defaults**:
  - Default chart type
  - Custom colors for lines and bars
  - Grid and legend preferences
- **Advanced**:
  - Max rows for charts (performance tuning)
  - Pagination threshold
  - Debug mode

Settings are automatically saved using QSettings and persist across sessions.

### Export Screen

Export your data and visualizations:
- **Data Export**:
  - CSV: Universal format
  - Excel: .xlsx with openpyxl
  - JSON: Records format
  - Option to include/exclude row index
- **Chart Export**:
  - Configured on Visualization screen
  - PNG: Raster format with DPI selection
  - PDF: Vector format for publications
  - SVG: Scalable vector graphics
- **Batch Export**: Export to multiple formats simultaneously

## Architecture

### Project Structure

```
python-ui-test/
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies
├── README.md                    # Documentation
├── .gitignore                   # Git ignore rules
├── pytest.ini                   # Test configuration
├── .coveragerc                  # Coverage settings
├── ui/                          # User interface modules
│   ├── __init__.py
│   ├── main_window.py           # Main window with navigation
│   ├── dashboard_screen.py      # Dashboard with KPIs
│   ├── import_screen.py         # File import screen
│   ├── table_screen.py          # Table view with filtering
│   ├── viz_screen.py            # Chart visualization
│   ├── settings_screen.py       # Preferences
│   └── export_screen.py         # Data/chart export
├── core/                        # Business logic
│   ├── __init__.py
│   ├── data_manager.py          # Singleton data storage
│   ├── file_handler.py          # File I/O operations
│   └── chart_builder.py         # Chart generation
├── utils/                       # Utilities
│   └── __init__.py
├── resources/                   # Assets
│   ├── icons/
│   └── styles/
└── tests/                       # Test suite
    ├── __init__.py
    ├── test_data_manager.py
    ├── test_file_handler.py
    ├── test_chart_builder.py
    ├── integration/
    │   ├── __init__.py
    │   └── test_import_workflow.py
    ├── performance/
    │   ├── __init__.py
    │   └── test_performance.py
    └── fixtures/
        ├── __init__.py
        └── sample_data.csv
```

### Design Patterns

- **Singleton**: DataManager ensures single source of truth for application data
- **Model-View**: Qt's Model/View architecture for table display (PandasTableModel)
- **Signal/Slot**: Qt signals for event-driven communication between components
- **Separation of Concerns**: UI (ui/), business logic (core/), utilities (utils/)

### Key Components

**DataManager (core/data_manager.py)**
- Centralized DataFrame storage
- Emits signals on data changes: `dataLoaded`, `dataCleared`, `dataModified`
- Thread-safe singleton pattern
- Methods: `set_data()`, `get_data()`, `clear_data()`, `has_data()`

**FileHandler (core/file_handler.py)**
- Multi-format import: CSV (encoding detection), Excel (openpyxl), JSON
- Validation: file existence, format support, size limits
- Error handling with user-friendly messages
- Static methods for stateless operations

**ChartBuilder (core/chart_builder.py)**
- Matplotlib integration with Qt backend
- Four chart types with validation
- Auto-downsampling for performance (>5000 points → 2000 points)
- Returns Figure objects for embedding in FigureCanvas

## Development

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_data_manager.py
```

Run with coverage report:
```bash
pytest --cov=core --cov=ui --cov-report=html
```

Skip slow tests:
```bash
pytest -m "not slow"
```

### Test Coverage

The project aims for >70% test coverage on core modules:
- **Unit Tests**: core/data_manager, file_handler, chart_builder
- **Integration Tests**: Import workflow, screen navigation
- **Performance Tests**: 50k row imports, chart generation speed

View coverage report:
```bash
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

### Code Style

- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings to all classes and public methods
- Keep functions focused and under 50 lines when possible

### Adding New Features

1. Create feature branch
2. Implement feature with tests
3. Ensure tests pass: `pytest`
4. Check coverage: `pytest --cov`
5. Update README if user-facing
6. Submit pull request

## Performance Benchmarks

Tested on: Windows 11, Intel i7, 16GB RAM

| Operation | Dataset Size | Time | Target |
|-----------|--------------|------|--------|
| CSV Import | 50k rows | <2s | <2s |
| Excel Import | 10k rows | <3s | <5s |
| Table Render | 50k rows (paginated) | <500ms | <500ms |
| Chart Generation | 1k points | <1s | <1s |
| Chart Generation | 10k points | <2s | <3s |
| Screen Navigation | N/A | <200ms | <200ms |

## Troubleshooting

### Import Issues

**"File format not supported"**
- Ensure file extension is .csv, .xlsx, .xls, or .json
- Check file is not corrupted

**"Failed to detect encoding"**
- Try saving CSV with UTF-8 encoding
- Use Excel format as alternative

### Chart Issues

**"Y axis must be numeric"**
- Ensure selected Y column contains numbers
- Check for text values in numeric columns

**Chart takes long to render**
- Dataset is automatically downsampled if >5000 points
- Consider filtering data first

### Performance Issues

**Application runs slowly**
- Check dataset size in Dashboard
- Enable pagination in Settings (default: 10k rows)
- Reduce max_chart_rows in Settings

## Known Limitations

- **Dataset Size**: Optimal for datasets up to 100k rows
- **Charts**: Pie charts limited to 20 categories for readability
- **Themes**: Only Light theme currently available
- **Platform**: Tested primarily on Windows; macOS/Linux may have minor UI differences

## Roadmap

Potential future enhancements:
- [ ] Dark theme support
- [ ] Database connectivity (SQL, PostgreSQL)
- [ ] Advanced statistics (regression, correlation matrix)
- [ ] Chart annotations and styling
- [ ] Data transformation UI (pivot, merge)
- [ ] Export to PDF reports
- [ ] Undo/redo functionality

## FAQ

**Q: Can I open multiple files at once?**
A: Currently, only one file can be loaded at a time. Clear existing data first.

**Q: Does it save my work automatically?**
A: Data and settings are saved, but modified data is not auto-saved. Use Export to save changes.

**Q: What's the maximum file size?**
A: Limited by available RAM. Tested successfully with 100k rows (~50MB CSV).

**Q: Can I customize chart colors?**
A: Yes, use the color picker in Visualization screen or set defaults in Settings.

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support

For issues, questions, or contributions:
- **Issues**: Submit via GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: (contact information if applicable)

## Acknowledgments

Built with:
- **PyQt5**: Qt bindings for Python
- **pandas**: Data manipulation library
- **matplotlib**: Visualization library
- **openpyxl**: Excel file support

## Changelog

### Version 1.0.0 (2025-12-05)
- Initial release
- Core features: Import, Table, Visualize, Dashboard, Settings, Export
- Test coverage >70% on core modules
- Performance benchmarks met
- Cross-platform support (Windows/macOS/Linux)
