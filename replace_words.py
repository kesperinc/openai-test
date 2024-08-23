import re

# 처리할 파일들의 리스트
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 변경할 패턴과 그 대체 텍스트를 정의
replacements = {
    r'해석:': '解曰:',
    r'해설:': '解曰:',
    r'정단:': '斷曰:'
}

# 각 파일을 처리
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # 정의된 패턴을 순차적으로 변경
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    # 변경된 내용을 동일한 파일에 다시 저장
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)

print("모든 파일에서 '해석:', '해설:'은 '解曰:'로, '정단:'은 '斷曰:'로 변경되었습니다.")
