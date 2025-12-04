# PyQt Data Visualization Dashboard

A desktop data visualization and analysis application built with PyQt5.

## Features

- Import data from CSV, Excel, and JSON files
- Interactive table view with sorting and filtering
- Multiple chart types (line, bar, scatter, pie)
- Dashboard with summary statistics
- Export data and charts in various formats

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation

1. Clone the repository or extract the project files

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

## Project Structure

```
python-ui-test/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore patterns
├── ui/                    # User interface modules
├── core/                  # Core business logic
├── utils/                 # Utility functions
└── resources/             # Icons and styles
    ├── icons/
    └── styles/
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project follows PEP 8 style guidelines.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
