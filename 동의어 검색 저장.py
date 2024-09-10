import re
from konlpy.tag import Mecab
from collections import defaultdict
from nltk.corpus import wordnet as wn
import os

# Mecab 객체 생성
mecab = Mecab()

# 처리할 파일 리스트
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 2글자 단어 저장을 위한 딕셔너리
unique_nouns_2char = defaultdict(lambda: {'count': 0, 'chapters': set()})

# 숫자 및 원숫자 제거를 위한 정규 표현식
number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日)\s*第[一二三四五六七八九十百千]+局')

# 동의어 파일을 저장할 경로 설정
synonym_output_file = '2char_synonyms.txt'

# 각 파일을 읽고 2글자 명사를 추출하여 딕셔너리에 추가
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read().strip()

        # 파일의 현재 챕터를 추적하기 위한 변수
        current_chapter = None

        # 숫자 제거
        content = number_pattern.sub('', content)

        # 챕터를 찾기
        lines = content.splitlines()
        for line in lines:
            chapter_match = chapter_pattern.search(line)
            if chapter_match:
                current_chapter = chapter_match.group()

            # 한자 및 한글 패턴을 제거한 나머지 텍스트에 대해 형태소 분석
            nouns = mecab.nouns(line)

            # 2글자 명사 필터링
            for noun in nouns:
                if len(noun) == 2:
                    unique_nouns_2char[noun]['count'] += 1
                    if current_chapter:
                        unique_nouns_2char[noun]['chapters'].add(current_chapter)

# WordNet과 OMW를 사용한 동의어 찾기
def get_wordnet_synonyms(word):
    """WordNet을 사용하여 동의어 목록을 반환"""
    synonyms = []
    synsets = wn.synsets(word, lang='kor')  # 한국어로 동의어를 찾음
    for synset in synsets:
        for lemma in synset.lemmas(lang='kor'):
            synonyms.append(lemma.name())
    return set(synonyms)

# 동의어 찾기 및 파일에 저장
with open(synonym_output_file, 'w', encoding='utf-8') as synonym_file:
    for noun, info in unique_nouns_2char.items():
        synonyms = get_wordnet_synonyms(noun)
        if synonyms:
            synonyms_str = ', '.join(synonyms)
            synonym_file.write(f"{noun}: {synonyms_str}\n")

# 결과 출력
print(f"2글자 단어의 동의어가 {synonym_output_file} 파일에 저장되었습니다.")
