"""
Main Window GUI for AI Commit
"""

import os
import sys
import threading
from pathlib import Path
from typing import Optional, List
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

from src.core.git_manager import GitManager
from src.core.ai_provider import AIProvider
from src.core.settings_manager import SettingsManager
from src.gui.settings_dialog import SettingsDialog
from src.utils.theme import ThemeManager
from src.utils.helpers import log_message


class AICommit:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Commit by RyuCode")
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.git_manager = GitManager()
        self.ai_provider = AIProvider(self.settings_manager)
        self.theme_manager = ThemeManager()
        
        # Variables
        self.selected_repo = tk.StringVar()
        self.ai_provider_var = tk.StringVar(value="gemini")
        self.commit_message = tk.StringVar()
        self.auto_push = tk.BooleanVar(value=self.settings_manager.get("auto_push", True))
        self.dark_mode = tk.BooleanVar(value=self.settings_manager.get("dark_mode", False))
        
        self.selected_files = []
        self.repos = []
        self.current_repo_path = None
        self.raw_git_status = []
        self._is_generating = False
        
        # Setup UI
        self.setup_ui()

        # Set application icon
        self.set_app_icon()
        
        # Auto scan on start
        self.root.after(500, self.scan_repositories)
    
    def setup_ui(self):
        """Setup user interface"""
        self.theme_manager.setup_theme(self.root, self.dark_mode.get())
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=2)
        main_frame.rowconfigure(6, weight=1)
        
        # Header Frame
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="AI Commit V1", font=('Helvetica', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Header buttons (Settings and Theme)
        header_buttons = ttk.Frame(header_frame)
        header_buttons.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(header_buttons, text="⚙️ Settings", command=self.open_settings).pack(side=tk.LEFT, padx=5)
        
        theme_frame = ttk.Frame(header_buttons)
        theme_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(theme_frame, text="🌙", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=2)
        theme_toggle = ttk.Checkbutton(
            theme_frame, 
            text="Dark Mode", 
            variable=self.dark_mode, 
            command=self.toggle_theme
        )
        theme_toggle.pack(side=tk.LEFT, padx=5)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        settings_frame.columnconfigure(1, weight=1)
        
        # AI Provider
        ttk.Label(settings_frame, text="AI Provider:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ai_frame = ttk.Frame(settings_frame)
        ai_frame.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Radiobutton(ai_frame, text="Gemini (Free)", variable=self.ai_provider_var, value="gemini").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ai_frame, text="ChatGPT", variable=self.ai_provider_var, value="chatgpt").pack(side=tk.LEFT, padx=5)
        
        # Auto Push
        ttk.Checkbutton(settings_frame, text="Auto Push to Origin", variable=self.auto_push).grid(row=0, column=2, padx=20, sticky=tk.E)
        
        # Repository Selection Frame
        repo_frame = ttk.LabelFrame(main_frame, text="📂 Select Repository", padding="10")
        repo_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        repo_frame.columnconfigure(1, weight=1)
        
        # Scan and Browse buttons
        repo_buttons = ttk.Frame(repo_frame)
        repo_buttons.grid(row=0, column=0, padx=5, sticky=tk.W)
        
        ttk.Button(repo_buttons, text="🔍 Scan", command=self.scan_repositories).pack(side=tk.LEFT, padx=2)
        ttk.Button(repo_buttons, text="📁 Browse", command=self.browse_repository).pack(side=tk.LEFT, padx=2)
        ttk.Button(repo_buttons, text="🔄 Refresh", command=self.load_changed_files).pack(side=tk.LEFT, padx=2)
        
        # Repository dropdown
        self.repo_combo = ttk.Combobox(repo_frame, textvariable=self.selected_repo, state="readonly")
        self.repo_combo.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.repo_combo.bind('<<ComboboxSelected>>', self.on_repo_selected)
        
        # Files Frame
        files_frame = ttk.LabelFrame(main_frame, text="📝 Changed Files", padding="10")
        files_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # File buttons
        file_buttons = ttk.Frame(files_frame)
        file_buttons.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(file_buttons, text="✅ Select All", command=self.select_all_files, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="❌ Clear Selection", command=self.clear_file_selection, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="➕ Add to Stage", command=self.add_selected_files, width=15).pack(side=tk.LEFT, padx=2)
        
        # Info label
        self.info_label = ttk.Label(
            files_frame,
            text="ℹ️ Select files and click 'Add to Stage' before generating commit message",
            foreground=self.theme_manager.get_accent_color(),
            font=('Helvetica', 8, 'italic')
        )
        self.info_label.pack(fill=tk.X, pady=(0, 5))
        
        # Files listbox with scrollbar
        files_scroll_frame = ttk.Frame(files_frame)
        files_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(files_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(
            files_scroll_frame,
            selectmode=tk.MULTIPLE,
            yscrollcommand=scrollbar.set,
            height=8,
            font=('Courier', 9),
            bg=self.theme_manager.get_text_bg(),
            fg=self.theme_manager.get_text_fg(),
            selectbackground=self.theme_manager.get_accent_color()
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Commit Message Frame
        message_frame = ttk.LabelFrame(main_frame, text="💬 Commit Message", padding="10")
        message_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Message text area
        self.message_text = scrolledtext.ScrolledText(
            message_frame, 
            height=4, 
            wrap=tk.WORD, 
            font=('Courier', 9),
            bg=self.theme_manager.get_text_bg(),
            fg=self.theme_manager.get_text_fg(),
            insertbackground=self.theme_manager.get_text_fg()
        )
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Message buttons
        msg_buttons = ttk.Frame(message_frame)
        msg_buttons.pack(fill=tk.X)
        ttk.Button(msg_buttons, text="🤖 Generate with AI", command=self.auto_add_and_generate, width=20).pack(side=tk.LEFT, padx=2)
        ttk.Button(msg_buttons, text="🗑️ Clear", command=self.clear_message, width=12).pack(side=tk.LEFT, padx=2)
        
        # Action Buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(action_frame, text="✅ Commit & Push", command=self.commit_and_push, width=18).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="💾 Commit Only", command=self.commit_only, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="❌ Cancel", command=self.root.quit, width=12).pack(side=tk.LEFT, padx=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(main_frame, text="📋 Activity Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=6, 
            wrap=tk.WORD, 
            font=('Courier', 8),
            bg=self.theme_manager.get_log_bg(),
            fg=self.theme_manager.get_log_fg(),
            state='disabled'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))

    def set_app_icon(self):
        """Set application icon with better path handling for EXE"""
        try:
            # Debug: Print current paths
            print("Setting application icon...")
        
            # Determine if running as EXE or script
            if getattr(sys, 'frozen', False):
                # Running as EXE - use temporary extraction directory
                base_path = sys._MEIPASS
                print(f"Running as EXE, MEIPASS: {base_path}")
            else:
                # Running as script - use current directory
                base_path = os.path.dirname(os.path.abspath(__file__))
                print(f"Running as script, base path: {base_path}")
        
            icon_paths = [
                os.path.join(base_path, "assets", "icon.ico"),
                os.path.join(base_path, "assets", "icon.png"),
                os.path.join(base_path, "icon.ico"),
                os.path.join(base_path, "icon.png"),
                "assets/icon.ico",
                "assets/icon.png",
                "icon.ico", 
                "icon.png"
            ]
        
            icon_found = False
            for path in icon_paths:
                exists = os.path.exists(path)
                print(f"Checking: {path} - {'EXISTS' if exists else 'MISSING'}")
            
                if exists:
                    try:
                        if path.endswith('.ico'):
                            self.root.iconbitmap(path)
                            print(f"Successfully set icon from: {path}")
                            icon_found = True
                            break
                        elif path.endswith('.png'):
                            icon_img = tk.PhotoImage(file=path)
                            self.root.iconphoto(True, icon_img)
                            print(f"Successfully set icon from: {path}")
                            icon_found = True
                            break
                    except Exception as icon_error:
                        print(f"Failed to set icon from {path}: {icon_error}")
                        continue
        
            if not icon_found:
                print("Warning: No valid icon file found in any location")
            
        except Exception as e:
            print(f"Icon setting error: {e}")
    
    def open_settings(self):
        """Open settings dialog"""
        SettingsDialog(self.root, self.settings_manager)
        # Update theme if changed in settings
        if self.dark_mode.get() != self.settings_manager.get("dark_mode", False):
            self.dark_mode.set(self.settings_manager.get("dark_mode", False))
            self.toggle_theme()
    
    def browse_repository(self):
        """Browse for specific repository folder"""
        folder = filedialog.askdirectory(
            initialdir=self.settings_manager.get("parent_folder", str(Path.home())),
            title="Select Git Repository"
        )
        if folder and self.git_manager.is_git_repo(folder):
            # Add to recent repos
            self.settings_manager.add_recent_repo(folder)
            
            # Create repo entry
            repo_name = Path(folder).name
            has_changes = self.git_manager.check_has_changes(folder)
            indicator = "🔴" if has_changes else "⚪"
            
            repo_entry = {
                'name': repo_name,
                'path': folder,
                'has_changes': has_changes,
                'display_name': f"{indicator} {repo_name} (browsed)"
            }
            
            # Add to repos list and select
            self.repos.append(repo_entry)
            current_values = list(self.repo_combo['values'])
            current_values.append(repo_entry['display_name'])
            self.repo_combo['values'] = current_values
            self.repo_combo.set(repo_entry['display_name'])
            self.on_repo_selected(None)
            
            self.log(f"📂 Selected repository: {repo_name}")
        elif folder:
            messagebox.showerror("Error", "Selected folder is not a Git repository!")
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.theme_manager.toggle_theme(self.root, self.dark_mode.get())
        
        # Update UI elements
        self.files_listbox.configure(
            bg=self.theme_manager.get_text_bg(),
            fg=self.theme_manager.get_text_fg(),
            selectbackground=self.theme_manager.get_accent_color()
        )
        
        self.message_text.configure(
            bg=self.theme_manager.get_text_bg(),
            fg=self.theme_manager.get_text_fg(),
            insertbackground=self.theme_manager.get_text_fg()
        )
        
        self.log_text.configure(
            bg=self.theme_manager.get_log_bg(),
            fg=self.theme_manager.get_log_fg()
        )
        
        self.info_label.configure(foreground=self.theme_manager.get_accent_color())
        
        # Save theme preference
        self.settings_manager.set("dark_mode", self.dark_mode.get())
        self.settings_manager.save_settings()
        
        self.log("🎨 Theme changed to " + ("Dark Mode" if self.dark_mode.get() else "Light Mode"))
    
    def log(self, message: str, level: str = "info"):
        """Add message to log"""
        log_message(self.log_text, message, level)
    
    def set_status(self, message: str):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def scan_repositories(self):
        """Scan for git repositories"""
        self.log("🔍 Scanning for repositories...")
        self.set_status("Scanning...")
        
        parent_folder = self.settings_manager.get("parent_folder", str(Path.home()))
        
        self.repos = self.git_manager.scan_repositories(parent_folder)
        
        if self.repos:
            repo_names = [repo['display_name'] for repo in self.repos]
            self.repo_combo['values'] = repo_names
            self.log(f"✅ Found {len(self.repos)} repositories in {parent_folder}", "success")
            
            # Auto-select first repo with changes
            for idx, repo in enumerate(self.repos):
                if repo['has_changes']:
                    self.repo_combo.current(idx)
                    self.on_repo_selected(None)
                    break
            else:  # Select first repo if no changes found
                if self.repos:
                    self.repo_combo.current(0)
                    self.on_repo_selected(None)
                    
            # Add to recent repos
            for repo in self.repos:
                self.settings_manager.add_recent_repo(repo['path'])
        else:
            self.log(f"❌ No git repositories found in {parent_folder}", "error")
            messagebox.showwarning("No Repositories", 
                f"No git repositories found in:\n{parent_folder}\n\nTry changing the parent folder in Settings.")
        
        self.set_status("Ready")
    
    def on_repo_selected(self, event):
        """Handle repository selection"""
        selected_idx = self.repo_combo.current()
        if selected_idx < 0 or selected_idx >= len(self.repos):
            return
        
        repo = self.repos[selected_idx]
        self.current_repo_path = repo['path']
        
        self.log(f"📂 Selected: {repo['name']}")
        self.load_changed_files()
        
        # Add to recent repos
        self.settings_manager.add_recent_repo(repo['path'])
    
    def load_changed_files(self):
        """Load changed files from selected repository"""
        if not self.current_repo_path:
            return
        
        self.files_listbox.delete(0, tk.END)
        
        success, output = self.git_manager.get_status(self.current_repo_path)
        
        if not success:
            self.log("❌ Failed to get file status", "error")
            return
        
        if not output.strip():
            self.log("ℹ️ No changes detected")
            self.raw_git_status = []
            return
        
        # Parse git status
        self.raw_git_status = self.git_manager.parse_git_status(output)
        
        for file_info in self.raw_git_status:
            status = file_info['status']
            filename = file_info['filename']
            file_type = file_info.get('type', 'regular')
            
            # Determine icon based on status
            if "??" in status or "A" in status:
                icon = "🆕"
            elif "M" in status:
                icon = "✏️"
            elif "D" in status:
                icon = "🗑️"
            elif "R" in status:
                icon = "🔄"
            else:
                icon = "📝"
            
            # For renamed files, show both names
            if file_type == 'renamed':
                old_file = file_info.get('old_filename', '')
                display_text = f"{icon} {old_file} → {filename}"
            else:
                display_text = f"{icon} {filename}"
            
            self.files_listbox.insert(tk.END, display_text)
        
        self.log(f"📝 Found {len(self.raw_git_status)} changed files")
    
    def select_all_files(self):
        """Select all files in listbox"""
        self.files_listbox.select_set(0, tk.END)
        self.log(f"✅ Selected all {self.files_listbox.size()} files")
    
    def clear_file_selection(self):
        """Clear file selection"""
        self.files_listbox.selection_clear(0, tk.END)
        self.log("❌ Cleared file selection")
    
    def add_selected_files(self):
        """Add selected files to git"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first!")
            return
        
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Files", "Please select files to add!")
            return
        
        if not self.raw_git_status:
            self.log("⚠️ No cached file data, refreshing...", "error")
            self.load_changed_files()
            messagebox.showwarning("Please Try Again", "File list refreshed. Please select files and try again.")
            return
        
        self.set_status("Adding files...")
        self.log(f"➕ Adding {len(selected_indices)} files to stage...")
        
        # Stage files
        success_count, error_messages = self.git_manager.stage_files(
            self.current_repo_path, self.raw_git_status, selected_indices, self.log
        )
        
        # Show results
        if success_count > 0:
            self.log(f"✅ Successfully staged {success_count} file(s)", "success")
            if not error_messages:
                messagebox.showinfo("Success", f"Staged {success_count} file(s) successfully!")
            else:
                messagebox.showwarning("Partial Success", 
                    f"Staged {success_count} file(s), but {len(error_messages)} failed.\nCheck Activity Log for details.")
        else:
            self.log("❌ No files were staged", "error")
            if error_messages:
                messagebox.showerror("Error", f"Failed to stage files:\n" + "\n".join(error_messages[:3]))
            else:
                messagebox.showerror("Error", "Failed to stage files. Check Activity Log for details.")
        
        self.set_status("Ready")
        self.root.after(500, self.load_changed_files)
    
    def auto_add_and_generate(self):
        """Auto add selected files then generate commit message"""
        if self._is_generating:
            self.log("⚠️ Already generating, please wait...", "error")
            return
        
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first!")
            return
        
        if self.files_listbox.size() == 0:
            messagebox.showinfo("No Changes", "No changed files detected in this repository.")
            return
        
        self.log("🔄 Auto-adding files before generating commit message...")
        
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            self.select_all_files()
            selected_indices = self.files_listbox.curselection()
        
        if not self.raw_git_status:
            self.log("⚠️ No file data available", "error")
            return
        
        # Auto stage files
        total_staged = self.git_manager.auto_stage_files(
            self.current_repo_path, self.raw_git_status, selected_indices, self.log
        )
        
        if total_staged > 0:
            self.log(f"✅ Total {total_staged} files staged", "success")
            self.root.after(200, self.generate_commit_message)
        else:
            messagebox.showwarning("No Files", "No files were staged")
            self.set_status("Ready")
    
    def generate_commit_message(self):
        """Generate commit message using AI"""
        if self._is_generating:
            return
    
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first!")
            return
    
        success, diff = self.git_manager.get_staged_diff(self.current_repo_path)
    
        # More defensive check
        if not success:
            messagebox.showwarning("Error", "Failed to get staged changes.")
            return
        
        # Handle both None and empty string cases
        if diff is None or (isinstance(diff, str) and not diff.strip()):
            messagebox.showwarning("No Staged Changes", "No staged changes found. Please stage files first.")
            return
    
        provider = self.ai_provider_var.get()
        self.set_status(f"Generating message with {provider}...")
        self.log(f"🤖 Generating commit message with {provider}...")
    
        self._is_generating = True
    
        thread = threading.Thread(target=self._generate_message_thread, args=(diff, provider))
        thread.daemon = True
        thread.start()
    
    def _generate_message_thread(self, diff: str, provider: str):
        """Generate message in separate thread"""
        try:
            message = self.ai_provider.generate_commit_message(diff, provider)
            self.root.after(0, self._update_message, message)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
        finally:
            self.root.after(0, lambda: setattr(self, '_is_generating', False))
            self.root.after(0, lambda: self.set_status("Ready"))
    
    def _update_message(self, message: str):
        """Update commit message (called from main thread)"""
        self.message_text.delete(1.0, tk.END)
        self.message_text.insert(1.0, message)
        self.log("✅ Commit message generated successfully", "success")
        self._is_generating = False
        self.set_status("Ready")
    
    def _show_error(self, error: str):
        """Show error message (called from main thread)"""
        self.log(f"❌ Error: {error}", "error")
        messagebox.showerror("Error", f"Failed to generate message:\n{error}")
        self._is_generating = False
        self.set_status("Ready")
    
    def clear_message(self):
        """Clear commit message"""
        self.message_text.delete(1.0, tk.END)
        self.log("🗑️ Cleared commit message")
    
    def commit_and_push(self):
        """Commit and push changes"""
        self._commit(push=True)
    
    def commit_only(self):
        """Commit without pushing"""
        self._commit(push=False)
    
    def _commit(self, push: bool = True):
        """Perform commit"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository!")
            return
        
        message = self.message_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("No Message", "Please enter or generate a commit message!")
            return
        
        first_line = message.split('\n')[0]
        if len(first_line) > 72:
            response = messagebox.askyesno(
                "Long Subject Line",
                f"The commit message subject is {len(first_line)} characters (recommended: 50-72).\n\nContinue anyway?"
            )
            if not response:
                return
        
        self.set_status("Committing...")
        self.log(f"📝 Committing with message: {first_line[:50]}...")
        
        # Commit changes
        success, output = self.git_manager.commit_changes(self.current_repo_path, message)
        
        if not success:
            self.log(f"❌ Commit failed: {output}", "error")
            messagebox.showerror("Commit Failed", f"Failed to commit:\n{output}")
            self.set_status("Ready")
            return
        
        self.log("✅ Commit successful!", "success")
        
        if push and self.auto_push.get():
            self.set_status("Pushing...")
            
            # Configure GitHub credentials if provided
            github_username = self.settings_manager.get("github_username")
            github_token = self.settings_manager.get("github_token")
            
            # Push changes
            success, output = self.git_manager.push_changes(
                self.current_repo_path, github_username, github_token, self.log
            )
            
            if success:
                self.log("✅ Push successful!", "success")
                messagebox.showinfo("Success", "Commit and push completed successfully!")
            else:
                self.log(f"❌ Push failed: {output}", "error")
                messagebox.showerror("Push Failed", f"Commit successful but push failed:\n{output}")
        else:
            messagebox.showinfo("Success", "Commit completed successfully!")
        
        self.set_status("Ready")
        self.clear_message()
        self.load_changed_files()