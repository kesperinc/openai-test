
from konlpy.tag import Mecab
m = Mecab()
test_sentence = "어정육임직지 소담주해 갑자순"
print(m.morphs(test_sentence))

# gapin.txt 파일에서 문장 읽기
with open('1gapja.txt', 'r', encoding='utf-8') as file:
    test_sentence = file.read().strip()
#
# 형태소 분석 수행
#
#morphs = m.morphs(test_sentence) 전체 
morphs = m.nouns(test_sentence)

# 분석 결과를 result.txt 파일에 저장
with open('result_nouns.txt', 'w', encoding='utf-8') as file:
    file.write(' '.join(morphs))

print(f"형태소 분석 결과가 result_nouns.txt 파일에 저장되었습니다: {' '.join(morphs)}")
#
# 형태소 분석 수행 : 명사 추출 후 2글자 이상 추출 
#
# gapin.txt 파일에서 문장 읽기
with open('1gapja.txt', 'r', encoding='utf-8') as file:
    test_sentence = file.read().strip()
nouns = m.nouns(test_sentence)
# 2글자 이상인 명사만 필터링
filtered_nouns = [noun for noun in nouns if len(noun) >= 2]

# 분석 결과를 result.txt 파일에 저장
with open('result_nouns_2ch.txt', 'w', encoding='utf-8') as file:
    file.write(' '.join(filtered_nouns))

print(f"2글자 이상 글자만 형태소 분석 결과가 result_nouns_2ch.txt 파일에 저장되었습니다: {' '.join(filtered_nouns)}")
#
# 형태소 분석 수행 : 명사 추출 후 2글자 이상 추출 후 하나만 저장 
#
nouns = m.nouns(test_sentence)

# 2글자 이상인 명사만 필터링 : set은 중복을 허용하지 않음 
filtered_nouns = list(set([noun for noun in nouns if len(noun) >= 2]))

# 필터링된 명사를 사전순으로 정렬
filtered_nouns.sort()

# 분석 결과를 result.txt 파일에 저장
with open('result_nouns_2ch_u.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(filtered_nouns))

print(f"2글자 이상 글자만 형태소 분석 하여 사전만들기 결과가 result_nouns_2ch_u.txt 파일에 저장되었습니다: {' '.join(filtered_nouns)}")