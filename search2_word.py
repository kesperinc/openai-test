import re
from konlpy.tag import Mecab

# Mecab 객체 생성
m = Mecab()

# 처리할 파일들의 리스트를 가져옴
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 단어별로 파일명, 챕터, 등장 횟수를 저장할 딕셔너리 생성
word_info = {}

# 숫자 및 원숫자 제거를 위한 정규 표현식
number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')

# 한글(한자), 한글(한자): 패턴과 한자만 있는 경우를 처리하기 위한 정규 표현식
hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)(:)?')
hanja_only_pattern = re.compile(r'[一-龥]{2,}')

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日\s第[一二三四五六七八九十百千]+局')

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

            # 한글(한자), 한글(한자): 패턴을 추출하여 저장
            matches = hanja_hangul_pattern.findall(line)
            for match in matches:
                word = match[0]
                if len(word) >= 2:  # 두 글자 이상인 경우만 저장
                    if word not in word_info:
                        word_info[word] = {'count': 0, 'locations': []}
                    word_info[word]['count'] += 1
                    word_info[word]['locations'].append((file_name, current_chapter))
        
            # 한자만 있는 경우를 처리하여 저장
            matches_hanja_only = hanja_only_pattern.findall(line)
            for match in matches_hanja_only:
                if len(match) >= 2:  # 두 글자 이상인 경우만 저장
                    if match not in word_info:
                        word_info[match] = {'count': 0, 'locations': []}
                    word_info[match]['count'] += 1
                    word_info[match]['locations'].append((file_name, current_chapter))

            # 한글(한자) 및 한자 패턴을 제거한 나머지 텍스트에 대해 형태소 분석
            line_cleaned = hanja_hangul_pattern.sub('', line)
            line_cleaned = hanja_only_pattern.sub('', line)
            nouns = m.nouns(line_cleaned)
            
            # 2글자 이상인 명사만 필터링하여 저장
            for noun in nouns:
                if len(noun) >= 2:
                    if noun not in word_info:
                        word_info[noun] = {'count': 0, 'locations': []}
                    word_info[noun]['count'] += 1
                    word_info[noun]['locations'].append((file_name, current_chapter))

# '課體'가 등장한 챕터를 찾습니다.
if '정단' in word_info:
    koyi_chapters = word_info['課體']['locations']
else:
    koyi_chapters = []

# '課體'가 챕터별로 2번 이상 등장하는 경우를 출력합니다.
chapter_counts = {}
for location in koyi_chapters:
    file_name, chapter = location
    if chapter not in chapter_counts:
        chapter_counts[chapter] = {'count': 0, 'files': set()}
    chapter_counts[chapter]['count'] += 1
    chapter_counts[chapter]['files'].add(file_name)

# 결과를 출력 및 저장
with open('jikji_koyi_multiple.txt', 'w', encoding='utf-8') as result_file:
    for chapter, info in chapter_counts.items():
        if info['count'] >= 2:
            files = ', '.join(info['files'])
            result_file.write(f"챕터: {chapter} (등장 횟수: {info['count']}회), 파일: {files}\n")

print("'課體'가 챕터별로 2번 이상 등장한 경우가 jikji_koyi_multiple.txt 파일에 저장되었습니다.")
