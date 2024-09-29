import os
from konlpy.tag import Mecab, Okt, Komoran

# 형태소 분석기 초기화
mecab = Mecab()
okt = Okt()
komoran = Komoran()

# 디렉토리 목록
directories = ["1.갑자순", "2.갑술순", "3.갑신순", "4.갑오순", "5.갑진순", "6.갑인순"]

def extract_nouns_with_mecab(text):
    return mecab.nouns(text)

def extract_nouns_with_okt(text):
    return okt.nouns(text)

def extract_nouns_with_komoran(text):
    return komoran.nouns(text)

def process_files():
    for directory in directories:
        dir_path = os.path.join(os.getcwd(), directory)
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 명사 추출 및 중복 제거
                nouns_mecab = set(extract_nouns_with_mecab(content))
                nouns_okt = set(extract_nouns_with_okt(content))
                #nouns_komoran = set(extract_nouns_with_komoran(content))

                # 서로 존재하지 않는 단어 추출
                extra_mecab = nouns_mecab - nouns_okt
                extra_okt = nouns_okt - nouns_mecab

                # 결과 파일 생성
                save_nouns_to_file(nouns_mecab, dir_path, file_name, "mecab")
                save_nouns_to_file(nouns_okt, dir_path, file_name, "okt")
                #save_nouns_to_file(nouns_komoran, dir_path, file_name, "komoran")

                # 서로 존재하지 않는 단어 저장
                save_nouns_to_file(extra_mecab, dir_path, file_name, "mecab_extra")
                save_nouns_to_file(extra_okt, dir_path, file_name, "okt_extra")

def save_nouns_to_file(nouns, dir_path, original_file_name, analyzer_name):
    base_name = os.path.splitext(original_file_name)[0]
    output_file_name = f"{base_name}_{analyzer_name}_명사.txt"
    output_file_path = os.path.join(dir_path, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for noun in sorted(nouns):  # 정렬된 형태로 저장
            output_file.write(noun + "\n")

if __name__ == "__main__":
    process_files()
    print("명사 추출이 완료되었습니다.")
