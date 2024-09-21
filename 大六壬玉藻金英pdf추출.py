import os
import re
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter

def ocr_pdf_to_text(pdf_path):
    all_text = ''
    try:
        images = convert_from_path(pdf_path)
        for img in images:
            # 이미지 전처리
            img = img.convert('L')  # 그레이스케일 변환
            img = img.filter(ImageFilter.SHARPEN)  # 샤프닝 필터 적용
            img = ImageEnhance.Contrast(img).enhance(2.0)  # 대비 향상
            
            text = pytesseract.image_to_string(img, lang='chi_sim')
            if text:
                all_text += text + '\n'
    except Exception as e:
        print(f"Error performing OCR on PDF: {e}")
    return all_text

def split_text_by_chapter(full_text):
    # 정규식 패턴 수정 (실제 챕터 제목에 맞게)
    pattern = r'(第[一二三四五六七八九十百千万0-9]+[卷章节篇])'
    splits = re.split(pattern, full_text)
    
    print(f"Splits length: {len(splits)}")
    
    chapters = []
    for i in range(1, len(splits), 2):
        chapter_title = splits[i]
        content = splits[i+1] if i+1 < len(splits) else ''
        chapters.append((chapter_title.strip(), content.strip()))
    return chapters

def save_chapters_to_files(chapters, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for idx, (chapter_title, content) in enumerate(chapters):
        # 파일명 생성
        file_name = f'{chapter_title}.txt' if chapter_title else f'chapter_{idx+1}.txt'
        # 파일명에 사용할 수 없는 문자 제거
        file_name = re.sub(r'[\\/*?:\"<>|]', '_', file_name)
        file_path = os.path.join(output_dir, file_name)
        
        # 텍스트를 파일에 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(chapter_title + '\n' + content)
        print(f'Saved {file_path}')

def process_pdf_and_save_chapters(pdf_file, output_dir):
    print(f"Processing PDF with OCR: {pdf_file}")
    full_text = ocr_pdf_to_text(pdf_file)
    
    print(f"Extracted text length: {len(full_text)}")
    if not full_text:
        print(f"No text extracted from {pdf_file}")
        return
    
    print("Extracted text sample:")
    print(full_text[:500])  # 처음 500자 출력

    # 텍스트 분할
    chapters = split_text_by_chapter(full_text)
    print(f"Number of chapters found: {len(chapters)}")

    if not chapters:
        print("No chapters found. Check the split pattern or the extracted text.")
        return

    # 텍스트 파일 저장
    save_chapters_to_files(chapters, output_dir)

# Tesseract 실행 파일 경로 설정 (필요한 경우)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# 사용 예시
pdf_file = './lr2024090902_大六壬玉藻金英.pdf'
output_directory = 'doc'  # 저장할 디렉토리
process_pdf_and_save_chapters(pdf_file, output_directory)
