import re

# 처리할 파일 이름
file_name = '4gapo.txt'

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日\s*第[一二三四五六七八九十百千]+局')

# 특정 챕터 (정유일 제6국) 설정
specific_chapter = "丁酉日 第六局"

# 파일을 읽고 챕터들을 추출
with open(file_name, 'r', encoding='utf-8') as file:
    content = file.read()

    # 챕터를 추출
    chapters = chapter_pattern.findall(content)

# 특정 챕터가 있는지 확인하고 출력
if specific_chapter in chapters:
    print(f"'{specific_chapter}'가 파일에 포함되어 있습니다.")
else:
    print(f"'{specific_chapter}'를 찾을 수 없습니다.")
