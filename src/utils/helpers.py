"""
Helper functions for AI Commit
"""

import tkinter as tk
from typing import Optional


def log_message(log_widget: tk.Text, message: str, level: str = "info"):
    """Add message to log widget"""
    log_widget.configure(state='normal')
    log_widget.insert(tk.END, f"{message}\n")
    log_widget.see(tk.END)
    
    if level == "error":
        # Get the line that was just inserted
        last_line_start = log_widget.index("end-2l")
        last_line_end = log_widget.index("end-1l")
        log_widget.tag_add("error", last_line_start, last_line_end)
        log_widget.tag_config("error", foreground="red")
    elif level == "success":
        last_line_start = log_widget.index("end-2l")
        last_line_end = log_widget.index("end-1l")
        log_widget.tag_add("success", last_line_start, last_line_end)
        log_widget.tag_config("success", foreground="green")
    elif level == "warning":
        last_line_start = log_widget.index("end-2l")
        last_line_end = log_widget.index("end-1l")
        log_widget.tag_add("warning", last_line_start, last_line_end)
        log_widget.tag_config("warning", foreground="orange")
    
    log_widget.configure(state='disabled')


def validate_commit_message(message: str) -> tuple[bool, Optional[str]]:
    """Validate commit message format"""
    if not message.strip():
        return False, "Commit message cannot be empty"
    
    lines = message.strip().split('\n')
    subject = lines[0]
    
    # Check subject line length
    if len(subject) > 72:
        return False, f"Subject line too long ({len(subject)} characters). Recommended: 50-72 characters."
    
    # Check if subject follows conventional commits format
    if not any(subject.startswith(prefix) for prefix in 
               ['feat:', 'fix:', 'docs:', 'style:', 'refactor:', 'test:', 'chore:']):
        return True, "Consider using conventional commits format: feat|fix|docs|style|refactor|test|chore"
    
    return True, None


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis if too long"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."