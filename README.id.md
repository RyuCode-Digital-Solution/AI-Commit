# 🤖 AI Commit

[![Language](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Bahasa](https://img.shields.io/badge/Bahasa-Indonesia-red)](README.id.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)

> Alat commit otomatis berbasis AI yang menghasilkan commit message berkualitas dan mendukung multi-project workspace

AI Commit adalah utilitas Python yang memanfaatkan kekuatan AI (Gemini & ChatGPT) untuk menganalisis perubahan kode Anda dan menghasilkan commit message yang mengikuti standar conventional commits secara otomatis.

**Tersedia dalam 2 versi:**

- 🖥️ **CLI Version** - Command line interface untuk terminal lovers
- 🎨 **GUI Version** - Graphical interface dengan Tkinter (tanpa dependency tambahan!)

---

## ✨ Fitur Utama

- 🎯 **Generate Commit Message Otomatis** - AI menganalisis diff dan membuat commit message yang deskriptif
- 🤖 **Multi AI Provider** - Support Gemini dan ChatGPT
- 📁 **Multi-Project Support** - Kelola multiple git repositories dalam satu workspace
- 🔍 **Auto-Detect Changes** - Scan dan tampilkan folder mana yang ada perubahan
- ➕ **Smart Git Add** - Auto-detect perubahan dengan opsi selective add
- 🚀 **Auto Push** - Otomatis push ke origin branch saat ini
- 📝 **Interactive Mode** - Konfirmasi dan edit sebelum commit
- 🎨 **Conventional Commits** - Mengikuti format conventional commits standard
- 🖼️ **GUI Interface** - User-friendly graphical interface
- 🌙 **Dark Mode** - Toggle antara light dan dark theme untuk kenyamanan mata

---

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
└── AI-Commit/            # Tool folder (jalankan script dari sini)
    ├── ai_commit.py
    └── ai_commit_gui.py
```

**Cara Kerja:**

- Tool dijalankan dari dalam folder `AI-Commit`
- Otomatis scan **parent directory** untuk menemukan semua git repositories (Folder1, Folder2, Folder3)
- Deteksi folder mana yang punya perubahan (ditandai dengan 🔴)
- Anda pilih folder yang ingin di-commit dan push

---

## 🚀 Instalasi

### Prerequisites

- Python 3.9 atau lebih baru
- Git terinstall
- API Key dari Gemini atau OpenAI

### Install Dependencies

```bash
# Klon repositori
git clone https://github.com/RyuCode-Digital-Solution/AI-Commit

# Masuk ke folder AI-Commit
cd AI-Commit

# Install required packages
pip install -r requirements.txt
```

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

---

## 🎨 GUI Version (Recommended)

![GUI Version](https://github.com/user-attachments/assets/2387bd34-3e15-4ce8-9c93-2ea69e3281b7)

### Fitur

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

### Cara Menggunakan

```bash
# Masuk ke folder AI-Commit
cd AI-Commit

# Jalankan GUI version
python ai_commit_gui.py
```

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

**Dark Theme:**

- Background gelap (#1e1e1e) yang nyaman untuk mata
- Text terang (#ffffff) untuk kontras optimal
- Frame abu-abu (#2d2d2d) untuk pemisahan yang jelas
- Accent biru gelap (#0e639c) untuk highlight
- Cocok untuk bekerja malam hari atau ruangan gelap

**Light Theme:**

- Background terang (#f0f0f0) untuk ruangan terang
- Text hitam (#000000) untuk ketajaman maksimal
- Frame putih (#ffffff) untuk tampilan bersih
- Accent biru cerah (#0078d4) untuk interaksi
- Cocok untuk bekerja siang hari atau ruangan terang

---

## 🖥️ CLI Version

![CLI Version](https://github.com/user-attachments/assets/804fe01e-1a86-450a-8731-64797c3929db)

### Quick Start

```bash
# Masuk ke folder AI-Commit
cd AI-Commit

# Jalankan tool
python ai_commit.py

# Tool akan scan parent folder dan tampilkan repositories
# Pilih repository yang ingin di-commit (yang ada 🔴)
# Pilih file yang ingin di-add
# Review commit message dari AI
# Confirm dan otomatis push!
```

### Command Line Options

| Option       | Short | Deskripsi                          | Contoh               |
| ------------ | ----- | ---------------------------------- | -------------------- |
| `--provider` | -     | Pilih AI provider (gemini/chatgpt) | `--provider chatgpt` |
| `--dir`      | `-d`  | Spesifikasi direktori target       | `--dir ../Folder1`   |
| `--all`      | `-a`  | Add semua file tanpa konfirmasi    | `--all`              |
| `--message`  | `-m`  | Custom commit message (skip AI)    | `-m "fix: bug"`      |
| `--no-push`  | -     | Commit tanpa push                  | `--no-push`          |
| `--help`     | `-h`  | Tampilkan help message             | `--help`             |

### Contoh CLI

```bash
# Auto-detect dan interactive
python ai_commit.py

# Folder spesifik dengan ChatGPT
python ai_commit.py --dir ../Folder1 --provider chatgpt

# Quick commit dengan custom message
python ai_commit.py --dir ../Folder2 -m "docs: update README" --no-push

# Full automation
python ai_commit.py --dir ../Folder3 --all
```

---

## 🎯 Perbandingan GUI vs CLI

| Fitur             | GUI        | CLI        |
| ----------------- | ---------- | ---------- |
| Kemudahan         | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     |
| Kecepatan         | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ |
| Visual Feedback   | ⭐⭐⭐⭐⭐ | ⭐⭐       |
| Automation        | ⭐⭐       | ⭐⭐⭐⭐⭐ |
| Remote Access     | ❌         | ✅         |
| Beginner Friendly | ✅         | ⚠️         |
| Dark Mode         | ✅         | ❌         |

**Rekomendasi:**

- 🎨 **Gunakan GUI** jika: pemula, prefer visual, bekerja local
- 🖥️ **Gunakan CLI** jika: power user, automation, remote work

---

## 🔧 Troubleshooting

### Problem: "GEMINI_API_KEY not found"

**Solusi:**

```bash
# Cek apakah sudah di-set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows CMD

# Jika kosong, set ulang
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

---

## ❓ FAQ

### Q: Bagaimana cara mengaktifkan Dark Mode di GUI?

**A:**

1. Buka aplikasi GUI (`python ai_commit_gui.py`)
2. Lihat pojok kanan atas, ada checkbox "🌙 Dark Mode"
3. Klik checkbox untuk toggle antara light dan dark theme
4. Theme akan langsung berubah untuk semua komponen UI

Dark Mode cocok untuk:

- Bekerja malam hari
- Mengurangi eye strain
- Ruangan dengan pencahayaan rendah
- Preferensi visual personal

### Q: Apakah Dark Mode disimpan setelah aplikasi ditutup?

**A:** Tidak, theme akan reset ke Light Mode setiap kali aplikasi dibuka. Ini adalah default behavior untuk sementara. Jika Anda ingin Dark Mode menjadi default, edit file `ai_commit_gui.py`:

```python
# Cari baris ini (sekitar line 30):
self.dark_mode = tk.BooleanVar(value=False)

# Ganti menjadi:
self.dark_mode = tk.BooleanVar(value=True)  # Default Dark Mode
```

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

### Q: GUI atau CLI, mana yang lebih baik?

**A:** Tergantung kebutuhan:

- **GUI**: Lebih mudah untuk pemula, visual feedback, cocok untuk daily use
- **CLI**: Lebih cepat, bisa di-automate, cocok untuk power users dan remote work

Anda bisa gunakan keduanya! GUI untuk commit biasa, CLI untuk scripting.

---

## 🤝 Contributing

Kontribusi selalu welcome!

### Cara Berkontribusi:

1. Fork repository
2. Buat feature branch
   ```bash
   git checkout -b feature/FiturKeren
   ```
3. Commit changes
   ```bash
   git commit -m 'feat: tambah fitur keren'
   ```
4. Push ke branch
   ```bash
   git push origin feature/FiturKeren
   ```
5. Buat Pull Request

### Ideas untuk Contribution:

- [x] CLI Version
- [x] GUI Version dengan Tkinter
- [x] Dark Mode
- [x] Smart File Matching
- [ ] PyQt5/PyQt6 version untuk advanced GUI
- [ ] System tray integration
- [ ] Drag & drop file support di GUI
- [ ] Git graph visualization
- [ ] Multi-repo batch commit
- [ ] Config file support
- [ ] Plugin system

---

## 🙏 Credits

- **AI Providers:**
  - [Google Gemini](https://ai.google.dev/) - Free AI dengan quota yang besar
  - [OpenAI](https://openai.com/) - GPT models yang powerful
- **Standards:**
  - [Conventional Commits](https://www.conventionalcommits.org/) - Format commit message
- **Terinspirasi dari:**
  - aicommits oleh Nutlope
  - GitHub Copilot

---

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

---

**Dibuat dengan ❤️ untuk developer yang menghargai commit history yang bersih**

⭐ **Star repository ini jika bermanfaat!**

🚀 **Happy Committing with AI!**

---

**[🇺🇸 Read in English](README.md)**
