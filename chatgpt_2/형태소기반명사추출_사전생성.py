import os
from konlpy.tag import Mecab, Okt
from collections import defaultdict

# 형태소 분석기 초기화
mecab = Mecab()
okt = Okt()

# 디렉토리 목록
directories = ["1.갑자순", "2.갑술순", "3.갑신순", "4.갑오순", "5.갑진순", "6.갑인순"]

def extract_nouns_with_mecab(text):
    return mecab.nouns(text)

def extract_nouns_with_okt(text):
    return okt.nouns(text)

def process_files():
    for directory in directories:
        dir_path = os.path.join(os.getcwd(), directory)
        dir_nouns = set()

        for file_name in os.listdir(dir_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 명사 추출 및 중복 제거
                nouns_mecab = set(extract_nouns_with_mecab(content))
                nouns_okt = set(extract_nouns_with_okt(content))

                # Mecab와 Okt 명사의 합집합을 구함
                combined_nouns = nouns_mecab.union(nouns_okt)
                
                # 결과를 dict 파일로 저장
                save_nouns_to_dict(combined_nouns, dir_path, file_name, "dict")

                # 디렉토리 내 모든 명사 합집합 구하기
                dir_nouns.update(combined_nouns)

        # 디렉토리 내 모든 명사를 하나의 파일로 저장
        save_nouns_to_dict(dir_nouns, dir_path, f"{directory}_전체", "combined_dict")

def save_nouns_to_dict(nouns, dir_path, base_name, suffix):
    output_file_name = f"{base_name}_{suffix}.txt"
    output_file_path = os.path.join(dir_path, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for noun in sorted(nouns):  # 정렬된 형태로 저장
            output_file.write(noun + "\n")

if __name__ == "__main__":
    process_files()
    print("명사 추출과 dict 파일 생성이 완료되었습니다.")
