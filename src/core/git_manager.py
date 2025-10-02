"""
Git Manager for handling Git operations
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any, Callable


class GitManager:
    def __init__(self):
        pass
    
    def run_git_command(self, command: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
        """Execute git command with hidden console"""
        try:
            # Hide console window for Windows
            startupinfo = None
            creationflags = 0
            if os.name == 'nt':  # Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
                creationflags = subprocess.CREATE_NO_WINDOW
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=cwd,
                timeout=30,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            output = result.stdout.strip() if result.stdout else ""
            return result.returncode == 0, output
        except subprocess.TimeoutExpired:
            return False, "Command timed out after 30 seconds"
        except subprocess.CalledProcessError as e:
            error_output = e.stderr if e.stderr else str(e)
            return False, error_output.strip()
        except FileNotFoundError:
            return False, "Git command not found. Is Git installed?"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def is_git_repo(self, path: str) -> bool:
        """Check if path is a git repository"""
        return (Path(path) / ".git").exists()
    
    def check_has_changes(self, repo_path: str) -> bool:
        """Check if repository has changes"""
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=repo_path
        )
        return success and bool(output)
    
    def scan_repositories(self, parent_folder: str) -> List[Dict[str, Any]]:
        """Scan for git repositories in parent folder"""
        repos = []
        scan_path = Path(parent_folder)
        
        if not scan_path.exists():
            return repos
        
        try:
            for item in sorted(scan_path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    if self.is_git_repo(str(item)):
                        has_changes = self.check_has_changes(str(item))
                        indicator = "🔴" if has_changes else "⚪"
                        
                        display_name = f"{indicator} {item.name}"
                        if item.resolve() == Path('.').resolve():
                            display_name += " (current)"
                        
                        repos.append({
                            'name': item.name,
                            'path': str(item),
                            'has_changes': has_changes,
                            'display_name': display_name
                        })
        except PermissionError:
            pass
        
        return repos
    
    def get_status(self, repo_path: str) -> Tuple[bool, str]:
        """Get git status with encoding handling"""
        success, output = self.run_git_command(
            ["git", "status", "--porcelain"],
            cwd=repo_path
        )
        
        if not success:
            return False, output
        
        # Ensure we return empty string instead of None
        return True, output if output is not None else ""
    
    def parse_git_status(self, output: str) -> List[Dict[str, Any]]:
        """Parse git status output correctly"""
        files = []
        
        if not output:
            return files
            
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
                
            # Git status format: XY filename
            status = line[:2].strip()
            filename = line[3:].strip()
            
            # Handle renamed files: "R  oldfile -> newfile"
            if '->' in filename:
                if 'R' in status:  # Renamed
                    parts = filename.split('->')
                    old_file = parts[0].strip()
                    new_file = parts[1].strip()
                    files.append({
                        'status': status,
                        'filename': new_file,
                        'old_filename': old_file,
                        'type': 'renamed'
                    })
                    continue
                elif 'C' in status:  # Copied
                    parts = filename.split('->')
                    old_file = parts[0].strip()
                    new_file = parts[1].strip()
                    files.append({
                        'status': status,
                        'filename': new_file,
                        'old_filename': old_file,
                        'type': 'copied'
                    })
                    continue
            
            # Handle regular files
            files.append({
                'status': status,
                'filename': filename,
                'type': 'regular'
            })
        
        return files
    
    def find_exact_file(self, repo_path: str, filename: str, raw_git_status: List[Dict]) -> Optional[str]:
        """Find exact file match in git status"""
        repo_path_obj = Path(repo_path)
        filename = filename.replace('\\', '/')
        
        # Direct check
        if (repo_path_obj / filename).exists():
            return filename
        
        # For deleted files, we don't expect them to exist
        for file_info in raw_git_status:
            if file_info['filename'] == filename:
                if 'D' in file_info['status']:
                    return filename
                if (repo_path_obj / filename).exists():
                    return filename
        
        return None
    
    def stage_files(self, repo_path: str, raw_git_status: List[Dict], 
                   selected_indices: List[int], log_func: Callable) -> Tuple[int, List[str]]:
        """Stage selected files"""
        files_to_add = []
        deleted_files = []
        renamed_files = []
        
        for i in selected_indices:
            if i < len(raw_git_status):
                file_info = raw_git_status[i]
                status_code = file_info['status']
                filename = file_info['filename']
                file_type = file_info.get('type', 'regular')
                
                if file_type == 'renamed':
                    old_filename = file_info.get('old_filename')
                    if old_filename:
                        renamed_files.append((old_filename, filename))
                elif 'D' in status_code:
                    deleted_files.append(filename)
                else:
                    files_to_add.append(filename)
        
        success_count = 0
        error_messages = []
        
        # Handle deleted files
        for filename in deleted_files:
            success_rm, output_rm = self.run_git_command(
                ["git", "rm", filename],
                cwd=repo_path
            )
            if success_rm:
                success_count += 1
                log_func(f"🗑️ Staged deletion: {filename}", "success")
            else:
                # Fallback to add for deleted files
                success_add, _ = self.run_git_command(
                    ["git", "add", "--", filename],
                    cwd=repo_path
                )
                if success_add:
                    success_count += 1
                    log_func(f"✅ Staged: {filename}", "success")
                else:
                    error_messages.append(f"Failed to stage {filename}")
                    log_func(f"❌ Failed to stage: {filename}", "error")
        
        # Handle renamed files
        for old_file, new_file in renamed_files:
            success_rm, _ = self.run_git_command(
                ["git", "rm", "--", old_file],
                cwd=repo_path
            )
            success_add, _ = self.run_git_command(
                ["git", "add", "--", new_file],
                cwd=repo_path
            )
            if success_rm and success_add:
                success_count += 1
                log_func(f"🔄 Staged rename: {old_file} → {new_file}", "success")
            else:
                error_messages.append(f"Failed to stage rename: {old_file} → {new_file}")
                log_func(f"❌ Failed rename: {old_file} → {new_file}", "error")
        
        # Handle other files
        for filename in files_to_add:
            actual_file = self.find_exact_file(repo_path, filename, raw_git_status)
            
            if actual_file:
                success_add, output_add = self.run_git_command(
                    ["git", "add", "--", actual_file],
                    cwd=repo_path
                )
                
                if success_add:
                    success_count += 1
                    log_func(f"✅ Staged: {actual_file}", "success")
                else:
                    error_messages.append(f"Failed to add {actual_file}")
                    log_func(f"❌ Failed to add: {actual_file}\n{output_add}", "error")
            else:
                # Try adding as-is
                success_add, output_add = self.run_git_command(
                    ["git", "add", "--", filename],
                    cwd=repo_path
                )
                if success_add:
                    success_count += 1
                    log_func(f"✅ Staged: {filename}", "success")
                else:
                    log_func(f"❌ File not found: {filename}", "error")
                    error_messages.append(f"File not found: {filename}")
        
        return success_count, error_messages
    
    def auto_stage_files(self, repo_path: str, raw_git_status: List[Dict],
                        selected_indices: List[int], log_func: Callable) -> int:
        """Auto stage files for AI generation"""
        files_to_add = []
        deleted_files = []
        renamed_files = []
        
        for i in selected_indices:
            if i < len(raw_git_status):
                file_info = raw_git_status[i]
                status_code = file_info['status']
                filename = file_info['filename']
                file_type = file_info.get('type', 'regular')
                
                if file_type == 'renamed':
                    old_filename = file_info.get('old_filename')
                    if old_filename:
                        renamed_files.append((old_filename, filename))
                elif 'D' in status_code:
                    deleted_files.append(filename)
                else:
                    files_to_add.append(filename)
        
        # Handle deleted files
        for filename in deleted_files:
            success_rm, _ = self.run_git_command(["git", "rm", filename], cwd=repo_path)
            if success_rm:
                log_func(f"🗑️ Staged deletion: {filename}")
        
        # Handle renamed files
        for old_file, new_file in renamed_files:
            self.run_git_command(["git", "rm", "--", old_file], cwd=repo_path)
            self.run_git_command(["git", "add", "--", new_file], cwd=repo_path)
            log_func(f"🔄 Staged rename: {old_file} → {new_file}")
        
        # Handle other files
        for filename in files_to_add:
            actual_file = self.find_exact_file(repo_path, filename, raw_git_status)
            if actual_file:
                success_add, _ = self.run_git_command(["git", "add", "--", actual_file], cwd=repo_path)
                if success_add:
                    log_func(f"✅ Staged: {actual_file}")
            else:
                self.run_git_command(["git", "add", "--", filename], cwd=repo_path)
        
        return len(files_to_add) + len(deleted_files) + len(renamed_files)
    
    def get_staged_diff(self, repo_path: str) -> Tuple[bool, Optional[str]]:
        """Get staged diff for AI analysis"""
        success, diff = self.run_git_command(["git", "diff", "--cached"], cwd=repo_path)
        
        if not success:
            return False, None
        
        # Handle case where diff might be None or empty
        if diff is None:
            return False, None
            
        diff = diff.strip()
        if not diff:
            return True, ""  # Return empty string instead of None
        
        return True, diff
    
    def commit_changes(self, repo_path: str, message: str) -> Tuple[bool, str]:
        """Commit staged changes"""
        return self.run_git_command(["git", "commit", "-m", message], cwd=repo_path)
    
    def push_changes(self, repo_path: str, github_username: str, 
                    github_token: str, log_func: Callable) -> Tuple[bool, str]:
        """Push changes to remote"""
        # Configure GitHub credentials if provided
        if github_username:
            self.run_git_command(["git", "config", "user.name", github_username], cwd=repo_path)
        
        # Get current branch
        success, branch = self.run_git_command(["git", "branch", "--show-current"], cwd=repo_path)
        if not success:
            return False, "Failed to get branch name"
        
        branch = branch.strip()
        log_func(f"🚀 Pushing to origin/{branch}...")
        
        # Push to remote
        return self.run_git_command(["git", "push", "origin", branch], cwd=repo_path)