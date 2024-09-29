import re
from collections import Counter
from konlpy.tag import Mecab

# Mecab 객체 생성
m = Mecab()

# 처리할 파일들의 리스트를 가져옴
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 단어별로 파일명과 챕터를 저장할 딕셔너리 생성
hanja_info = {}

# 숫자 및 원숫자 제거를 위한 정규 표현식
number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')

# 한자만 있는 경우를 처리하기 위한 정규 표현식
hanja_only_pattern = re.compile(r'[一-龥]{2,}')

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日\s第[一二三四五六七八九十百千]+局')

# 각 파일을 읽고 한자 단어들을 추출하여 딕셔너리에 추가
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read().strip()
        
        # 파일의 현재 챕터를 추적하기 위한 변수
        current_chapter = None
        
        # 숫자 및 원숫자를 먼저 제거
        content = number_pattern.sub('', content)

        # 챕터를 찾기
        lines = content.splitlines()
        for line in lines:
            chapter_match = chapter_pattern.search(line)
            if chapter_match:
                current_chapter = chapter_match.group()

            # 한자만 있는 경우를 추출하여 저장
            matches_hanja_only = hanja_only_pattern.findall(line)
            for match in matches_hanja_only:
                if len(match) >= 1:  # 두 글자 이상인 경우만 저장
                    if match not in hanja_info:
                        hanja_info[match] = set()  # 챕터별로 저장하기 위해 set 사용
                    hanja_info[match].add(current_chapter)

# 각 한자 단어가 등장한 챕터 수를 계산
hanja_chapter_counts = {hanja: len(chapters) for hanja, chapters in hanja_info.items()}

# 등장 횟수에 따라 내림차순으로 정렬
sorted_hanja_by_count = sorted(hanja_chapter_counts.items(), key=lambda x: x[1], reverse=True)

# 결과를 출력 및 저장
with open('jikji_hanja_frequency_sorted.txt', 'w', encoding='utf-8') as result_file:
    for hanja, count in sorted_hanja_by_count:
        result_file.write(f"{hanja}: {count}개 챕터에서 등장\n")

print("한자 단어가 등장한 챕터 수에 따라 정렬된 결과가 jikji_hanja_frequency_sorted.txt 파일에 저장되었습니다.")
