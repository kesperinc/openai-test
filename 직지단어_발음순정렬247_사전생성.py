import re
from konlpy.tag import Mecab, Okt, Komoran
from collections import defaultdict
from jamo import h2j, j2hcj
import os

# Mecab, Okt, Komoran 객체 생성
mecab = Mecab()
okt = Okt()
komoran = Komoran()

# 처리할 파일들의 리스트를 가져옴
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 단어 저장을 위한 딕셔너리 생성 (등장 횟수와 챕터를 함께 저장)
unique_nouns_2char = defaultdict(lambda: {'count': 0, 'chapters': set()})
unique_nouns_3to4char = defaultdict(lambda: {'count': 0, 'chapters': set()})
unique_nouns_5to6char = defaultdict(lambda: {'count': 0, 'chapters': set()})

# 7글자 이상의 한자 저장을 위한 딕셔너리 (등장 횟수와 챕터를 함께 저장)
hanja_7char_info = defaultdict(lambda: {'count': 0, 'chapters': set()})

# 숫자 및 원숫자 제거를 위한 정규 표현식
number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')

# 한글(한자), 한자만 있는 경우를 처리하기 위한 정규 표현식
hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)')
hanja_only_pattern = re.compile(r'[一-龥]{2,}')  # 한자만 두 글자 이상 있는 경우 매칭

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日)\s*第[一二三四五六七八九十百千]+局')

# 제외할 7글자 이상의 한자 목록 (제공된 텍스트 내용)
exclude_list = {
    "乙戊己辛壬五日", "已災凶逃反無疑", "游都合處喜降卒", "戌亥子丑寅卯辰",
    "不動人情有怨心", "常占須主身搖動", "往復雙雙兩事因", "反吟占事休言定",
    "傳課皆空事莫追", "鬼來又向病中居", "惟有庚日不宜見", "求財謀望始圖維",
    "顧祖迎親復舊廬", "蛇虎疾病朱官方", "三刑六害同傳日", "變剋翻爲兩面非",
    "龍陰后合可迍藏", "除定開危卯未方", "死囚刑剋便災臨", "旺相相生灾未發",
    "時不利兮遁悶之", "亥酉未兮報君知", "君子待時方可吉", "小人病患且防危",
    "閉口凡占莫測機", "陰陽間剋傳藏課", "縱然帶惡不成嗔", "上下喜忻三六合",
    "旺體分處災祥別", "財休財旺因時斷", "三六相呼聲相應", "上下喜忻三六合",
    "三六相呼見喜忻", "東方朔射覆無移集"
}

# 각 파일을 읽고 명사를 추출하여 딕셔너리에 추가
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read().strip()

        # 파일의 현재 챕터를 추적하기 위한 변수
        current_chapter = None

        # 숫자 및 원숫자를 제거
        content = number_pattern.sub('', content)

        # 챕터를 찾기
        lines = content.splitlines()
        for line in lines:
            chapter_match = chapter_pattern.search(line)
            if chapter_match:
                current_chapter = chapter_match.group()

            # 한글(한자) 및 한자 패턴을 추출하여 저장
            matches = hanja_hangul_pattern.findall(line)
            for match in matches:
                if len(match) <= 2:
                    unique_nouns_2char[match]['count'] += 1
                    if current_chapter:
                        unique_nouns_2char[match]['chapters'].add(current_chapter)
                elif 3 <= len(match) <= 4:
                    unique_nouns_3to4char[match]['count'] += 1
                    if current_chapter:
                        unique_nouns_3to4char[match]['chapters'].add(current_chapter)
                elif 5 <= len(match) <= 6:
                    unique_nouns_5to6char[match]['count'] += 1
                    if current_chapter:
                        unique_nouns_5to6char[match]['chapters'].add(current_chapter)

            # 한자만 있는 경우를 추출하여 저장
            matches_hanja_only = hanja_only_pattern.findall(line)
            for match in matches_hanja_only:
                if len(match) <= 2:
                    unique_nouns_2char[match]['count'] += 1
                    if current_chapter:
                        unique_nouns_2char[match]['chapters'].add(current_chapter)
                elif 3 <= len(match) <= 4:
                    unique_nouns_3to4char[match]['count'] += 1
                    if current_chapter:
                        unique_nouns_3to4char[match]['chapters'].add(current_chapter)
                elif 5 <= len(match) <= 6:
                    unique_nouns_5to6char[match]['count'] += 1
                    if current_chapter:
                        unique_nouns_5to6char[match]['chapters'].add(current_chapter)
                elif len(match) >= 7 and match not in exclude_list:
                    hanja_7char_info[match]['count'] += 1
                    if current_chapter:
                        hanja_7char_info[match]['chapters'].add(current_chapter)

            # 한자 및 한글 패턴을 제거한 나머지 텍스트에 대해 형태소 분석
            line_cleaned = hanja_hangul_pattern.sub('', line)
            line_cleaned = hanja_only_pattern.sub('', line)
            nouns = mecab.nouns(line_cleaned)

            # 2글자 이상인 명사 필터링
            for noun in nouns:
                if len(noun) <= 2:
                    unique_nouns_2char[noun]['count'] += 1
                    if current_chapter:
                        unique_nouns_2char[noun]['chapters'].add(current_chapter)
                elif 3 <= len(noun) <= 4:
                    unique_nouns_3to4char[noun]['count'] += 1
                    if current_chapter:
                        unique_nouns_3to4char[noun]['chapters'].add(current_chapter)
                elif 5 <= len(noun) <= 6:
                    unique_nouns_5to6char[noun]['count'] += 1
                    if current_chapter:
                        unique_nouns_5to6char[noun]['chapters'].add(current_chapter)

# 발음에 따라 정렬하기 위한 헬퍼 함수
def pronunciation_key(word):
    return j2hcj(h2j(word))

# 사용자 사전을 위한 단어 목록 생성
mecab_user_dict = []
okt_user_dict = []
komoran_user_dict = []

def check_word_in_mecab(word):
    """Mecab 사전에 단어가 있는지 확인"""
    return len(mecab.pos(word)) == 1 and mecab.pos(word)[0][0] == word

def check_word_in_okt(word):
    """Okt 사전에 단어가 있는지 확인"""
    tokens = okt.pos(word)
    return len(tokens) == 1 and tokens[0][0] == word

def check_word_in_komoran(word):
    """Komoran 사전에 단어가 있는지 확인"""
    tokens = komoran.pos(word)
    return len(tokens) == 1 and tokens[0][0] == word

# 단어를 사용자 사전으로 추가할지 여부를 체크
def add_to_user_dict(word):
    if not check_word_in_mecab(word):
        mecab_user_dict.append(word)
    if not check_word_in_okt(word):
        okt_user_dict.append(word)
    if not check_word_in_komoran(word):
        komoran_user_dict.append(word)

# 모든 명사들에 대해 사전 존재 여부 확인
for word in unique_nouns_2char:
    add_to_user_dict(word)
for word in unique_nouns_3to4char:
    add_to_user_dict(word)
for word in unique_nouns_5to6char:
    add_to_user_dict(word)
for word in hanja_7char_info:
    add_to_user_dict(word)

# 사용자 사전을 dict 디렉토리에 저장
os.makedirs('dict', exist_ok=True)

# Mecab 사용자 사전 저장
with open('dict/mecab_user_dict.csv', 'w', encoding='utf-8') as mecab_file:
    for word in mecab_user_dict:
        mecab_file.write(f"{word},NNP,*,F,{word},*,*,*,*\n")

# Okt 사용자 사전 저장 (리스트 형태)
with open('dict/okt_user_dict.txt', 'w', encoding='utf-8') as okt_file:
    for word in okt_user_dict:
        okt_file.write(f"{word}\n")

# Komoran 사용자 사전 저장
with open('dict/komoran_user_dict.txt', 'w', encoding='utf-8') as komoran_file:
    for word in komoran_user_dict:
        komoran_file.write(f"{word}\tNNP\n")

# 파일에 단어 저장
def save_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for noun, info in data:
            chapters = ', '.join(sorted(info['chapters']))
            file.write(f"{noun}: {info['count']}회 등장, 간지 국수: {chapters}\n")

# 2글자 이하의 명사를 저장
sorted_2char = sorted(sorted(unique_nouns_2char.items(), key=lambda x: x[1]['count'], reverse=True), key=lambda x: (pronunciation_key(x[0]), x[0]))
save_to_file('jikji_2char.txt', sorted_2char)

# 3글자 이상 4글자 이하의 명사를 저장
sorted_3to4char = sorted(sorted(unique_nouns_3to4char.items(), key=lambda x: x[1]['count'], reverse=True), key=lambda x: (pronunciation_key(x[0]), x[0]))
save_to_file('jikji_4char.txt', sorted_3to4char)

# 5글자와 6글자의 명사를 저장
sorted_5to6char = sorted(sorted(unique_nouns_5to6char.items(), key=lambda x: x[1]['count'], reverse=True), key=lambda x: (pronunciation_key(x[0]), x[0]))
save_to_file('jikji_5to6char.txt', sorted_5to6char)

# 7글자 이상의 한자를 저장
sorted_hanja_7char = sorted(hanja_7char_info.items(), key=lambda x: x[1]['count'], reverse=True)
save_to_file('jikji_7char_hanja.txt', sorted_hanja_7char)

# 사용자 사전에 저장된 단어의 수를 출력
print(f"Mecab 사용자 사전에 저장된 단어 수: {len(mecab_user_dict)}")
print(f"Okt 사용자 사전에 저장된 단어 수: {len(okt_user_dict)}")
print(f"Komoran 사용자 사전에 저장된 단어 수: {len(komoran_user_dict)}")

print("모든 파일에서 중복되지 않는 2글자 이하의 명사는 jikji_2char.txt에 저장되었습니다.")
print("모든 파일에서 중복되지 않는 3글자 이상 4글자 이하의 명사는 jikji_4char.txt에 저장되었습니다.")
print("모든 파일에서 중복되지 않는 5글자와 6글자의 명사는 jikji_5to6char.txt에 저장되었습니다.")
print("모든 파일에서 중복되지 않는 7글자 이상의 한자는 jikji_7char_hanja.txt에 저장되었습니다.")
print("사용자 사전이 dict 디렉토리에 저장되었습니다.")
