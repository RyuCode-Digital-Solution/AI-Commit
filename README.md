# 🤖 AI Commit

> Alat commit otomatis berbasis AI yang menghasilkan commit message berkualitas dan mendukung multi-project workspace

AI Commit adalah utilitas Python yang memanfaatkan kekuatan AI (Gemini & ChatGPT) untuk menganalisis perubahan kode Anda dan menghasilkan commit message yang mengikuti standar conventional commits secara otomatis.

**Tersedia dalam 2 versi:**

- 🖥️ **CLI Version** - Command line interface untuk terminal lovers
- 🎨 **GUI Version** - Graphical interface dengan Tkinter (no additional dependencies!)

## ✨ Fitur Utama

- 🎯 **Generate Commit Message Otomatis** - AI menganalisis diff dan membuat commit message yang deskriptif
- 🤖 **Multi AI Provider** - Support Gemini dan ChatGPT
- 📁 **Multi-Project Support** - Kelola multiple git repositories dalam satu workspace
- 🔍 **Auto-Detect Changes** - Scan dan tampilkan folder mana yang ada perubahan
- ➕ **Smart Git Add** - Auto-detect perubahan dengan opsi selective add
- 🚀 **Auto Push** - Otomatis push ke origin branch saat ini
- 📝 **Interactive Mode** - Konfirmasi dan edit sebelum commit
- 🎨 **Conventional Commits** - Mengikuti format conventional commits standard
- 🖼️ **GUI Interface** - User-friendly graphical interface (NEW!)

## 📂 Struktur Folder yang Didukung

Tool ini **dirancang khusus** untuk bekerja dengan struktur workspace seperti ini:

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
└── AI-Commit/            # Tool folder (di sini Anda jalankan script)
    └── ai_commit.py
```

**Cara Kerja:**

- Tool dijalankan dari dalam folder `AI-Commit`
- Otomatis scan **parent directory** untuk menemukan semua git repositories (Folder1, Folder2, Folder3)
- Deteksi folder mana yang punya perubahan (ditandai dengan 🔴)
- Anda pilih folder yang ingin di-commit dan push

## 🚀 Instalasi

### Prerequisites

- Python 3.8 atau lebih baru
- Git terinstall
- API Key dari Gemini atau OpenAI

### Install Dependencies

```bash
# Masuk ke folder AI-Commit
cd AI-Commit

# Install required packages
pip install -r requirements.txt
```

## 🎨 GUI Version (Recommended)

### Screenshot

```
┌─────────────────────────────────────────────┐
│                🤖 AI Commit                 |
├─────────────────────────────────────────────┤
│ ⚙️ Settings                                 │
│   AI Provider: ⚪ Gemini  ⚪ ChatGPT        │
│   ☑ Auto Push to Origin                     │
├─────────────────────────────────────────────┤
│ 📁 Select Repository                        │
│   [🔍 Scan] [🔴 Folder1      ▼]            │
├─────────────────────────────────────────────┤
│ 📝 Changed Files                            │
│   ☑ ✏️ src/main.py                         │
│   ☑ 🆕 src/utils.py                        │
│   ☐ 🗑️ old_file.py                         │
│   [✅ Select All] [❌ Clear] [➕ Add]       │
├─────────────────────────────────────────────┤
│ 💬 Commit Message                           │
│   feat(core): add utility functions...      │
│   [🤖 Generate] [🗑️ Clear]                 │
├─────────────────────────────────────────────┤
│   [✅ Commit & Push] [💾 Commit] [❌ Cancel]│
├─────────────────────────────────────────────┤
│ 📋 Log                                      │
│   ✅ Repository scanned                     │
│   ✅ Files added to staging                 │
└─────────────────────────────────────────────┘
```

### Cara Menggunakan GUI

```bash
# Masuk ke folder AI-Commit
cd AI-Commit

# Jalankan GUI version
python ai_commit_gui.py
```

### Fitur GUI

1. **🔍 Auto-Scan** - Otomatis scan repositories saat aplikasi dibuka
2. **🎯 Visual Selection** - Pilih repository dan files dengan mouse
3. **🤖 One-Click AI** - Generate commit message dengan satu klik
4. **📊 Real-time Log** - Lihat semua aktivitas di panel log
5. **⚙️ Easy Settings** - Toggle AI provider dan auto-push
6. **✅ Batch Selection** - Select all atau clear selection dengan mudah
7. **🎨 Modern UI** - Clean and intuitive interface
8. **🌙 Dark Mode** - Toggle antara light dan dark theme
9. **📝 Smart File Matching** - Otomatis mencari file yang mirip jika terjadi error
10. **🔄 Auto Refresh** - File list otomatis refresh setelah staging

### Workflow GUI

1. **Buka aplikasi** → Auto-scan akan berjalan
2. **Pilih repository** dari dropdown (yang 🔴 ada perubahan)
3. **Toggle Dark Mode** jika diperlukan (🌙 checkbox di kanan atas)
4. **Pilih files** yang ingin di-commit (atau Select All)
5. **Klik "➕ Add to Stage"** untuk stage files
6. **Klik "🤖 Generate with AI"** untuk AI commit message (atau tulis manual)
7. **Review message** di text area
8. **Klik "✅ Commit & Push"** untuk commit dan push

### Dark Mode

GUI mendukung **light dan dark theme** untuk kenyamanan mata Anda:

**Cara Mengaktifkan:**

- Cek/Uncek checkbox **"🌙 Dark Mode"** di pojok kanan atas
- Theme akan langsung berubah untuk semua komponen

**Dark Theme Features:**

- Background gelap (#1e1e1e) yang nyaman untuk mata
- Text terang (#ffffff) untuk kontras optimal
- Frame abu-abu (#2d2d2d) untuk pemisahan yang jelas
- Accent biru gelap (#0e639c) untuk highlight
- Cocok untuk bekerja malam hari atau ruangan gelap

**Light Theme Features:**

- Background terang (#f0f0f0) untuk ruangan terang
- Text hitam (#000000) untuk ketajaman maksimal
- Frame putih (#ffffff) untuk tampilan bersih
- Accent biru cerah (#0078d4) untuk interaksi
- Cocok untuk bekerja siang hari atau ruangan terang

## 🖥️ CLI Version

## 🔑 Konfigurasi

### 1. Dapatkan API Key

#### Gemini API Key (Gratis - Recommended)

1. Kunjungi [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Login dengan akun Google
3. Klik "Create API Key"
4. Copy API key yang dihasilkan

#### OpenAI API Key (Berbayar)

1. Kunjungi [OpenAI Platform](https://platform.openai.com/api-keys)
2. Login atau buat akun
3. Klik "Create new secret key"
4. Copy API key yang dihasilkan

### 2. Set Environment Variables

#### Linux/Mac

**Temporary (untuk session saat ini):**

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Permanent (tambahkan ke ~/.bashrc atau ~/.zshrc):**

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

1. Buka "System Properties" → "Environment Variables"
2. Klik "New" di User Variables
3. Variable name: `GEMINI_API_KEY`
4. Variable value: your-api-key
5. Ulangi untuk `OPENAI_API_KEY`

### 3. Verifikasi Instalasi

```bash
cd AI-Commit
python ai_commit.py --help
```

Jika berhasil, Anda akan melihat help message dengan semua opsi yang tersedia.

## 📖 Cara Penggunaan

### GUI Version (Simple & Visual)

```bash
cd AI-Commit
python ai_commit_gui.py
```

**Keuntungan GUI:**

- ✅ Tidak perlu hafal command line options
- ✅ Visual file selection dengan checkbox
- ✅ Real-time preview commit message
- ✅ Activity log yang jelas
- ✅ Cocok untuk pemula

### CLI Version (Fast & Scriptable)

```bash
cd AI-Commit
python ai_commit.py
```

**Keuntungan CLI:**

- ✅ Cepat dan efisien untuk power users
- ✅ Bisa di-script dan di-automate
- ✅ Remote-friendly (via SSH)
- ✅ Minimal resource usage

### Perbandingan GUI vs CLI

| Fitur             | GUI        | CLI        |
| ----------------- | ---------- | ---------- |
| Ease of Use       | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     |
| Speed             | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ |
| Visual Feedback   | ⭐⭐⭐⭐⭐ | ⭐⭐       |
| Automation        | ⭐⭐       | ⭐⭐⭐⭐⭐ |
| Remote Access     | ❌         | ✅         |
| Beginner Friendly | ✅         | ⚠️         |

**Rekomendasi:**

- 🎨 **Gunakan GUI** jika: pemula, prefer visual, bekerja local
- 🖥️ **Gunakan CLI** jika: power user, automation, remote work

### Quick Start

```bash
# 1. Masuk ke folder AI-Commit
cd AI-Commit

# 2. Jalankan tool
python ai_commit.py

# 3. Tool akan scan parent folder dan tampilkan repositories
# 4. Pilih repository yang ingin di-commit (yang ada 🔴)
# 5. Pilih file yang ingin di-add
# 6. Review commit message dari AI
# 7. Confirm dan otomatis push!
```

### Contoh Output Lengkap

```bash
$ python ai_commit.py

🤖 AI Commit (Provider: GEMINI)
==================================================
🔍 Scanning: /home/user/workspace

📁 Git repositories ditemukan:
   1. Folder1 🔴
   2. Folder2 ⚪
   3. Folder3 🔴
   4. AI-Commit (current) ⚪

   🔴 = Ada perubahan yang belum di-commit
   ⚪ = Tidak ada perubahan

💡 Hanya 'Folder1' yang ada perubahan. Gunakan? (Y/n): y
✅ Dipilih: Folder1

📂 Working directory: Folder1
📍 Path: /home/user/workspace/Folder1

📝 Perubahan terdeteksi (3 file):
   1. ✏️ src/main.py
   2. 🆕 src/utils.py
   3. 🗑️ old_file.py

❓ Add semua file? (y/n/select): y
✅ File berhasil di-add!

🔍 Menganalisis perubahan...

💡 AI menyarankan commit message:
   feat(core): add utility functions and refactor main module

❓ Gunakan message ini? (y/n/edit): y

📝 Committing dengan message:
   feat(core): add utility functions and refactor main module

✅ Commit berhasil!

🚀 Pushing ke origin/main...
✅ Push berhasil!
```

## 🎯 Fitur Detail

### 1. Auto-Detect Changes di Parent Folder

Tool akan **scan parent directory** dan menampilkan:

- ✅ Semua git repositories yang ditemukan
- 🔴 Indicator untuk folder yang punya perubahan
- ⚪ Indicator untuk folder yang tidak ada perubahan
- 📍 Marker "(current)" untuk folder tempat tool dijalankan

### 2. Smart Selection

Jika hanya 1 folder yang punya perubahan, tool akan:

- Otomatis suggest folder tersebut
- Tanya konfirmasi (Y/n)
- Langsung lanjut jika user setuju

### 3. Selective File Add

Setelah memilih repository:

```
📝 Perubahan terdeteksi (5 file):
   1. ✏️ modified_file.py
   2. 🆕 new_file.py
   3. 🗑️ deleted_file.py
   4. ✏️ config.json
   5. 📝 README.md

❓ Add semua file? (y/n/select):
```

**Opsi:**

- `y` - Add semua file
- `n` - Batalkan
- `select` - Pilih file tertentu (input: 1,2,5)

### 4. AI-Generated Commit Message

AI menganalisis `git diff` dan generate message dengan format:

```
<type>(<scope>): <subject>

<body>
```

Dengan interactive options:

- `y` - Gunakan message AI
- `n` - Batalkan
- `edit` - Edit manual

## 💡 Contoh Penggunaan

### GUI Version Examples

#### Example 1: First Time User

```bash
cd AI-Commit
python ai_commit_gui.py
```

1. Aplikasi terbuka → Auto-scan running
2. Dropdown menampilkan: `🔴 Folder1`, `⚪ Folder2`, `🔴 Folder3`
3. Pilih `Folder1` dari dropdown
4. Files muncul di listbox dengan checkbox
5. Klik "Select All" → semua files ter-check
6. Klik "➕ Add" → files di-stage
7. Klik "🤖 Generate" → AI generate commit message
8. Review message (bisa edit manual)
9. Klik "✅ Commit & Push"
10. Log menampilkan: "✅ Commit successful! ✅ Push successful!"

#### Example 2: Selective Files

```bash
python ai_commit_gui.py
```

1. Pilih repository `Folder2`
2. Check hanya file yang related (misalnya: 1, 3, 5)
3. Klik "➕ Add"
4. Manual tulis commit message atau generate dengan AI
5. Klik "💾 Commit Only" (tanpa push)

#### Example 3: Switch AI Provider

```bash
python ai_commit_gui.py
```

1. Di Settings, pilih "ChatGPT" radio button
2. Pilih repository
3. Add files
4. Klik "🤖 Generate" → akan use ChatGPT
5. Commit & Push

### CLI Version Examples

#### Contoh 1: Workflow Normal (Auto-detect)

```bash
cd AI-Commit
python ai_commit.py
```

Tool akan scan parent folder, tampilkan semua repositories, dan pilih yang ada perubahan.

### Contoh 2: Specify Folder Langsung

```bash
cd AI-Commit
python ai_commit.py --dir ../Folder1
```

Langsung ke `Folder1` tanpa perlu pilih.

### Contoh 3: Multiple Folders dengan Changes

```bash
cd AI-Commit
python ai_commit.py
```

Output:

```
📁 Git repositories ditemukan:
   1. Folder1 🔴
   2. Folder2 ⚪
   3. Folder3 🔴

❓ Pilih repository (nomor): 1
```

### Contoh 4: Add All & Auto Push dengan ChatGPT

```bash
cd AI-Commit
python ai_commit.py --dir ../Folder2 --all --provider chatgpt
```

### Contoh 5: Custom Message & No Push

```bash
cd AI-Commit
python ai_commit.py --dir ../Folder3 -m "fix: critical bug" --no-push
```

### Contoh 6: Selective File Add

```bash
cd AI-Commit
python ai_commit.py

# Saat ditanya "Add semua file?"
select

# Input nomor file yang ingin di-add
1,3,5
```

## 🛠️ Command Line Options

| Option       | Short | Description                        | Example              |
| ------------ | ----- | ---------------------------------- | -------------------- |
| `--provider` | -     | Pilih AI provider (gemini/chatgpt) | `--provider chatgpt` |
| `--dir`      | `-d`  | Spesifikasi direktori target       | `--dir ../Folder1`   |
| `--all`      | `-a`  | Add semua file tanpa konfirmasi    | `--all`              |
| `--message`  | `-m`  | Custom commit message (skip AI)    | `-m "fix: bug"`      |
| `--no-push`  | -     | Commit tanpa push                  | `--no-push`          |
| `--help`     | `-h`  | Tampilkan help message             | `--help`             |

### Kombinasi Options

```bash
# Full auto dengan Gemini
cd AI-Commit
python ai_commit.py --dir ../Folder1 --all

# Custom message dengan ChatGPT, no push
cd AI-Commit
python ai_commit.py --dir ../Folder2 -m "docs: update" --provider chatgpt --no-push

# Interactive dengan auto-detect
cd AI-Commit
python ai_commit.py --provider gemini
```

## 🎨 Conventional Commits Format

Tool ini menghasilkan commit message mengikuti standar [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>
```

### Types yang Umum

- `feat` - Fitur baru
- `fix` - Bug fix
- `docs` - Perubahan dokumentasi
- `style` - Perubahan formatting (tidak mengubah logika)
- `refactor` - Refactoring code
- `test` - Menambah atau memperbaiki test
- `chore` - Maintenance task
- `perf` - Performance improvement

### Contoh Commit Messages

```
feat(auth): add OAuth2 authentication support

fix(api): resolve database connection timeout issue

docs(readme): add installation guide for Windows

refactor(core): simplify error handling logic

test(utils): add unit tests for date formatter
```

## 🔧 Troubleshooting

### Problem: "GEMINI_API_KEY not found"

**Solusi:**

```bash
# Cek apakah sudah di-set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows CMD

# Set ulang
export GEMINI_API_KEY="your-api-key"  # Linux/Mac
set GEMINI_API_KEY=your-api-key  # Windows
```

### Problem: "Tidak ada git repository ditemukan"

**Solusi:**

1. Pastikan Anda menjalankan tool dari **dalam folder AI-Commit**
2. Pastikan folder sibling (Folder1, Folder2, dll) adalah git repositories
3. Cek dengan:
   ```bash
   cd ../Folder1
   ls -la .git  # Linux/Mac
   dir .git  # Windows
   ```
4. Jika belum git repo, init dulu:
   ```bash
   cd ../Folder1
   git init
   git remote add origin <your-repo-url>
   ```

### Problem: "Tidak ada perubahan yang terdeteksi"

**Solusi:**

- Tool hanya detect **uncommitted changes**
- Cek manual:
  ```bash
  cd ../Folder1
  git status
  ```
- Pastikan ada file yang modified/new/deleted

### Problem: "Push gagal"

**Kemungkinan penyebab:**

**1. Tidak ada remote origin**

```bash
cd ../Folder1
git remote add origin https://github.com/username/repo.git
```

**2. Authentication gagal**

```bash
# Setup SSH key atau credentials
git config credential.helper store
git push origin main  # input credentials sekali
```

**3. Branch belum di-track**

```bash
cd ../Folder1
git push --set-upstream origin main
```

### Problem: "Import Error - google.generativeai not found"

**Solusi:**

```bash
# Pastikan di folder AI-Commit
cd AI-Commit

# Install dependencies
pip install google-generativeai openai

# Atau upgrade pip dulu
pip install --upgrade pip
pip install google-generativeai openai
```

### Problem: "GUI tidak muncul / Error Tkinter"

**Solusi:**

**Linux:**

```bash
# Install tkinter
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install python3-tkinter  # CentOS/RHEL
```

**macOS:**

```bash
# Tkinter sudah included, tapi jika error:
brew install python-tk
```

**Windows:**

- Tkinter sudah included dalam Python installer
- Jika tidak ada, reinstall Python dan check "tcl/tk" option

### Problem: "GUI freeze saat generate message"

**Solusi:**

- Ini normal, AI sedang processing
- GUI menggunakan threading jadi tidak freeze
- Jika benar-benar freeze, coba:
  1. Close dan restart aplikasi
  2. Check API key sudah benar
  3. Check koneksi internet

### Problem: "Tool tidak scan folder parent dengan benar"

**Solusi:**

Pastikan struktur folder Anda seperti ini:

```
workspace/
├── Folder1/ (git repo)
├── Folder2/ (git repo)
├── Folder3/ (git repo)
└── AI-Commit/
    └── ai_commit.py  ← Jalankan dari sini!
```

Jalankan HARUS dari dalam `AI-Commit`:

```bash
# BENAR ✅
cd AI-Commit
python ai_commit.py

# SALAH ❌
cd workspace
python AI-Commit/ai_commit.py
```

### Problem: API Rate Limit

**Solusi:**

- **Gemini**: Gratis dengan limit harian (~60 requests/minute), tunggu atau upgrade
- **OpenAI**: Top-up credit di https://platform.openai.com/account/billing

## ❓ FAQ

### Q: GUI atau CLI, mana yang lebih baik?

**A:** Tergantung kebutuhan:

- **GUI**: Lebih mudah untuk pemula, visual feedback, cocok untuk daily use
- **CLI**: Lebih cepat, bisa di-automate, cocok untuk power users dan remote work

Anda bisa gunakan keduanya! GUI untuk commit biasa, CLI untuk scripting.

### Q: Apakah tool ini gratis?

**A:** Tool-nya 100% gratis dan open source. Namun untuk AI:

- **Gemini API**: Gratis dengan quota harian yang cukup (recommended)
- **OpenAI API**: Berbayar, sekitar $0.002 per commit

### Q: Apakah data saya aman?

**A:**

- ✅ Tool hanya mengirim **git diff** (perubahan code) ke AI
- ✅ Tidak ada data yang disimpan di server
- ✅ API key disimpan lokal di environment variable Anda
- ⚠️ Jangan commit file yang berisi secret/password/token

### Q: Bisakah digunakan untuk private repository?

**A:** Ya, tool ini bekerja dengan semua git repository (public/private). Tool hanya membaca local changes.

### Q: Bisakah menjalankan GUI di background?

**A:** GUI perlu display, tidak bisa background. Untuk background/automation, gunakan CLI version.

### Q: Apakah GUI consume banyak resource?

**A:** Tidak. Tkinter sangat ringan (~10-20MB RAM). Jauh lebih ringan dari Electron-based apps.

### Q: Bisakah custom tampilan GUI?

**A:** Ya, edit `ai_commit_gui.py`. Tkinter support theming dengan `ttk.Style()`. Bisa ganti warna, font, layout, dll.

### Q: Kenapa harus dijalankan dari folder AI-Commit?

**A:** Karena tool di-design untuk scan **parent directory**. Jika dijalankan dari workspace root, tool akan scan workspace root (tidak menemukan apa-apa). Struktur yang benar:

```
workspace/           ← Parent directory yang di-scan
├── Folder1/        ← Akan terdeteksi
├── Folder2/        ← Akan terdeteksi
└── AI-Commit/      ← Jalankan dari sini
    └── ai_commit.py
```

### Q: Bisa tidak pakai AI? Manual saja?

**A:** Ya bisa! Gunakan option `-m`:

```bash
python ai_commit.py --dir ../Folder1 -m "your commit message"
```

### Q: Bagaimana jika saya tidak puas dengan commit message AI?

**A:**

1. Pilih `edit` untuk menulis ulang
2. Pilih `n` untuk batalkan dan coba lagi
3. Switch provider: `--provider chatgpt` atau `--provider gemini`
4. Gunakan `-m` untuk manual message

### Q: Apakah bisa integrasi dengan Git GUI?

**A:** Tool ini CLI-based, tapi bisa dipanggil dari:

- Git GUI yang support custom commands
- Shell scripts
- Git hooks (pre-commit, post-commit)

### Q: Bisakah skip interactive mode untuk automation?

**A:** Ya! Gunakan kombinasi `--all` dan `-m`:

```bash
# Full automation
python ai_commit.py --dir ../Folder1 --all -m "auto commit"
```

Untuk CI/CD atau automation scripts.

### Q: Apakah support monorepo?

**A:** Ya, tool dapat mendeteksi dan bekerja dengan multiple repositories dalam satu workspace.

### Q: Bagaimana jika ada banyak folder dengan perubahan?

**A:** Tool akan menampilkan semua folder dengan indicator 🔴/⚪ dan Anda pilih mana yang ingin di-commit terlebih dahulu. Anda bisa jalankan tool berkali-kali untuk commit folder-folder berbeda.

### Q: Apakah bisa commit multiple folders sekaligus?

**A:** Tidak. Tool di-design untuk commit satu repository per execution. Tapi Anda bisa:

1. Jalankan tool untuk Folder1
2. Jalankan lagi untuk Folder2
3. Dst.

Atau buat bash script:

```bash
#!/bin/bash
cd AI-Commit
python ai_commit.py --dir ../Folder1 --all -m "update"
python ai_commit.py --dir ../Folder2 --all -m "update"
python ai_commit.py --dir ../Folder3 --all -m "update"
```

### Q: Bagaimana cara update tool ini?

**A:**

```bash
cd AI-Commit
# Jika dari git repo
git pull origin main

# Atau download file terbaru dan replace ai_commit.py
```

### Q: Bisakah custom format commit message?

**A:** Ya, edit source code di function `generate_commit_message()` untuk modify prompt yang dikirim ke AI.

## 🚀 Tips & Best Practices

### 1. Workflow Harian

**Dengan GUI:**

```bash
cd AI-Commit
python ai_commit_gui.py

# Atau buat desktop shortcut untuk quick access
```

**Dengan CLI:**

```bash
# Morning routine - cek semua project
cd AI-Commit
python ai_commit.py
```

### 2. Quick Commit untuk Urgent Fix

**GUI:** Buka app → Pilih repo → Select files → Generate → Commit

**CLI:**

```bash
cd AI-Commit
python ai_commit.py --dir ../Folder1 --all -m "hotfix: critical bug"
```

### 3. Desktop Shortcut untuk GUI (Windows)

Buat file `AI-Commit.bat`:

```batch
@echo off
cd C:\path\to\AI-Commit
python ai_commit_gui.py
```

Klik kanan → Send to → Desktop (create shortcut)

### 4. Desktop Shortcut untuk GUI (Linux/Mac)

Buat file `ai-commit.sh`:

```bash
#!/bin/bash
cd ~/workspace/AI-Commit
python3 ai_commit_gui.py
```

```bash
chmod +x ai-commit.sh
# Copy to desktop atau Applications
```

### 5. Custom Alias untuk CLI

```bash
# Cek dulu changes di folder tertentu
cd ../Folder1
git status
git diff

# Baru commit dengan AI
cd ../AI-Commit
python ai_commit.py --dir ../Folder1
```

### 4. Selective Commit untuk Clean History

```bash
cd AI-Commit
python ai_commit.py --dir ../Folder1

# Pilih 'select' saat ditanya
# Input: 1,2,4 (hanya file related)
# Ulangi untuk file lainnya dengan commit message berbeda
```

### 5. Custom Alias untuk Cepat

Tambahkan ke `~/.bashrc` atau `~/.zshrc`:

```bash
# Alias untuk quick commit
alias aicommit='cd ~/workspace/AI-Commit && python ai_commit.py'
alias aicommit-f1='cd ~/workspace/AI-Commit && python ai_commit.py --dir ../Folder1'
alias aicommit-f2='cd ~/workspace/AI-Commit && python ai_commit.py --dir ../Folder2'

# Dengan ChatGPT
alias aicommit-gpt='cd ~/workspace/AI-Commit && python ai_commit.py --provider chatgpt'
```

Lalu gunakan:

```bash
# Dari mana saja
aicommit
aicommit-f1
aicommit-gpt
```

### 6. Pre-commit Check Script

Buat `check_all.sh` di folder AI-Commit:

```bash
#!/bin/bash
cd "$(dirname "$0")"

echo "🔍 Checking all repositories for changes..."
python ai_commit.py
```

Jalankan:

```bash
cd AI-Commit
chmod +x check_all.sh
./check_all.sh
```

## 📊 Use Cases

### Use Case 1: Developer dengan Multiple Projects

**Scenario:** Anda maintain 5 project berbeda dalam satu workspace

**Solution:**

```
workspace/
├── project-frontend/
├── project-backend/
├── project-mobile/
├── project-docs/
├── project-infra/
└── AI-Commit/
```

```bash
cd AI-Commit
python ai_commit.py
# Pilih project yang ada changes
# Commit dengan AI-generated message
```

### Use Case 2: Team Lead Review Changes

**Scenario:** Review dan commit changes dari team

**Solution:**

```bash
# Cek semua project
cd AI-Commit
python ai_commit.py

# Review file-file yang berubah
# Selective add untuk clean commits
# Push ke remote untuk team review
```

### Use Case 3: Freelancer dengan Client Projects

**Scenario:** Manage multiple client projects

**Solution:**

```
workspace/
├── client-a-project/
├── client-b-project/
├── client-c-project/
└── AI-Commit/
```

```bash
# Quick commit untuk client A
cd AI-Commit
python ai_commit.py --dir ../client-a-project --all

# Review commit untuk client B
python ai_commit.py --dir ../client-b-project
```

### Use Case 4: CI/CD Integration

**Scenario:** Automated commits dalam CI/CD pipeline

**Solution:**

```yaml
# .gitlab-ci.yml or .github/workflows/auto-commit.yml
script:
  - cd AI-Commit
  - python ai_commit.py --dir ../project --all -m "chore: automated update" --provider gemini
```

## 🤝 Contributing

Kontribusi selalu welcome!

### Cara Berkontribusi:

1. Fork repository
2. Buat feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit changes
   ```bash
   git commit -m 'feat: add amazing feature'
   ```
4. Push ke branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Buat Pull Request

### Contributing Ideas:

- [x] CLI Version
- [x] GUI Version with Tkinter
- [ ] PyQt5/PyQt6 version untuk advanced GUI
- [x] Dark mode theme untuk GUI
- [ ] System tray integration
- [ ] Drag & drop file support di GUI
- [ ] Git graph visualization
- [ ] Multi-repo batch commit
- [ ] Commit templates library
- [ ] Integration dengan GitHub/GitLab API
- [ ] Webhook support
- [ ] Slack/Discord notifications
- [ ] Statistics & analytics dashboard
- [ ] Plugin system
- [ ] Mobile app (React Native/Flutter)
- [ ] Web version
- [ ] Browser extension

## 🙏 Credits

- **AI Providers:**
  - [Google Gemini](https://ai.google.dev/) - Free AI with generous quota
  - [OpenAI](https://openai.com/) - Powerful GPT models
- **Standards:**
  - [Conventional Commits](https://www.conventionalcommits.org/) - Commit message format
- **Inspired by:**
  - aicommits by Nutlope
  - GitHub Copilot
  - GitMoji

## 📞 Support & Contact

### Menemukan Bug?

- 🐛 Buat issue di repository dengan label `bug`
- Sertakan error message dan langkah reproduksi

### Punya Saran?

- 💡 Buat issue dengan label `enhancement`
- Jelaskan use case dan expected behavior

### Butuh Bantuan?

- 📖 Baca FAQ dan Troubleshooting di atas
- 💬 Buat issue dengan label `question`
- 📧 Email: dev@ryucode.com

### Follow Updates

- ⭐ Star repository untuk updates
- 👀 Watch untuk notifications
- 🔔 Follow untuk new releases

---

**Made with ❤️ for developers who value clean commit history**

⭐ **Star repository ini jika bermanfaat!**

🚀 **Happy Committing with AI!**

---

## 📸 Screenshots

### GUI Version

**Main Window:**

- Clean and modern interface
- Auto-scan on startup
- Visual file selection
- Real-time log output
- AI-powered commit messages

**Key Features Visible:**

- 🔴 Red indicator for repos with changes
- ⚪ White indicator for clean repos
- 🆕 New file icon
- ✏️ Modified file icon
- 🗑️ Deleted file icon

### CLI Version
![CLI Version](https://github.com/user-attachments/assets/60e0027d-c407-465d-90e8-8e130d2241ea)

**Terminal Output:**

- Color-coded indicators
- Interactive prompts
- Progress feedback
- Clear status messages

---

## 🎯 Quick Links

- 📖 [Documentation](#-daftar-isi)
- 🐛 [Report Bug](https://github.com/RyuCode-Digital-Solution/AI-Commit/issues)
- 💡 [Request Feature](https://github.com/RyuCode-Digital-Solution/AI-Commit/issues)
- 🤝 [Contribute](https://github.com/RyuCode-Digital-Solution/AI-Commit/pulls)
- ⭐ [Star on GitHub](https://github.com/RyuCode-Digital-Solution/AI-Commit)

## 🌟 Show Your Support

Jika tool ini membantu Anda:

- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code
- 📢 Share dengan teman

## 📱 Connect

- 🌐 Website: [ryucode.com](https://ryucode.com)
- 📧 Email: dev@ryucode.com

**Thank you for using AI Commit! 🙏**
