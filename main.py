#!/usr/bin/env python3
"""
AI Commit - Main Entry Point
"""

import tkinter as tk
from src.gui.main_window import AICommit


def main():
    """Main function"""
    root = tk.Tk()
    app = AICommit(root)
    root.mainloop()


if __name__ == "__main__":
    main()