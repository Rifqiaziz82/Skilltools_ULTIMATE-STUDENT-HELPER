Perfect! Sekarang saya akan buat dokumentasi lengkap dan file requirements untuk dependencies:
Action: file_editor create /app/backend/STUDENT_HELPER_GUIDE.md --file-text "# 🎓 ULTIMATE STUDENT HELPER SKILL - Panduan Lengkap

OpenClaw Python Skill yang powerful untuk membantu pelajar/mahasiswa dengan berbagai kebutuhan studi!

## 🚀 Fitur Utama

### 1. 📸 OCR - Scan Catatan Jadi Text
**Super Berguna!** Foto catatan tulis tangan atau halaman buku langsung jadi text yang bisa dicopy!

```python
from student_helper_skill import StudentHelperSkill

skill = StudentHelperSkill()

# Scan foto catatan
result = skill.ocr_image_to_text(\"foto_catatan.jpg\")
print(result['text'])  # Text dari catatan!
print(f\"Confidence: {result['confidence']}%\")
print(f\"Total kata: {result['word_count']}\")
```

**Kasus Penggunaan:**
- Foto catatan teman → jadi text
- Scan halaman buku → copy text-nya
- Foto soal ujian → jadi text editable

---

### 2. 🤖 AI Summarizer - Ringkas Dokumen Panjang
**Hemat Waktu!** Materi 20 halaman → jadi ringkasan 1 halaman!

```python
import asyncio

# Ringkas text panjang
long_text = \"\"\"... materi panjang dari buku ...\"\"\"
result = await skill.summarize_text(long_text, api_key=\"your-emergent-key\")
print(result['summary'])
print(f\"Kompresi: {result['compression_ratio']}x lebih pendek\")

# Atau langsung dari PDF
result = skill.summarize_pdf(\"materi_kuliah.pdf\", api_key=\"your-key\")
print(result['summary'])
```

**Kasus Penggunaan:**
- Ringkas jurnal penelitian
- Rangkum ebook panjang
- Summary artikel untuk tugas

---

### 3. 🎙️ Audio to Text - Transkrip Rekaman
**Gak Perlu Nulis Lagi!** Rekaman kuliah langsung jadi catatan tertulis!

```python
import asyncio

# Transkrip rekaman kuliah
result = await skill.transcribe_audio(
    \"rekaman_kuliah.mp3\",
    api_key=\"your-emergent-key\",
    language='id'  # 'id' untuk Indonesia, 'en' untuk English
)
print(result['transcript'])
print(f\"Durasi: {result['duration']} detik\")
print(f\"Total kata: {result['word_count']}\")
```

**Kasus Penggunaan:**
- Rekaman kuliah → catatan
- Rekaman presentasi → transkrip
- Interview → text tertulis

---

### 4. 📄 PDF Operations - Gabung & Pisah PDF
**Compile Tugas!** Gabung banyak PDF jadi satu, atau pisah PDF jadi per halaman.

```python
# Gabung beberapa PDF
result = skill.merge_pdfs(
    [\"tugas1.pdf\", \"tugas2.pdf\", \"tugas3.pdf\"],
    \"tugas_lengkap.pdf\"
)
print(f\"Berhasil gabung {result['total_files_merged']} file!\")

# Pisah PDF per halaman
result = skill.split_pdf(
    \"buku.pdf\",
    \"output_folder/\",
    pages_per_file=1  # 1 halaman per file
)
print(f\"Berhasil split jadi {result['total_files_created']} file\")

# Extract text dari PDF
result = skill.extract_text_from_pdf(\"dokumen.pdf\")
print(result['text'])
print(f\"Total {result['total_pages']} halaman\")
```

**Kasus Penggunaan:**
- Gabung banyak file tugas jadi satu
- Split buku PDF per chapter
- Extract text dari PDF

---

### 5. 📚 Citation Generator - Daftar Pustaka Otomatis
**Bikin Sitasi Mudah!** Generate citation APA, MLA, atau Chicago otomatis.

```python
# Generate citation APA style
result = skill.generate_citation(
    title=\"Machine Learning for Beginners\",
    authors=[\"John Doe\", \"Jane Smith\"],
    year=2024,
    publisher=\"Tech Press\",
    url=\"https://example.com/book\",
    citation_style='apa'  # 'apa', 'mla', atau 'chicago'
)
print(result['citation'])
# Output: Doe, J. & Smith, J. (2024). Machine Learning for Beginners. Tech Press. https://example.com/book
```

**Kasus Penggunaan:**
- Buat daftar pustaka untuk skripsi
- Generate citation untuk tugas
- Format referensi otomatis

---

### 6. 🖼️ Image Processing - Resize, Compress, Convert
**Optimize Gambar!** Ubah ukuran, compress, atau convert format gambar.

```python
# Resize gambar
result = skill.resize_image(
    \"gambar_besar.jpg\",
    \"gambar_kecil.jpg\",
    width=800,  # pixels
    maintain_aspect=True
)
print(f\"Dari {result['original_size']} → {result['new_size']}\")

# Compress gambar (kecilkan file size)
result = skill.compress_image(
    \"gambar.jpg\",
    \"gambar_compressed.jpg\",
    quality=85  # 0-100, makin tinggi makin bagus
)
print(f\"Hemat {result['compression_ratio']} space!\")

# Convert format
result = skill.convert_image_format(
    \"gambar.png\",
    \"gambar.webp\",
    target_format='WebP'
)
```

**Kasus Penggunaan:**
- Compress gambar untuk upload
- Resize gambar untuk presentasi
- Convert format gambar

---

### 7. 📊 Excel/CSV Processing
**Olah Data Mudah!** Convert Excel ke JSON atau CSV ke Excel.

```python
# Excel → JSON (untuk API/web)
result = skill.excel_to_json(\"data.xlsx\", sheet_name=\"Sheet1\")
print(result['data'])  # JSON data
print(f\"Total {result['total_rows']} baris\")

# CSV → Excel
result = skill.csv_to_excel(\"data.csv\", \"output.xlsx\")
print(f\"Berhasil convert {result['total_rows']} baris\")
```

**Kasus Penggunaan:**
- Convert data Excel untuk web app
- Ubah CSV jadi Excel yang lebih rapi
- Extract data dari spreadsheet

---

### 8. 📖 Study Helpers - Keywords & Flashcards
**Belajar Lebih Efektif!** Extract keywords penting atau buat flashcards otomatis.

```python
# Extract keywords dari materi
result = skill.extract_keywords(
    \"... text materi panjang ...\",
    top_n=10  # 10 keywords teratas
)
print(result['keywords'])

# Buat flashcards otomatis
result = skill.create_flashcards(
    \"... text materi ...\",
    num_cards=10
)
for card in result['flashcards']:
    print(f\"Q: {card['question']}\")
    print(f\"A: {card['answer']}\n\")
```

**Kasus Penggunaan:**
- Cepat tau poin penting materi
- Buat flashcards untuk belajar
- Identify konsep utama

---

### 9. 📁 File Management
**Kelola File!** Upload, download, list, dan delete file.

```python
# Upload/save file
with open(\"document.pdf\", 'rb') as f:
    file_content = f.read()

result = skill.save_file(file_content, \"document.pdf\")
print(f\"File ID: {result['file_id']}\")
print(f\"Size: {result['file_size_mb']} MB\")

# List semua file
files = skill.list_files()
for f in files:
    print(f\"{f['filename']} - {f['file_size_mb']} MB\")

# Download file
file_id = \"xxx-xxx-xxx\"
content = skill.get_file(file_id)

# Delete file
result = skill.delete_file(file_id)
```

---

## 📦 Installation

### 1. Install Dependencies

```bash
# Masuk ke folder backend
cd /app/backend

# Install semua requirements
pip install Pillow PyPDF2 pytesseract pandas openpyxl python-docx pdf2image
```

### 2. Install Tesseract OCR (untuk OCR feature)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-ind tesseract-ocr-eng
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Download dari: https://github.com/tesseract-ocr/tesseract

### 3. Install Poppler (untuk PDF to Image)

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

---

## 🔑 API Keys (Untuk AI Features)

Beberapa fitur butuh API key:

### Fitur yang butuh API Key:
- **AI Summarizer** - Butuh OpenAI/Emergent API key
- **Audio Transcription** - Butuh OpenAI/Emergent API key

### Cara dapat API Key:

1. **Emergent LLM Key (Recommended):**
   - Sudah tersedia di environment
   - Bisa untuk OpenAI GPT, Gemini, Claude
   - Paling mudah digunakan

2. **OpenAI API Key:**
   - Daftar di https://platform.openai.com/
   - Buat API key di dashboard
   - Ada free tier untuk testing

### Cara gunakan:

```python
# Gunakan Emergent API key (sudah ada di environment)
import os
api_key = os.environ.get('EMERGENT_API_KEY')

# Atau langsung pass API key
result = await skill.summarize_text(text, api_key=\"your-key-here\")
```

---

## 💡 Contoh Penggunaan Lengkap

### Scenario 1: Compile Tugas dari Berbagai Sumber

```python
from student_helper_skill import StudentHelperSkill
import asyncio

skill = StudentHelperSkill()

# 1. Scan catatan tulis tangan
catatan = skill.ocr_image_to_text(\"catatan_kuliah.jpg\")
with open(\"catatan_text.txt\", 'w') as f:
    f.write(catatan['text'])

# 2. Ringkas PDF panjang
ringkasan = skill.summarize_pdf(\"jurnal_panjang.pdf\", api_key=\"your-key\")
with open(\"ringkasan.txt\", 'w') as f:
    f.write(ringkasan['summary'])

# 3. Transkrip rekaman
transkrip = await skill.transcribe_audio(\"diskusi.mp3\", api_key=\"your-key\")
with open(\"transkrip.txt\", 'w') as f:
    f.write(transkrip['transcript'])

# 4. Generate citation
citation = skill.generate_citation(
    title=\"Referensi Penting\",
    authors=[\"Author Name\"],
    year=2024,
    citation_style='apa'
)
print(f\"Sitasi: {citation['citation']}\")

print(\"✅ Semua bahan tugas siap!\")
```

### Scenario 2: Optimize PDF untuk Upload

```python
# Split PDF besar jadi per chapter
skill.split_pdf(\"buku_lengkap.pdf\", \"chapters/\", pages_per_file=10)

# Atau gabung beberapa PDF
skill.merge_pdfs(
    [\"chapter1.pdf\", \"chapter2.pdf\", \"chapter3.pdf\"],
    \"buku_complete.pdf\"
)
```

### Scenario 3: Belajar dari Rekaman Kuliah

```python
import asyncio

async def process_kuliah():
    skill = StudentHelperSkill()
    
    # 1. Transkrip rekaman
    transkrip = await skill.transcribe_audio(
        \"kuliah_minggu_ini.mp3\",
        api_key=\"your-key\"
    )
    
    # 2. Extract keywords
    keywords = skill.extract_keywords(transkrip['transcript'])
    print(\"Poin penting:\", keywords['keywords'])
    
    # 3. Buat ringkasan
    ringkasan = await skill.summarize_text(
        transkrip['transcript'],
        api_key=\"your-key\"
    )
    print(\"Ringkasan:\", ringkasan['summary'])
    
    # 4. Buat flashcards
    flashcards = skill.create_flashcards(transkrip['transcript'])
    for card in flashcards['flashcards']:
        print(f\"\nQ: {card['question']}\")
        print(f\"A: {card['answer']}\")

# Run
asyncio.run(process_kuliah())
```

---

## 🎯 Tips Penggunaan

### Untuk OCR Terbaik:
- Gunakan foto yang jelas dan terang
- Pastikan text tidak blur
- Foto dari atas (tidak miring)
- Gunakan resolusi tinggi

### Untuk Summarization Terbaik:
- Gunakan AI summarization dengan API key (bukan simple)
- Text yang jelas dan terstruktur lebih baik
- Specify max_length sesuai kebutuhan

### Untuk Audio Transcription:
- Audio yang jernih memberikan hasil terbaik
- Format MP3, WAV, M4A didukung
- Specify bahasa yang benar ('id' atau 'en')

---

## ⚡ Performance Tips

```python
# Untuk file besar, gunakan batch processing
files = [\"file1.pdf\", \"file2.pdf\", \"file3.pdf\"]

for pdf_file in files:
    result = skill.extract_text_from_pdf(pdf_file)
    # Process each file...

# Untuk banyak gambar, compress dalam loop
images = [\"img1.jpg\", \"img2.jpg\", \"img3.jpg\"]

for img in images:
    skill.compress_image(img, f\"compressed_{img}\", quality=85)
```

---

## 🐛 Troubleshooting

### \"pytesseract not found\"
```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr

# Atau untuk macOS
brew install tesseract
```

### \"pdf2image error\"
```bash
# Install poppler
sudo apt-get install poppler-utils

# Atau untuk macOS
brew install poppler
```

### \"API key required\"
Untuk AI features (summarizer, transcription), Anda butuh API key:
- Gunakan Emergent API key yang sudah tersedia
- Atau daftar di OpenAI untuk API key

---

## 📚 Full API Reference

Lihat docstring di setiap function untuk detail lengkap:

```python
# Check available methods
skill = StudentHelperSkill()
help(skill.ocr_image_to_text)
help(skill.summarize_text)
help(skill.transcribe_audio)
# dll...
```

---

## 🎓 Kesimpulan

**Student Helper Skill** adalah toolkit lengkap untuk pelajar/mahasiswa yang ingin:
- ✅ Hemat waktu belajar
- ✅ Organize materi lebih baik  
- ✅ Convert berbagai format file dengan mudah
- ✅ Automate tugas-tugas repetitif
- ✅ Belajar lebih efektif dengan flashcards & ringkasan

**Fitur Paling Berguna:**
1. OCR - Scan catatan
2. AI Summarizer - Ringkas materi
3. Audio to Text - Transkrip kuliah
4. PDF Merge - Compile tugas
5. Citation Generator - Daftar pustaka

---

## 📞 Support

Jika ada pertanyaan atau butuh bantuan:
- Baca dokumentasi ini dengan teliti
- Check error messages dan troubleshooting section
- Pastikan semua dependencies terinstall

**Selamat menggunakan Ultimate Student Helper Skill! 🚀📚**

---

Created with ❤️ by E1 Agent
Version 1.0.0 | 2025
"
Observation: Create successful: /app/backend/STUDENT_HELPER_GUIDE.md
