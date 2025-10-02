import os
import subprocess
import sys
import platform
from typing import Optional, List, Tuple
from pathlib import Path

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

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def clear_terminal():
    """Clear terminal screen for all OS and terminals"""
    os_name = platform.system()
    
    if os_name == "Windows":
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        os.system('clear')
    
    print("\033[H\033[J", end="")

class AICommit:
    def __init__(self, ai_provider: str = "gemini"):
        """
        Initialize AI Commit
        
        Args:
            ai_provider: "gemini" or "chatgpt"
        """
        self.ai_provider = ai_provider.lower()
        
        if self.ai_provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise ImportError("Install google-generativeai: pip install google-generativeai")
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "GEMINI_API_KEY not found. Set it with:\n"
                    "  export GEMINI_API_KEY='your-key'  # Linux/Mac\n"
                    "  set GEMINI_API_KEY=your-key       # Windows"
                )
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
            
        elif self.ai_provider == "chatgpt":
            if not OPENAI_AVAILABLE:
                raise ImportError("Install openai: pip install openai")
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found. Set it with:\n"
                    "  export OPENAI_API_KEY='your-key'  # Linux/Mac\n"
                    "  set OPENAI_API_KEY=your-key       # Windows"
                )
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError("AI providers must be 'gemini' or 'chatgpt'")

    def run_git_command(self, command: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
        """Execute git command"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd,
                timeout=30  # Add timeout to prevent hanging
            )
            return True, result.stdout
        except subprocess.TimeoutExpired:
            return False, "Command timed out after 30 seconds"
        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except FileNotFoundError:
            return False, "Git command not found. Is Git installed?"

    def is_git_repo(self, path: str) -> bool:
        """Check if path is a git repository"""
        git_dir = Path(path) / ".git"
        return git_dir.exists()

    def check_has_changes(self, repo_path: str) -> bool:
        """Quick check if repository has any changes"""
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=repo_path
        )
        if success and output.strip():
            return True
        return False

    def find_git_repos(self, base_path: str = ".") -> List[Tuple[str, str, bool]]:
        """
        Find all git repositories in parent directory
        Returns: List of (name, path, has_changes)
        """
        repos = []
        base_path = Path(base_path).resolve()
        
        # Get parent directory (where sibling folders are)
        parent_path = base_path.parent
        current_folder_name = base_path.name
        
        print(f"🔍 Scanning: {parent_path}")
        
        # Scan all folders in parent directory
        for item in sorted(parent_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                if self.is_git_repo(str(item)):
                    # Check if this folder has changes
                    has_changes = self.check_has_changes(str(item))
                    
                    # Mark current folder
                    display_name = item.name
                    if item.name == current_folder_name:
                        display_name = f"{item.name} (current)"
                    
                    repos.append((display_name, str(item), has_changes))
        
        return repos

    def select_directory(self, specific_dir: Optional[str] = None) -> Optional[str]:
        """Select directory to work with"""
        if specific_dir:
            # Handle relative path from parent
            if specific_dir.startswith('../'):
                current_path = Path('.').resolve()
                dir_path = (current_path.parent / specific_dir.replace('../', '')).resolve()
            else:
                dir_path = Path(specific_dir).resolve()
            
            if not dir_path.exists():
                print(f"❌ The directory '{specific_dir}' was not found")
                return None
            if not self.is_git_repo(str(dir_path)):
                print(f"❌ '{specific_dir}' is not a git repository")
                return None
            return str(dir_path)
        
        # Auto-detect git repos in parent directory
        repos = self.find_git_repos()
        
        if not repos:
            print("❌ No git repository found in the parent folder")
            print("💡 Tip: Make sure the sibling folders are git repositories.")
            return None
        
        # Show all repositories with change indicators
        print("\n📂 Git repositories found:")
        
        repos_with_changes = []
        repos_without_changes = []
        
        for idx, (name, path, has_changes) in enumerate(repos, 1):
            if has_changes:
                repos_with_changes.append((idx, name, path))
                print(f"   {idx}. {name} 🔴")
            else:
                repos_without_changes.append((idx, name, path))
                print(f"   {idx}. {name} ⚪")
        
        print("\n   🔴 = There are changes that have not been committed")
        print("   ⚪ = No changes")
        
        # Auto-select if only one repo has changes
        if len(repos_with_changes) == 1 and len(repos) > 1:
            auto_select = repos_with_changes[0]
            response = input(f"\n💡 Only '{auto_select[1].replace(' (current)', '')}' has been changed. Use it? (Y/n): ").lower()
            if response != 'n':
                display_name = auto_select[1].replace(" (current)", "")
                print(f"✅ Selected: {display_name}")
                return auto_select[2]
        
        # Manual selection
        while True:
            try:
                choice = input("\n▶ Select repository (number): ")
                idx = int(choice) - 1
                if 0 <= idx < len(repos):
                    selected = repos[idx]
                    display_name = selected[0].replace(" (current)", "")
                    print(f"✅ Selected: {display_name}")
                    return selected[1]
                else:
                    print("❌ Invalid number")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Cancelled")
                return None

    def get_changed_files(self, repo_path: str) -> Optional[List[Tuple[str, str]]]:
        """Get list of changed files"""
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=repo_path
        )
        
        if not success:
            return None
        
        files = []
        for line in output.strip().split('\n'):
            if line and len(line) >= 3:  # Ensure minimum length
                # Parse git status output
                status = line[:2]
                filename = line[3:]
                if status.strip():  # Has changes
                    # Handle renamed files: "R  old.txt -> new.txt"
                    if 'R' in status and '->' in filename:
                        filename = filename.split('->')[-1].strip()
                    files.append((status, filename))
        
        return files

    def auto_git_add(self, repo_path: str, add_all: bool = False) -> bool:
        """Automatically add files with selection"""
        files = self.get_changed_files(repo_path)
        
        if not files:
            print("❌ No changes detected")
            return False
        
        print(f"\n📝 Changes detected ({len(files)} files):")
        for idx, (status, filename) in enumerate(files, 1):
            status_icon = "🆕" if "?" in status else "✏️" if "M" in status else "🗑️" if "D" in status else "📝"
            print(f"   {idx}. {status_icon} {filename}")
        
        if add_all:
            print("\n➕ Adding all files...")
            success, output = self.run_git_command(["git", "add", "."], cwd=repo_path)
        else:
            response = input("\n▶ Add all files? (y/n/select): ").lower()
            
            if response == 'y':
                success, output = self.run_git_command(["git", "add", "."], cwd=repo_path)
            elif response == 'select':
                print("📌 Enter the file numbers you want to add (separate them with commas, for example: 1,3,5)")
                selection = input("   Number: ")
                try:
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    selected_files = [files[i][1] for i in indices if 0 <= i < len(files)]
                    
                    if not selected_files:
                        print("❌ No valid files")
                        return False
                    
                    # Normalize paths for cross-platform compatibility
                    normalized_files = [f.replace('\\', '/') for f in selected_files]
                    
                    success, output = self.run_git_command(
                        ["git", "add", "--"] + normalized_files,
                        cwd=repo_path
                    )
                except (ValueError, IndexError):
                    print("❌ Invalid input")
                    return False
            else:
                print("❌ Cancelled")
                return False
        
        if not success:
            print(f"❌ Git add failed: {output}")
            return False
        
        print("✅ File successfully added!")
        return True

    def get_git_diff(self, repo_path: str) -> Optional[str]:
        """Get staged changes"""
        success, diff = self.run_git_command(["git", "diff", "--cached"], cwd=repo_path)
        if not success or not diff.strip():
            print("❌ No changes have been staged.")
            return None
        return diff

    def get_current_branch(self, repo_path: str) -> Optional[str]:
        """Get current branch name"""
        success, branch = self.run_git_command(
            ["git", "branch", "--show-current"],
            cwd=repo_path
        )
        if success:
            return branch.strip()
        return None

    def generate_commit_message(self, diff: str) -> Optional[str]:
        """Generate commit message using AI"""
        # Truncate diff to avoid token limits
        diff_truncated = diff[:3000] if len(diff) > 3000 else diff
        
        prompt = f"""Generate a clear commit message following conventional commits format.

Git diff:
```
{diff_truncated}
```

Format: <type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore
Use English, be concise. Return only the commit message."""

        try:
            if self.ai_provider == "gemini":
                response = self.model.generate_content(prompt)
                message = response.text.strip()
            else:  # chatgpt
                response = self.client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates git commit messages."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200,
                    timeout=30  # Add timeout
                )
                message = response.choices[0].message.content.strip()
            
            # Validate message length (Git recommends 50 chars for subject)
            if len(message.split('\n')[0]) > 72:
                print("⚠️  Warning: Commit message subject is longer than 72 characters")
            
            return message
            
        except Exception as e:
            print(f"❌ Error generating commit message: {e}")
            return None

    def commit_and_push(self, repo_path: str, message: str, push: bool = True) -> bool:
        """Commit changes and optionally push"""
        # Commit
        print(f"\n📝 Committing with message:")
        print(f"   {message}\n")
        
        success, output = self.run_git_command(
            ["git", "commit", "-m", message],
            cwd=repo_path
        )
        if not success:
            print(f"❌ Commit failed: {output}")
            return False
        
        print("✅ Commit successful!")
        
        if not push:
            return True
        
        # Get current branch
        branch = self.get_current_branch(repo_path)
        if not branch:
            print("❌ Failed to get branch name")
            return False
        
        # Push
        print(f"\n🚀 Pushing to origin/{branch}...")
        success, output = self.run_git_command(
            ["git", "push", "origin", branch],
            cwd=repo_path
        )
        
        if not success:
            print(f"❌ Push failed: {output}")
            return False
        
        print("✅ Push successful!")
        return True

    def run(self, push: bool = True, custom_message: Optional[str] = None, 
            specific_dir: Optional[str] = None, add_all: bool = False):
        """Main execution flow"""
        clear_terminal()
        print(f"🤖 AI Commit (Provider: {self.ai_provider.upper()})")
        print("=" * 50)
        
        # Select directory
        repo_path = self.select_directory(specific_dir)
        if not repo_path:
            return
        
        repo_name = Path(repo_path).name
        print(f"\n📂 Working directory: {repo_name}")
        print(f"📍 Path: {repo_path}")
        
        # Auto git add
        if not self.auto_git_add(repo_path, add_all):
            return
        
        # Get diff
        diff = self.get_git_diff(repo_path)
        if not diff:
            return
        
        # Generate or use custom message
        if custom_message:
            commit_message = custom_message
            print(f"\n📝 Using a custom message: {commit_message}")
        else:
            print("\n🔍 Analyzing changes...")
            commit_message = self.generate_commit_message(diff)
            
            if not commit_message:
                return
            
            # Confirm
            print(f"\n💡 AI suggests commit message:")
            print(f"   {commit_message}")
            
            response = input("\n▶ Use this message? (y/n/edit): ").lower()
            
            if response == 'n':
                print("❌ Cancelled.")
                return
            elif response == 'edit':
                commit_message = input("📝 Enter a new commit message: ")
        
        # Commit and push
        self.commit_and_push(repo_path, commit_message, push)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-powered git commit tool")
    parser.add_argument(
        "--provider",
        choices=["gemini", "chatgpt"],
        default="gemini",
        help="AI provider (default: gemini)"
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Just commit without pushing"
    )
    parser.add_argument(
        "-m", "--message",
        type=str,
        help="Custom commit message (skip AI generation)"
    )
    parser.add_argument(
        "-d", "--dir",
        type=str,
        help="Specific directory/folder for commit (use ../FolderName for sibling folders)"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Add all files without confirmation"
    )
    
    args = parser.parse_args()
    
    try:
        ai_commit = AICommit(ai_provider=args.provider)
        ai_commit.run(
            push=not args.no_push,
            custom_message=args.message,
            specific_dir=args.dir,
            add_all=args.all
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()