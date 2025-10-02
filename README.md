# 🤖 AI Commit

[![Language](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Bahasa](https://img.shields.io/badge/Bahasa-Indonesia-red)](README.id.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)

> An AI-powered commit tool that generates high-quality commit messages and supports multi-project workspaces

AI Commit is a Python utility that leverages the power of AI (Gemini & ChatGPT) to analyze your code changes and automatically generate commit messages that follow the **Conventional Commits** standard.

![GUI Version](https://github.com/user-attachments/assets/2387bd34-3e15-4ce8-9c93-2ea69e3281b7)

---

## ✨ Key Features

- **🔍 Auto-Scan** – Automatically scans repositories when the app starts
- **🎯 Visual Selection** – Select repositories and files with your mouse
- **🤖 One-Click AI** – Generate commit messages with a single click
- **📊 Real-time Log** – View all activities in the log panel
- **⚙️ Easy Settings** – Toggle AI provider and auto-push options
- **✅ Batch Selection** – Select all or clear selection with ease
- **🎨 Modern UI** – Clean and intuitive interface
- **🌙 Dark Mode** – Switch between light and dark themes
- **📝 Smart File Matching** – Auto-detect similar files if errors occur
- **⚙️ Settings Manager** – Load/save settings from JSON with error handling
- **🔧 Settings Dialog** – Organized tab-based interface
- **🤖 AI Configuration** – Choose custom models and manage API keys
- **🐙 GitHub Integration** – Username and token support for private repositories
- **📂 Repository Management** – Custom parent folder & recent repositories
- **🔄 Auto Refresh** – Manually refresh to detect file changes
- **🎯 Better Organization** – All configurations in one place

### Workflow

1. **Open the app** → Auto-scan runs automatically
2. **Select a repository** from the dropdown (🔴 indicates changes)
3. **Configure Settings (first-time setup)** – Click **⚙️ Settings**
4. **Select files** to commit (or click Select All)
5. **Click "➕ Add to Stage"** to stage files
6. **Click "🤖 Generate with AI"** to create commit messages (or write manually)
7. **Review the message** in the text area
8. **Click "✅ Commit & Push"** to commit and push changes

### Settings Configuration

**Access Settings:** Click the **⚙️ Settings** button in the main window

##### AI Settings Tab

- **AI Provider:** Choose between Gemini or ChatGPT
- **API Key:** Enter the API key for the chosen provider
- **Model Selection:** Select specific models (gemini-1.5-pro, gpt-4, etc.)

##### GitHub Tab

- **GitHub Username:** Your GitHub username
- **GitHub Token:** Personal access token for private repos
- **Auto-configure Git:** Automatically set git config with credentials

##### Repository Tab

- **Parent Folder:** Custom folder for scanning repositories
- **Recent Repositories:** History of previously opened repos
- **Browse Repository:** Manually select a repository folder
- **Refresh Button:** Manually refresh to detect changes

### Dark Mode

The GUI supports **light and dark themes** for better eye comfort:

**How to enable:**

- Toggle the **"🌙 Dark Mode"** checkbox in the top-right corner
- The theme instantly updates for all components

**Dark Theme:**

- Comfortable dark background (#1e1e1e)
- Bright text (#ffffff) for contrast
- Gray frames (#2d2d2d) for clear separation
- Deep blue accents (#0e639c) for highlights
- Perfect for night-time or low-light environments

**Light Theme:**

- Bright background (#f0f0f0) for well-lit rooms
- Black text (#000000) for maximum clarity
- White frames (#ffffff) for a clean look
- Bright blue accents (#0078d4) for interactions
- Best for daytime or bright environments

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or later
- Git installed
- API Key from Gemini or OpenAI

### Windows

- Download [AI-Commit.exe](https://github.com/RyuCode-Digital-Solution/AI-Commit/blob/v1/dist/AI-Commit.exe) – Stable version 1 (1.0.0)

---

## 🔑 Configuration

#### Gemini API Key (Free – Recommended)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

#### OpenAI API Key (Paid)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Log in or create an account
3. Click "Create new secret key"
4. Copy the generated key

#### GitHub Token

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes: **repo** and **workflow**
4. Copy the generated token

---

## ❓ FAQ

### Q: How do I enable Dark Mode in the GUI?

**A:**

1. Open the app
2. In the top-right corner, check the **"🌙 Dark Mode"** box
3. Toggle to switch between light and dark themes
4. The theme updates instantly across the UI

Dark Mode is useful for:

- Night-time work
- Reducing eye strain
- Low-light environments
- Personal preference

### Q: How do I configure the GitHub token?

**A:**

1. Click **⚙️ Settings**
2. Open the **GitHub** tab
3. Enter your GitHub username and token
4. Check "Auto-configure Git" for automatic setup
5. Click Save

### Q: How do I add a custom parent folder?

**A:**

1. Open **Settings → Repository tab**
2. Click "Browse" next to **Parent Folder**
3. Select the folder containing your Git repositories
4. Click Save
5. The repository dropdown updates automatically

### Q: Is this tool free?

**A:** The tool itself is 100% free and open-source. For AI usage:

- **Gemini API:** Free with a generous daily quota (recommended)
- **OpenAI API:** Paid, around $0.002 per commit

### Q: Is my data safe?

**A:**

- ✅ Only **git diff** (code changes) is sent to the AI
- ✅ No data is stored on external servers
- ✅ API keys and settings are stored locally
- ⚠️ Do not commit files containing secrets/passwords/tokens

---

## 🤝 Contributing

Contributions are always welcome!

### How to Contribute:

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/CoolFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'feat: add cool feature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/CoolFeature
   ```
5. Create a Pull Request

---

## 🙏 Credits

- **AI Providers:**
  - [Google Gemini](https://ai.google.dev/) – Free AI with large quota
  - [OpenAI](https://openai.com/) – Powerful GPT models
- **Standards:**
  - [Conventional Commits](https://www.conventionalcommits.org/) – Commit message standard
- **Inspired by:**
  - aicommits by Nutlope
  - GitHub Copilot

---

## 📞 Support & Contact

### Found a Bug?

- 🐛 Open an issue with the label `bug`
- Include error messages and reproduction steps

### Have Suggestions?

- 💡 Open an issue with the label `enhancement`
- Describe the use case and expected behavior

### Need Help?

- 📖 Read FAQ and Troubleshooting above
- 💬 Open an issue with the label `question`
- 📧 Email: dev@ryucode.com

---

**Built with ❤️ for developers who value clean commit history**

⭐ **Star this repository if you find it useful!**

🚀 **Happy Committing with AI!**

---

**[🇮🇩 Baca dalam Bahasa Indonesia](README.id.md)**
