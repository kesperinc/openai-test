import re
import unicodedata

# 파일 목록
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 특수 문자를 제거하고 텍스트를 정규화하는 함수
def normalize_text(text):
    normalized_text = unicodedata.normalize('NFC', text)
    # 제거할 특수 문자 패턴 정의
    special_char_pattern = re.compile(r'[^\w\s\[\]【】「」『』()（）\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]')
    # 특수 문자 제거
    cleaned_text = special_char_pattern.sub('', normalized_text)
    return cleaned_text

# 소담 주해 섹션을 추출하는 함수
def extract_sodam_section(content):
    # 소담 주해 시작 패턴: '【소담 註解】'
    sodam_start_pattern = re.compile(r'【소담\s*註解】')
    # 섹션을 추출하기 위해 소담 주해 부분부터 끝까지 추출
    sodam_sections = []
    sections = sodam_start_pattern.split(content)
    
    if len(sections) > 1:
        # 첫 번째 요소는 소담 주해 시작 이전의 내용이므로 제외
        for section in sections[1:]:
            sodam_sections.append('【소담 註解】' + section)
    
    return sodam_sections

# 정규화된 텍스트와 소담 주해를 저장할 파일들
normalized_files = []
sodam_output_file = 'sodam_sections.txt'

# 정규화된 파일 저장 디렉토리
normalized_dir = 'normalized_files/'

with open(sodam_output_file, 'w', encoding='utf-8') as sodam_output:
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
        sodam_sections = extract_sodam_section(content)
        for section in sodam_sections:
            sodam_output.write(section + '\n\n')

print("정규화된 파일들이 'normalized_files/' 디렉토리에 저장되었습니다.")
print(f"모든 파일에서 소담 주해 섹션이 '{sodam_output_file}'에 저장되었습니다.")
