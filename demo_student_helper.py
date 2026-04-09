Perfect! Sekarang saya buat file demo/contoh penggunaan yang bisa langsung dijalankan:
Action: file_editor create /app/backend/demo_student_helper.py --file-text "\"\"\"
🧪 DEMO - Ultimate Student Helper Skill
Contoh penggunaan berbagai fitur dari Student Helper Skill

Jalankan file ini untuk test semua fitur!
\"\"\"

import asyncio
import sys
from pathlib import Path

# Import skill
from student_helper_skill import StudentHelperSkill, get_skill_info


def print_section(title):
    \"\"\"Helper untuk print section header\"\"\"
    print(\"\n\" + \"=\" * 60)
    print(f\"🔹 {title}\")
    print(\"=\" * 60)


def demo_skill_info():
    \"\"\"Demo: Get skill information\"\"\"
    print_section(\"SKILL INFORMATION\")
    
    info = get_skill_info()
    print(f\"📦 {info['name']} v{info['version']}\")
    print(f\"📝 {info['description']}\n\")
    print(\"✨ Features:\")
    for feature in info['features']:
        print(f\"   {feature}\")


def demo_file_management(skill):
    \"\"\"Demo: File management operations\"\"\"
    print_section(\"FILE MANAGEMENT\")
    
    # Create test file
    test_content = b\"Hello, this is a test file for Student Helper Skill!\"
    result = skill.save_file(test_content, \"test_demo.txt\")
    
    if result['success']:
        print(f\"✅ File saved: {result['filename']}\")
        print(f\"   File ID: {result['file_id']}\")
        print(f\"   Size: {result['file_size']} bytes\")
    
    # List files
    print(\"\n📁 Files in storage:\")
    files = skill.list_files()
    for f in files[:5]:  # Show max 5
        print(f\"   - {f['filename']} ({f['file_size_mb']} MB)\")
    
    if len(files) > 5:
        print(f\"   ... dan {len(files) - 5} file lainnya\")


def demo_pdf_operations(skill):
    \"\"\"Demo: PDF operations\"\"\"
    print_section(\"PDF OPERATIONS\")
    
    # Create sample text for demo PDF
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    try:
        # Create sample PDF
        pdf_path = \"/tmp/sample_text.pdf\"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, \"Student Helper Skill - Demo PDF\")
        c.drawString(100, 700, \"Ini adalah contoh PDF untuk testing.\")
        c.drawString(100, 680, \"PDF ini berisi text yang bisa di-extract.\")
        c.save()
        
        print(f\"📄 Created sample PDF: {pdf_path}\")
        
        # Extract text from PDF
        result = skill.extract_text_from_pdf(pdf_path)
        if result['success']:
            print(f\"\n✅ Text extracted from PDF:\")
            print(f\"   Total pages: {result['total_pages']}\")
            print(f\"   Word count: {result['word_count']}\")
            print(f\"   Preview: {result['text'][:100]}...\")
        
    except ImportError:
        print(\"⚠️ reportlab not installed. Install: pip install reportlab\")
        print(\"   Skipping PDF demo...\")


def demo_image_processing(skill):
    \"\"\"Demo: Image processing\"\"\"
    print_section(\"IMAGE PROCESSING\")
    
    try:
        from PIL import Image
        import numpy as np
        
        # Create sample image
        img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        original_path = \"/tmp/demo_image.png\"
        img.save(original_path)
        print(f\"🖼️ Created sample image: {original_path}\")
        
        # Resize image
        resized_path = \"/tmp/demo_resized.png\"
        result = skill.resize_image(original_path, resized_path, width=50, height=50)
        if result['success']:
            print(f\"\n✅ Image resized:\")
            print(f\"   From {result['original_size']} → {result['new_size']}\")
        
        # Compress image
        compressed_path = \"/tmp/demo_compressed.jpg\"
        img_jpg = Image.new('RGB', (200, 200), color='red')
        img_jpg.save(original_path.replace('.png', '.jpg'))
        
        result = skill.compress_image(
            original_path.replace('.png', '.jpg'),
            compressed_path,
            quality=50
        )
        if result['success']:
            print(f\"\n✅ Image compressed:\")
            print(f\"   Original: {result['original_size_mb']} MB\")
            print(f\"   Compressed: {result['compressed_size_mb']} MB\")
            print(f\"   Saved: {result['compression_ratio']}\")
        
    except Exception as e:
        print(f\"⚠️ Error in image demo: {e}\")


def demo_ocr(skill):
    \"\"\"Demo: OCR functionality\"\"\"
    print_section(\"OCR - TEXT EXTRACTION\")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create image with text
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw text on image
        text = \"Student Helper Skill - OCR Demo\"
        draw.text((10, 30), text, fill='black')
        
        img_path = \"/tmp/ocr_demo.png\"
        img.save(img_path)
        print(f\"📸 Created sample image with text: {img_path}\")
        
        # Perform OCR
        result = skill.ocr_image_to_text(img_path, language='eng')
        if result['success']:
            print(f\"\n✅ OCR Result:\")
            print(f\"   Extracted text: '{result['text']}'\")
            print(f\"   Confidence: {result['confidence']}%\")
            print(f\"   Word count: {result['word_count']}\")
        else:
            print(f\"❌ OCR failed: {result['error']}\")
        
    except Exception as e:
        print(f\"⚠️ Error in OCR demo: {e}\")


def demo_citation_generator(skill):
    \"\"\"Demo: Citation generator\"\"\"
    print_section(\"CITATION GENERATOR\")
    
    # APA style
    result = skill.generate_citation(
        title=\"Machine Learning for Students\",
        authors=[\"John Doe\", \"Jane Smith\"],
        year=2024,
        publisher=\"Education Press\",
        citation_style='apa'
    )
    if result['success']:
        print(f\"📚 APA Style:\")
        print(f\"   {result['citation']}\")
    
    # MLA style
    result = skill.generate_citation(
        title=\"Deep Learning Basics\",
        authors=[\"Alice Brown\"],
        year=2025,
        publisher=\"Tech Books\",
        citation_style='mla'
    )
    if result['success']:
        print(f\"\n📚 MLA Style:\")
        print(f\"   {result['citation']}\")
    
    # Chicago style
    result = skill.generate_citation(
        title=\"AI in Education\",
        authors=[\"Bob Wilson\", \"Carol Davis\", \"David Lee\"],
        year=2024,
        publisher=\"Academic Press\",
        citation_style='chicago'
    )
    if result['success']:
        print(f\"\n📚 Chicago Style:\")
        print(f\"   {result['citation']}\")


def demo_keywords_extraction(skill):
    \"\"\"Demo: Keywords extraction\"\"\"
    print_section(\"KEYWORDS EXTRACTION\")
    
    sample_text = \"\"\"
    Machine learning adalah cabang dari artificial intelligence yang memungkinkan
    komputer untuk belajar dari data tanpa diprogram secara eksplisit. Deep learning
    adalah subset dari machine learning yang menggunakan neural networks dengan
    banyak layers. Python adalah bahasa pemrograman yang populer untuk machine
    learning karena memiliki banyak library seperti TensorFlow dan PyTorch.
    \"\"\"
    
    result = skill.extract_keywords(sample_text, top_n=5)
    if result['success']:
        print(f\"📖 Text analysis:\")
        print(f\"   Total words: {result['total_words']}\")
        print(f\"   Unique words: {result['unique_words']}\")
        print(f\"\n🔑 Top keywords:\")
        for i, keyword in enumerate(result['keywords'], 1):
            print(f\"   {i}. {keyword}\")


def demo_flashcards(skill):
    \"\"\"Demo: Flashcards generation\"\"\"
    print_section(\"FLASHCARDS GENERATOR\")
    
    sample_text = \"\"\"
    Python adalah bahasa pemrograman tingkat tinggi, dirancang untuk mudah dibaca.
    Machine learning memungkinkan komputer belajar dari data, tanpa pemrograman eksplisit.
    Neural network adalah model komputasi, terinspirasi dari otak manusia.
    Deep learning menggunakan neural networks dengan banyak layer, untuk tugas kompleks.
    \"\"\"
    
    result = skill.create_flashcards(sample_text, num_cards=4)
    if result['success']:
        print(f\"🎴 Generated {result['total_cards']} flashcards:\n\")
        for card in result['flashcards']:
            print(f\"   Card #{card['id']}:\")
            print(f\"   Q: {card['question']}\")
            print(f\"   A: {card['answer']}\n\")


async def demo_summarizer(skill):
    \"\"\"Demo: Text summarization\"\"\"
    print_section(\"AI SUMMARIZER (requires API key)\")
    
    long_text = \"\"\"
    Artificial intelligence (AI) adalah simulasi kecerdasan manusia dalam mesin
    yang diprogram untuk berpikir seperti manusia dan meniru tindakan mereka.
    Machine learning adalah subset dari AI yang memberikan sistem kemampuan
    untuk secara otomatis belajar dan meningkat dari pengalaman tanpa diprogram
    secara eksplisit. Deep learning adalah subset dari machine learning yang
    menggunakan neural networks dengan banyak layers untuk menganalisis berbagai
    faktor data. Python telah menjadi bahasa pemrograman pilihan untuk AI dan
    machine learning karena kesederhanaannya dan ekosistem library yang kuat
    seperti TensorFlow, PyTorch, dan scikit-learn. Aplikasi AI mencakup
    pengenalan suara, computer vision, natural language processing, dan banyak lagi.
    \"\"\"
    
    # Without API key (simple summarization)
    result = await skill.summarize_text(long_text, max_length=50)
    if result['success']:
        print(f\"📝 Summary (Simple Method):\")
        print(f\"   Original: {result['original_length']} words\")
        print(f\"   Summary: {result['summary_length']} words\")
        print(f\"   Compression: {result['compression_ratio']}x\")
        print(f\"\n   {result['summary'][:200]}...\")
        if result.get('note'):
            print(f\"\n   ℹ️ {result['note']}\")


async def demo_audio_transcription(skill):
    \"\"\"Demo: Audio transcription\"\"\"
    print_section(\"AUDIO TRANSCRIPTION (requires API key)\")
    
    print(\"🎙️ Audio to Text Transcription:\")
    print(\"   Fitur ini membutuhkan:\")
    print(\"   1. File audio (MP3, WAV, M4A, dll)\")
    print(\"   2. API key (OpenAI atau Emergent)\")
    print(\"\n   Contoh penggunaan:\")
    print(\"\"\"
    result = await skill.transcribe_audio(
        'rekaman_kuliah.mp3',
        api_key='your-api-key',
        language='id'
    )
    print(result['transcript'])
    \"\"\")
    print(\"\n   ℹ️ Demo dilewati karena butuh API key dan file audio\")


def demo_excel_processing(skill):
    \"\"\"Demo: Excel/CSV processing\"\"\"
    print_section(\"EXCEL/CSV PROCESSING\")
    
    try:
        import pandas as pd
        
        # Create sample data
        data = {
            'Nama': ['Alice', 'Bob', 'Carol'],
            'Nilai': [90, 85, 95],
            'Mata Kuliah': ['Python', 'Machine Learning', 'AI']
        }
        df = pd.DataFrame(data)
        
        # Save as Excel
        excel_path = \"/tmp/demo_data.xlsx\"
        df.to_excel(excel_path, index=False)
        print(f\"📊 Created sample Excel: {excel_path}\")
        
        # Convert to JSON
        result = skill.excel_to_json(excel_path)
        if result['success']:
            print(f\"\n✅ Excel → JSON:\")
            print(f\"   Total rows: {result['total_rows']}\")
            print(f\"   Columns: {result['columns']}\")
            print(f\"   Data preview:\")
            for row in result['data'][:2]:
                print(f\"      {row}\")
        
        # Save as CSV and convert back
        csv_path = \"/tmp/demo_data.csv\"
        df.to_csv(csv_path, index=False)
        
        output_excel = \"/tmp/demo_converted.xlsx\"
        result = skill.csv_to_excel(csv_path, output_excel)
        if result['success']:
            print(f\"\n✅ CSV → Excel:\")
            print(f\"   Output: {result['output_file']}\")
            print(f\"   Total rows: {result['total_rows']}\")
        
    except Exception as e:
        print(f\"⚠️ Error in Excel demo: {e}\")


async def main():
    \"\"\"Main demo function\"\"\"
    print(\"\n\" + \"🎓\" * 30)
    print(\"   ULTIMATE STUDENT HELPER SKILL - DEMO\")
    print(\"🎓\" * 30)
    
    # Initialize skill
    print(\"\n⚙️ Initializing Student Helper Skill...\")
    skill = StudentHelperSkill(storage_dir=\"/tmp/student_helper_demo\")
    print(\"✅ Skill initialized!\n\")
    
    # Run demos
    try:
        demo_skill_info()
        demo_file_management(skill)
        demo_citation_generator(skill)
        demo_keywords_extraction(skill)
        demo_flashcards(skill)
        demo_image_processing(skill)
        demo_ocr(skill)
        demo_excel_processing(skill)
        await demo_summarizer(skill)
        await demo_audio_transcription(skill)
        # demo_pdf_operations(skill)  # Uncomment if reportlab installed
        
        print_section(\"DEMO COMPLETE\")
        print(\"✅ Semua demo berhasil dijalankan!\")
        print(\"\n📚 Untuk penggunaan lengkap, lihat:\")
        print(\"   - STUDENT_HELPER_GUIDE.md\")
        print(\"   - student_helper_skill.py (docstrings)\")
        
        print(\"\n💡 Tips:\")
        print(\"   - Untuk AI features (summarizer, transcription), gunakan API key\")
        print(\"   - Install reportlab untuk PDF generation: pip install reportlab\")
        print(\"   - Lihat panduan lengkap di STUDENT_HELPER_GUIDE.md\")
        
    except Exception as e:
        print(f\"\n❌ Error during demo: {e}\")
        import traceback
        traceback.print_exc()
    
    print(\"\n\" + \"🎓\" * 30 + \"\n\")


if __name__ == \"__main__\":
    # Run async main
    asyncio.run(main())
"
Observation: Create successful: /app/backend/demo_student_helper.py
