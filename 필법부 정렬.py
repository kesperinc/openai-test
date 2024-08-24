# 정렬할 파일 이름과 결과를 저장할 파일 이름을 설정합니다.
input_file = 'jikji_필법부_국수.txt'
output_file = 'jikji_필법부_국수_정렬.txt'

# 파일에서 한자 구절을 읽어옵니다.
with open(input_file, 'r', encoding='utf-8') as file:
    hanja_phrases = file.readlines()

# 읽어온 구절을 정리합니다. (문자열 앞뒤의 공백을 제거)
hanja_phrases = [phrase.strip() for phrase in hanja_phrases]

# 한자 구절을 알파벳 순서로 정렬합니다.
sorted_hanja_phrases = sorted(hanja_phrases)

# 정렬된 구절을 새로운 파일에 저장합니다.
with open(output_file, 'w', encoding='utf-8') as file:
    for phrase in sorted_hanja_phrases:
        file.write(phrase + '\n')

print(f"정렬된 한자 구절이 '{output_file}' 파일에 저장되었습니다.")
