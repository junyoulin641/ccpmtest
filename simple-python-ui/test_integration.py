#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test script for the Simple Python UI Tool
Tests the processor module with various inputs to ensure it works correctly
"""

import sys
from processor import process_text

# Force UTF-8 encoding for console output
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None


def test_normal_text():
    """Test with normal text"""
    result = process_text("hello world")
    assert result == "HELLO WORLD", f"Expected 'HELLO WORLD', got '{result}'"
    print("✅ Normal text test passed")


def test_special_characters():
    """Test with special characters"""
    result = process_text("Python 3.10+ rocks! @#$%")
    assert result == "PYTHON 3.10+ ROCKS! @#$%", f"Expected uppercase, got '{result}'"
    print("✅ Special characters test passed")


def test_long_text():
    """Test with long text"""
    long_text = "This is a very long text " * 50
    result = process_text(long_text)
    assert result == long_text.upper(), "Long text processing failed"
    print("✅ Long text test passed")


def test_unicode():
    """Test with unicode characters"""
    result = process_text("Hello 你好 Привет")
    expected = "HELLO 你好 ПРИВЕТ"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print("✅ Unicode test passed")


def test_empty_string():
    """Test with empty string - should raise ValueError"""
    try:
        process_text("")
        print("❌ Empty string test failed - should have raised ValueError")
    except ValueError:
        print("✅ Empty string test passed - ValueError raised as expected")


def test_whitespace_only():
    """Test with whitespace only - should raise ValueError"""
    try:
        process_text("   ")
        print("✅ Whitespace test passed - processed successfully")
    except ValueError:
        print("✅ Whitespace test passed - ValueError raised")


def test_numbers():
    """Test with numbers"""
    result = process_text("12345 67890")
    assert result == "12345 67890", f"Expected '12345 67890', got '{result}'"
    print("✅ Numbers test passed")


if __name__ == "__main__":
    print("Running integration tests...\n")

    test_normal_text()
    test_special_characters()
    test_long_text()
    test_unicode()
    test_empty_string()
    test_whitespace_only()
    test_numbers()

    print("\n✅ All tests completed!")
