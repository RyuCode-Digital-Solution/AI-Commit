# 🤖 AI Commit

[![Language](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Bahasa](https://img.shields.io/badge/Bahasa-Indonesia-red)](README.id.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)

> Alat commit otomatis berbasis AI yang menghasilkan commit message berkualitas dan mendukung multi-project workspace

AI Commit adalah utilitas Python yang memanfaatkan kekuatan AI (Gemini & ChatGPT) untuk menganalisis perubahan kode Anda dan menghasilkan commit message yang mengikuti standar conventional commits secara otomatis.

![Demo](https://github.com/user-attachments/assets/48a59cd7-e394-4b28-b708-4b84ede4d795)

---

## ✨ Fitur Utama

- **🔍 Auto-Scan** - Otomatis scan repositories saat aplikasi dibuka
- **🎯 Visual Selection** - Pilih repository dan files dengan mouse
- **🤖 One-Click AI** - Generate commit message dengan satu klik
- **📊 Real-time Log** - Lihat semua aktivitas di panel log
- **⚙️ Easy Settings** - Toggle AI provider dan auto-push
- **✅ Batch Selection** - Select all atau clear selection dengan mudah
- **🎨 Modern UI** - Clean and intuitive interface
- **🌙 Dark Mode** - Toggle antara light dan dark theme
- **📝 Smart File Matching** - Otomatis mencari file yang mirip jika terjadi error
- **⚙️ Settings Manager** - Load/save settings dari file JSON dengan error handling
- **🔧 Settings Dialog** - Tab-based interface yang terorganisir
- **🤖 AI Configuration** - Pilih model custom dan kelola API keys
- **🐙 GitHub Integration** - Username dan token untuk private repositories
- **📂 Repository Management** - Custom parent folder dan recent repositories
- **🔄 Auto Refresh** - Manual refresh untuk file changes
- **🎯 Better Organization** - Semua konfigurasi dalam satu tempat

### Alur Kerja

1. **Buka aplikasi** → Auto-scan akan berjalan
2. **Pilih repository** dari dropdown (yang 🔴 ada perubahan)
3. **Konfigurasi Settings (jika pertama kali)** - Klik tombol ⚙️ Settings
4. **Pilih files** yang ingin di-commit (atau Select All)
5. **Klik "➕ Add to Stage"** untuk stage files
6. **Klik "🤖 Generate with AI"** untuk AI commit message (atau tulis manual)
7. **Review message** di text area
8. **Klik "✅ Commit & Push"** untuk commit dan push

### Konfigurasi Pengaturan

**Akses Settings:** Klik tombol **⚙️ Settings** di main window

##### AI Settings Tab

- **AI Provider:** Pilih antara Gemini atau ChatGPT
- **API Key: Input** API key untuk provider yang dipilih
- Model Selection: Pilih model specific (gemini-1.5-pro, gpt-4, dll)

##### GitHub Tab

- **GitHub Username:** Username GitHub Anda
- **GitHub Token:** Personal access token untuk private repos
- **Auto-configure Git:** Otomatis set git config dengan credentials

##### Repository Tab

- **Parent Folder:** Custom folder untuk scan repositories
- **Recent Repositories:** History repo yang pernah dibuka
- **Browse Repository:** Pilih folder repo secara manual
- **Refresh Button:** Manual refresh untuk detect changes

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

## 🚀 Instalasi

### Prerequisites

- Python 3.9 atau lebih baru
- Git terinstall
- API Key dari Gemini atau OpenAI

### Windows

- Unduh [AI-Commit.exe](https://github.com/RyuCode-Digital-Solution/AI-Commit/blob/v1/dist/AI-Commit.exe) - Versi 1 (1.0.0) stabil.

---

## 🔑 Konfigurasi

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

#### GitHub Token

1. Kunjungi [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Klik "Generate new token"
3. Pilih scope "repo" dan "workflow"
4. Copy token yang dihasilkan

---

## ❓ FAQ

### Q: Bagaimana cara mengaktifkan Dark Mode di GUI?

**A:**

1. Buka aplikasi
2. Lihat pojok kanan atas, ada checkbox "🌙 Dark Mode"
3. Klik checkbox untuk toggle antara light dan dark theme
4. Theme akan langsung berubah untuk semua komponen UI

Dark Mode cocok untuk:

- Bekerja malam hari
- Mengurangi eye strain
- Ruangan dengan pencahayaan rendah
- Preferensi visual personal

### Q: Bagaimana cara mengkonfigurasi GitHub token?

**A:**

1. Klik tombol **⚙️ Settings**
2. Pilih GitHub tab
3. Input username dan token GitHub Anda
4. Centang "Auto-configure Git" untuk set credentials otomatis
5. Klik Save

### Q: Bagaimana cara menambah custom parent folder?

**A:**

1. Buka **Settings → Repository tab**
2. Klik "Browse" di sebelah "Parent Folder"
3. Pilih folder yang berisi git repositories Anda
4. Klik Save
5. Repository dropdown akan otomatis ter-update

### Q: Apakah tool ini gratis?

**A:** Tool-nya 100% gratis dan open source. Namun untuk AI:

- **Gemini API**: Gratis dengan quota harian yang cukup (recommended)
- **OpenAI API**: Berbayar, sekitar $0.002 per commit

### Q: Apakah data saya aman?

**A:**

- ✅ Tool hanya mengirim **git diff** (perubahan code) ke AI
- ✅ Tidak ada data yang disimpan di server
- ✅ API key dan settings disimpan lokal
- ⚠️ Jangan commit file yang berisi secret/password/token

## 🤝 Berkontribusi

Kontribusi selalu welcome!

### Cara Berkontribusi:

1. Fork repository
2. Buat feature branch
   ```bash
   git checkout -b feature/FiturKeren
   ```
3. Commit perubahan
   ```bash
   git commit -m 'feat: tambah fitur keren'
   ```
4. Push ke branch
   ```bash
   git push origin feature/FiturKeren
   ```
5. Buat Pull Request

---

## 🙏 Kredit

- **AI Providers:**
  - [Google Gemini](https://ai.google.dev/) - Free AI dengan quota yang besar
  - [OpenAI](https://openai.com/) - GPT models yang powerful
- **Standards:**
  - [Conventional Commits](https://www.conventionalcommits.org/) - Format commit message
- **Terinspirasi dari:**
  - aicommits oleh Nutlope
  - GitHub Copilot

---

## 📞 Dukungan & Kontak

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

🚀 **Selamat Berkomitmen dengan AI!**

---

**[🇺🇸 Read in English](README.md)**
