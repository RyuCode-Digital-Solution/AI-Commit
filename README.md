# 🤖 AI Commit

> Alat commit otomatis berbasis AI yang menghasilkan commit message berkualitas dan mendukung multi-project workspace

AI Commit adalah utilitas Python yang memanfaatkan kekuatan AI (Gemini & ChatGPT) untuk menganalisis perubahan kode Anda dan menghasilkan commit message yang mengikuti standar conventional commits secara otomatis.

## ✨ Fitur Utama

- 🎯 **Generate Commit Message Otomatis** - AI menganalisis diff dan membuat commit message yang deskriptif
- 🤖 **Multi AI Provider** - Support Gemini dan ChatGPT
- 📁 **Multi-Project Support** - Kelola multiple git repositories dalam satu workspace
- ➕ **Smart Git Add** - Auto-detect perubahan dengan opsi selective add
- 🚀 **Auto Push** - Otomatis push ke origin branch saat ini
- 📝 **Interactive Mode** - Konfirmasi dan edit sebelum commit
- 🎨 **Conventional Commits** - Mengikuti format conventional commits standard
- 🔍 **File Selection** - Pilih file spesifik yang ingin di-commit

## 📋 Daftar Isi

- [Instalasi](#-instalasi)
- [Konfigurasi](#-konfigurasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Fitur Detail](#-fitur-detail)
- [Contoh Penggunaan](#-contoh-penggunaan)
- [Command Line Options](#-command-line-options)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)

## 🚀 Instalasi

### Prerequisites

- Python 3.8 atau lebih baru
- Git terinstall
- API Key dari Gemini atau OpenAI

### Install Dependencies

```bash
# Clone atau download repository ini
git clone https://github.com/RyuCode-Digital-Solution/AI-Commit
cd AI-Commit

# Install required packages
pip install -r requirements.txt
```

## 🔑 Konfigurasi

### 1. Dapatkan API Key

#### Gemini API Key (Gratis)
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

#### Linux/Mac (Temporary - untuk session saat ini)
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
export OPENAI_API_KEY="your-openai-api-key-here"
```

#### Linux/Mac (Permanent - tambahkan ke ~/.bashrc atau ~/.zshrc)
```bash
echo 'export GEMINI_API_KEY="your-gemini-api-key-here"' >> ~/.bashrc
echo 'export OPENAI_API_KEY="your-openai-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows (Command Prompt)
```cmd
set GEMINI_API_KEY=your-gemini-api-key-here
set OPENAI_API_KEY=your-openai-api-key-here
```

#### Windows (PowerShell)
```powershell
$env:GEMINI_API_KEY="your-gemini-api-key-here"
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

#### Windows (Permanent - System Environment Variables)
1. Buka "System Properties" → "Environment Variables"
2. Klik "New" di User Variables
3. Variable name: `GEMINI_API_KEY`
4. Variable value: your-api-key
5. Ulangi untuk `OPENAI_API_KEY`

### 3. Verifikasi Instalasi

```bash
python ai_commit.py --help
```

Jika berhasil, Anda akan melihat help message dengan semua opsi yang tersedia.

## 📖 Cara Penggunaan

### Penggunaan Dasar

```bash
# 1. Jalankan tool (akan auto-detect repositories)
python ai_commit.py

# 2. Pilih repository dari list
# 3. Pilih file yang ingin di-add
# 4. Review commit message yang di-generate AI
# 5. Confirm dan push
```

### Struktur Folder yang Didukung

```
workspace/
├── folder_projek_lain/    # Git repo 1
│   ├── .git/
│   └── ...
├── ai_commit/             # Git repo 2
│   ├── .git/
│   └── ...
└── ai_commit.py           # Script tool
```

Tool akan otomatis mendeteksi semua folder yang merupakan git repository.

## 🎯 Fitur Detail

### 1. Auto-Detect Git Repositories

Tool akan scan folder saat ini dan menampilkan semua git repositories yang ditemukan:

```
📁 Git repositories ditemukan:
   1. folder_projek_lain
   2. ai_commit
   3. website_project

❓ Pilih repository (nomor): 2
```

### 2. Smart Git Add dengan Preview

Setelah memilih repository, tool menampilkan semua file yang berubah:

```
📝 Perubahan terdeteksi (3 file):
   1. ✏️ src/main.py
   2. 🆕 src/utils.py
   3. 🗑️ old_file.py

❓ Add semua file? (y/n/select):
```

**Opsi:**
- `y` - Add semua file
- `n` - Batalkan
- `select` - Pilih file tertentu (contoh: 1,3)

### 3. AI-Generated Commit Message

AI akan menganalisis perubahan dan generate commit message:

```
💡 AI menyarankan commit message:
   feat(core): add utility functions and refactor main module
   
   - Added new utility functions in utils.py
   - Refactored main.py for better code organization
   - Removed deprecated old_file.py

❓ Gunakan message ini? (y/n/edit):
```

**Opsi:**
- `y` - Gunakan message tersebut
- `n` - Batalkan commit
- `edit` - Edit manual commit message

### 4. Auto Push ke Current Branch

Setelah commit berhasil, otomatis push ke origin dengan branch saat ini:

```
✅ Commit berhasil!

🚀 Pushing ke origin/main...
✅ Push berhasil!
```

## 💡 Contoh Penggunaan

### Contoh 1: Workflow Normal

```bash
# Jalankan dengan Gemini (default)
python ai_commit.py
```

**Output:**
```
🤖 AI Commit (Provider: GEMINI)
==================================================

📁 Git repositories ditemukan:
   1. folder_projek_lain
   2. ai_commit

❓ Pilih repository (nomor): 2
✅ Dipilih: ai_commit

📂 Working directory: /home/user/workspace/ai_commit

📝 Perubahan terdeteksi (2 file):
   1. ✏️ ai_commit.py
   2. 🆕 README.md

❓ Add semua file? (y/n/select): y
✅ File berhasil di-add!

🔍 Menganalisis perubahan...

💡 AI menyarankan commit message:
   docs: add comprehensive README with installation guide

❓ Gunakan message ini? (y/n/edit): y

📝 Committing dengan message:
   docs: add comprehensive README with installation guide

✅ Commit berhasil!

🚀 Pushing ke origin/main...
✅ Push berhasil!
```

### Contoh 2: Spesifik Direktori dengan ChatGPT

```bash
python ai_commit.py --dir ai_commit --provider chatgpt
```

### Contoh 3: Add Semua File Tanpa Konfirmasi

```bash
python ai_commit.py --dir folder_projek_lain --all
```

### Contoh 4: Custom Message & No Push

```bash
python ai_commit.py --dir ai_commit -m "fix: critical bug fix" --no-push
```

### Contoh 5: Selective File Add

```bash
python ai_commit.py --dir ai_commit
# Pilih 'select' saat ditanya
# Input: 1,3,5 (untuk memilih file 1, 3, dan 5)
```

## 🛠️ Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--provider` | - | Pilih AI provider (gemini/chatgpt) | `--provider chatgpt` |
| `--dir` | `-d` | Spesifikasi direktori target | `--dir ai_commit` |
| `--all` | `-a` | Add semua file tanpa konfirmasi | `--all` |
| `--message` | `-m` | Custom commit message (skip AI) | `-m "fix: bug"` |
| `--no-push` | - | Commit tanpa push | `--no-push` |
| `--help` | `-h` | Tampilkan help message | `--help` |

### Kombinasi Options

```bash
# Full auto mode
python ai_commit.py --dir ai_commit --all --provider gemini

# Quick commit tanpa AI
python ai_commit.py --dir ai_commit --all -m "chore: update deps" --no-push

# Selective dengan ChatGPT
python ai_commit.py --provider chatgpt
```

## 🎨 Conventional Commits Format

Tool ini menghasilkan commit message mengikuti standar [Conventional Commits](https://www.conventionalcommits.org/):

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
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
- `ci` - CI/CD changes
- `build` - Build system changes

### Contoh Commit Messages

```
feat(auth): add OAuth2 authentication support

fix(api): resolve null pointer exception in user service

docs(readme): update installation instructions

refactor(core): simplify database connection logic

test(utils): add unit tests for helper functions

chore(deps): update dependencies to latest versions
```

## 🔧 Troubleshooting

### Problem: "GEMINI_API_KEY not found"

**Solusi:**
```bash
# Pastikan environment variable sudah di-set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows CMD

# Jika kosong, set ulang
export GEMINI_API_KEY="your-api-key"
```

### Problem: "Tidak ada git repository ditemukan"

**Solusi:**
- Pastikan folder memiliki `.git` directory
- Jalankan `git init` di folder project jika belum
- Gunakan `--dir` untuk specify direktori:
  ```bash
  python ai_commit.py --dir path/to/your/repo
  ```

### Problem: "Tidak ada perubahan yang terdeteksi"

**Solusi:**
- Pastikan ada file yang dimodifikasi
- Cek dengan `git status`
- Tool hanya detect file yang belum di-stage

### Problem: "Push gagal"

**Kemungkinan penyebab:**
1. Tidak ada remote origin
   ```bash
   git remote add origin <url>
   ```

2. Authentication gagal
   ```bash
   # Setup SSH key atau credentials
   git config credential.helper store
   ```

3. Branch belum di-track
   ```bash
   git push --set-upstream origin <branch-name>
   ```

### Problem: Import Error

**Solusi:**
```bash
# Install dependencies yang kurang
pip install google-generativeai openai

# Atau upgrade pip terlebih dahulu
pip install --upgrade pip
pip install google-generativeai openai
```

### Problem: API Rate Limit

**Solusi:**
- Gemini: Gratis dengan limit harian, tunggu 24 jam atau upgrade
- OpenAI: Top-up credit di platform

## ❓ FAQ

### Q: Apakah tool ini gratis?

**A:** Tool-nya gratis, namun:
- **Gemini API**: Gratis dengan quota harian yang cukup untuk penggunaan normal
- **OpenAI API**: Berbayar, perlu top-up credit (sekitar $0.002 per commit)

### Q: Apakah data saya aman?

**A:** 
- Tool hanya mengirim git diff (perubahan code) ke AI
- Tidak ada data yang disimpan di server
- API key disimpan lokal di environment variable Anda
- Sebaiknya tidak commit file yang berisi secret/password

### Q: Bisakah digunakan untuk private repository?

**A:** Ya, tool ini bekerja dengan semua git repository (public/private).

### Q: Apakah bisa custom format commit message?

**A:** Ya, ada beberapa cara:
1. Gunakan `-m` untuk custom message manual
2. Pilih `edit` saat konfirmasi untuk edit AI-generated message
3. Modify prompt di source code untuk custom format

### Q: Bagaimana jika saya tidak puas dengan commit message yang di-generate?

**A:**
1. Pilih `edit` untuk menulis ulang
2. Pilih `n` untuk batalkan dan coba lagi
3. Gunakan `--provider chatgpt` jika Gemini kurang sesuai (atau sebaliknya)

### Q: Bisakah digunakan di Windows?

**A:** Ya, fully compatible dengan Windows, Linux, dan macOS.

### Q: Apakah bisa integrasi dengan Git GUI?

**A:** Tool ini CLI-based, namun bisa dipanggil dari Git GUI yang support custom commands.

### Q: Bagaimana cara update tool ini?

**A:**
```bash
git pull origin main  # Jika dari git repo
# Atau download file terbaru dan replace
```

### Q: Bisa tidak skip interactive mode?

**A:** Ya, gunakan kombinasi `--all` dan `-m`:
```bash
python ai_commit.py --dir ai_commit --all -m "your message"
```

### Q: Apakah support monorepo?

**A:** Ya, tool dapat mendeteksi dan bekerja dengan multiple repositories dalam satu workspace.

## 🤝 Contributing

Kontribusi selalu welcome! Silakan:
1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

MIT License - Silakan digunakan untuk keperluan pribadi maupun komersial.

## 🙏 Credits

- Powered by [Google Gemini](https://ai.google.dev/) and [OpenAI](https://openai.com/)
- Conventional Commits: [conventionalcommits.org](https://www.conventionalcommits.org/)

## 📞 Support

Jika menemukan bug atau punya saran:
- Buat issue di repository
- Email: dev@ryucode.com
- Website: ryucode.com

---

**Made with ❤️ for developers who hate writing commit messages**

⭐ Star repository ini jika bermanfaat!
