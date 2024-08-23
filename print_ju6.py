import re

# 처리할 파일 이름
file_name = '4gapo.txt'

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日\s*第[一二三四五六七八九十百千]+局')

# 특정 챕터 설정
start_chapter = "丁酉日 第六局"
end_chapter = "丁酉日 第七局"

# 파일을 읽고 내용을 추출
with open(file_name, 'r', encoding='utf-8') as file:
    content = file.read()

# 특정 챕터의 시작과 끝 위치를 찾음
start_match = re.search(re.escape(start_chapter), content)
end_match = re.search(re.escape(end_chapter), content)

# 내용 추출 및 출력
if start_match and end_match:
    start_index = start_match.start()
    end_index = end_match.start()
    extracted_content = content[start_index:end_index].strip()
    print(f"'{start_chapter}'부터 '{end_chapter}'까지의 내용:")
    print(extracted_content)
elif start_match and not end_match:
    start_index = start_match.start()
    extracted_content = content[start_index:].strip()
    print(f"'{start_chapter}'부터 파일 끝까지의 내용:")
    print(extracted_content)
else:
    print(f"'{start_chapter}' 또는 '{end_chapter}'를 찾을 수 없습니다.")
