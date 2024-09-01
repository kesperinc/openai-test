import os
import re
from collections import defaultdict

class TextProcessor:
    def __init__(self, file_list=None):
        self.origin_dir = 'data/origin'
        self.normalized_dir = 'data/normalized'
        self.chapter_dir = 'data/chapters'
        self.unique_nouns_by_chapter = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'count': 0, 'chapters': set()})))

        # file_list가 주어지지 않은 경우 origin 디렉토리의 모든 텍스트 파일을 사용
        if file_list is None:
            self.file_list = [os.path.join(self.origin_dir, file) for file in os.listdir(self.origin_dir) if file.endswith('.txt')]
        else:
            self.file_list = file_list

    def preprocess_text(self):
        # 디렉토리가 없으면 생성
        os.makedirs(self.normalized_dir, exist_ok=True)
        os.makedirs(self.chapter_dir, exist_ok=True)

        number_pattern = re.compile(r'[0-9①②③④⑤⑥⑦⑧⑨⑩]+')
        hanja_hangul_pattern = re.compile(r'(\w+)\([一-龥]+\)')
        hanja_only_pattern = re.compile(r'[一-龥]{2,}')
        chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日)\s*第[一二三四五六七八九十百千]+局')

        for file_name in self.file_list:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
            except FileNotFoundError:
                print(f"Error: File {file_name} not found.")
                continue
            except IOError:
                print(f"Error: Cannot read file {file_name}.")
                continue

            # 정규화 과정
            normalized_content = number_pattern.sub('', content)
            normalized_content = hanja_hangul_pattern.sub('', normalized_content)
            normalized_content = hanja_only_pattern.sub('', normalized_content)

            # 정규화된 내용을 normalized 디렉토리에 저장
            normalized_file_path = os.path.join(self.normalized_dir, os.path.basename(file_name))
            with open(normalized_file_path, 'w', encoding='utf-8') as normalized_file:
                normalized_file.write(normalized_content)

            # 각 챕터별로 텍스트 파일 생성
            self._create_chapter_files(content, chapter_pattern, file_name)

    def _create_chapter_files(self, content, chapter_pattern, original_file_name):
        lines = content.splitlines()
        current_chapter = None
        chapter_content = []

        for line in lines:
            chapter_match = chapter_pattern.search(line)
            if chapter_match:
                if current_chapter:
                    # 이전 챕터의 내용 저장
                    self._save_chapter_file(current_chapter, chapter_content, original_file_name)

                # 새로운 챕터 시작
                current_chapter = chapter_match.group()
                chapter_content = [line]  # 현재 챕터 이름부터 포함
            else:
                # 챕터 내용에 라인 추가
                chapter_content.append(line)

        # 마지막 챕터 내용 저장
        if current_chapter:
            self._save_chapter_file(current_chapter, chapter_content, original_file_name)

    def _save_chapter_file(self, chapter, content_lines, original_file_name):
        # 파일명/챕터명 디렉토리 생성
        chapter_file_dir = os.path.join(self.chapter_dir, os.path.basename(original_file_name).replace('.txt', ''))
        os.makedirs(chapter_file_dir, exist_ok=True)

        # 챕터 내용 저장
        chapter_file_path = os.path.join(chapter_file_dir, f"{chapter}.txt")
        with open(chapter_file_path, 'w', encoding='utf-8') as chapter_file:
            chapter_file.write('\n'.join(content_lines))
