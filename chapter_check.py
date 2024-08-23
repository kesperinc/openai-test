import re

# 처리할 파일들의 리스트
file_list = ['1gapja.txt', '2gapsul.txt', '3gapsin.txt', '4gapo.txt', '5gapjin.txt', '6gapin.txt']

# 챕터 패턴: 간지+일 제X국 형태를 매칭
chapter_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]日)\s第([一二三四五六七八九十百千]+)局')

# 결과를 저장할 파일
with open('chapter_list.txt', 'w', encoding='utf-8') as output_file:
    # 각 파일을 읽고 챕터를 추출하여 출력
    for file_name in file_list:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        # 챕터를 추출
        chapters = chapter_pattern.findall(content)

        # 챕터를 간지별로 분류
        ganji_chapters = {}
        for ganji, guk in chapters:
            if ganji not in ganji_chapters:
                ganji_chapters[ganji] = []
            ganji_chapters[ganji].append(guk)

        # 결과를 파일에 저장
        output_file.write(f"파일명: {file_name}\n")
        for ganji, guks in ganji_chapters.items():
            output_file.write(f"  {ganji}:\n")
            for i, guk in enumerate(guks, start=1):
                output_file.write(f"    제{i}국: {ganji} 第{guk}局\n")

            # 간지별로 12개의 챕터가 있는지 확인
            if len(guks) != 12:
                output_file.write(f"    [경고] {ganji}에 포함된 챕터 수가 {len(guks)}개입니다. (12개가 아님)\n")
        output_file.write("\n")  # 각 파일의 결과를 구분하기 위해 줄바꿈 추가

print("모든 파일의 챕터 정보가 chapter_list.txt 파일에 저장되었습니다.")
