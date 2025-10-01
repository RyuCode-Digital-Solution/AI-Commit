import os
import subprocess
import threading
from pathlib import Path
from typing import Optional, List
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_MODEL = "gpt-4o-mini"

class AICommitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Commit - GUI")
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_repo = tk.StringVar()
        self.ai_provider = tk.StringVar(value="gemini")
        self.commit_message = tk.StringVar()
        self.auto_push = tk.BooleanVar(value=True)
        self.dark_mode = tk.BooleanVar(value=False)
        self.selected_files = []
        self.repos = []
        self.current_repo_path = None
        self.raw_git_status = []  # Store raw git status data
        
        # Color schemes
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
        
        # Setup UI
        self.setup_ui()
        
        # Auto scan on start
        self.root.after(500, self.scan_repositories)
    
    def setup_ui(self):
        """Setup user interface"""
        # Configure root
        self.root.configure(bg=self.current_theme['bg'])
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.apply_theme()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure grid weights for responsiveness
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=2)  # Files frame
        main_frame.rowconfigure(6, weight=1)  # Log frame
        
        # Header Frame with Title and Theme Toggle
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="🤖 AI Commit", 
            font=('Helvetica', 18, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Theme Toggle
        theme_frame = ttk.Frame(header_frame)
        theme_frame.grid(row=0, column=1, sticky=tk.E)
        
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
        ttk.Radiobutton(ai_frame, text="Gemini (Free)", variable=self.ai_provider, value="gemini").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ai_frame, text="ChatGPT", variable=self.ai_provider, value="chatgpt").pack(side=tk.LEFT, padx=5)
        
        # Auto Push
        ttk.Checkbutton(settings_frame, text="Auto Push to Origin", variable=self.auto_push).grid(row=0, column=2, padx=20, sticky=tk.E)
        
        # Repository Selection Frame
        repo_frame = ttk.LabelFrame(main_frame, text="📁 Select Repository", padding="10")
        repo_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        repo_frame.columnconfigure(1, weight=1)
        
        # Scan button
        ttk.Button(repo_frame, text="🔍 Scan Repositories", command=self.scan_repositories).grid(row=0, column=0, padx=5)
        
        # Repository dropdown
        self.repo_combo = ttk.Combobox(repo_frame, textvariable=self.selected_repo, state="readonly")
        self.repo_combo.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.repo_combo.bind('<<ComboboxSelected>>', self.on_repo_selected)
        
        # Files Frame
        files_frame = ttk.LabelFrame(main_frame, text="📝 Changed Files", padding="10")
        files_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # File buttons - PINDAH KE ATAS
        file_buttons = ttk.Frame(files_frame)
        file_buttons.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(file_buttons, text="✅ Select All", command=self.select_all_files, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="❌ Clear Selection", command=self.clear_file_selection, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="➕ Add to Stage", command=self.add_selected_files, width=15).pack(side=tk.LEFT, padx=2)
        
        # Info label
        info_label = ttk.Label(
            files_frame,
            text="ℹ️ Select files and click 'Add to Stage' before generating commit message",
            foreground=self.current_theme['accent'],
            font=('Helvetica', 8, 'italic')
        )
        info_label.pack(fill=tk.X, pady=(0, 5))
        self.info_label = info_label  # Store reference for theme switching
        
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
            bg=self.current_theme['text_bg'],
            fg=self.current_theme['text_fg'],
            selectbackground=self.current_theme['accent']
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
            bg=self.current_theme['text_bg'],
            fg=self.current_theme['text_fg'],
            insertbackground=self.current_theme['text_fg']
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
            bg=self.current_theme['log_bg'],
            fg=self.current_theme['log_fg'],
            state='disabled'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def apply_theme(self):
        """Apply current theme to UI"""
        theme = self.current_theme
        
        # Configure ttk styles
        self.style.configure('TFrame', background=theme['bg'])
        self.style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TLabelframe', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TButton', background=theme['button_bg'], foreground=theme['fg'])
        self.style.configure('TCheckbutton', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TRadiobutton', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TCombobox', fieldbackground=theme['text_bg'], background=theme['bg'])
        
        # Map for button states
        self.style.map('TButton',
            background=[('active', theme['accent'])],
            foreground=[('active', '#ffffff')]
        )
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.dark_mode.get():
            self.current_theme = self.dark_theme
        else:
            self.current_theme = self.light_theme
        
        # Apply theme
        self.root.configure(bg=self.current_theme['bg'])
        self.apply_theme()
        
        # Update widgets that need manual color change
        self.files_listbox.configure(
            bg=self.current_theme['text_bg'],
            fg=self.current_theme['text_fg'],
            selectbackground=self.current_theme['accent']
        )
        
        self.message_text.configure(
            bg=self.current_theme['text_bg'],
            fg=self.current_theme['text_fg'],
            insertbackground=self.current_theme['text_fg']
        )
        
        self.log_text.configure(
            bg=self.current_theme['log_bg'],
            fg=self.current_theme['log_fg']
        )
        
        self.info_label.configure(foreground=self.current_theme['accent'])
        
        self.log("🎨 Theme changed to " + ("Dark Mode" if self.dark_mode.get() else "Light Mode"))
    
    def log(self, message: str, level: str = "info"):
        """Add message to log"""
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
        if level == "error":
            # Get the line that was just inserted
            last_line_start = self.log_text.index("end-2l")
            last_line_end = self.log_text.index("end-1l")
            self.log_text.tag_add("error", last_line_start, last_line_end)
            self.log_text.tag_config("error", foreground="red")
        elif level == "success":
            last_line_start = self.log_text.index("end-2l")
            last_line_end = self.log_text.index("end-1l")
            self.log_text.tag_add("success", last_line_start, last_line_end)
            self.log_text.tag_config("success", foreground="green")
        
        self.log_text.configure(state='disabled')
    
    def set_status(self, message: str):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def run_git_command(self, command: list, cwd: Optional[str] = None) -> tuple[bool, str]:
        """Execute git command"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def is_git_repo(self, path: str) -> bool:
        """Check if path is a git repository"""
        return (Path(path) / ".git").exists()
    
    def check_has_changes(self, repo_path: str) -> bool:
        """Check if repository has changes"""
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=repo_path
        )
        return success and bool(output.strip())
    
    def scan_repositories(self):
        """Scan for git repositories"""
        self.log("🔍 Scanning for repositories...")
        self.set_status("Scanning...")
        
        current_path = Path('.').resolve()
        parent_path = current_path.parent
        
        self.repos = []
        repo_names = []
        
        for item in sorted(parent_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                if self.is_git_repo(str(item)):
                    has_changes = self.check_has_changes(str(item))
                    indicator = "🔴" if has_changes else "⚪"
                    
                    display_name = f"{indicator} {item.name}"
                    if item.name == current_path.name:
                        display_name += " (current)"
                    
                    self.repos.append({
                        'name': item.name,
                        'path': str(item),
                        'has_changes': has_changes,
                        'display_name': display_name
                    })
                    repo_names.append(display_name)
        
        if self.repos:
            self.repo_combo['values'] = repo_names
            self.log(f"✅ Found {len(self.repos)} repositories", "success")
            
            # Auto-select first repo with changes
            for idx, repo in enumerate(self.repos):
                if repo['has_changes']:
                    self.repo_combo.current(idx)
                    self.on_repo_selected(None)
                    break
        else:
            self.log("❌ No git repositories found", "error")
            messagebox.showwarning("No Repositories", "No git repositories found in parent folder!")
        
        self.set_status("Ready")
    
    def on_repo_selected(self, event):
        """Handle repository selection"""
        selected_idx = self.repo_combo.current()
        if selected_idx < 0:
            return
        
        repo = self.repos[selected_idx]
        self.current_repo_path = repo['path']
        
        self.log(f"📂 Selected: {repo['name']}")
        self.load_changed_files()
    
    def load_changed_files(self):
        """Load changed files from selected repository"""
        if not self.current_repo_path:
            return
        
        self.files_listbox.delete(0, tk.END)
        
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=self.current_repo_path
        )
        
        if not success:
            self.log("❌ Failed to get file status", "error")
            return
        
        if not output.strip():
            self.log("ℹ️ No changes detected")
            self.raw_git_status = []
            return
        
        # Store raw git status for accurate file operations
        self.raw_git_status = []
        
        for line in output.strip().split('\n'):
            if line and len(line) > 3:
                status = line[:2]
                filename = line[3:].strip()  # Get clean filename
                
                # Store raw data
                self.raw_git_status.append({
                    'status': status,
                    'filename': filename
                })
                
                # Display with icon (visual only)
                if "?" in status:
                    icon = "🆕"
                elif "M" in status:
                    icon = "✏️"
                elif "D" in status:
                    icon = "🗑️"
                elif "A" in status:
                    icon = "➕"
                elif "R" in status:
                    icon = "🔄"
                else:
                    icon = "📝"
                
                display_text = f"{icon} {filename}"
                self.files_listbox.insert(tk.END, display_text)
        
        self.log(f"📝 Found {len(self.raw_git_status)} changed files")
        
        # Debug log - show what we stored
        for idx, item in enumerate(self.raw_git_status):
            self.log(f"  [{idx}] status='{item['status']}' file='{item['filename']}'", "info")
    
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
        
        # Check if raw_git_status is available
        if not hasattr(self, 'raw_git_status') or not self.raw_git_status:
            self.log("⚠️ No cached file data, refreshing...", "error")
            self.load_changed_files()
            messagebox.showwarning("Please Try Again", "File list refreshed. Please select files and try again.")
            return
        
        self.set_status("Adding files...")
        self.log(f"➕ Adding {len(selected_indices)} files to stage...")
        
        files_to_add = []
        deleted_files = []
        
        for i in selected_indices:
            if i < len(self.raw_git_status):
                file_info = self.raw_git_status[i]
                status_code = file_info['status']
                filename = file_info['filename']
                
                self.log(f"📋 Index {i}: status='{status_code}' file='{filename}'")
                
                # Handle different file statuses
                if 'D' in status_code:
                    deleted_files.append(filename)
                else:
                    files_to_add.append(filename)
            else:
                self.log(f"⚠️ Index {i} out of range (max: {len(self.raw_git_status)-1})", "error")
        
        success_count = 0
        error_messages = []
        
        # Handle deleted files
        for filename in deleted_files:
            # Check if file exists in filesystem
            file_path = Path(self.current_repo_path) / filename
            
            success_rm, output_rm = self.run_git_command(
                ["git", "rm", filename],
                cwd=self.current_repo_path
            )
            if success_rm:
                success_count += 1
                self.log(f"🗑️ Staged deletion: {filename}", "success")
            else:
                error_messages.append(f"rm {filename}: {output_rm}")
                self.log(f"❌ Failed rm: {filename}", "error")
        
        # Handle other files (add one by one)
        for filename in files_to_add:
            # Check if file exists
            file_path = Path(self.current_repo_path) / filename
            
            if not file_path.exists():
                # Try to find similar file
                parent_dir = file_path.parent
                file_stem = file_path.stem
                file_ext = file_path.suffix
                
                self.log(f"⚠️ File not found: {filename}", "error")
                self.log(f"  Looking for similar files in {parent_dir}...")
                
                # Search for similar files
                if parent_dir.exists():
                    similar_files = []
                    for f in parent_dir.iterdir():
                        if f.is_file():
                            # Check if name is similar
                            if file_stem.lower() in f.stem.lower() or f.stem.lower() in file_stem.lower():
                                if f.suffix == file_ext:
                                    similar_files.append(f.name)
                    
                    if similar_files:
                        self.log(f"  Found similar: {', '.join(similar_files)}")
                        # Use the first match
                        actual_filename = str(parent_dir / similar_files[0])
                        if parent_dir != Path(self.current_repo_path):
                            actual_filename = str(Path(parent_dir.name) / similar_files[0])
                        else:
                            actual_filename = similar_files[0]
                        
                        self.log(f"  Using: {actual_filename}")
                        filename = actual_filename
                    else:
                        error_messages.append(f"File not found: {filename}")
                        continue
            
            success_add, output_add = self.run_git_command(
                ["git", "add", "--", filename],
                cwd=self.current_repo_path
            )
            if success_add:
                success_count += 1
                self.log(f"✅ Staged: {filename}", "success")
            else:
                error_messages.append(f"add {filename}: {output_add}")
                self.log(f"❌ Failed add: {filename}", "error")
        
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
            messagebox.showerror("Error", "Failed to stage files. Check Activity Log for details.")
        
        self.set_status("Ready")
        
        # Refresh file list
        self.root.after(500, self.load_changed_files)
    
    def auto_add_and_generate(self):
        """Auto add selected files (or all) then generate commit message"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first!")
            return
        
        # Check if there are changes
        if self.files_listbox.size() == 0:
            messagebox.showinfo("No Changes", "No changed files detected in this repository.")
            return
        
        self.log("🔄 Auto-adding files before generating commit message...")
        
        # Auto select all if nothing selected
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            self.select_all_files()
            selected_indices = self.files_listbox.curselection()
        
        # Get fresh git status
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=self.current_repo_path
        )
        
        if not success:
            messagebox.showerror("Error", "Failed to get git status")
            return
        
        lines = output.strip().split('\n')
        files_to_add = []
        deleted_files = []
        
        for i in selected_indices:
            if i < len(lines) and lines[i]:
                status_code = lines[i][:2]
                filename = lines[i][3:].strip()
                
                if 'D' in status_code:
                    deleted_files.append(filename)
                else:
                    files_to_add.append(filename)
        
        # Handle deleted files
        for filename in deleted_files:
            success_rm, _ = self.run_git_command(
                ["git", "rm", filename],
                cwd=self.current_repo_path
            )
            if success_rm:
                self.log(f"🗑️ Staged deletion: {filename}")
        
        # Handle other files
        for filename in files_to_add:
            success_add, _ = self.run_git_command(
                ["git", "add", "--", filename],
                cwd=self.current_repo_path
            )
            if success_add:
                self.log(f"✅ Staged: {filename}")
        
        total_staged = len(files_to_add) + len(deleted_files)
        if total_staged > 0:
            self.log(f"✅ Total {total_staged} files staged", "success")
            # Now generate commit message
            self.root.after(200, self.generate_commit_message)
        else:
            messagebox.showwarning("No Files", "No files were staged")
            self.set_status("Ready")
    
    def generate_commit_message(self):
        """Generate commit message using AI"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first!")
            return
        
        # Get staged changes
        success, diff = self.run_git_command(
            ["git", "diff", "--cached"],
            cwd=self.current_repo_path
        )
        
        if not success or not diff.strip():
            messagebox.showwarning("No Staged Changes", "No staged changes found. Files have been added, please try again.")
            return
        
        provider = self.ai_provider.get()
        self.set_status(f"Generating message with {provider}...")
        self.log(f"🤖 Generating commit message with {provider}...")
        
        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self._generate_message_thread, args=(diff, provider))
        thread.daemon = True
        thread.start()
    
    def _generate_message_thread(self, diff: str, provider: str):
        """Generate message in separate thread"""
        try:
            if provider == "gemini":
                if not GEMINI_AVAILABLE:
                    raise ImportError("google-generativeai not installed")
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not set")
                
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(GEMINI_MODEL)
                
                prompt = f"""Generate a clear commit message following conventional commits format.

Git diff:
```
{diff[:3000]}
```

Format: <type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore
Use English, be concise. Return only the commit message."""
                
                response = model.generate_content(prompt)
                message = response.text.strip()
                
            else:  # chatgpt
                if not OPENAI_AVAILABLE:
                    raise ImportError("openai not installed")
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not set")
                
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You generate git commit messages."},
                        {"role": "user", "content": f"Generate commit message for:\n{diff[:3000]}"}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                message = response.choices[0].message.content.strip()
            
            # Update UI in main thread
            self.root.after(0, self._update_message, message)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_message(self, message: str):
        """Update commit message (called from main thread)"""
        self.message_text.delete(1.0, tk.END)
        self.message_text.insert(1.0, message)
        self.log("✅ Commit message generated successfully", "success")
        self.set_status("Ready")
    
    def _show_error(self, error: str):
        """Show error message (called from main thread)"""
        self.log(f"❌ Error: {error}", "error")
        messagebox.showerror("Error", f"Failed to generate message:\n{error}")
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
        
        self.set_status("Committing...")
        self.log(f"📝 Committing with message: {message[:50]}...")
        
        # Commit
        success, output = self.run_git_command(
            ["git", "commit", "-m", message],
            cwd=self.current_repo_path
        )
        
        if not success:
            self.log(f"❌ Commit failed: {output}", "error")
            messagebox.showerror("Commit Failed", f"Failed to commit:\n{output}")
            self.set_status("Ready")
            return
        
        self.log("✅ Commit successful!", "success")
        
        if push and self.auto_push.get():
            self.set_status("Pushing...")
            
            # Get current branch
            success, branch = self.run_git_command(
                ["git", "branch", "--show-current"],
                cwd=self.current_repo_path
            )
            
            if not success:
                self.log("❌ Failed to get branch name", "error")
                self.set_status("Ready")
                return
            
            branch = branch.strip()
            self.log(f"🚀 Pushing to origin/{branch}...")
            
            # Push
            success, output = self.run_git_command(
                ["git", "push", "origin", branch],
                cwd=self.current_repo_path
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
        # Refresh file list
        self.load_changed_files()


def main():
    root = tk.Tk()
    app = AICommitGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
