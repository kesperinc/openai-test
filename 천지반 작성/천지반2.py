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

def create_tianpan_grid(month_zang, divination_hour):
    # 천반 배치 리스트 (기본적인 6x6 외곽 그리드)
    tianpan_grid = [
        ['  ', '午', '未', '申', '酉', '  '],
        ['  ', '巳', '午', '未', '申', '  '],
        ['巳', '辰', '  ', '  ', '酉', '戌'],
        ['辰', '卯', '  ', '  ', '戌', '亥'],
        ['  ', '寅', '丑', '子', '亥', '  '],
        ['  ', '卯', '寅', '丑', '子', '  ']
    ]
    
    # 고정된 지반 배치 리스트 (4x4 중앙 그리드)
    diban_grid = [
        ['巳', '午', '未', '申'],
        ['辰', '  ', '  ', '酉'],
        ['卯', '  ', '  ', '戌'],
        ['寅', '丑', '子', '亥']
    ]
    
    # 텍스트 그리드 초기화
    grid = [['  ' for _ in range(6)] for _ in range(6)]

    # 천반 그리드 설정
    for i in range(6):
        for j in range(6):
            if tianpan_grid[i][j].strip():
                grid[i][j] = tianpan_grid[i][j]

    # 지반 그리드 설정 (4x4 중앙 고정 배치)
    for i in range(4):
        for j in range(4):
            if diban_grid[i][j].strip():
                grid[i + 1][j + 1] = diban_grid[i][j]

    # 천반의 시작 위치를 지반의 위치와 맞추기 위해 조정
    start_positions = {'巳': (1, 1), '午': (1, 2), '未': (1, 3), '申': (1, 4),
                       '酉': (2, 4), '戌': (3, 4), '亥': (4, 4), '子': (4, 3),
                       '丑': (4, 2), '寅': (4, 1), '卯': (3, 1), '辰': (2, 1)}
    # 천반의 위치
    tianpan_positions = {'巳': (0, 1), '午': (0, 2), '未': (0, 3), '申': (0, 4),
                         '酉': (2, 5), '戌': (3, 5), '亥': (5, 4), '子': (5, 3),
                         '丑': (5, 2), '寅': (5, 1), '卯': (3, 0), '辰': (2, 0)}
    # 천반 지지 설정: 월장 위치에서 시작하여 점시의 위치를 계산
    start_position = start_positions[divination_hour]
    x, y = start_position
    grid[x][y] = month_zang

    # 그리드 출력
    for row in grid:
        print(' '.join(row))

def main():
    # 사용자로부터 월장과 점시 입력받기
    month_zang, divination_hour = get_user_input()
    
    # 천반과 지반이 배치된 텍스트 그리드 출력
    print("천반과 고정된 지반이 배치된 텍스트 그리드 출력 중...")
    create_tianpan_grid(month_zang, divination_hour)

# 프로그램 실행
if __name__ == "__main__":
    main()
