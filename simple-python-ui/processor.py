"""
Text processing module for Simple Python UI
Contains the processing logic that can be easily swapped out

EXTENSIBILITY:
To customize the processing logic, simply modify the process_text() function.
The function contract is:
  - Input: str (the text to process)
  - Output: str (the processed text)
  - Raises: Exception if processing fails

Examples of alternative implementations:
  - Text reversal: return input_text[::-1]
  - Lowercase: return input_text.lower()
  - Word count: return f"Word count: {len(input_text.split())}"
  - ROT13: return input_text.encode('rot13')
"""


def process_text(input_text: str) -> str:
    """
    Process input text and return the result.

    Default implementation: Convert text to uppercase.

    Args:
        input_text: The text to process. Must be a non-empty string.

    Returns:
        str: The processed text (uppercase version of input)

    Raises:
        ValueError: If input_text is empty or invalid
        Exception: If processing fails for any other reason

    Examples:
        >>> process_text("hello world")
        'HELLO WORLD'
        >>> process_text("Python 3.10+")
        'PYTHON 3.10+'
    """
    if not input_text or not isinstance(input_text, str):
        raise ValueError("Input must be a non-empty string")

    # Default implementation: uppercase conversion
    return input_text.upper()


# Additional helper functions can be added here if needed
# For example:
# def validate_input(text: str) -> bool:
#     """Validate input text before processing"""
#     return bool(text and text.strip())
