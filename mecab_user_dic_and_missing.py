import json
import csv
import os
import re

# JSON 파일이 저장된 디렉토리 경로
input_directory = 'std_kor_dic'

# Mecab 사용자 사전 파일 경로
output_file_path = 'mecab_user_dict.csv'

# Mecab 사전에 없는 단어를 저장할 파일 경로
missing_words_output_path = 'missing_mecab_words.csv'

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

# 한글과 한자 분리 및 한자 추가 함수
def extract_hanja(word):
    """한글 옆에 한자가 있으면 한자를 추출하고 반환"""
    hanja_pattern = re.compile(r'\((.*?)\)')  # 괄호 안에 있는 한자 추출
    match = hanja_pattern.search(word)
    
    if match:
        hanja = match.group(1)  # 한자 추출
        word = re.sub(hanja_pattern, '', word).strip()  # 한글만 남김
        return word, hanja
    return word, None

# Mecab 사전에 단어가 있는지 확인하는 함수
def is_in_mecab(word, mecab_words):
    """Mecab 사전에 단어가 있는지 확인"""
    return word in mecab_words

# JSON 파일을 읽고 Mecab 사전 포맷으로 변환하여 저장하는 함수
def convert_json_to_mecab_format(input_directory, output_file_path, missing_words_output_path):
    # Mecab 사전에 없는 단어 리스트
    missing_words = []

    # 기존 Mecab 사전에 등록된 단어 리스트 가져오기
    mecab_words = set()
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                mecab_words.add(row[0])

    # CSV 파일 열기 (쓰기 모드)
    with open(output_file_path, 'a', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
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

                        pos_info = item['word_info'].get('pos_info', [])
                        pos = pos_info[0].get('pos', '*') if pos_info else '*'  # 품사
                        
                        # '품사 없음'을 '*'로 처리
                        if pos == "품사 없음":
                            pos = '*'

                        pronunciation_info = item['word_info'].get('pronunciation_info', [])
                        pronunciation = pronunciation_info[0]['pronunciation'] if pronunciation_info else '*'  # 발음

                        # 한글과 한자 분리 및 추가
                        word, hanja = extract_hanja(word)

                        # Mecab 사전에 있는지 확인
                        if not is_in_mecab(word, mecab_words):
                            missing_words.append(word)
                            writer.writerow([word, pos, '*', '*', pronunciation, '*', '*', '*', '*'])
                            mecab_words.add(word)

                        # 한자가 있으면 한자도 사전에 추가
                        if hanja and not is_in_mecab(hanja, mecab_words):
                            missing_words.append(hanja)
                            writer.writerow([hanja, pos, '*', '*', pronunciation, '*', '*', '*', '*'])
                            mecab_words.add(hanja)

                        # word_type이 한자어일 경우 original_language에 있는 한자 추가
                        word_type = item['word_info'].get('word_type', '')
                        original_language = item['word_info'].get('origin', '')
                        if word_type == '한자어' and original_language:
                            original_language_clean = clean_word(normalize_text(original_language))
                            if not is_in_mecab(original_language_clean, mecab_words):
                                missing_words.append(original_language_clean)
                                writer.writerow([original_language_clean, pos, '*', '*', pronunciation, '*', '*', '*', '*'])
                                mecab_words.add(original_language_clean)

    # Mecab 사전에 없는 단어를 별도 파일로 저장
    with open(missing_words_output_path, 'w', encoding='utf-8', newline='') as missing_file:
        writer = csv.writer(missing_file)
        for word in missing_words:
            writer.writerow([word])

    print(f"Mecab 사용자 사전이 {output_file_path}에 저장되었습니다.")
    print(f"Mecab 사전에 없는 단어가 {missing_words_output_path}에 저장되었습니다.")

# 실행
convert_json_to_mecab_format(input_directory, output_file_path, missing_words_output_path)
