---
name: python-ui-test
status: in-progress
created: 2025-12-04T07:05:29Z
progress: 87%
prd: .claude/prds/python-ui-test.md
github: https://github.com/junyoulin641/ccpmtest/issues/8
---

# Epic: PyQt Data Visualization Dashboard

## Overview

Build a desktop data visualization dashboard using PyQt5/PySide6 with 6+ screens for data import, visualization, and analysis. The application uses a Model-View architecture with pandas for data processing and matplotlib for charting, targeting datasets up to 100k rows with sub-second performance.

## Architecture Decisions

**GUI Framework: PyQt5**
- Rationale: Mature, well-documented, cross-platform Qt bindings
- Alternative considered: PySide6 (Qt official bindings) - both acceptable
- Trade-off: PyQt5 has better community resources

**Visualization Library: matplotlib**
- Rationale: Native Qt integration, widely used, flexible
- Alternative considered: pyqtgraph (faster) - reserved for future optimization
- Trade-off: matplotlib slower but easier to customize

**Data Management: pandas**
- Rationale: Industry standard for tabular data, excellent file I/O
- Built-in CSV/Excel support through pandas.read_csv/read_excel
- DataFrame provides filtering, sorting, and transformation

**Architecture Pattern: Model-View with Signal/Slot**
- Qt's Signal/Slot mechanism for event handling
- Separation: UI widgets (ui/), business logic (core/), utilities (utils/)
- Centralized data manager for state management

## Technical Approach

### Application Structure
```
python-ui-test/
├── main.py                    # Entry point, QApplication setup
├── requirements.txt           # Dependencies
├── ui/
│   ├── main_window.py        # Main container with QStackedWidget
│   ├── dashboard_screen.py   # Dashboard with KPI widgets
│   ├── import_screen.py      # File import with QFileDialog
│   ├── table_screen.py       # QTableView with pandas model
│   ├── viz_screen.py         # Matplotlib FigureCanvas
│   ├── settings_screen.py    # Configuration panel
│   └── export_screen.py      # Export controls
├── core/
│   ├── data_manager.py       # Centralized DataFrame storage
│   ├── file_handler.py       # File I/O with validation
│   └── chart_builder.py      # Matplotlib chart generation
└── utils/
    └── validators.py         # Input validation helpers
```

### Core Components

**Main Window (QMainWindow)**
- QStackedWidget for screen switching
- QMenuBar with File/Edit/View/Tools/Help menus
- QToolBar with navigation buttons
- QStatusBar for state messages
- Left sidebar with QPushButton navigation

**Data Manager (Singleton)**
- Holds current DataFrame in memory
- Emits signals on data changes (loaded, filtered, sorted)
- Provides methods: load_file(), get_data(), filter_data(), export_data()
- Thread safety for background operations

**File Handler**
- Support formats: CSV (pandas.read_csv), Excel (openpyxl), JSON (pandas.read_json)
- QFileDialog for file selection
- Validation: file size limits, format verification
- Error handling with user-friendly QMessageBox

**Table View**
- QTableView with QAbstractTableModel (pandas adapter)
- Sortable columns via header clicks
- Search/filter with QLineEdit
- Pagination for >10k rows using model slicing

**Chart Builder**
- FigureCanvas (matplotlib) embedded in QWidget
- Chart types: line (plot), bar (bar), scatter (scatter), pie (pie)
- Interactive NavigationToolbar for zoom/pan
- Export to PNG via savefig()

### UI/UX Patterns

**Navigation**
- Sidebar with 6 navigation buttons (Dashboard, Import, Table, Visualize, Settings, Export)
- Highlight active screen with QSS styling
- Keyboard shortcuts: Ctrl+1 through Ctrl+6

**Data Flow**
1. User imports file → File Handler validates → Data Manager loads DataFrame
2. Data Manager emits dataChanged signal → All screens refresh
3. User creates chart → Chart Builder reads from Data Manager → Renders to canvas
4. User exports → Export Screen reads Data Manager → File Handler saves

**Error Handling**
- Try/except blocks with specific error messages
- QMessageBox for user notifications (critical, warning, info)
- Logging to file for debugging

## Implementation Strategy

### Phase 1: Foundation & Core (MVP)
**Goal**: Working application skeleton with data import and table view
- Set up project structure, requirements.txt
- Implement main window with navigation framework
- Create Data Manager singleton
- Build File Handler with CSV support
- Implement Table Screen with sortable view
- Basic error handling

### Phase 2: Visualization
**Goal**: Add charting capabilities
- Integrate matplotlib FigureCanvas
- Implement Chart Builder with 3 chart types (line, bar, scatter)
- Create Visualization Screen with chart type selector
- Add chart export to PNG

### Phase 3: Additional Screens & Polish
**Goal**: Complete remaining screens and UX refinements
- Implement Dashboard Screen with summary statistics
- Create Settings Screen (theme, preferences)
- Build Export Screen (multi-format export)
- Add keyboard shortcuts
- Improve styling with QSS

### Testing Approach
- Unit tests: pytest for core/ modules (data_manager, file_handler, chart_builder)
- Integration tests: pytest-qt for UI workflows
- Manual testing: Load 50k row CSV, verify performance <2s
- Platform testing: Windows, macOS, Linux

### Risk Mitigation
- **Risk**: Large datasets cause UI freezing
  - **Mitigation**: QThread for file loading, pagination for table view
- **Risk**: Matplotlib slow rendering
  - **Mitigation**: Lazy loading, cache rendered charts
- **Risk**: Cross-platform font/styling inconsistencies
  - **Mitigation**: Test early on all platforms, use QSS for consistent styling

## Task Breakdown Preview

Breaking this down into 8 focused tasks:

- [ ] **Project Setup**: Create project structure, requirements.txt, main.py entry point, QApplication boilerplate
- [ ] **Main Window & Navigation**: Implement QMainWindow with QStackedWidget, sidebar navigation, menu/toolbar/statusbar
- [ ] **Data Manager & File Import**: Build Data Manager singleton, File Handler with CSV/Excel support, validation
- [ ] **Table View Screen**: Create QTableView with pandas model adapter, sorting, filtering, search functionality
- [ ] **Chart Visualization Screen**: Integrate matplotlib FigureCanvas, implement line/bar/scatter charts, chart builder logic
- [ ] **Dashboard Screen**: Build overview screen with summary statistics, KPI widgets, data preview
- [ ] **Settings & Export Screens**: Implement settings panel and export functionality (CSV, Excel, PNG charts)
- [ ] **Testing & Documentation**: Write unit tests (pytest), integration tests (pytest-qt), README with setup instructions

Each task is self-contained and can be developed incrementally.

## Dependencies

**External Python Packages**
```
PyQt5>=5.15.0          # GUI framework
pandas>=1.3.0          # Data manipulation
matplotlib>=3.4.0      # Charting
openpyxl>=3.0.0        # Excel support
numpy>=1.21.0          # Numerical operations
pytest>=7.0.0          # Testing
pytest-qt>=4.0.0       # Qt testing
```

**System Requirements**
- Python 3.8+ installed
- Qt5 system libraries (usually included with PyQt5)
- 4GB RAM minimum
- 100MB disk space

**Development Tools**
- Qt Designer (optional, for visual UI design)
- Code editor with Python support

**No Internal Dependencies**
- Standalone application
- No database or backend services

## Success Criteria (Technical)

**Performance Benchmarks**
- Application launch: <3 seconds from cold start
- CSV import (50k rows): <2 seconds
- Table view rendering: <500ms initial load
- Chart generation: <1 second per chart
- Screen transitions: <200ms
- Memory usage: <500MB with 100k row dataset

**Quality Gates**
- Test coverage: >70% for core/ modules
- Zero critical bugs in file import/export
- All 6 screens functional and navigable
- Successful cross-platform testing on Windows/macOS/Linux
- No crashes during 1-hour stress test

**Acceptance Criteria**
- User can import CSV/Excel with visual confirmation
- Data displays correctly in sortable table
- User can create line/bar/scatter charts from data
- Charts are interactive (zoom/pan) and exportable
- Navigation between all 6 screens works smoothly
- Error messages are clear and actionable
- Application follows platform UI conventions

**Code Quality**
- Modular architecture with clear separation of concerns
- Consistent coding style (PEP 8)
- Comprehensive docstrings for public methods
- No hardcoded paths or magic numbers
- Proper exception handling throughout

## Estimated Effort

**Overall Complexity: Medium**
- 8 distinct implementation tasks
- Leverages mature libraries (PyQt5, pandas, matplotlib)
- Well-defined scope with clear exclusions

**Critical Path**
1. Project Setup → Main Window → Data Manager (Foundation)
2. Table View Screen (First functional screen)
3. Chart Visualization (Core value delivery)
4. Remaining screens & testing (Completion)

**Resource Requirements**
- 1 developer with Python/PyQt experience
- Access to Windows/macOS/Linux for testing
- No external services or infrastructure needed

**Risk Areas Requiring Extra Time**
- Chart performance optimization (may need caching strategy)
- Cross-platform testing and bug fixes
- UX polish and styling consistency

**Delivery Milestones**
- Phase 1 (Foundation): Working import + table view
- Phase 2 (Visualization): Charts functional
- Phase 3 (Complete): All screens + polish + tests

## Tasks Created

- [ ] #9 - Project Setup and Structure (parallel: true)
- [ ] #10 - Main Window and Navigation Framework (parallel: false)
- [ ] #11 - Data Manager and File Import System (parallel: true)
- [ ] #12 - Table View Screen with Sorting and Filtering (parallel: false)
- [ ] #13 - Chart Visualization Screen (parallel: true)
- [ ] #14 - Dashboard Screen with Summary Statistics (parallel: true)
- [ ] #15 - Settings and Export Screens (parallel: true)
- [ ] #16 - Testing and Documentation (parallel: false)

Total tasks: 8
Parallel tasks: 5
Sequential tasks: 3
Estimated total effort: 77-94 hours
