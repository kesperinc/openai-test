import re
from konlpy.tag import Mecab, Okt, Komoran
from collections import defaultdict
from jamo import h2j, j2hcj
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TextProcessor:
    def __init__(self, file_list):
        self.file_list = file_list
        self.mecab = Mecab()
        self.okt = Okt()
        self.komoran = Komoran()
        self.unique_nouns_by_chapter = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'chapters': set()}))
        self.mecab_user_dict = []
        self.okt_user_dict = []
        self.komoran_user_dict = []
        self.mecab_existing_dict = []
        self.okt_existing_dict = []
        self.komoran_existing_dict = []

    def preprocess_text(self):
        number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')
        hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)')
        hanja_only_pattern = re.compile(r'[一-龥]{2,}')
        chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日)\s*第[一二三四五六七八九十百千]+局')
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

        for file_name in self.file_list:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read().strip()

                current_chapter = None
                content = number_pattern.sub('', content)

                lines = content.splitlines()
                for line in lines:
                    chapter_match = chapter_pattern.search(line)
                    if chapter_match:
                        current_chapter = chapter_match.group()
                    elif current_chapter is None:
                        current_chapter = '기본_챕터'  # 기본 챕터 설정

                    matches = hanja_hangul_pattern.findall(line)
                    for match in matches:
                        self._process_match(match, current_chapter)

                    matches_hanja_only = hanja_only_pattern.findall(line)
                    for match in matches_hanja_only:
                        self._process_hanja(match, current_chapter, exclude_list)

                    line_cleaned = hanja_hangul_pattern.sub('', line)
                    line_cleaned = hanja_only_pattern.sub('', line)
                    nouns = self.mecab.nouns(line_cleaned)
                    self._process_nouns(nouns, current_chapter)

        self._create_user_dicts()

    def _process_match(self, match, current_chapter):
        if len(match) <= 2:
            self.unique_nouns_by_chapter[current_chapter]['2char'][match]['count'] += 1
            self.unique_nouns_by_chapter[current_chapter]['2char'][match]['chapters'].add(current_chapter)
        elif 3 <= len(match) <= 4:
            self.unique_nouns_by_chapter[current_chapter]['3to4char'][match]['count'] += 1
            self.unique_nouns_by_chapter[current_chapter]['3to4char'][match]['chapters'].add(current_chapter)
        elif 5 <= len(match) <= 6:
            self.unique_nouns_by_chapter[current_chapter]['5to6char'][match]['count'] += 1
            self.unique_nouns_by_chapter[current_chapter]['5to6char'][match]['chapters'].add(current_chapter)

    def _process_hanja(self, match, current_chapter, exclude_list):
        if len(match) <= 2:
            self.unique_nouns_by_chapter[current_chapter]['2char'][match]['count'] += 1
            self.unique_nouns_by_chapter[current_chapter]['2char'][match]['chapters'].add(current_chapter)
        elif 3 <= len(match) <= 4:
            self.unique_nouns_by_chapter[current_chapter]['3to4char'][match]['count'] += 1
            self.unique_nouns_by_chapter[current_chapter]['3to4char'][match]['chapters'].add(current_chapter)
        elif 5 <= len(match) <= 6:
            self.unique_nouns_by_chapter[current_chapter]['5to6char'][match]['count'] += 1
            self.unique_nouns_by_chapter[current_chapter]['5to6char'][match]['chapters'].add(current_chapter)
        elif len(match) >= 7 and match not in exclude_list:
            self.unique_nouns_by_chapter[current_chapter]['7char'][match]['count'] += 1
            self.unique_nouns_by_chapter[current_chapter]['7char'][match]['chapters'].add(current_chapter)

    def _process_nouns(self, nouns, current_chapter):
        for noun in nouns:
            if len(noun) <= 2:
                self.unique_nouns_by_chapter[current_chapter]['2char'][noun]['count'] += 1
                self.unique_nouns_by_chapter[current_chapter]['2char'][noun]['chapters'].add(current_chapter)
            elif 3 <= len(noun) <= 4:
                self.unique_nouns_by_chapter[current_chapter]['3to4char'][noun]['count'] += 1
                self.unique_nouns_by_chapter[current_chapter]['3to4char'][noun]['chapters'].add(current_chapter)
            elif 5 <= len(noun) <= 6:
                self.unique_nouns_by_chapter[current_chapter]['5to6char'][noun]['count'] += 1
                self.unique_nouns_by_chapter[current_chapter]['5to6char'][noun]['chapters'].add(current_chapter)

    def _create_user_dicts(self):
        for chapter, categories in self.unique_nouns_by_chapter.items():
            for category, nouns in categories.items():
                for word in nouns:
                    if not self._check_word_in_mecab(word):
                        self.mecab_user_dict.append(word)
                    else:
                        self.mecab_existing_dict.append(word)

                    if not self._check_word_in_okt(word):
                        self.okt_user_dict.append(word)
                    else:
                        self.okt_existing_dict.append(word)

                    if not self._check_word_in_komoran(word):
                        self.komoran_user_dict.append(word)
                    else:
                        self.komoran_existing_dict.append(word)

    def _check_word_in_mecab(self, word):
        return len(self.mecab.pos(word)) == 1 and self.mecab.pos(word)[0][0] == word

    def _check_word_in_okt(self, word):
        tokens = self.okt.pos(word)
        return len(tokens) == 1 and tokens[0][0] == word

    def _check_word_in_komoran(self, word):
        tokens = self.komoran.pos(word)
        return len(tokens) == 1 and tokens[0][0] == word

    def save_user_dicts(self):
        os.makedirs('dict', exist_ok=True)
        with open('dict/mecab_user_dict.csv', 'w', encoding='utf-8') as mecab_file:
            for word in self.mecab_user_dict:
                mecab_file.write(f"{word},NNP,*,F,{word},*,*,*,*\n")

        with open('dict/okt_user_dict.txt', 'w', encoding='utf-8') as okt_file:
            for word in self.okt_user_dict:
                okt_file.write(f"{word}\n")

        with open('dict/komoran_user_dict.txt', 'w', encoding='utf-8') as komoran_file:
            for word in self.komoran_user_dict:
                komoran_file.write(f"{word}\tNNP\n")

        with open('dict/mecab_existing_dict.csv', 'w', encoding='utf-8') as mecab_existing_file:
            for word in self.mecab_existing_dict:
                mecab_existing_file.write(f"{word},NNP,*,F,{word},*,*,*,*\n")

        with open('dict/okt_existing_dict.txt', 'w', encoding='utf-8') as okt_existing_file:
            for word in self.okt_existing_dict:
                okt_existing_file.write(f"{word}\n")

        with open('dict/komoran_existing_dict.txt', 'w', encoding='utf-8') as komoran_existing_file:
            for word in self.komoran_existing_dict:
                komoran_existing_file.write(f"{word}\tNNP\n")

    def get_all_nouns_by_chapter(self):
        all_nouns_by_chapter = {}
        for chapter, categories in self.unique_nouns_by_chapter.items():
            all_nouns_by_chapter[chapter] = []
            for category, nouns in categories.items():
                all_nouns_by_chapter[chapter].extend(nouns.keys())
        return all_nouns_by_chapter

class TFIDFTrainer:
    def __init__(self, processor):
        self.processor = processor
        self.vectorizer = TfidfVectorizer(stop_words=None, min_df=1)
        self.tfidf_matrix = None
        self.feature_names = None
        self.chapters = []

    def train(self):
        # 각 챕터별 명사들을 하나의 문서로 처리하여 TF-IDF 계산
        nouns_by_chapter = self.processor.get_all_nouns_by_chapter()
        self.chapters = list(nouns_by_chapter.keys())
        sentences = [' '.join(nouns) for nouns in nouns_by_chapter.values()]

        if not sentences:
            print("No sentences found after preprocessing.")
            return

        self.tfidf_matrix = self.vectorizer.fit_transform(sentences)
        self.feature_names = self.vectorizer.get_feature_names_out()
        print(f"TF-IDF 매트릭스가 생성되었습니다. 크기: {self.tfidf_matrix.shape}")

    def find_similar_words(self, word, top_n=5):
        if word not in self.feature_names:
            print(f"단어 '{word}'가 TF-IDF 모델에 없습니다.")
            return []

        word_idx = self.vectorizer.vocabulary_.get(word)
        word_tfidf = self.tfidf_matrix[:, word_idx].T
        cosine_similarities = cosine_similarity(word_tfidf, self.tfidf_matrix).flatten()
        
        related_indices = cosine_similarities.argsort()[-(top_n + 1):-1][::-1]
        similar_chapters = [(self.chapters[idx], cosine_similarities[idx]) for idx in related_indices]
        
        return similar_chapters

# 파일 리스트 정의
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 텍스트 전처리 및 TF-IDF 모델 훈련
processor = TextProcessor(file_list)
processor.preprocess_text()
processor.save_processed_files()

tfidf_trainer = TFIDFTrainer(processor)
tfidf_trainer.train()

# 유사 단어 검색 반복
while True:
    input_word = input("유사 단어를 찾을 단어를 입력하세요 (종료하려면 'exit' 입력): ")
    if input_word.lower() == 'exit':
        break

    similar_chapters = tfidf_trainer.find_similar_words(input_word)

    if similar_chapters:
        print(f"단어 '{input_word}'와 관련된 챕터들:")
        for chapter, similarity in similar_chapters:
            print(f"챕터: {chapter}, 유사도: {similarity:.4f}")
    else:
        print(f"단어 '{input_word}'와 관련된 챕터를 찾을 수 없습니다.")
