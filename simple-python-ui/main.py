#!/usr/bin/env python3
"""
Simple Python UI Tool
A lightweight tkinter-based text processing application
"""

import tkinter as tk
from processor import process_text


def main():
    """Create and run the main application window"""
    # Create main window
    root = tk.Tk()
    root.title("Simple Python UI Tool")
    root.geometry("800x600")
    root.minsize(400, 300)

    # Add title label
    title_label = tk.Label(root, text="Text Processing Tool",
                           font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Add input section
    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(input_frame, text="Input:").pack(anchor=tk.W)
    input_entry = tk.Entry(input_frame, font=("Arial", 12))
    input_entry.pack(fill=tk.X)

    # Add execute button
    execute_btn = tk.Button(root, text="Execute",
                            font=("Arial", 12),
                            width=20, height=2)
    execute_btn.pack(pady=20)

    # Add result display
    result_frame = tk.Frame(root)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    tk.Label(result_frame, text="Result:").pack(anchor=tk.W)
    result_text = tk.Text(result_frame, font=("Arial", 11),
                          height=10, state='disabled')
    result_text.pack(fill=tk.BOTH, expand=True)

    # Add status bar
    status_bar = tk.Label(root, text="Idle",
                          bd=1, relief=tk.SUNKEN,
                          anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()
