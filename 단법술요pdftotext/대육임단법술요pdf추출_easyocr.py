import os
import re
from pdf2image import convert_from_path
import easyocr
import numpy as np

def ocr_pdf_to_text(pdf_path):
    all_text = ''
    try:
        # PDF를 이미지로 변환
        images = convert_from_path(pdf_path, dpi=300)
        
        # EasyOCR 모델 초기화 (중국어 간체)
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        
        for img in images:
            # 이미지를 넘파이 배열로 변환
            img_array = np.array(img)
            
            # OCR 수행
            result = reader.readtext(img_array, detail=0, paragraph=True)
            for text in result:
                if text:
                    all_text += text + '\n'
    except Exception as e:
        print(f"Error performing OCR on PDF: {e}")
    return all_text

def create_chapter_pattern(chapter_titles):
    escaped_titles = [re.escape(title) for title in chapter_titles]
    # 긴 제목부터 매칭되도록 정렬
    escaped_titles.sort(key=len, reverse=True)
    pattern = '|'.join(escaped_titles)
    return pattern

def split_text_by_chapter(full_text, chapter_titles):
    # 챕터 제목 패턴 생성
    pattern = create_chapter_pattern(chapter_titles)
    # 챕터 제목 위치 찾기
    matches = list(re.finditer(pattern, full_text))
    
    print(f"Number of chapters found: {len(matches)}")
    
    chapters = []
    
    if not matches:
        print("No chapter headings found.")
        return chapters
    
    for idx, match in enumerate(matches):
        chapter_title = match.group(0).strip()
        start = match.end()
        
        if idx+1 < len(matches):
            end = matches[idx+1].start()
        else:
            end = len(full_text)
        
        content = full_text[start:end].strip()
        chapters.append((chapter_title, content))
    
    return chapters

def save_chapters_to_files(chapters, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for idx, (chapter_title, content) in enumerate(chapters):
        # 파일명 생성: 챕터 번호 + 제목
        # 파일명에 사용할 수 없는 문자 제거
        safe_title = re.sub(r'[\\/*?:\"<>|]', '_', chapter_title)
        file_name = f'{safe_title}.txt'
        file_path = os.path.join(output_dir, file_name)
        
        # 텍스트를 파일에 저장 (UTF-8 인코딩)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(chapter_title + '\n' + content)
        print(f'Saved {file_path}')

def process_pdf_and_save_chapters(pdf_file, output_dir, chapter_titles):
    print(f"Processing PDF with EasyOCR: {pdf_file}")
    full_text = ocr_pdf_to_text(pdf_file)
    
    print(f"Extracted text length: {len(full_text)}")
    if not full_text:
        print(f"No text extracted from {pdf_file}")
        return
    
    print("Extracted text sample:")
    print(full_text[:500])  # 처음 500자 출력
    
    # 텍스트 분할
    chapters = split_text_by_chapter(full_text, chapter_titles)
    
    if not chapters:
        print("No chapters found. Check the split pattern or the extracted text.")
        return
    
    # 텍스트 파일 저장
    save_chapters_to_files(chapters, output_dir)

# 제공된 목차 리스트
chapter_titles = [
    '一、壬书的选择',
    '二、大六壬的学习',
    '三、迅捷起课的方法',
    '四、壬占总纲',
    '五、理气',
    '六、取类',
    '七、察类',
    '八、求财占察类简释',
    '九、察类的一个例子',
    '十、类象琐谈',
    '十一、闲谈干支定位',
    '十二、几个经典课例类象的分析',
    '十三、大六王一揽登堂总断赋',
    '十四、《王归》谋望占的类象分析',
    '十五、《王归》婚姻占的类象分析',
    '十六、《壬归》出行占的类象分析',
    '十七、《壬归》求财占“琐占约云”简释',
    '十八、天官类神',
    '十九、铸印课',
    '二十、空亡详释',
    '二十一、干之寄宫空亡仍以空论',
    '二十二、发用杂论',
    '二十三、脱空、脱盗',
    '二十四、破败',
    '二十五、以理观课余论',
    '二十六、《大六王指南 指学赋》中的类象',
    '二十七、《大六王会寒指南》出行章简释',
    '二十八、《大六壬会篡指南》趋谒章简释',
    '二十九、《大六王会篡指南》贼盗章简释',
    '三十、《指南》两个行人课的综合论断',
    '三十一、关于旺禄临身',
    '三十二、“四课看现状,三传看发展”',
    '三十三、探究六壬源起·用软件起课·练手',
]

# 사용 예시
pdf_file = './북해한인_대육임단법술요1.pdf'
output_directory = '단법술요'  # 저장할 디렉토리
process_pdf_and_save_chapters(pdf_file, output_directory, chapter_titles)
