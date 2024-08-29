import re
from konlpy.tag import Mecab
from collections import defaultdict
from jamo import h2j, j2hcj

# Mecab 객체 생성
m = Mecab()

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
            nouns = m.nouns(line_cleaned)

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

# 명사를 등장 횟수에 따라 내림차순으로 정렬
sorted_nouns_2char = sorted(unique_nouns_2char.items(), key=lambda x: x[1]['count'], reverse=True)
sorted_nouns_3to4char = sorted(unique_nouns_3to4char.items(), key=lambda x: x[1]['count'], reverse=True)
sorted_nouns_5to6char = sorted(unique_nouns_5to6char.items(), key=lambda x: x[1]['count'], reverse=True)
sorted_hanja_7char = sorted(hanja_7char_info.items(), key=lambda x: x[1]['count'], reverse=True)

# 발음에 따라 정렬하기 위한 헬퍼 함수
def pronunciation_key(word):
    return j2hcj(h2j(word))

# 2글자 이하의 명사를 jikji_2char.txt 파일에 저장
with open('jikji_2char.txt', 'w', encoding='utf-8') as result_2char_file:
    # 한자만 저장
    for noun, info in sorted(sorted_nouns_2char, key=lambda x: (pronunciation_key(x[0]), x[0])):
        if re.fullmatch(hanja_only_pattern, noun):
            chapters = ', '.join(sorted(info['chapters']))
            result_2char_file.write(f"{noun}: {info['count']}회 등장, 간지 국수: {chapters}\n")
    # 한글만 저장
    for noun, info in sorted(sorted_nouns_2char, key=lambda x: (pronunciation_key(x[0]), x[0])):
        if not re.fullmatch(hanja_only_pattern, noun):
            chapters = ', '.join(sorted(info['chapters']))
            result_2char_file.write(f"{noun}: {info['count']}회 등장, 간지 국수: {chapters}\n")

# 3글자 이상 4글자 이하의 명사를 jikji_4char.txt 파일에 저장
with open('jikji_4char.txt', 'w', encoding='utf-8') as result_4char_file:
    # 한자만 저장
    for noun, info in sorted(sorted_nouns_3to4char, key=lambda x: (pronunciation_key(x[0]), x[0])):
        if re.fullmatch(hanja_only_pattern, noun):
            chapters = ', '.join(sorted(info['chapters']))
            result_4char_file.write(f"{noun}: {info['count']}회 등장, 간지 국수: {chapters}\n")
    # 한글만 저장
    for noun, info in sorted(sorted_nouns_3to4char, key=lambda x: (pronunciation_key(x[0]), x[0])):
        if not re.fullmatch(hanja_only_pattern, noun):
            chapters = ', '.join(sorted(info['chapters']))
            result_4char_file.write(f"{noun}: {info['count']}회 등장, 간지 국수: {chapters}\n")

# 5글자와 6글자의 명사를 jikji_5to6char.txt 파일에 저장
with open('jikji_5to6char.txt', 'w', encoding='utf-8') as result_5to6char_file:
    # 한자만 저장
    for noun, info in sorted(sorted_nouns_5to6char, key=lambda x: (pronunciation_key(x[0]), x[0])):
        if re.fullmatch(hanja_only_pattern, noun):
            chapters = ', '.join(sorted(info['chapters']))
            result_5to6char_file.write(f"{noun}: {info['count']}회 등장, 간지 국수: {chapters}\n")
    # 한글만 저장
    for noun, info in sorted(sorted_nouns_5to6char, key=lambda x: (pronunciation_key(x[0]), x[0])):
        if not re.fullmatch(hanja_only_pattern, noun):
            chapters = ', '.join(sorted(info['chapters']))
            result_5to6char_file.write(f"{noun}: {info['count']}회 등장, 간지 국수: {chapters}\n")

# 7글자 이상의 한자를 jikji_7char_hanja.txt 파일에 저장
with open('jikji_7char_hanja.txt', 'w', encoding='utf-8') as result_7char_hanja_file:
    for hanja, info in sorted_hanja_7char:
        chapters = ', '.join(sorted(info['chapters']))
        result_7char_hanja_file.write(f"{hanja}: {info['count']}회 등장, 간지 국수: {chapters}\n")

print("모든 파일에서 중복되지 않는 2글자 이하의 명사는 jikji_2char.txt에 저장되었습니다.")
print("모든 파일에서 중복되지 않는 3글자 이상 4글자 이하의 명사는 jikji_4char.txt에 저장되었습니다.")
print("모든 파일에서 중복되지 않는 5글자와 6글자의 명사는 jikji_5to6char.txt에 저장되었습니다.")
print("모든 파일에서 중복되지 않는 7글자 이상의 한자는 jikji_7char_hanja.txt에 저장되었습니다.")
