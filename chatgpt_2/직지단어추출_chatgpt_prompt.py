import os
import re
from collections import defaultdict
from openai import OpenAI

client = OpenAI()

# 처리할 파일들의 리스트
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']
file_list = ['6gapin.txt']


# 명사 저장을 위한 딕셔너리 생성 (등장 횟수와 챕터를 함께 저장)
unique_nouns_2char = defaultdict(lambda: {'count': 0, 'chapters': set()})
unique_nouns_3to4char = defaultdict(lambda: {'count': 0, 'chapters': set()})
unique_nouns_5char = defaultdict(lambda: {'count': 0, 'chapters': set()})
hanja_7char_info = defaultdict(lambda: {'count': 0, 'chapters': set()})

# 숫자 및 원숫자 제거를 위한 정규 표현식
number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')

# 한글(한자), 한자만 있는 경우를 처리하기 위한 정규 표현식
hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)')
hanja_only_pattern = re.compile(r'[一-龥]{2,}')  # 한자만 두 글자 이상 있는 경우 매칭

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日)\s*第[一二三四五六七八九十百千]+局')

# 제외할 7글자 이상의 한자 목록
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

def extract_nouns_from_text(text):
    """ChatGPT API를 사용하여 텍스트에서 명사만 추출"""
    response = client.chat.completions.create(
        model="gpt-4o",  # 모델은 필요에 따라 조정
        messages=[
            {"role": "system", "content": "너는 지금부터 언어학에 관해 나에게 조언을 해주는 조력자로 행동해 줘. 한글과 한자에 대해 잘 알고 있고 아래 사용자의 질문에 답해 줘."},
            {"role": "user", "content": f"주어지는 텍스트에서 명사만 추출해 줘. 한글 한자가 섞여 있는 문자이지만, 빈칸으로 명사를 구분할 수 있을 거야. 한 글자 한글이나 한자는 제외하고, 주어진 텍스트에서 중요한 의미를 가진 단어와 문서에 등장하는 단어 중심으로 추출해 줘. 글자 수가 4글자 이상인 단어는 반드시 추출해 주고, 2 글자 이상의 단어만 추출해 줘. 단어는 번호를 붙이지 말고, 몇 개를 추출했는지 알려주고, 한 줄에 빈 칸으로 구분해서 출력해 줘. : {text}"}
        ]
    )    
    # API 응답에서 명사 추출
    nouns_string = response.choices[0].message.content.strip()
    # 추출된 명사를 리스트로 변환
    nouns = nouns_string.split(', ')
    return nouns

# 결과를 저장할 디렉토리
output_dir = 'chatgpt_2'
os.makedirs(output_dir, exist_ok=True)

# 각 파일을 읽고 명사를 추출하여 딕셔너리에 추가
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read().strip()

        # 파일의 현재 챕터를 추적하기 위한 변수
        current_chapter = None
        chapter_content = []

        # 숫자 및 원숫자를 제거
        content = number_pattern.sub('', content)

        # 챕터를 찾기
        lines = content.splitlines()
        for line in lines:
            chapter_match = chapter_pattern.search(line)
            if chapter_match:
                # 이전 챕터에 대해 명사 추출 및 파일 저장
                if current_chapter:
                    chapter_text = "\n".join(chapter_content)
                    print(f"Extracting nouns for chapter: {current_chapter} in {file_name}")
                    nouns = extract_nouns_from_text(chapter_text)

                    # 명사 정보를 딕셔너리에 저장
                    for noun in nouns:
                        if len(noun) <= 2:
                            unique_nouns_2char[noun]['count'] += 1
                            unique_nouns_2char[noun]['chapters'].add(current_chapter)
                        elif 3 <= len(noun) <= 4:
                            unique_nouns_3to4char[noun]['count'] += 1
                            unique_nouns_3to4char[noun]['chapters'].add(current_chapter)
                        elif len(noun) >= 5:
                            unique_nouns_5char[noun]['count'] += 1
                            unique_nouns_5char[noun]['chapters'].add(current_chapter)

                    # 챕터별로 파일 저장
                    with open(os.path.join(output_dir, f"{os.path.basename(file_name)}_{current_chapter}.txt"), 'w', encoding='utf-8') as chapter_file:
                        chapter_file.write('\n'.join(nouns))
                    
                    print(f"Finished processing Chapter: {current_chapter}")

                # 새로운 챕터 시작
                current_chapter = chapter_match.group()
                chapter_content = [line]  # 현재 챕터의 첫 번째 줄을 추가
                print(f"Processing new Chapter: {current_chapter}")
            else:
                # 현재 챕터에 내용을 추가
                chapter_content.append(line)

        # 마지막 챕터 처리
        if current_chapter:
            chapter_text = "\n".join(chapter_content)
            print(f"Extracting nouns for chapter: {current_chapter} in {file_name}")
            nouns = extract_nouns_from_text(chapter_text)

            # 명사 정보를 딕셔너리에 저장
            for noun in nouns:
                if len(noun) <= 2:
                    unique_nouns_2char[noun]['count'] += 1
                    unique_nouns_2char[noun]['chapters'].add(current_chapter)
                elif 3 <= len(noun) <= 4:
                    unique_nouns_3to4char[noun]['count'] += 1
                    unique_nouns_3to4char[noun]['chapters'].add(current_chapter)
                elif len(noun) >= 5:
                    unique_nouns_5char[noun]['count'] += 1
                    unique_nouns_5char[noun]['chapters'].add(current_chapter)

            # 마지막 챕터별로 파일 저장
            with open(os.path.join(output_dir, f"{os.path.basename(file_name)}_{current_chapter}.txt"), 'w', encoding='utf-8') as chapter_file:
                chapter_file.write('\n'.join(nouns))
            
            print(f"Finished processing Chapter: {current_chapter}")

print("모든 파일에서 명사가 추출되어 chatgpt 디렉토리에 저장되었습니다.")
