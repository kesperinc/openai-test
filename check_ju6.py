import re
from collections import Counter
from konlpy.tag import Mecab

# Mecab 객체 생성
m = Mecab()

# 처리할 파일들의 리스트를 가져옴
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 단어별로 파일명과 챕터를 저장할 딕셔너리 생성
word_info = {}

# 특정 단어들을 설정
specific_words = {'課體': set(), '課意': set(), '解曰': set(), '斷曰': set()}  # 특정 단어를 위한 집합

# 숫자 및 원숫자 제거를 위한 정규 표현식
number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')

# 한글(한자), 한글(한자): 패턴과 한자만 있는 경우를 처리하기 위한 정규 표현식
hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)(:)?')
hanja_only_pattern = re.compile(r'[一-龥]{2,}')

# 챕터 패턴: 간지+일 제X국 형태를 매칭 (더 세부적으로 조정)
chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日\s*第[一二三四五六七八九十百千]+局)')

# 모든 챕터를 저장할 집합
all_chapters = set()

# 각 파일을 읽고 단어들을 추출하여 딕셔너리에 추가
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
                    if word in specific_words:
                        specific_words[word].add(current_chapter)
        
            # 한자만 있는 경우를 처리하여 저장
            matches_hanja_only = hanja_only_pattern.findall(line)
            for match in matches_hanja_only:
                if len(match) >= 2:  # 두 글자 이상인 경우만 저장
                    if match not in word_info:
                        word_info[match] = set()  # 챕터별로 저장하기 위해 set 사용
                    word_info[match].add(current_chapter)
                    if match in specific_words:
                        specific_words[match].add(current_chapter)

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
                    if noun in specific_words:
                        specific_words[noun].add(current_chapter)

# 각 단어가 등장한 챕터 수를 계산
word_chapter_counts = {word: len(chapters) for word, chapters in word_info.items()}

# 등장 횟수에 따라 내림차순으로 정렬
sorted_words_by_count = sorted(word_chapter_counts.items(), key=lambda x: x[1], reverse=True)

# 결과를 출력 및 저장
with open('jikji_frequency_sorted.txt', 'w', encoding='utf-8') as result_file:
    for word, count in sorted_words_by_count:
        result_file.write(f"{word}: {count}개 챕터에서 등장\n")

    # 특정 단어의 챕터 수와 720개 챕터가 아닌 경우 출력
    result_file.write("\n특정 단어의 챕터 수 확인:\n")
    for word, chapters in specific_words.items():
        count = len(chapters)
        result_file.write(f"{word}: {count}개 챕터에서 등장\n")
        if count != 720:
            missing_chapters = all_chapters - chapters
            result_file.write(f"  [경고] {word}가 누락된 챕터들 ({len(missing_chapters)}개):\n")
            for chapter in sorted(missing_chapters):
                result_file.write(f"    - {chapter}\n")

print("각 단어가 등장한 챕터 수에 따라 정렬된 결과와 특정 단어의 챕터 수 확인 결과가 jikji_frequency_sorted.txt 파일에 저장되었습니다.")
