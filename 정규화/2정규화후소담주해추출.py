import os
import re
import unicodedata

# 파일 목록
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 특수 문자를 제거하고 텍스트를 정규화하는 함수
def normalize_text(text):
    normalized_text = unicodedata.normalize('NFC', text)
    # 제거할 특수 문자 패턴 정의 (':'를 제거하지 않음)
    special_char_pattern = re.compile(r'[^\w\s\[\]【】「」『』()（）\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF:：]')
    # 특수 문자 제거
    cleaned_text = special_char_pattern.sub('', normalized_text)
    return cleaned_text

# 소담 주해 섹션을 추출하는 함수
def extract_sodam_sections(content):
    # 챕터 패턴: 간지+일 제X국 형태를 매칭
    chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日\s*第[一二三四五六七八九十百千]+局)')
    # 소담 주해 시작 패턴: '【소담 註解】'
    sodam_start_pattern = re.compile(r'【소담\s*註解】')

    # 챕터 정보 추출
    chapters = chapter_pattern.split(content)
    sodam_sections = []

    # 각 챕터에서 소담 주해 추출
    for i in range(1, len(chapters), 2):
        chapter_title = chapters[i].strip()
        chapter_content = chapters[i + 1]

        # 소담 주해 추출
        sodam_start_match = sodam_start_pattern.search(chapter_content)
        if sodam_start_match:
            sodam_text = chapter_content[sodam_start_match.start():].strip()
            sodam_sections.append(f"{chapter_title}\n{sodam_text}")

    return sodam_sections

# 정규화된 텍스트와 소담 주해를 저장할 파일들
normalized_files = []
sodam_dir = 'sodam_juhye/'
os.makedirs(sodam_dir, exist_ok=True)  # 소담 주해 디렉토리 생성

# 정규화된 파일 저장 디렉토리
normalized_dir = 'normalized_files/'
os.makedirs(normalized_dir, exist_ok=True)  # 정규화된 파일 디렉토리 생성

for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 텍스트를 정규화하고 새로운 파일에 저장
    normalized_content = normalize_text(content)
    normalized_file_name = normalized_dir + 'normalized_' + file_name
    with open(normalized_file_name, 'w', encoding='utf-8') as norm_file:
        norm_file.write(normalized_content)
    
    # 정규화된 파일 이름 저장
    normalized_files.append(normalized_file_name)

    # 소담 주해 섹션을 추출하여 파일에 저장
    sodam_sections = extract_sodam_sections(content)
    sodam_file_name = sodam_dir + 'sodam_' + file_name
    with open(sodam_file_name, 'w', encoding='utf-8') as sodam_output:
        for section in sodam_sections:
            sodam_output.write(section + '\n\n')

print("정규화된 파일들이 'normalized_files/' 디렉토리에 저장되었습니다.")
print("모든 파일에서 소담 주해 섹션이 'sodam_juhye/' 디렉토리에 저장되었습니다.")
