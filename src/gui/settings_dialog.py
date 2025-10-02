"""
Settings Dialog for AI Commit
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from src.core.settings_manager import GEMINI_MODELS, OPENAI_MODELS


class SettingsDialog:
    def __init__(self, parent, settings_manager):
        self.settings_manager = settings_manager
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚙️ Settings")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup settings UI"""
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # AI Settings Tab
        ai_frame = ttk.Frame(notebook, padding="10")
        notebook.add(ai_frame, text="🤖 AI Settings")
        
        # Gemini Settings
        gemini_frame = ttk.LabelFrame(ai_frame, text="Google Gemini", padding="10")
        gemini_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(gemini_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.gemini_key = ttk.Entry(gemini_frame, width=50, show="•")
        self.gemini_key.grid(row=0, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        self.gemini_key.insert(0, self.settings_manager.get("gemini_api_key", ""))
        
        ttk.Label(gemini_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.gemini_model = ttk.Combobox(gemini_frame, width=30, values=GEMINI_MODELS)
        self.gemini_model.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.gemini_model.set(self.settings_manager.get("gemini_model", "gemini-2.5-flash"))
        
        # OpenAI Settings
        openai_frame = ttk.LabelFrame(ai_frame, text="OpenAI ChatGPT", padding="10")
        openai_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(openai_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.openai_key = ttk.Entry(openai_frame, width=50, show="•")
        self.openai_key.grid(row=0, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        self.openai_key.insert(0, self.settings_manager.get("openai_api_key", ""))
        
        ttk.Label(openai_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.openai_model = ttk.Combobox(openai_frame, width=30, values=OPENAI_MODELS)
        self.openai_model.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.openai_model.set(self.settings_manager.get("openai_model", "gpt-4o-mini"))
        
        # GitHub Settings Tab
        github_frame = ttk.Frame(notebook, padding="10")
        notebook.add(github_frame, text="🐙 GitHub")
        
        ttk.Label(github_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.github_username = ttk.Entry(github_frame, width=30)
        self.github_username.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.github_username.insert(0, self.settings_manager.get("github_username", ""))
        
        ttk.Label(github_frame, text="Token:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.github_token = ttk.Entry(github_frame, width=50, show="•")
        self.github_token.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.github_token.insert(0, self.settings_manager.get("github_token", ""))
        
        # Info text about GitHub token
        info_text = """GitHub Personal Access Token:
• Required for pushing to private repositories
• Create at: https://github.com/settings/tokens
• Required scopes: repo, write:public_key (for push)"""
        
        info_label = ttk.Label(github_frame, text=info_text, justify=tk.LEFT, foreground="blue")
        info_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Repository Settings Tab
        repo_frame = ttk.Frame(notebook, padding="10")
        notebook.add(repo_frame, text="📂 Repository")
        
        ttk.Label(repo_frame, text="Parent Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        folder_frame = ttk.Frame(repo_frame)
        folder_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.parent_folder = tk.StringVar(value=self.settings_manager.get("parent_folder", str(Path.home())))
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.parent_folder, width=40)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(folder_frame, text="Browse...", command=self.browse_folder).pack(side=tk.RIGHT, padx=5)
        
        # Recent repositories
        ttk.Label(repo_frame, text="Recent Repositories:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.recent_listbox = tk.Listbox(repo_frame, height=6)
        self.recent_listbox.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Load recent repos
        recent_repos = self.settings_manager.get("recent_repos", [])
        for repo in recent_repos:
            self.recent_listbox.insert(tk.END, repo)
        
        # Buttons for recent repos
        recent_buttons = ttk.Frame(repo_frame)
        recent_buttons.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(recent_buttons, text="Select", command=self.select_recent).pack(side=tk.LEFT, padx=2)
        ttk.Button(recent_buttons, text="Remove", command=self.remove_recent).pack(side=tk.LEFT, padx=2)
        ttk.Button(recent_buttons, text="Clear All", command=self.clear_recent).pack(side=tk.LEFT, padx=2)
        
        # Configure grid weights
        repo_frame.columnconfigure(1, weight=1)
        repo_frame.rowconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="💾 Save", command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def browse_folder(self):
        """Browse for parent folder"""
        folder = filedialog.askdirectory(initialdir=self.parent_folder.get())
        if folder:
            self.parent_folder.set(folder)
    
    def select_recent(self):
        """Select recent repository"""
        selection = self.recent_listbox.curselection()
        if selection:
            repo_path = self.recent_listbox.get(selection[0])
            self.parent_folder.set(repo_path)
    
    def remove_recent(self):
        """Remove selected recent repository"""
        selection = self.recent_listbox.curselection()
        if selection:
            self.recent_listbox.delete(selection[0])
    
    def clear_recent(self):
        """Clear all recent repositories"""
        self.recent_listbox.delete(0, tk.END)
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Save AI settings
            self.settings_manager.set("gemini_api_key", self.gemini_key.get().strip())
            self.settings_manager.set("openai_api_key", self.openai_key.get().strip())
            self.settings_manager.set("gemini_model", self.gemini_model.get())
            self.settings_manager.set("openai_model", self.openai_model.get())
            
            # Save GitHub settings
            self.settings_manager.set("github_username", self.github_username.get().strip())
            self.settings_manager.set("github_token", self.github_token.get().strip())
            
            # Save repository settings
            self.settings_manager.set("parent_folder", self.parent_folder.get())
            
            # Save recent repositories from listbox
            recent_repos = []
            for i in range(self.recent_listbox.size()):
                recent_repos.append(self.recent_listbox.get(i))
            self.settings_manager.set("recent_repos", recent_repos)
            
            if self.settings_manager.save_settings():
                messagebox.showinfo("Success", "Settings saved successfully!")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")