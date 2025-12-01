# Simple Python UI

A lightweight, standalone Python UI toolkit for text processing operations built with tkinter.

## Overview

Simple Python UI provides a clean, reusable template for building quick text processing tools with a graphical interface. It features a simple architecture that separates UI from processing logic, making it easy to customize for different use cases.

**Key Features:**
- Zero external dependencies (uses only Python standard library)
- Cross-platform (Windows, macOS, Linux)
- Easy to customize processing logic
- Clean, functional interface
- Extensible design

## Requirements

- Python 3.10 or higher
- tkinter (included with standard Python installation)

**Note:** On some Linux distributions, tkinter may need to be installed separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Installation

No installation required! Simply clone or download the project:

```bash
git clone <repository-url>
cd simple-python-ui
```

## Usage

Run the application:

```bash
python main.py
```

**Basic Workflow:**
1. Launch the application
2. Enter text in the input field
3. Click the "Execute" button
4. View the processed result below

## Customizing Processing Logic

The default implementation converts text to uppercase. To customize the processing logic, edit the `process_text()` function in `processor.py`:

### Example 1: Text Reversal
```python
def process_text(input_text: str) -> str:
    """Reverse the input text"""
    if not input_text or not isinstance(input_text, str):
        raise ValueError("Input must be a non-empty string")

    return input_text[::-1]
```

### Example 2: Word Count
```python
def process_text(input_text: str) -> str:
    """Count words in the input text"""
    if not input_text or not isinstance(input_text, str):
        raise ValueError("Input must be a non-empty string")

    word_count = len(input_text.split())
    char_count = len(input_text)

    return f"Words: {word_count}\nCharacters: {char_count}"
```

### Example 3: Simple Calculator
```python
def process_text(input_text: str) -> str:
    """Evaluate a simple math expression"""
    if not input_text or not isinstance(input_text, str):
        raise ValueError("Input must be a non-empty string")

    try:
        result = eval(input_text)
        return f"Result: {result}"
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")
```

**Important:** Keep the function signature as `(str) -> str` and raise exceptions for errors.

## Project Structure

```
simple-python-ui/
├── main.py          # UI layer (tkinter widgets and event handlers)
├── processor.py     # Processing logic (easily customizable)
└── README.md        # This file
```

## Troubleshooting

### "No module named 'tkinter'"
- Tkinter is not installed. See Requirements section for installation instructions.

### "No module named 'processor'"
- Make sure you're running `python main.py` from the project directory.

### Processing errors not displaying
- Check that your `process_text()` function raises exceptions with descriptive messages.

### Window doesn't resize properly
- This is expected on some window managers. The app is designed for 800x600 but should adapt.

## Contributing

This is a personal tool template, but feel free to fork and customize for your needs!

## License

MIT License - feel free to use and modify.

## Future Enhancements

Potential features for future versions:
- Multiple processing modes (dropdown selector)
- History of previous operations
- Copy to clipboard functionality
- Dark mode theme
- Keyboard shortcuts

---

**Built with Python and tkinter**
