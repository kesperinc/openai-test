import re
from konlpy.tag import Mecab

# Mecab 객체 생성
m = Mecab()

# 처리할 파일들의 리스트를 가져옴
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 중복을 제거하기 위해 명사들을 저장할 집합(set) 생성
unique_nouns = set()
unique_nouns_4char = set()

# 한자 및 한글 패턴에 매칭되는 단어를 추출하기 위한 정규 표현식
# 예: '빈주불투형재상(漢字)' 형식의 문자열
hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)')

# 각 파일을 읽고 명사를 추출하여 집합에 추가
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read().strip()

        # 한자와 매칭되는 한글 패턴을 먼저 추출하여 저장
        matches = hanja_hangul_pattern.findall(content)
        for match in matches:
            unique_nouns.add(match)
            if len(match) >= 4:
                unique_nouns_4char.add(match)
        
        # 한자 및 한글 패턴을 제거한 나머지 텍스트에 대해 형태소 분석
        content = hanja_hangul_pattern.sub('', content)
        nouns = m.nouns(content)
        
        # 2글자 이상인 명사 필터링
        for noun in nouns:
            if len(noun) >= 2:
                unique_nouns.add(noun)
            if len(noun) >= 4:
                unique_nouns_4char.add(noun)

# 집합을 리스트로 변환하고 사전순으로 정렬
sorted_nouns = sorted(unique_nouns)
sorted_nouns_4char = sorted(unique_nouns_4char)

# 2글자 이상의 명사를 jikji.txt 파일에 저장
with open('jikji.txt', 'w', encoding='utf-8') as result_file:
    result_file.write('\n'.join(sorted_nouns))

# 4글자 이상의 명사를 jikji_2char.txt 파일에 저장
with open('jikji_2char.txt', 'w', encoding='utf-8') as result_4char_file:
    result_4char_file.write('\n'.join(sorted_nouns_4char))

print("모든 파일에서 중복되지 않는 2글자 이상의 명사는 jikji.txt에 저장되었습니다.")
print("모든 파일에서 중복되지 않는 4글자 이상의 명사는 jikji_2char.txt에 저장되었습니다.")
