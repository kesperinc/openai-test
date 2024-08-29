def get_user_input():
    """
    사용자로부터 연, 월, 일, 시, 월장을 입력받는 함수.
    """
    # 천간 한글 -> 한자 매핑 사전
    tiangan_korean_to_chinese = {
        '갑': '甲', '을': '乙', '병': '丙', '정': '丁', 
        '무': '戊', '기': '己', '경': '庚', '신': '辛', 
        '임': '壬', '계': '癸'
    }

    # 지지 한글 -> 한자 매핑 사전
    dizhi_korean_to_chinese = {
        '자': '子', '축': '丑', '인': '寅', '묘': '卯', 
        '진': '辰', '사': '巳', '오': '午', '미': '未', 
        '신': '申', '유': '酉', '술': '戌', '해': '亥'
    }

    # 사용자가 연, 월, 일, 시를 입력하는 형식
    user_input = input("연월일시를 입력하세요 (예: 갑진년 임신월 오장 신유일 진시): ").strip()

    # 입력된 문자열을 공백으로 분리하여 각 요소 추출
    parts = user_input.split()

    # 초기화
    year = month = month_zang_input = day = hour = None

    # 각 요소를 분석하여 연, 월, 일, 시, 월장을 식별
    for part in parts:
        if '년' in part:
            year = part
        elif '월' in part:
            month = part
        elif '장' in part:
            month_zang_input = part
        elif '일' in part:
            day = part
        elif '시' in part:
            hour = part

    # 연의 천간과 지지를 한자로 변환
    year_gan = tiangan_korean_to_chinese.get(year[0], year[0]) if year else ''
    year_zhi = dizhi_korean_to_chinese.get(year[1], year[1]) if year else ''

    # 월의 천간과 지지를 한자로 변환 (월의 천간이 생략될 수도 있음)
    if month and len(month) > 2:  # 예: 임신월
        month_gan = tiangan_korean_to_chinese.get(month[0], month[0])
        month_zhi = dizhi_korean_to_chinese.get(month[1], month[1])
    else:  # 예: 신월
        month_gan = ''
        month_zhi = dizhi_korean_to_chinese.get(month[0], month[0]) if month else ''

    # 월장에서 월장의 지지를 한자로 변환
    month_zang = dizhi_korean_to_chinese.get(month_zang_input[0], month_zang_input[0]) if month_zang_input else ''

    # 일의 천간과 지지를 한자로 변환
    day_gan = tiangan_korean_to_chinese.get(day[0], day[0]) if day else ''
    day_zhi = dizhi_korean_to_chinese.get(day[1], day[1]) if day else ''

    # 시의 천간과 지지를 한자로 변환 (시의 천간이 생략될 수도 있음)
    if hour and len(hour) > 2:  # 예: 정유시
        hour_gan = tiangan_korean_to_chinese.get(hour[0], hour[0])
        hour_zhi = dizhi_korean_to_chinese.get(hour[1], hour[1])
    else:  # 예: 유시
        hour_gan = ''
        hour_zhi = dizhi_korean_to_chinese.get(hour[0], hour[0]) if hour else ''

    # 변환된 연, 월, 일, 시 출력
    print(f"변환된 입력: {year_gan}{year_zhi}년 {month_gan}{month_zhi}월 {month_zang}장 {day_gan}{day_zhi}일 {hour_gan}{hour_zhi}시")
    
    return year_gan, year_zhi, month_gan, month_zhi, month_zang, day_gan, day_zhi, hour_gan, hour_zhi

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

def find_tianjiang_start_index(day_gan, hour_zhi, tianpan_sequence):
    """
    천간과 점시를 기반으로 천장의 시작 인덱스를 찾는 함수.
    """
    # 천간에 따른 천장 시작 위치
    tianjiang_start_positions = {
        '甲': ('丑', '未'), '戊': ('丑', '未'), '庚': ('丑', '未'),
        '乙': ('子', '申'), '己': ('子', '申'),
        '丙': ('亥', '酉'), '丁': ('亥', '酉'),
        '壬': ('巳', '卯'), '癸': ('巳', '卯'),
        '辛': ('午', '寅')
    }

    # 시간에 따른 천장 선택
    if hour_zhi in ['卯', '辰', '巳', '午', '未', '申']:
        # 낮 시간: 앞의 천장 위치 사용
        start_zhi = tianjiang_start_positions[day_gan][0]
    else:
        # 밤 시간: 뒤의 천장 위치 사용
        start_zhi = tianjiang_start_positions[day_gan][1]

    # 천반에서 시작 인덱스를 찾음
    start_index = tianpan_sequence.index(start_zhi)
    
    # 천장의 시작 위치(지지)를 반환하도록 수정
    return tianpan_sequence[start_index]

def place_tianjiang(grid, start_index, tianjiang_list):
    """
    천반에서 시작 인덱스를 기반으로 천장을 배치하는 함수.
    """
    # 천반의 위치 설정 (반시계 방향 순환)
    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (0, 0), '午': (0, 1), '未': (0, 2), '申': (0, 3),
                      '酉': (1, 3), '戌': (2, 3), '亥': (3, 3), '子': (3, 2),
                      '丑': (3, 1), '寅': (3, 0), '卯': (2, 0), '辰': (1, 0)}

    # 천반에서 시작 인덱스 찾기
    reverse_order = tianpan_positions[start_index] in ['巳', '午', '未', '申', '酉', '戌']
    
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

    # 6x6 천반과 천장을 결합한 배열 초기화
    combined_grid = [['  ' for _ in range(6)] for _ in range(6)]

    # 천반의 위치 설정 (4x4 내부)
    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (1, 1), '午': (1, 2), '未': (1, 3), '申': (1, 4),
                      '酉': (2, 4), '戌': (3, 4), '亥': (4, 4), '子': (4, 3),
                      '丑': (4, 2), '寅': (4, 1), '卯': (3, 1), '辰': (2, 1)}

    # 점시의 위치에서부터 월장 순서를 4x4 내부에 배치
    start_index = tianpan_positions.index(divination_hour)
    for i in range(12):
        pos_index = (start_index + i) % 12
        x, y = tianpan_coords[tianpan_positions[pos_index]]
        combined_grid[x][y] = month_zang_sequence[i]

    # 천장의 시작 인덱스 찾기
    tianjiang_start_zhi = find_tianjiang_start_index(day_gan, divination_hour, month_zang_sequence)

    # 천장의 위치 설정 (바깥쪽 테두리)
    tianjiang_positions = {'巳': (0, 1), '午': (0, 2), '未': (0, 3), '申': (0, 4),
                           '酉': (2, 5), '戌': (3, 5), '亥': (5, 4), '子': (5, 3),
                           '丑': (5, 2), '寅': (5, 1), '卯': (3, 0), '辰': (2, 0)}

    # 천장을 결합하여 6x6 배열의 바깥쪽 테두리에 배치
    start_index = tianpan_positions.index(tianjiang_start_zhi)
    for i in range(12):
        pos_index = (start_index + i) % 12
        x, y = tianjiang_positions[tianpan_positions[pos_index]]
        combined_grid[x][y] = tianjiang_list[i]

    # 6x6 그리드 출력
    print("\n6x6 천반 및 천장이 결합된 배열:")
    for row in combined_grid:
        print(' '.join(row))


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


def create_4x4_tianjiang(day_gan, divination_hour, tianjiang_list, month_zang_sequence):
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
    start_index = find_tianjiang_start_index(day_gan, divination_hour, month_zang_sequence)

    # 천장을 결합하여 4x4 배열에 배치
    place_tianjiang(tianjiang_grid, start_index, tianjiang_list)

    # 4x4 그리드 출력
    print("\n4x4 천장 배열:")
    for row in tianjiang_grid:
        print(' '.join(row))

def main():
    # 사용자로부터 연, 월, 일, 시, 월장 입력받기
    year_gan, year_zhi, month_gan, month_zhi, month_zang, day_gan, day_zhi, hour_gan, hour_zhi = get_user_input()
    
    # 입력된 월장으로부터 12개의 월장 순서 생성
    month_zang_sequence = create_month_zang_sequence(month_zang)

    # 천장 순서 생성
    tianjiang_list, _ = create_tianjiang_sequence()

    # 6x6 천반과 지반이 결합된 텍스트 그리드 출력
    #create_6x6_tianpan_and_diban(month_zang_sequence, hour_zhi)

    # 6x6 천반 및 천장 배열 출력
    create_6x6_tianpan_and_tianjiang(month_zang_sequence, hour_zhi, day_gan, tianjiang_list)

    # 4x4 천반 배열 출력
    #create_4x4_tianpan(month_zang_sequence, hour_zhi)

    # 4x4 천장 배열 출력
    create_4x4_tianjiang(day_gan, hour_zhi, tianjiang_list, month_zang_sequence)


# 프로그램 실행
if __name__ == "__main__":
    main()
