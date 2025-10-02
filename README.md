# 🤖 AI Commit

[![Language](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Bahasa](https://img.shields.io/badge/Bahasa-Indonesia-red)](README.id.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)

> AI-powered automatic commit tool that generates quality commit messages and supports multi-project workspace

AI Commit is a Python utility that leverages AI power (Gemini & ChatGPT) to analyze your code changes and automatically generate commit messages following conventional commits standards.

**Available in 2 versions:**

- 🖥️ **CLI Version** - Command line interface for terminal lovers
- 🎨 **GUI Version** - Graphical interface with Tkinter (no additional dependencies!)

---

## ✨ Key Features

- 🎯 **Auto-Generate Commit Messages** - AI analyzes diff and creates descriptive commit messages
- 🤖 **Multi AI Provider** - Support for Gemini and ChatGPT
- 📁 **Multi-Project Support** - Manage multiple git repositories in one workspace
- 🔍 **Auto-Detect Changes** - Scan and display which folders have changes
- ➕ **Smart Git Add** - Auto-detect changes with selective add option
- 🚀 **Auto Push** - Automatically push to origin current branch
- 📝 **Interactive Mode** - Confirmation and edit before commit
- 🎨 **Conventional Commits** - Follow conventional commits standard format
- 🖼️ **GUI Interface** - User-friendly graphical interface
- 🌙 **Dark Mode** - Toggle between light and dark theme for eye comfort

---

## 📂 Supported Folder Structure

This tool is **specifically designed** to work with workspace structure like this:

```
workspace/
├── Folder1/              # Git Repository 1
│   ├── .git/
│   └── ...
├── Folder2/              # Git Repository 2
│   ├── .git/
│   └── ...
├── Folder3/              # Git Repository 3
│   ├── .git/
│   └── ...
└── AI-Commit/            # Tool folder (run script from here)
    ├── ai_commit.py
    └── ai_commit_gui.py
```

**How it works:**

- Tool runs from inside `AI-Commit` folder
- Automatically scans **parent directory** to find all git repositories (Folder1, Folder2, Folder3)
- Detects which folders have changes (marked with 🔴)
- You choose which folder to commit and push

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or newer
- Git installed
- API Key from Gemini or OpenAI

### Install Dependencies

```bash
# Clone repository
git clone https://github.com/RyuCode-Digital-Solution/AI-Commit

# Enter AI-Commit folder
cd AI-Commit

# Install required packages
pip install -r requirements.txt
```

## 🔑 Configuration

### 1. Get API Key

#### Gemini API Key (Free - Recommended)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Login with Google account
3. Click "Create API Key"
4. Copy the generated API key

#### OpenAI API Key (Paid)

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Login or create account
3. Click "Create new secret key"
4. Copy the generated API key

### 2. Set Environment Variables

#### Linux/Mac

**Temporary (current session only):**

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Permanent (add to ~/.bashrc or ~/.zshrc):**

```bash
echo 'export GEMINI_API_KEY="your-gemini-api-key-here"' >> ~/.bashrc
echo 'export OPENAI_API_KEY="your-openai-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

**Command Prompt (Temporary):**

```cmd
set GEMINI_API_KEY=your-gemini-api-key-here
set OPENAI_API_KEY=your-openai-api-key-here
```

**PowerShell (Temporary):**

```powershell
$env:GEMINI_API_KEY="your-gemini-api-key-here"
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

**Permanent (System Environment Variables):**

1. Open "System Properties" → "Environment Variables"
2. Click "New" in User Variables
3. Variable name: `GEMINI_API_KEY`
4. Variable value: your-api-key
5. Repeat for `OPENAI_API_KEY`

---

## 🎨 GUI Version (Recommended)

![GUI Version](https://github.com/user-attachments/assets/2387bd34-3e15-4ce8-9c93-2ea69e3281b7)

### Features

1. **🔍 Auto-Scan** - Automatically scan repositories on app startup
2. **🎯 Visual Selection** - Choose repository and files with mouse
3. **🤖 One-Click AI** - Generate commit message with one click
4. **📊 Real-time Log** - View all activities in log panel
5. **⚙️ Easy Settings** - Toggle AI provider and auto-push
6. **✅ Batch Selection** - Select all or clear selection easily
7. **🎨 Modern UI** - Clean and intuitive interface
8. **🌙 Dark Mode** - Toggle between light and dark theme
9. **📝 Smart File Matching** - Auto-detect similar files on error
10. **🔄 Auto Refresh** - File list auto-refreshes after staging

### How to Use

```bash
# Enter AI-Commit folder
cd AI-Commit

# Run GUI version
python ai_commit_gui.py
```

### GUI Workflow

1. **Open app** → Auto-scan runs
2. **Select repository** from dropdown (with 🔴 changes indicator)
3. **Toggle Dark Mode** if needed (🌙 checkbox top right)
4. **Select files** to commit (or Select All)
5. **Click "➕ Add to Stage"** to stage files
6. **Click "🤖 Generate with AI"** for AI commit message (or write manually)
7. **Review message** in text area
8. **Click "✅ Commit & Push"** to commit and push

### Dark Mode

GUI supports **light and dark themes** for your eye comfort:

**How to Activate:**

- Check/Uncheck **"🌙 Dark Mode"** checkbox in top right corner
- Theme instantly changes for all components

**Dark Theme:**

- Dark background (#1e1e1e) comfortable for eyes
- Light text (#ffffff) for optimal contrast
- Gray frames (#2d2d2d) for clear separation
- Dark blue accent (#0e639c) for highlights
- Perfect for night work or dark rooms

**Light Theme:**

- Light background (#f0f0f0) for bright rooms
- Black text (#000000) for maximum sharpness
- White frames (#ffffff) for clean appearance
- Bright blue accent (#0078d4) for interaction
- Perfect for daytime work or bright rooms

---

## 🖥️ CLI Version

![CLI Version](https://github.com/user-attachments/assets/804fe01e-1a86-450a-8731-64797c3929db)

### Quick Start

```bash
# Enter AI-Commit folder
cd AI-Commit

# Run tool
python ai_commit.py

# Tool will scan parent folder and display repositories
# Choose repository to commit (marked with 🔴)
# Select files to add
# Review AI-generated commit message
# Confirm and auto push!
```

### Command Line Options

| Option       | Short | Description                         | Example              |
| ------------ | ----- | ----------------------------------- | -------------------- |
| `--provider` | -     | Choose AI provider (gemini/chatgpt) | `--provider chatgpt` |
| `--dir`      | `-d`  | Specify target directory            | `--dir ../Folder1`   |
| `--all`      | `-a`  | Add all files without confirmation  | `--all`              |
| `--message`  | `-m`  | Custom commit message (skip AI)     | `-m "fix: bug"`      |
| `--no-push`  | -     | Commit without push                 | `--no-push`          |
| `--help`     | `-h`  | Display help message                | `--help`             |

### CLI Examples

```bash
# Auto-detect and interactive
python ai_commit.py

# Specific folder with ChatGPT
python ai_commit.py --dir ../Folder1 --provider chatgpt

# Quick commit with custom message
python ai_commit.py --dir ../Folder2 -m "docs: update README" --no-push

# Full automation
python ai_commit.py --dir ../Folder3 --all
```

---

## 🎯 GUI vs CLI Comparison

| Feature           | GUI        | CLI        |
| ----------------- | ---------- | ---------- |
| Ease of Use       | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     |
| Speed             | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ |
| Visual Feedback   | ⭐⭐⭐⭐⭐ | ⭐⭐       |
| Automation        | ⭐⭐       | ⭐⭐⭐⭐⭐ |
| Remote Access     | ❌         | ✅         |
| Beginner Friendly | ✅         | ⚠️         |
| Dark Mode         | ✅         | ❌         |

**Recommendation:**

- 🎨 **Use GUI** if: beginner, prefer visual, working locally
- 🖥️ **Use CLI** if: power user, automation, remote work

---

## 🔧 Troubleshooting

### Problem: "GEMINI_API_KEY not found"

**Solution:**

```bash
# Check if already set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows CMD

# If empty, set again
export GEMINI_API_KEY="your-api-key"  # Linux/Mac
set GEMINI_API_KEY=your-api-key  # Windows
```

### Problem: "No git repositories found"

**Solution:**

1. Ensure you run tool from **inside AI-Commit folder**
2. Ensure sibling folders (Folder1, Folder2, etc) are git repositories
3. Check with:
   ```bash
   cd ../Folder1
   ls -la .git  # Linux/Mac
   dir .git  # Windows
   ```
4. If not git repo yet, init first:
   ```bash
   cd ../Folder1
   git init
   git remote add origin <your-repo-url>
   ```

### Problem: "GUI not appearing / Tkinter Error"

**Solution:**

**Linux:**

```bash
# Install tkinter
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install python3-tkinter  # CentOS/RHEL
```

**macOS:**

```bash
# Tkinter already included, but if error:
brew install python-tk
```

**Windows:**

- Tkinter already included in Python installer
- If missing, reinstall Python and check "tcl/tk" option

---

## ❓ FAQ

### Q: How to activate Dark Mode in GUI?

**A:**

1. Open GUI app (`python ai_commit_gui.py`)
2. Look at top right corner, there's "🌙 Dark Mode" checkbox
3. Click checkbox to toggle between light and dark theme
4. Theme instantly changes for all UI components

Dark Mode suitable for:

- Night work
- Reducing eye strain
- Low-light rooms
- Personal visual preference

### Q: Is Dark Mode saved after app closes?

**A:** No, theme resets to Light Mode each time app opens. This is default behavior for now. If you want Dark Mode as default, edit `ai_commit_gui.py`:

```python
# Find this line (around line 30):
self.dark_mode = tk.BooleanVar(value=False)

# Change to:
self.dark_mode = tk.BooleanVar(value=True)  # Default Dark Mode
```

### Q: Is this tool free?

**A:** Tool is 100% free and open source. However for AI:

- **Gemini API**: Free with sufficient daily quota (recommended)
- **OpenAI API**: Paid, around $0.002 per commit

### Q: Is my data safe?

**A:**

- ✅ Tool only sends **git diff** (code changes) to AI
- ✅ No data stored on server
- ✅ API key stored locally in your environment variables
- ⚠️ Don't commit files containing secrets/passwords/tokens

### Q: GUI or CLI, which is better?

**A:** Depends on your needs:

- **GUI**: Easier for beginners, visual feedback, suitable for daily use
- **CLI**: Faster, can be automated, suitable for power users and remote work

You can use both! GUI for regular commits, CLI for scripting.

---

## 🤝 Contributing

Contributions always welcome!

### How to Contribute:

1. Fork repository
2. Create feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit changes
   ```bash
   git commit -m 'feat: add amazing feature'
   ```
4. Push to branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Create Pull Request

### Contributing Ideas:

- [x] CLI Version
- [x] GUI Version with Tkinter
- [x] Dark Mode
- [x] Smart File Matching
- [ ] PyQt5/PyQt6 version for advanced GUI
- [ ] System tray integration
- [ ] Drag & drop file support in GUI
- [ ] Git graph visualization
- [ ] Multi-repo batch commit
- [ ] Config file support
- [ ] Plugin system

---

## 🙏 Credits

- **AI Providers:**
  - [Google Gemini](https://ai.google.dev/) - Free AI with generous quota
  - [OpenAI](https://openai.com/) - Powerful GPT models
- **Standards:**
  - [Conventional Commits](https://www.conventionalcommits.org/) - Commit message format
- **Inspired by:**
  - aicommits by Nutlope
  - GitHub Copilot

---

## 📞 Support & Contact

### Found a Bug?

- 🐛 Create issue in repository with `bug` label
- Include error message and reproduction steps

### Have a Suggestion?

- 💡 Create issue with `enhancement` label
- Explain use case and expected behavior

### Need Help?

- 📖 Read FAQ and Troubleshooting above
- 💬 Create issue with `question` label
- 📧 Email: dev@ryucode.com

---

**Made with ❤️ for developers who value clean commit history**

⭐ **Star this repository if helpful!**

🚀 **Happy Committing with AI!**

---

**[🇮🇩 Baca dalam Bahasa Indonesia](README.id.md)**
