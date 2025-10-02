"""
Theme Manager for AI Commit
"""

import tkinter as tk
from tkinter import ttk


class ThemeManager:
    def __init__(self):
        self.light_theme = {
            'bg': '#f0f0f0',
            'fg': '#000000',
            'frame_bg': '#ffffff',
            'text_bg': '#ffffff',
            'text_fg': '#000000',
            'button_bg': '#e0e0e0',
            'accent': '#0078d4',
            'log_bg': '#f9f9f9',
            'log_fg': '#333333'
        }
        
        self.dark_theme = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'frame_bg': '#2d2d2d',
            'text_bg': '#252526',
            'text_fg': '#d4d4d4',
            'button_bg': '#3e3e42',
            'accent': '#0e639c',
            'log_bg': '#1e1e1e',
            'log_fg': '#cccccc'
        }
        
        self.current_theme = self.light_theme
        self.style = None
    
    def setup_theme(self, root: tk.Tk, dark_mode: bool = False):
        """Setup theme for the application"""
        if dark_mode:
            self.current_theme = self.dark_theme
        else:
            self.current_theme = self.light_theme
        
        root.configure(bg=self.current_theme['bg'])
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply current theme to ttk styles"""
        theme = self.current_theme
        
        self.style.configure('TFrame', background=theme['bg'])
        self.style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TLabelframe', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TButton', background=theme['button_bg'], foreground=theme['fg'])
        self.style.configure('TCheckbutton', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TRadiobutton', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TCombobox', fieldbackground=theme['text_bg'], background=theme['bg'])
        
        self.style.map('TButton',
            background=[('active', theme['accent'])],
            foreground=[('active', '#ffffff')]
        )
    
    def toggle_theme(self, root: tk.Tk, dark_mode: bool):
        """Toggle between dark and light theme"""
        if dark_mode:
            self.current_theme = self.dark_theme
        else:
            self.current_theme = self.light_theme
        
        root.configure(bg=self.current_theme['bg'])
        self._apply_theme()
    
    def get_bg(self) -> str:
        """Get background color"""
        return self.current_theme['bg']
    
    def get_fg(self) -> str:
        """Get foreground color"""
        return self.current_theme['fg']
    
    def get_text_bg(self) -> str:
        """Get text background color"""
        return self.current_theme['text_bg']
    
    def get_text_fg(self) -> str:
        """Get text foreground color"""
        return self.current_theme['text_fg']
    
    def get_accent_color(self) -> str:
        """Get accent color"""
        return self.current_theme['accent']
    
    def get_log_bg(self) -> str:
        """Get log background color"""
        return self.current_theme['log_bg']
    
    def get_log_fg(self) -> str:
        """Get log foreground color"""
        return self.current_theme['log_fg']