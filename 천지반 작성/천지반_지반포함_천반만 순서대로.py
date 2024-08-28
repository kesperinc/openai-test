def get_user_input():
    """
    사용자로부터 월장과 점시를 입력받는 함수.
    """
    # 한글 -> 한자 매핑 사전
    korean_to_chinese = {
        '해': '亥', '자': '子', '축': '丑', '인': '寅',
        '묘': '卯', '진': '辰', '사': '巳', '오': '午',
        '미': '未', '신': '申', '유': '酉', '술': '戌'
    }

    # 월장 입력받기
    month_zang_korean = input("월장을 입력하세요 (예: 사): ").strip()
    
    # 점시 입력받기
    divination_hour_korean = input("점시를 입력하세요 (예: 진): ").strip()
    
    # 한글 입력을 한자로 변환
    month_zang = korean_to_chinese.get(month_zang_korean, month_zang_korean)
    divination_hour = korean_to_chinese.get(divination_hour_korean, divination_hour_korean)
    
    return month_zang, divination_hour

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

def create_6x6_grid(month_zang_sequence, divination_hour):
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

def create_4x4_grid(month_zang_sequence, divination_hour):
    """
    4x4 그리드에 천반을 배열하여 출력하는 함수.
    """
    # 4x4 천반 배열 초기화
    tianpan_grid = [['  ' for _ in range(4)] for _ in range(4)]

    # 고정된 지반 배치 리스트 (4x4 중앙 그리드)
    diban_grid = [
        ['巳', '午', '未', '申'],
        ['辰', '  ', '  ', '酉'],
        ['卯', '  ', '  ', '戌'],
        ['寅', '丑', '子', '亥']
    ]

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

def main():
    # 사용자로부터 월장과 점시 입력받기
    month_zang, divination_hour = get_user_input()
    
    # 입력된 월장으로부터 12개의 월장 순서 생성
    month_zang_sequence = create_month_zang_sequence(month_zang)
    
    # 6x6 천반과 지반이 결합된 텍스트 그리드 출력
    create_6x6_grid(month_zang_sequence, divination_hour)

    # 4x4 천반 배열 출력
    create_4x4_grid(month_zang_sequence, divination_hour)

# 프로그램 실행
if __name__ == "__main__":
    main()
