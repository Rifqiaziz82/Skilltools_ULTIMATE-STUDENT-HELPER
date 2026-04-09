
Action: file_editor create /app/backend/student_helper_skill.py --file-text "\"\"\"
🎓 ULTIMATE STUDENT HELPER SKILL
================================
OpenClaw Python Skill untuk membantu pelajar/mahasiswa dengan berbagai kebutuhan studi.

Features:
- 📁 File Management (Upload/Download/Convert)
- 📸 OCR - Scan catatan tulis tangan jadi text
- 🤖 AI Summarizer - Ringkas dokumen panjang
- 🎙️ Audio to Text - Transkrip rekaman kuliah
- 📄 PDF Operations (Merge, Split, Extract)
- 📚 Citation Generator - Buat daftar pustaka otomatis
- 🖼️ Image Processing (Resize, Compress, Convert)
- 🌐 Document Translator

Author: E1 Agent
Version: 1.0.0
Python: 3.11+
\"\"\"

import os
import io
import json
import base64
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict, Any, BinaryIO
from datetime import datetime
import uuid

# Core libraries
import asyncio
from pydantic import BaseModel, Field

# File processing libraries
try:
    from PIL import Image
    import PyPDF2
    from PyPDF2 import PdfReader, PdfWriter, PdfMerger
except ImportError:
    print(\"⚠️ Install: pip install Pillow PyPDF2\")

# OCR library
try:
    import pytesseract
    from PIL import Image
except ImportError:
    print(\"⚠️ Install: pip install pytesseract pillow\")
    print(\"⚠️ Also install Tesseract-OCR: https://github.com/tesseract-ocr/tesseract\")

# Excel/CSV processing
try:
    import pandas as pd
except ImportError:
    print(\"⚠️ Install: pip install pandas openpyxl\")

# Document processing
try:
    from docx import Document
except ImportError:
    print(\"⚠️ Install: pip install python-docx\")


class StudentHelperSkill:
    \"\"\"
    Main class untuk Student Helper Skill.
    Menyediakan berbagai fungsi untuk membantu kebutuhan pelajar.
    \"\"\"
    
    def __init__(self, storage_dir: str = \"/tmp/student_helper\"):
        \"\"\"
        Initialize Student Helper Skill
        
        Args:
            storage_dir: Directory untuk menyimpan file yang diupload
        \"\"\"
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        print(f\"✅ Student Helper Skill initialized. Storage: {self.storage_dir}\")
    
    # ==========================================
    # 📁 FILE MANAGEMENT
    # ==========================================
    
    def save_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        \"\"\"
        Save file ke storage
        
        Args:
            file_content: Binary content dari file
            filename: Nama file
            
        Returns:
            Dict dengan info file yang disimpan
        \"\"\"
        try:
            file_id = str(uuid.uuid4())
            file_ext = Path(filename).suffix
            safe_filename = f\"{file_id}{file_ext}\"
            file_path = self.storage_dir / safe_filename
            
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            file_size = len(file_content)
            
            return {
                \"success\": True,
                \"file_id\": file_id,
                \"filename\": filename,
                \"safe_filename\": safe_filename,
                \"file_path\": str(file_path),
                \"file_size\": file_size,
                \"file_size_mb\": round(file_size / (1024 * 1024), 2),
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def get_file(self, file_id: str) -> Optional[bytes]:
        \"\"\"
        Retrieve file dari storage berdasarkan file_id
        
        Args:
            file_id: ID file yang ingin diambil
            
        Returns:
            Binary content dari file atau None jika tidak ditemukan
        \"\"\"
        try:
            # Cari file dengan file_id
            for file_path in self.storage_dir.glob(f\"{file_id}.*\"):
                with open(file_path, 'rb') as f:
                    return f.read()
            return None
        except Exception as e:
            print(f\"❌ Error getting file: {e}\")
            return None
    
    def list_files(self) -> List[Dict[str, Any]]:
        \"\"\"
        List semua file yang ada di storage
        
        Returns:
            List of file info dictionaries
        \"\"\"
        files = []
        for file_path in self.storage_dir.glob(\"*\"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    \"filename\": file_path.name,
                    \"file_path\": str(file_path),
                    \"file_size\": stat.st_size,
                    \"file_size_mb\": round(stat.st_size / (1024 * 1024), 2),
                    \"created_at\": datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
        return files
    
    def delete_file(self, file_id: str) -> Dict[str, Any]:
        \"\"\"
        Delete file dari storage
        
        Args:
            file_id: ID file yang ingin dihapus
            
        Returns:
            Dict dengan status operasi
        \"\"\"
        try:
            for file_path in self.storage_dir.glob(f\"{file_id}.*\"):
                file_path.unlink()
                return {\"success\": True, \"message\": f\"File {file_id} deleted\"}
            return {\"success\": False, \"error\": \"File not found\"}
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    # ==========================================
    # 📸 OCR - SCAN CATATAN JADI TEXT
    # ==========================================
    
    def ocr_image_to_text(self, image_path: str, language: str = 'ind+eng') -> Dict[str, Any]:
        \"\"\"
        Extract text dari gambar menggunakan OCR (Optical Character Recognition)
        SUPER BERGUNA: Foto catatan tulis tangan → jadi text yang bisa dicopy!
        
        Args:
            image_path: Path ke file gambar
            language: Bahasa untuk OCR ('ind' untuk Indonesia, 'eng' untuk English)
            
        Returns:
            Dict dengan extracted text dan metadata
            
        Example:
            skill = StudentHelperSkill()
            result = skill.ocr_image_to_text(\"foto_catatan.jpg\")
            print(result['text'])  # Text dari catatan!
        \"\"\"
        try:
            # Buka gambar
            img = Image.open(image_path)
            
            # Preprocessing: Convert ke grayscale untuk hasil lebih baik
            img = img.convert('L')
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(img, lang=language)
            
            # Get additional info
            ocr_data = pytesseract.image_to_data(img, lang=language, output_type=pytesseract.Output.DICT)
            confidence = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidence) / len(confidence) if confidence else 0
            
            return {
                \"success\": True,
                \"text\": extracted_text.strip(),
                \"word_count\": len(extracted_text.split()),
                \"char_count\": len(extracted_text),
                \"confidence\": round(avg_confidence, 2),
                \"language\": language,
                \"image_size\": img.size,
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def ocr_pdf_to_text(self, pdf_path: str, language: str = 'ind+eng') -> Dict[str, Any]:
        \"\"\"
        Extract text dari PDF yang berisi scan/gambar menggunakan OCR
        
        Args:
            pdf_path: Path ke file PDF
            language: Bahasa untuk OCR
            
        Returns:
            Dict dengan extracted text dari semua halaman
        \"\"\"
        try:
            from pdf2image import convert_from_path
            
            # Convert PDF pages to images
            images = convert_from_path(pdf_path)
            
            all_text = []
            total_confidence = 0
            
            for i, img in enumerate(images):
                # OCR each page
                text = pytesseract.image_to_string(img, lang=language)
                all_text.append(f\"--- Page {i+1} ---\n{text}\n\")
                
                # Calculate confidence
                ocr_data = pytesseract.image_to_data(img, lang=language, output_type=pytesseract.Output.DICT)
                confidence = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
                if confidence:
                    total_confidence += sum(confidence) / len(confidence)
            
            combined_text = \"\n\".join(all_text)
            avg_confidence = total_confidence / len(images) if images else 0
            
            return {
                \"success\": True,
                \"text\": combined_text,
                \"total_pages\": len(images),
                \"word_count\": len(combined_text.split()),
                \"confidence\": round(avg_confidence, 2),
                \"timestamp\": datetime.now().isoformat()
            }
        except ImportError:
            return {\"success\": False, \"error\": \"Install pdf2image: pip install pdf2image\"}
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    # ==========================================
    # 🤖 AI SUMMARIZER - RINGKAS DOKUMEN
    # ==========================================
    
    async def summarize_text(self, text: str, max_length: int = 500, api_key: Optional[str] = None) -> Dict[str, Any]:
        \"\"\"
        Ringkas text panjang jadi singkat menggunakan AI
        SUPER BERGUNA: Materi 20 halaman → jadi ringkasan 1 halaman!
        
        Args:
            text: Text yang ingin diringkas
            max_length: Panjang maksimal ringkasan (dalam kata)
            api_key: OpenAI/Emergent API key (optional)
            
        Returns:
            Dict dengan ringkasan dan metadata
            
        Example:
            skill = StudentHelperSkill()
            long_text = \"... materi panjang ...\"
            result = await skill.summarize_text(long_text)
            print(result['summary'])
        \"\"\"
        try:
            # Jika tidak ada API key, gunakan summarization sederhana
            if not api_key:
                return self._simple_summarize(text, max_length)
            
            # Jika ada API key, gunakan AI summarization
            from emergentintegrations import Client
            
            client = Client(api_key=api_key)
            
            prompt = f\"\"\"Ringkas text berikut menjadi poin-poin penting dalam Bahasa Indonesia.
Buatlah ringkasan yang mudah dipahami untuk pelajar.

TEXT:
{text[:8000]}  # Limit untuk avoid token limit

INSTRUKSI:
- Buat ringkasan maksimal {max_length} kata
- Gunakan bullet points
- Fokus pada poin penting
- Bahasa Indonesia yang jelas
\"\"\"
            
            response = client.chat.completions.create(
                model=\"gpt-4o-mini\",
                messages=[{\"role\": \"user\", \"content\": prompt}],
                temperature=0.5
            )
            
            summary = response.choices[0].message.content
            
            return {
                \"success\": True,
                \"summary\": summary,
                \"original_length\": len(text.split()),
                \"summary_length\": len(summary.split()),
                \"compression_ratio\": round(len(text) / len(summary), 2),
                \"timestamp\": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def _simple_summarize(self, text: str, max_length: int = 500) -> Dict[str, Any]:
        \"\"\"
        Simple summarization tanpa AI (extractive summarization)
        Mengambil kalimat-kalimat paling penting
        \"\"\"
        try:
            sentences = text.replace('\n', ' ').split('.')
            sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
            
            # Ambil kalimat pertama dan beberapa kalimat penting
            important_sentences = sentences[:min(10, len(sentences))]
            summary = '. '.join(important_sentences) + '.'
            
            # Trim jika terlalu panjang
            words = summary.split()
            if len(words) > max_length:
                summary = ' '.join(words[:max_length]) + '...'
            
            return {
                \"success\": True,
                \"summary\": summary,
                \"original_length\": len(text.split()),
                \"summary_length\": len(summary.split()),
                \"compression_ratio\": round(len(text) / len(summary), 2),
                \"method\": \"extractive\",
                \"note\": \"Gunakan API key untuk AI-powered summarization yang lebih baik\",
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def summarize_pdf(self, pdf_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        \"\"\"
        Ringkas PDF langsung
        
        Args:
            pdf_path: Path ke file PDF
            api_key: API key untuk AI summarization
            
        Returns:
            Dict dengan ringkasan PDF
        \"\"\"
        try:
            # Extract text dari PDF
            text = self.extract_text_from_pdf(pdf_path)
            
            if not text.get('success'):
                return text
            
            # Summarize text
            import asyncio
            summary_result = asyncio.run(self.summarize_text(text['text'], api_key=api_key))
            
            return {
                **summary_result,
                \"source_file\": pdf_path,
                \"total_pages\": text.get('total_pages', 0)
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    # ==========================================
    # 🎙️ AUDIO TO TEXT - TRANSKRIP REKAMAN
    # ==========================================
    
    async def transcribe_audio(self, audio_path: str, api_key: Optional[str] = None, language: str = 'id') -> Dict[str, Any]:
        \"\"\"
        Convert rekaman audio jadi text (transcription)
        SUPER BERGUNA: Rekaman kuliah → jadi catatan tertulis!
        
        Args:
            audio_path: Path ke file audio (mp3, wav, m4a, dll)
            api_key: OpenAI/Emergent API key
            language: Kode bahasa ('id' untuk Indonesia, 'en' untuk English)
            
        Returns:
            Dict dengan transkrip dan metadata
            
        Example:
            skill = StudentHelperSkill()
            result = await skill.transcribe_audio(\"rekaman_kuliah.mp3\", api_key=\"your-key\")
            print(result['transcript'])
        \"\"\"
        try:
            if not api_key:
                return {
                    \"success\": False,
                    \"error\": \"API key required untuk audio transcription\",
                    \"note\": \"Dapatkan API key dari OpenAI atau gunakan Emergent API key\"
                }
            
            from emergentintegrations import Client
            
            client = Client(api_key=api_key)
            
            # Open audio file
            with open(audio_path, 'rb') as audio_file:
                # Transcribe using Whisper
                transcript = client.audio.transcriptions.create(
                    model=\"whisper-1\",
                    file=audio_file,
                    language=language,
                    response_format=\"verbose_json\"
                )
            
            return {
                \"success\": True,
                \"transcript\": transcript.text,
                \"language\": language,
                \"duration\": transcript.duration if hasattr(transcript, 'duration') else None,
                \"word_count\": len(transcript.text.split()),
                \"timestamp\": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    # ==========================================
    # 📄 PDF OPERATIONS
    # ==========================================
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        \"\"\"
        Extract text dari PDF (untuk PDF yang sudah ada text-nya, bukan scan)
        
        Args:
            pdf_path: Path ke file PDF
            
        Returns:
            Dict dengan extracted text
        \"\"\"
        try:
            reader = PdfReader(pdf_path)
            
            all_text = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                all_text.append(f\"--- Page {i+1} ---\n{text}\n\")
            
            combined_text = \"\n\".join(all_text)
            
            return {
                \"success\": True,
                \"text\": combined_text,
                \"total_pages\": len(reader.pages),
                \"word_count\": len(combined_text.split()),
                \"char_count\": len(combined_text),
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def merge_pdfs(self, pdf_paths: List[str], output_path: str) -> Dict[str, Any]:
        \"\"\"
        Gabung beberapa PDF jadi satu file
        BERGUNA: Compile banyak file tugas jadi satu!
        
        Args:
            pdf_paths: List of PDF file paths yang ingin digabung
            output_path: Path untuk output file
            
        Returns:
            Dict dengan info hasil merge
            
        Example:
            skill = StudentHelperSkill()
            result = skill.merge_pdfs(
                [\"tugas1.pdf\", \"tugas2.pdf\", \"tugas3.pdf\"],
                \"tugas_lengkap.pdf\"
            )
        \"\"\"
        try:
            merger = PdfMerger()
            
            for pdf in pdf_paths:
                merger.append(pdf)
            
            merger.write(output_path)
            merger.close()
            
            # Get output file size
            output_size = Path(output_path).stat().st_size
            
            return {
                \"success\": True,
                \"output_file\": output_path,
                \"total_files_merged\": len(pdf_paths),
                \"output_size_mb\": round(output_size / (1024 * 1024), 2),
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def split_pdf(self, pdf_path: str, output_dir: str, pages_per_file: int = 1) -> Dict[str, Any]:
        \"\"\"
        Pisah PDF jadi file-file kecil
        
        Args:
            pdf_path: Path ke PDF yang ingin dipisah
            output_dir: Directory untuk output files
            pages_per_file: Jumlah halaman per file
            
        Returns:
            Dict dengan info hasil split
        \"\"\"
        try:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            output_files = []
            
            for i in range(0, total_pages, pages_per_file):
                writer = PdfWriter()
                
                # Add pages
                for j in range(i, min(i + pages_per_file, total_pages)):
                    writer.add_page(reader.pages[j])
                
                # Write output file
                output_file = output_path / f\"page_{i+1}_to_{min(i+pages_per_file, total_pages)}.pdf\"
                with open(output_file, 'wb') as f:
                    writer.write(f)
                
                output_files.append(str(output_file))
            
            return {
                \"success\": True,
                \"total_pages\": total_pages,
                \"total_files_created\": len(output_files),
                \"output_files\": output_files,
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    # ==========================================
    # 📚 CITATION GENERATOR
    # ==========================================
    
    def generate_citation(self, 
                         title: str,
                         authors: List[str],
                         year: int,
                         publisher: Optional[str] = None,
                         url: Optional[str] = None,
                         citation_style: str = 'apa') -> Dict[str, Any]:
        \"\"\"
        Generate citation/sitasi untuk daftar pustaka
        BERGUNA: Bikin daftar pustaka otomatis!
        
        Args:
            title: Judul buku/artikel
            authors: List of author names
            year: Tahun publikasi
            publisher: Penerbit (optional)
            url: URL (optional, untuk web sources)
            citation_style: Style sitasi ('apa', 'mla', 'chicago')
            
        Returns:
            Dict dengan citation dalam berbagai format
            
        Example:
            skill = StudentHelperSkill()
            citation = skill.generate_citation(
                title=\"Machine Learning Basics\",
                authors=[\"John Doe\", \"Jane Smith\"],
                year=2024,
                publisher=\"Tech Press\",
                citation_style='apa'
            )
            print(citation['citation'])
        \"\"\"
        try:
            authors_formatted = self._format_authors(authors, citation_style)
            
            if citation_style.lower() == 'apa':
                citation = self._generate_apa_citation(
                    authors_formatted, year, title, publisher, url
                )
            elif citation_style.lower() == 'mla':
                citation = self._generate_mla_citation(
                    authors_formatted, title, publisher, year, url
                )
            elif citation_style.lower() == 'chicago':
                citation = self._generate_chicago_citation(
                    authors_formatted, year, title, publisher, url
                )
            else:
                return {\"success\": False, \"error\": f\"Unknown citation style: {citation_style}\"}
            
            return {
                \"success\": True,
                \"citation\": citation,
                \"style\": citation_style.upper(),
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def _format_authors(self, authors: List[str], style: str) -> str:
        \"\"\"Format author names based on citation style\"\"\"
        if not authors:
            return \"\"
        
        if style.lower() == 'apa':
            if len(authors) == 1:
                return authors[0]
            elif len(authors) == 2:
                return f\"{authors[0]} & {authors[1]}\"
            else:
                return f\"{authors[0]}, et al.\"
        
        elif style.lower() == 'mla':
            if len(authors) == 1:
                return authors[0]
            elif len(authors) == 2:
                return f\"{authors[0]} and {authors[1]}\"
            else:
                return f\"{authors[0]}, et al.\"
        
        else:  # Chicago
            if len(authors) == 1:
                return authors[0]
            elif len(authors) <= 3:
                return \", \".join(authors[:-1]) + f\", and {authors[-1]}\"
            else:
                return f\"{authors[0]} et al.\"
    
    def _generate_apa_citation(self, authors: str, year: int, title: str, 
                              publisher: Optional[str], url: Optional[str]) -> str:
        \"\"\"Generate APA style citation\"\"\"
        citation = f\"{authors} ({year}). {title}.\"
        if publisher:
            citation += f\" {publisher}.\"
        if url:
            citation += f\" {url}\"
        return citation
    
    def _generate_mla_citation(self, authors: str, title: str, 
                              publisher: Optional[str], year: int, 
                              url: Optional[str]) -> str:
        \"\"\"Generate MLA style citation\"\"\"
        citation = f\"{authors}. {title}.\"
        if publisher:
            citation += f\" {publisher},\"
        citation += f\" {year}.\"
        if url:
            citation += f\" {url}.\"
        return citation
    
    def _generate_chicago_citation(self, authors: str, year: int, title: str,
                                   publisher: Optional[str], url: Optional[str]) -> str:
        \"\"\"Generate Chicago style citation\"\"\"
        citation = f\"{authors}. {year}. {title}.\"
        if publisher:
            citation += f\" {publisher}.\"
        if url:
            citation += f\" {url}.\"
        return citation
    
    # ==========================================
    # 🖼️ IMAGE PROCESSING
    # ==========================================
    
    def resize_image(self, image_path: str, output_path: str, 
                    width: Optional[int] = None, height: Optional[int] = None,
                    maintain_aspect: bool = True) -> Dict[str, Any]:
        \"\"\"
        Resize/ubah ukuran gambar
        
        Args:
            image_path: Path ke gambar
            output_path: Path untuk output
            width: Lebar baru (pixels)
            height: Tinggi baru (pixels)
            maintain_aspect: Maintain aspect ratio
            
        Returns:
            Dict dengan info hasil resize
        \"\"\"
        try:
            img = Image.open(image_path)
            original_size = img.size
            
            if maintain_aspect:
                if width and not height:
                    aspect_ratio = img.size[1] / img.size[0]
                    height = int(width * aspect_ratio)
                elif height and not width:
                    aspect_ratio = img.size[0] / img.size[1]
                    width = int(height * aspect_ratio)
            
            if not width or not height:
                return {\"success\": False, \"error\": \"Specify width or height\"}
            
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            resized.save(output_path)
            
            return {
                \"success\": True,
                \"original_size\": original_size,
                \"new_size\": (width, height),
                \"output_file\": output_path,
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def compress_image(self, image_path: str, output_path: str, 
                      quality: int = 85) -> Dict[str, Any]:
        \"\"\"
        Compress gambar untuk reduce file size
        BERGUNA: Upload gambar yang file size-nya kegedean!
        
        Args:
            image_path: Path ke gambar
            output_path: Path untuk output
            quality: Quality level (0-100, higher = better quality)
            
        Returns:
            Dict dengan info hasil compress
        \"\"\"
        try:
            img = Image.open(image_path)
            
            # Get original file size
            original_size = Path(image_path).stat().st_size
            
            # Save with compression
            img.save(output_path, optimize=True, quality=quality)
            
            # Get compressed file size
            compressed_size = Path(output_path).stat().st_size
            
            compression_ratio = round((1 - compressed_size / original_size) * 100, 2)
            
            return {
                \"success\": True,
                \"original_size_mb\": round(original_size / (1024 * 1024), 2),
                \"compressed_size_mb\": round(compressed_size / (1024 * 1024), 2),
                \"compression_ratio\": f\"{compression_ratio}%\",
                \"output_file\": output_path,
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def convert_image_format(self, image_path: str, output_path: str, 
                           target_format: str = 'PNG') -> Dict[str, Any]:
        \"\"\"
        Convert format gambar (JPG ↔ PNG ↔ WebP, dll)
        
        Args:
            image_path: Path ke gambar
            output_path: Path untuk output
            target_format: Target format ('PNG', 'JPEG', 'WebP', dll)
            
        Returns:
            Dict dengan info hasil convert
        \"\"\"
        try:
            img = Image.open(image_path)
            original_format = img.format
            
            # Convert RGBA to RGB for JPEG
            if target_format.upper() == 'JPEG' and img.mode == 'RGBA':
                img = img.convert('RGB')
            
            img.save(output_path, format=target_format.upper())
            
            return {
                \"success\": True,
                \"original_format\": original_format,
                \"new_format\": target_format.upper(),
                \"output_file\": output_path,
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    # ==========================================
    # 📊 EXCEL/CSV PROCESSING
    # ==========================================
    
    def excel_to_json(self, excel_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        \"\"\"
        Convert Excel ke JSON
        BERGUNA: Convert data Excel untuk dipakai di API/web!
        
        Args:
            excel_path: Path ke file Excel
            sheet_name: Nama sheet (optional, default: first sheet)
            
        Returns:
            Dict dengan JSON data
        \"\"\"
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Convert to JSON
            json_data = df.to_dict(orient='records')
            
            return {
                \"success\": True,
                \"data\": json_data,
                \"total_rows\": len(df),
                \"columns\": list(df.columns),
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def csv_to_excel(self, csv_path: str, output_path: str) -> Dict[str, Any]:
        \"\"\"
        Convert CSV ke Excel
        
        Args:
            csv_path: Path ke CSV file
            output_path: Path untuk output Excel
            
        Returns:
            Dict dengan info hasil convert
        \"\"\"
        try:
            df = pd.read_csv(csv_path)
            df.to_excel(output_path, index=False)
            
            return {
                \"success\": True,
                \"total_rows\": len(df),
                \"columns\": list(df.columns),
                \"output_file\": output_path,
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    # ==========================================
    # 📖 STUDY HELPER UTILITIES
    # ==========================================
    
    def extract_keywords(self, text: str, top_n: int = 10) -> Dict[str, Any]:
        \"\"\"
        Extract keywords penting dari text
        BERGUNA: Cepat tau poin penting dari materi!
        
        Args:
            text: Text yang ingin diextract keywords-nya
            top_n: Jumlah top keywords yang ingin diambil
            
        Returns:
            Dict dengan list keywords
        \"\"\"
        try:
            # Simple keyword extraction based on word frequency
            # Remove common words (stopwords)
            stopwords = {'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan',
                        'adalah', 'ini', 'itu', 'atau', 'the', 'a', 'an', 'and', 'or',
                        'but', 'in', 'on', 'at', 'to', 'for', 'of', 'as', 'by'}
            
            words = text.lower().split()
            words = [w.strip('.,!?;:()[]{}\\"\'') for w in words]
            words = [w for w in words if w and len(w) > 3 and w not in stopwords]
            
            # Count frequency
            from collections import Counter
            word_freq = Counter(words)
            
            # Get top keywords
            keywords = [word for word, count in word_freq.most_common(top_n)]
            
            return {
                \"success\": True,
                \"keywords\": keywords,
                \"total_words\": len(text.split()),
                \"unique_words\": len(set(words)),
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}
    
    def create_flashcards(self, text: str, num_cards: int = 10) -> Dict[str, Any]:
        \"\"\"
        Buat flashcards otomatis dari materi
        BERGUNA: Belajar jadi lebih efektif dengan flashcards!
        
        Args:
            text: Text materi
            num_cards: Jumlah flashcards yang ingin dibuat
            
        Returns:
            Dict dengan flashcards
        \"\"\"
        try:
            # Split into sentences
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 30]
            
            # Create simple flashcards (statement format)
            flashcards = []
            for i, sentence in enumerate(sentences[:num_cards]):
                # Try to extract key concept (first part as question, second as answer)
                parts = sentence.split(',')
                if len(parts) >= 2:
                    flashcards.append({
                        \"id\": i + 1,
                        \"question\": parts[0].strip() + \"?\",
                        \"answer\": ','.join(parts[1:]).strip()
                    })
                else:
                    flashcards.append({
                        \"id\": i + 1,
                        \"question\": f\"Jelaskan: {sentence[:50]}...\",
                        \"answer\": sentence
                    })
            
            return {
                \"success\": True,
                \"flashcards\": flashcards,
                \"total_cards\": len(flashcards),
                \"note\": \"Untuk flashcards yang lebih baik, gunakan AI dengan API key\",
                \"timestamp\": datetime.now().isoformat()
            }
        except Exception as e:
            return {\"success\": False, \"error\": str(e)}


# ==========================================
# 🚀 HELPER FUNCTIONS & EXAMPLES
# ==========================================

def get_skill_info() -> Dict[str, Any]:
    \"\"\"
    Get informasi tentang Student Helper Skill
    \"\"\"
    return {
        \"name\": \"Ultimate Student Helper Skill\",
        \"version\": \"1.0.0\",
        \"description\": \"OpenClaw Python skill untuk membantu pelajar dengan berbagai kebutuhan studi\",
        \"features\": [
            \"📁 File Management (Upload/Download/Convert)\",
            \"📸 OCR - Scan catatan jadi text\",
            \"🤖 AI Summarizer - Ringkas dokumen\",
            \"🎙️ Audio to Text - Transkrip rekaman\",
            \"📄 PDF Operations (Merge/Split/Extract)\",
            \"📚 Citation Generator - Daftar pustaka otomatis\",
            \"🖼️ Image Processing (Resize/Compress/Convert)\",
            \"📊 Excel/CSV Processing\",
            \"📖 Study Helpers (Keywords, Flashcards)\"
        ],
        \"requirements\": [
            \"Pillow\",
            \"PyPDF2\",
            \"pytesseract\",
            \"pandas\",
            \"openpyxl\",
            \"python-docx\",
            \"pdf2image\",
            \"emergentintegrations (untuk AI features)\"
        ],
        \"author\": \"E1 Agent\",
        \"created\": \"2025\"
    }


# Example usage
if __name__ == \"__main__\":
    print(\"🎓 ULTIMATE STUDENT HELPER SKILL\")
    print(\"=\" * 50)
    
    # Initialize skill
    skill = StudentHelperSkill()
    
    # Print skill info
    info = get_skill_info()
    print(f\"\n✨ {info['name']} v{info['version']}\")
    print(f\"📝 {info['description']}\n\")
    
    print(\"🔥 FEATURES:\")
    for feature in info['features']:
        print(f\"  {feature}\")
    
    print(\"\n\" + \"=\" * 50)
    print(\"✅ Skill ready to use!\")
    print(\"\nContoh penggunaan:\")
    print(\"\"\"
    # Import skill
    from student_helper_skill import StudentHelperSkill
    
    # Initialize
    skill = StudentHelperSkill()
    
    # OCR - Scan catatan
    result = skill.ocr_image_to_text(\"foto_catatan.jpg\")
    print(result['text'])
    
    # Summarize PDF
    result = skill.summarize_pdf(\"materi_kuliah.pdf\", api_key=\"your-key\")
    print(result['summary'])
    
    # Transcribe audio
    import asyncio
    result = asyncio.run(skill.transcribe_audio(\"rekaman.mp3\", api_key=\"your-key\"))
    print(result['transcript'])
    
    # Merge PDFs
    result = skill.merge_pdfs(
        [\"file1.pdf\", \"file2.pdf\"],
        \"output.pdf\"
    )
    
    # Generate citation
    result = skill.generate_citation(
        title=\"Book Title\",
        authors=[\"Author Name\"],
        year=2024,
        citation_style='apa'
    )
    print(result['citation'])
    \"\"\")
"
Observation: Create successful: /app/backend/student_helper_skill.py
