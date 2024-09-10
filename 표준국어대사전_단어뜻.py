import json
import os
import re

# JSON 파일이 저장된 디렉토리 경로
input_directory = 'std_kor_dic'

# 단어 뜻을 저장할 파일 경로
output_file_path = '표준국어대사전_단어뜻.txt'

# 윈도우 파일 포맷 정규화 함수
def normalize_text(text):
    """윈도우 포맷의 텍스트를 UTF-8로 정규화하고 불필요한 공백을 제거"""
    return text.replace('\r\n', '\n').strip()

# 특수문자 제거 및 빈칸 추가 함수
def clean_word(word):
    """단어 전처리: 
    1. 맨 앞의 - 제거
    2. 단어 내 - 제거
    3. 단어 내 ^를 빈칸으로 대체
    4. 단어 내 ㆍ를 빈칸으로 대체
    5. 단어 끝에 붙은 일련 번호(01, 02 등) 제거
    6. 중간의 불필요한 빈칸 제거"""
    word = re.sub(r'^-', '', word)  # 맨 앞의 '-' 제거
    word = re.sub(r'-', '', word)  # 단어 내 '-' 제거
    word = re.sub(r'\^', ' ', word)  # '^'를 빈칸으로 대체
    word = re.sub(r'ㆍ', ' ', word)  # 'ㆍ'를 빈칸으로 대체
    word = re.sub(r'\d{2}$', '', word)  # 단어 끝에 붙은 2자리 숫자 제거
    word = re.sub(r'\s+', '', word)  # 중간의 불필요한 빈칸 제거
    return word

# JSON 파일을 읽고 단어와 뜻을 정리하여 저장하는 함수
def extract_words_and_definitions(input_directory, output_file_path):
    # 중복 단어 처리를 위한 딕셔너리
    word_definitions = {}

    # 디렉토리 내 모든 .json 파일 처리
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)

            # JSON 파일 열기
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

                # JSON 데이터에서 필요한 정보 추출
                for item in data['channel']['item']:
                    word = normalize_text(item['word_info'].get('word', ''))  # 단어 정규화
                    word = clean_word(word)  # 특수문자 및 일련 번호 제거

                    # original_language에서 한자 추출
                    original_language_info = item['word_info'].get('original_language_info', [])

                    # 한자가 있는 경우 처리
                    if original_language_info:
                        original_language = original_language_info[0].get('original_language', '')
                        word_with_hanja = f"{word}({original_language})" if original_language else word
                    else:
                        word_with_hanja = word  # 한자가 없는 경우는 단어 그대로 저장

                    # original_definition 추출
                    original_definition = item['word_info']['pos_info'][0]['comm_pattern_info'][0]['sense_info'][0].get('definition', '')

                    # 단어에 해당하는 정의가 이미 있을 경우 한자와 함께 추가
                    if word_with_hanja in word_definitions:
                        word_definitions[word_with_hanja].append(original_definition)
                    else:
                        word_definitions[word_with_hanja] = [original_definition]

    # 단어를 가나다 순으로 정렬
    sorted_words = sorted(word_definitions.items())

    # 결과 파일로 저장
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for word_with_hanja, definitions in sorted_words:
            for definition in definitions:
                output_file.write(f"{word_with_hanja}: {definition}\n")

    print(f"단어와 뜻이 {output_file_path}에 저장되었습니다.")

# 실행
extract_words_and_definitions(input_directory, output_file_path)
