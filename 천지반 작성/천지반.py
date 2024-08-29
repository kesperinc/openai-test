def create_tianpan_grid():
    # 천반 배치 리스트
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

    # 그리드 출력
    for row in grid:
        print(' '.join(row))

def main():
    print("천반과 고정된 지반이 배치된 텍스트 그리드 출력 중...")
    create_tianpan_grid()

# 프로그램 실행
if __name__ == "__main__":
    main()
