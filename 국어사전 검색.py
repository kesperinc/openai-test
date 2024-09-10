import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Mecab 사용자 사전 CSV 파일 경로
user_dict_path = 'dict/mecab_user_dict.csv'

# 출력 파일 경로
output_file_path = 'mecab_words_info_all.txt'

# 국립국어원 표준 대사전에서 단어를 검색하는 함수
def search_std_korean_dict(word):
    """국립국어원 표준국어대사전에서 단어 정보를 검색하는 함수"""
    url = f"https://stdict.korean.go.kr/search/searchResult.do?pageSize=10&searchKeyword={word}"
    
    # 웹 페이지 요청
    response = requests.get(url)
    response.raise_for_status()  # 에러 발생 시 예외 발생
    
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 검색 결과에서 첫 번째 항목 가져오기
    word_info = {}
    result = soup.find('div', class_='td_txt')
    if result:
        word_info['word'] = word
        definition = result.find('span', class_='definition').get_text(strip=True)
        word_info['definition'] = definition
    else:
        word_info['word'] = word
        word_info['definition'] = "정보를 찾을 수 없습니다."

    return word_info

# Mecab 사용자 사전 CSV 파일을 읽어서 한글 단어 목록을 가져오는 함수
def read_mecab_user_dict(file_path):
    """Mecab 사용자 사전 CSV 파일에서 한글 단어 목록을 읽어오는 함수"""
    df = pd.read_csv(file_path, header=None)
    words = df[0].tolist()  # 첫 번째 컬럼에서 단어만 가져옴
    
    # 한글만 필터링 (유니코드 한글 범위에 있는 문자만 통과)
    korean_words = [word for word in words if re.match("^[가-힣]+$", word)]
    return korean_words

# 결과를 파일로 저장하는 함수
def save_word_info_to_file(word_info, file_path):
    """단어 정보를 파일에 저장하는 함수"""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"단어: {word_info['word']}\n")
        file.write(f"뜻풀이: {word_info['definition']}\n")
        file.write("="*50 + "\n")

# 단어 검색 및 저장 작업을 진행하는 함수 (전체 한글 단어 처리)
def process_all_korean_words(user_dict_path, output_file_path):
    """Mecab 사용자 사전에 있는 한글 단어 전체를 표준 대사전에서 검색하고 파일에 저장하는 함수"""
    words = read_mecab_user_dict(user_dict_path)  # 한글 단어 전체를 가져옴
    
    for word in words:
        word_info = search_std_korean_dict(word)
        save_word_info_to_file(word_info, output_file_path)
        print(f"{word}에 대한 정보를 저장했습니다.")

# 실행
process_all_korean_words(user_dict_path, output_file_path)
print(f"모든 한글 단어에 대한 정보가 {output_file_path} 파일에 저장되었습니다.")
