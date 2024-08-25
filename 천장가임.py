def get_user_input():
    """
    사용자로부터 연, 월, 일, 시, 월장을 입력받는 함수.
    """
    # 한글 -> 한자 매핑 사전
    korean_to_chinese = {
        '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊', '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸',
        '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰', '사': '巳', '오': '午', '미': '未', '신': '申', '유': '酉', '술': '戌', '해': '亥'
    }

    # 사용자가 연, 월, 일, 시를 입력하는 형식
    user_input = input("연월일시를 입력하세요 (예: 갑진년 임신월 오장 신유일 진시): ").strip()

    # 입력된 문자열을 공백으로 분리하여 각 요소 추출
    year, month, month_zang_input, day, hour = user_input.split()

    # 연, 월, 일, 시의 천간과 지지를 한자로 변환
    year_gan = korean_to_chinese.get(year[0], year[0])
    year_zhi = korean_to_chinese.get(year[1], year[1])
    month_gan = korean_to_chinese.get(month[0], month[0])
    month_zhi = korean_to_chinese.get(month[1], month[1])
    day_gan = '辛' if day[0] == '신' else korean_to_chinese.get(day[0], day[0])  # 천간 '신'은 항상 '辛'
    day_zhi = korean_to_chinese.get(day[1], day[1])
    hour_zhi = korean_to_chinese.get(hour[0], hour[0])

    # 월장에서 월장의 지지를 추출
    month_zang = korean_to_chinese.get(month_zang_input[0], month_zang_input[0])  # 월장의 첫 글자

    # 변환된 연, 월, 일, 시 출력
    print(f"변환된 입력: {year_gan}{year_zhi}년 {month_gan}{month_zhi}월 {month_zang}장 {day_gan}{day_zhi}일 {hour_zhi}시")
    
    return year_gan, year_zhi, month_gan, month_zhi, month_zang, day_gan, day_zhi, hour_zhi

def create_month_zang_sequence(start_month_zang):
    """
    입력받은 월장을 시작으로 12개의 월장 순서를 생성하는 함수.
    """
    # 12지지 리스트를 한자로 정의
    zhi_list = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 시작 월장의 인덱스 찾기
    start_index = zhi_list.index(start_month_zang)
    
    # 월장 순서 생성
    month_zang_sequence = []
    for i in range(12):
        current_index = (start_index + i) % 12
        month_zang_sequence.append(zhi_list[current_index])
    
    return month_zang_sequence

def create_tianjiang_sequence():
    """
    천장 순서를 생성하는 함수.
    """
    # 12천장 리스트와 이름 정의
    tianjiang_list = ['貴', '匕', '朱', '合', '勾', '靑', '空', '白', '常', '玄', '陰', '后']
    tianjiang_names = ['귀인', '등사', '주작', '육합', '구진', '청룡', '천공', '백호', '태상', '현무', '태음', '천후']
    
    return tianjiang_list, tianjiang_names

def find_tianjiang_start_index(day_gan, hour_zhi):
    """
    천간과 점시를 기반으로 천장의 시작 인덱스를 찾는 함수.
    """
    # 천간에 따른 지반 시작 위치
    tianjiang_start_positions = {
        '甲': ('丑', '未'), '戊': ('丑', '未'), '庚': ('丑', '未'),
        '乙': ('子', '申'), '己': ('子', '申'),
        '丙': ('亥', '酉'), '丁': ('亥', '酉'),
        '壬': ('巳', '卯'), '癸': ('巳', '卯'),
        '辛': ('午', '寅')
    }
    
    # 지반에 따른 천장의 방향 설정
    if hour_zhi in ['卯', '辰', '巳', '午', '未', '申']:
        index = 0  # 앞의 지반을 사용
    else:
        index = 1  # 뒤의 지반을 사용
    
    # 시작 인덱스 반환
    return tianjiang_start_positions[day_gan][index]

def place_tianjiang(grid, start_zhi, tianjiang_list):
    """
    천반에서 시작 인덱스와 같은 글자를 찾아서 천장을 배치하는 함수.
    """
    # 천반의 위치 설정
    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (0, 0), '午': (0, 1), '未': (0, 2), '申': (0, 3),
                      '酉': (1, 3), '戌': (2, 3), '亥': (3, 3), '子': (3, 2),
                      '丑': (3, 1), '寅': (3, 0), '卯': (2, 0), '辰': (1, 0)}

    # 시작 인덱스 찾기
    start_index = tianpan_positions.index(start_zhi)
    
    # 지반이 '亥', '子', '丑', '寅', '卯', '辰'에 있는 경우와 아닌 경우의 배치 방식
    reverse_order = start_zhi in ['巳', '午', '未', '申', '酉', '戌']
    
    # 천장 배치
    if reverse_order:
        for i in range(12):
            pos_index = (start_index - i) % 12
            x, y = tianpan_coords[tianpan_positions[pos_index]]
            grid[x][y] = tianjiang_list[i]
    else:
        for i in range(12):
            pos_index = (start_index + i) % 12
            x, y = tianpan_coords[tianpan_positions[pos_index]]
            grid[x][y] = tianjiang_list[i]

def create_6x6_tianpan_and_diban(month_zang_sequence, divination_hour):
    """
    6x6 그리드에 천반과 지반을 배치하여 출력하는 함수.
    """
    # 6x6 천반 배열 초기화
    tianpan_grid = [
        ['  ', '巳', '午', '未', '申', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['辰', '  ', '  ', '  ', '  ', '酉'],
        ['卯', '  ', '  ', '  ', '  ', '戌'],
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '寅', '丑', '子', '亥', '  ']
    ]
    
    # 고정된 지반 배치 리스트 (4x4 중앙 그리드)
    diban_grid = [
        ['巳', '午', '未', '申'],
        ['辰', '  ', '  ', '酉'],
        ['卯', '  ', '  ', '戌'],
        ['寅', '丑', '子', '亥']
    ]
    
    # 천반과 지반을 결합한 6x6 배열 초기화
    combined_grid = [['  ' for _ in range(6)] for _ in range(6)]
    
    # 천반 그리드 설정 (바깥쪽 테두리만 설정)
    for i in range(6):
        for j in range(6):
            if tianpan_grid[i][j].strip():
                combined_grid[i][j] = tianpan_grid[i][j]

    # 지반 그리드 설정 (4x4 중앙 고정 배치)
    for i in range(4):
        for j in range(4):
            if diban_grid[i][j].strip():
                combined_grid[i + 1][j + 1] = diban_grid[i][j]

    # 천반의 위치 설정
    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (0, 1), '午': (0, 2), '未': (0, 3), '申': (0, 4),
                      '酉': (2, 5), '戌': (3, 5), '亥': (5, 4), '子': (5, 3),
                      '丑': (5, 2), '寅': (5, 1), '卯': (3, 0), '辰': (2, 0)}

    # 점시의 위치에서부터 월장 순서를 배열
    start_index = tianpan_positions.index(divination_hour)
    for i in range(12):
        pos_index = (start_index + i) % 12
        x, y = tianpan_coords[tianpan_positions[pos_index]]
        combined_grid[x][y] = month_zang_sequence[i]

    # 6x6 그리드 출력
    print("\n6x6 천반과 지반이 결합된 배열:")
    for row in combined_grid:
        print(' '.join(row))

def create_6x6_tianpan_and_tianjiang(month_zang_sequence, divination_hour, day_gan, tianjiang_list):
    """
    6x6 그리드에 천반과 천장을 배치하여 출력하는 함수.
    """
    # 6x6 천반 배열 초기화
    tianpan_grid = [
        ['  ', '巳', '午', '未', '申', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['辰', '  ', '  ', '  ', '  ', '酉'],
        ['卯', '  ', '  ', '  ', '  ', '戌'],
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '寅', '丑', '子', '亥', '  ']
    ]
    
    # 6x6 천반 배열 초기화
    combined_grid = [['  ' for _ in range(6)] for _ in range(6)]

    # 천반 그리드 설정 (바깥쪽 테두리만 설정)
    for i in range(6):
        for j in range(6):
            if tianpan_grid[i][j].strip():
                combined_grid[i][j] = tianpan_grid[i][j]

    # 천반의 위치 설정
    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (0, 1), '午': (0, 2), '未': (0, 3), '申': (0, 4),
                      '酉': (2, 5), '戌': (3, 5), '亥': (5, 4), '子': (5, 3),
                      '丑': (5, 2), '寅': (5, 1), '卯': (3, 0), '辰': (2, 0)}

    # 점시의 위치에서부터 월장 순서를 배열
    start_index = tianpan_positions.index(divination_hour)
    for i in range(12):
        pos_index = (start_index + i) % 12
        x, y = tianpan_coords[tianpan_positions[pos_index]]
        combined_grid[x][y] = month_zang_sequence[i]

    # 천장의 시작 인덱스 찾기
    tianjiang_start_zhi = find_tianjiang_start_index(day_gan, divination_hour)
    
    # 천장을 결합하여 6x6 배열에 배치
    place_tianjiang(combined_grid, tianjiang_start_zhi, tianjiang_list)

    # 6x6 그리드 출력
    print("\n6x6 천반 및 천장이 결합된 배열:")
    for row in combined_grid:
        print(' '.join(row))

def create_4x4_tianpan(month_zang_sequence, divination_hour):
    """
    4x4 그리드에 천반만 배치하여 출력하는 함수.
    """
    # 4x4 천반 배열 초기화
    tianpan_grid = [['  ' for _ in range(4)] for _ in range(4)]

    # 천반의 위치 설정
    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (0, 0), '午': (0, 1), '未': (0, 2), '申': (0, 3),
                      '酉': (1, 3), '戌': (2, 3), '亥': (3, 3), '子': (3, 2),
                      '丑': (3, 1), '寅': (3, 0), '卯': (2, 0), '辰': (1, 0)}

    # 점시의 위치에서부터 월장 순서를 배열
    start_index = tianpan_positions.index(divination_hour)
    for i in range(12):
        pos_index = (start_index + i) % 12
        x, y = tianpan_coords[tianpan_positions[pos_index]]
        tianpan_grid[x][y] = month_zang_sequence[i]

    # 4x4 그리드 출력
    print("\n4x4 천반 배열:")
    for row in tianpan_grid:
        print(' '.join(row))

def create_4x4_tianjiang(day_gan, divination_hour, tianjiang_list):
    """
    4x4 그리드에 천장만 배치하여 출력하는 함수.
    """
    # 4x4 천장 배열 초기화
    tianjiang_grid = [['  ' for _ in range(4)] for _ in range(4)]

    # 천반의 위치 설정
    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (0, 0), '午': (0, 1), '未': (0, 2), '申': (0, 3),
                      '酉': (1, 3), '戌': (2, 3), '亥': (3, 3), '子': (3, 2),
                      '丑': (3, 1), '寅': (3, 0), '卯': (2, 0), '辰': (1, 0)}

    # 천장의 시작 인덱스 찾기
    tianjiang_start_zhi = find_tianjiang_start_index(day_gan, divination_hour)

    # 천장을 결합하여 4x4 배열에 배치
    place_tianjiang(tianjiang_grid, tianjiang_start_zhi, tianjiang_list)

    # 4x4 그리드 출력
    print("\n4x4 천장 배열:")
    for row in tianjiang_grid:
        print(' '.join(row))

def main():
    # 사용자로부터 연, 월, 일, 시, 월장 입력받기
    year_gan, year_zhi, month_gan, month_zhi, month_zang, day_gan, day_zhi, divination_hour = get_user_input()
    
    # 입력된 월장으로부터 12개의 월장 순서 생성
    month_zang_sequence = create_month_zang_sequence(month_zang)

    # 천장 순서 생성
    tianjiang_list, _ = create_tianjiang_sequence()

    # 6x6 천반과 지반이 결합된 텍스트 그리드 출력
    create_6x6_tianpan_and_diban(month_zang_sequence, divination_hour)

    # 6x6 천반 및 천장 배열 출력
    create_6x6_tianpan_and_tianjiang(month_zang_sequence, divination_hour, day_gan, tianjiang_list)

    # 4x4 천반 배열 출력
    create_4x4_tianpan(month_zang_sequence, divination_hour)

    # 4x4 천장 배열 출력
    create_4x4_tianjiang(day_gan, divination_hour, tianjiang_list)

# 프로그램 실행
if __name__ == "__main__":
    main()
