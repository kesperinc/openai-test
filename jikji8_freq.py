import re
from konlpy.tag import Mecab

# Mecab 객체 생성
m = Mecab()

# 처리할 파일들의 리스트를 가져옴
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 단어별로 파일명과 챕터를 저장할 딕셔너리 생성
word_info = {}

# 숫자 및 원숫자 제거를 위한 정규 표현식
number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')

# 한글(한자), 한글(한자): 패턴과 한자만 있는 경우를 처리하기 위한 정규 표현식
hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)(:)?')
hanja_only_pattern = re.compile(r'[一-龥]{2,}')

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日\s第[一二三四五六七八九十百千]+局')

# 각 파일을 읽고 단어들을 추출하여 딕셔너리에 추가
all_chapters = set()  # 모든 챕터를 저장
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
                all_chapters.add(current_chapter)

            # 한글(한자), 한글(한자): 패턴을 추출하여 저장
            matches = hanja_hangul_pattern.findall(line)
            for match in matches:
                word = match[0]
                if len(word) >= 2:  # 두 글자 이상인 경우만 저장
                    if word not in word_info:
                        word_info[word] = set()  # 챕터별로 저장하기 위해 set 사용
                    word_info[word].add(current_chapter)
        
            # 한자만 있는 경우를 처리하여 저장
            matches_hanja_only = hanja_only_pattern.findall(line)
            for match in matches_hanja_only:
                if len(match) >= 2:  # 두 글자 이상인 경우만 저장
                    if match not in word_info:
                        word_info[match] = set()  # 챕터별로 저장하기 위해 set 사용
                    word_info[match].add(current_chapter)

            # 한글(한자) 및 한자 패턴을 제거한 나머지 텍스트에 대해 형태소 분석
            line_cleaned = hanja_hangul_pattern.sub('', line)
            line_cleaned = hanja_only_pattern.sub('', line)
            nouns = m.nouns(line_cleaned)
            
            # 2글자 이상인 명사만 필터링하여 저장
            for noun in nouns:
                if len(noun) >= 2:
                    if noun not in word_info:
                        word_info[noun] = set()  # 챕터별로 저장하기 위해 set 사용
                    word_info[noun].add(current_chapter)

# '課體'가 등장한 챕터를 찾습니다.
if '課體' in word_info:
    koyi_chapters = set(word_info['課體'])
else:
    koyi_chapters = set()

# '課體'가 포함되지 않은 챕터를 찾습니다.
chapters_without_koyi = all_chapters - koyi_chapters

# 결과를 출력합니다.
if chapters_without_koyi:
    print("다음 챕터에 '課體'가 포함되지 않았습니다:")
    for chapter in sorted(chapters_without_koyi):
        print(f"  챕터: {chapter}")
else:
    print("'課體'가 모든 챕터에 포함되어 있습니다.")

# '課體'가 포함되지 않은 챕터를 파일에 저장
with open('chapters_without_課體.txt', 'w', encoding='utf-8') as result_file:
    if chapters_without_koyi:
        for chapter in sorted(chapters_without_koyi):
            result_file.write(f"챕터: {chapter}\n")
    else:
        result_file.write("'課體'가 모든 챕터에 포함되어 있습니다.\n")

print("'課體'가 포함되지 않은 챕터와 파일 정보가 chapters_without_課體.txt 파일에 저장되었습니다.")
