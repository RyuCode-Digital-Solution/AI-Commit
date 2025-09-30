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


class AICommitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Commit - GUI")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_repo = tk.StringVar()
        self.ai_provider = tk.StringVar(value="gemini")
        self.commit_message = tk.StringVar()
        self.auto_push = tk.BooleanVar(value=True)
        self.selected_files = []
        self.repos = []
        self.current_repo_path = None
        
        # Setup UI
        self.setup_ui()
        
        # Auto scan on start
        self.root.after(500, self.scan_repositories)
    
    def setup_ui(self):
        """Setup user interface"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🤖 AI Commit", 
            font=('Helvetica', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # AI Provider
        ttk.Label(settings_frame, text="AI Provider:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ai_frame = ttk.Frame(settings_frame)
        ai_frame.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Radiobutton(ai_frame, text="Gemini (Free)", variable=self.ai_provider, value="gemini").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ai_frame, text="ChatGPT", variable=self.ai_provider, value="chatgpt").pack(side=tk.LEFT, padx=5)
        
        # Auto Push
        ttk.Checkbutton(settings_frame, text="Auto Push to Origin", variable=self.auto_push).grid(row=0, column=2, padx=20)
        
        # Repository Selection Frame
        repo_frame = ttk.LabelFrame(main_frame, text="📁 Select Repository", padding="10")
        repo_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Scan button
        ttk.Button(repo_frame, text="🔍 Scan Repositories", command=self.scan_repositories).grid(row=0, column=0, padx=5)
        
        # Repository dropdown
        self.repo_combo = ttk.Combobox(repo_frame, textvariable=self.selected_repo, state="readonly", width=50)
        self.repo_combo.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.repo_combo.bind('<<ComboboxSelected>>', self.on_repo_selected)
        repo_frame.columnconfigure(1, weight=1)
        
        # Files Frame
        files_frame = ttk.LabelFrame(main_frame, text="📝 Changed Files", padding="10")
        files_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(3, weight=1)
        
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
            font=('Courier', 9)
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # File buttons
        file_buttons = ttk.Frame(files_frame)
        file_buttons.pack(fill=tk.X, pady=5)
        ttk.Button(file_buttons, text="✅ Select All", command=self.select_all_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="❌ Clear Selection", command=self.clear_file_selection).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="➕ Add Selected Files", command=self.add_selected_files).pack(side=tk.LEFT, padx=2)
        
        # Commit Message Frame
        message_frame = ttk.LabelFrame(main_frame, text="💬 Commit Message", padding="10")
        message_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Message text area
        self.message_text = scrolledtext.ScrolledText(message_frame, height=4, wrap=tk.WORD, font=('Courier', 9))
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Message buttons
        msg_buttons = ttk.Frame(message_frame)
        msg_buttons.pack(fill=tk.X)
        ttk.Button(msg_buttons, text="🤖 Generate with AI", command=self.generate_commit_message).pack(side=tk.LEFT, padx=2)
        ttk.Button(msg_buttons, text="🗑️ Clear", command=self.clear_message).pack(side=tk.LEFT, padx=2)
        
        # Action Buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(action_frame, text="✅ Commit & Push", command=self.commit_and_push, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="💾 Commit Only", command=self.commit_only).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="❌ Cancel", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD, font=('Courier', 8))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def log(self, message: str, level: str = "info"):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
        if level == "error":
            self.log_text.tag_add("error", "end-2l", "end-1l")
            self.log_text.tag_config("error", foreground="red")
    
    def set_status(self, message: str):
        """Update status bar"""
        self.status_label.config(text=message)
    
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
            self.log(f"✅ Found {len(self.repos)} repositories")
            
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
            return
        
        for line in output.strip().split('\n'):
            if line:
                status = line[:2]
                filename = line[3:]
                
                icon = "🆕" if "?" in status else "✏️" if "M" in status else "🗑️" if "D" in status else "📝"
                self.files_listbox.insert(tk.END, f"{icon} {filename}")
        
        self.log(f"📝 Found {self.files_listbox.size()} changed files")
    
    def select_all_files(self):
        """Select all files in listbox"""
        self.files_listbox.select_set(0, tk.END)
    
    def clear_file_selection(self):
        """Clear file selection"""
        self.files_listbox.selection_clear(0, tk.END)
    
    def add_selected_files(self):
        """Add selected files to git"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first!")
            return
        
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Files", "Please select files to add!")
            return
        
        self.set_status("Adding files...")
        
        # Get all lines from git status
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=self.current_repo_path
        )
        
        lines = output.strip().split('\n')
        files_to_add = [lines[i][3:] for i in selected_indices if i < len(lines)]
        
        if not files_to_add:
            return
        
        # Add files
        success, output = self.run_git_command(
            ["git", "add"] + files_to_add,
            cwd=self.current_repo_path
        )
        
        if success:
            self.log(f"✅ Added {len(files_to_add)} files to staging")
            messagebox.showinfo("Success", f"Added {len(files_to_add)} files to staging area")
        else:
            self.log(f"❌ Failed to add files: {output}", "error")
            messagebox.showerror("Error", f"Failed to add files:\n{output}")
        
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
            messagebox.showwarning("No Changes", "No staged changes found. Please add files first!")
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
                model = genai.GenerativeModel('gemini-2.5-flash')
                
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
                    model="gpt-4o-mini",
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
        self.log("✅ Commit message generated")
        self.set_status("Ready")
    
    def _show_error(self, error: str):
        """Show error message (called from main thread)"""
        self.log(f"❌ Error: {error}", "error")
        messagebox.showerror("Error", f"Failed to generate message:\n{error}")
        self.set_status("Ready")
    
    def clear_message(self):
        """Clear commit message"""
        self.message_text.delete(1.0, tk.END)
    
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
        
        self.log("✅ Commit successful")
        
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
                self.log("✅ Push successful!")
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
