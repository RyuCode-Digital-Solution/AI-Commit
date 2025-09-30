import os
import subprocess
import sys
from typing import Optional, List
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


class AICommit:
    def __init__(self, ai_provider: str = "gemini"):
        """
        Initialize AI Commit
        
        Args:
            ai_provider: "gemini" atau "chatgpt"
        """
        self.ai_provider = ai_provider.lower()
        
        if self.ai_provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise ImportError("Install google-generativeai: pip install google-generativeai")
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("Set GEMINI_API_KEY environment variable")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            
        elif self.ai_provider == "chatgpt":
            if not OPENAI_AVAILABLE:
                raise ImportError("Install openai: pip install openai")
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("Set OPENAI_API_KEY environment variable")
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError("AI provider harus 'gemini' atau 'chatgpt'")

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

    def find_git_repos(self, base_path: str = ".") -> List[tuple[str, str, bool]]:
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
                print(f"❌ Direktori '{specific_dir}' tidak ditemukan")
                return None
            if not self.is_git_repo(str(dir_path)):
                print(f"❌ '{specific_dir}' bukan git repository")
                return None
            return str(dir_path)
        
        # Auto-detect git repos in parent directory
        repos = self.find_git_repos()
        
        if not repos:
            print("❌ Tidak ada git repository ditemukan di parent folder")
            print("💡 Tip: Pastikan folder sibling adalah git repositories")
            return None
        
        # Show all repositories with change indicators
        print("\n📁 Git repositories ditemukan:")
        
        repos_with_changes = []
        repos_without_changes = []
        
        for idx, (name, path, has_changes) in enumerate(repos, 1):
            if has_changes:
                repos_with_changes.append((idx, name, path))
                print(f"   {idx}. {name} 🔴")
            else:
                repos_without_changes.append((idx, name, path))
                print(f"   {idx}. {name} ⚪")
        
        print("\n   🔴 = Ada perubahan yang belum di-commit")
        print("   ⚪ = Tidak ada perubahan")
        
        # Auto-select if only one repo has changes
        if len(repos_with_changes) == 1 and len(repos) > 1:
            auto_select = repos_with_changes[0]
            response = input(f"\n💡 Hanya '{auto_select[1].replace(' (current)', '')}' yang ada perubahan. Gunakan? (Y/n): ").lower()
            if response != 'n':
                display_name = auto_select[1].replace(" (current)", "")
                print(f"✅ Dipilih: {display_name}")
                return auto_select[2]
        
        # Manual selection
        while True:
            try:
                choice = input("\n❓ Pilih repository (nomor): ")
                idx = int(choice) - 1
                if 0 <= idx < len(repos):
                    selected = repos[idx]
                    display_name = selected[0].replace(" (current)", "")
                    print(f"✅ Dipilih: {display_name}")
                    return selected[1]
                else:
                    print("❌ Nomor tidak valid")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Dibatalkan")
                return None

    def get_changed_files(self, repo_path: str) -> Optional[List[str]]:
        """Get list of changed files"""
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=repo_path
        )
        
        if not success:
            return None
        
        files = []
        for line in output.strip().split('\n'):
            if line:
                # Parse git status output
                status = line[:2]
                filename = line[3:]
                if status.strip():  # Has changes
                    files.append((status, filename))
        
        return files

    def auto_git_add(self, repo_path: str, add_all: bool = False) -> bool:
        """Automatically add files with selection"""
        files = self.get_changed_files(repo_path)
        
        if not files:
            print("❌ Tidak ada perubahan yang terdeteksi")
            return False
        
        print(f"\n📝 Perubahan terdeteksi ({len(files)} file):")
        for idx, (status, filename) in enumerate(files, 1):
            status_icon = "🆕" if "?" in status else "✏️" if "M" in status else "🗑️" if "D" in status else "📝"
            print(f"   {idx}. {status_icon} {filename}")
        
        if add_all:
            print("\n➕ Menambahkan semua file...")
            success, output = self.run_git_command(["git", "add", "."], cwd=repo_path)
        else:
            response = input("\n❓ Add semua file? (y/n/select): ").lower()
            
            if response == 'y':
                success, output = self.run_git_command(["git", "add", "."], cwd=repo_path)
            elif response == 'select':
                print("📌 Masukkan nomor file yang ingin di-add (pisahkan dengan koma, contoh: 1,3,5)")
                selection = input("   Nomor: ")
                try:
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    selected_files = [files[i][1] for i in indices if 0 <= i < len(files)]
                    
                    if not selected_files:
                        print("❌ Tidak ada file yang valid")
                        return False
                    
                    success, output = self.run_git_command(
                        ["git", "add"] + selected_files,
                        cwd=repo_path
                    )
                except (ValueError, IndexError):
                    print("❌ Input tidak valid")
                    return False
            else:
                print("❌ Dibatalkan")
                return False
        
        if not success:
            print(f"❌ Git add gagal: {output}")
            return False
        
        print("✅ File berhasil di-add!")
        return True

    def get_git_diff(self, repo_path: str) -> Optional[str]:
        """Get staged changes"""
        success, diff = self.run_git_command(["git", "diff", "--cached"], cwd=repo_path)
        if not success or not diff.strip():
            print("❌ Tidak ada perubahan yang di-stage.")
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
        prompt = f"""Berdasarkan git diff berikut, buatkan commit message yang jelas dan deskriptif mengikuti conventional commits format.

Git diff:
```
{diff[:3000]}
```

Buatkan commit message dengan format:
<type>(<scope>): <subject>

<body (opsional)>

Type bisa: feat, fix, docs, style, refactor, test, chore
Gunakan bahasa Inggris, singkat dan jelas.
Berikan hanya commit message tanpa penjelasan tambahan."""

        try:
            if self.ai_provider == "gemini":
                response = self.model.generate_content(prompt)
                return response.text.strip()
            else:  # chatgpt
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates git commit messages."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Error generating commit message: {e}")
            return None

    def commit_and_push(self, repo_path: str, message: str, push: bool = True) -> bool:
        """Commit changes and optionally push"""
        # Commit
        print(f"\n📝 Committing dengan message:")
        print(f"   {message}\n")
        
        success, output = self.run_git_command(
            ["git", "commit", "-m", message],
            cwd=repo_path
        )
        if not success:
            print(f"❌ Commit gagal: {output}")
            return False
        
        print("✅ Commit berhasil!")
        
        if not push:
            return True
        
        # Get current branch
        branch = self.get_current_branch(repo_path)
        if not branch:
            print("❌ Gagal mendapatkan nama branch")
            return False
        
        # Push
        print(f"\n🚀 Pushing ke origin/{branch}...")
        success, output = self.run_git_command(
            ["git", "push", "origin", branch],
            cwd=repo_path
        )
        
        if not success:
            print(f"❌ Push gagal: {output}")
            return False
        
        print("✅ Push berhasil!")
        return True

    def run(self, push: bool = True, custom_message: Optional[str] = None, 
            specific_dir: Optional[str] = None, add_all: bool = False):
        """Main execution flow"""
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
            print(f"\n📝 Menggunakan custom message: {commit_message}")
        else:
            print("\n🔍 Menganalisis perubahan...")
            commit_message = self.generate_commit_message(diff)
            
            if not commit_message:
                return
            
            # Confirm
            print(f"\n💡 AI menyarankan commit message:")
            print(f"   {commit_message}")
            
            response = input("\n❓ Gunakan message ini? (y/n/edit): ").lower()
            
            if response == 'n':
                print("❌ Dibatalkan.")
                return
            elif response == 'edit':
                commit_message = input("📝 Masukkan commit message baru: ")
        
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
        help="Commit saja tanpa push"
    )
    parser.add_argument(
        "-m", "--message",
        type=str,
        help="Custom commit message (skip AI generation)"
    )
    parser.add_argument(
        "-d", "--dir",
        type=str,
        help="Specific directory/folder untuk commit (gunakan ../FolderName untuk sibling folders)"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Add semua file tanpa konfirmasi"
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
