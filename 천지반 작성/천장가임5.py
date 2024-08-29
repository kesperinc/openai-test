# 전역 변수
zhi_list = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
tianjiang_list = ['貴', '匕', '朱', '合', '勾', '靑', '空', '白', '常', '玄', '陰', '后']

noble_positions = {
    '甲': ('丑', '未'), '戊': ('丑', '未'), '庚': ('丑', '未'),
    '乙': ('子', '申'), '己': ('子', '申'),
    '丙': ('亥', '酉'), '丁': ('亥', '酉'),
    '壬': ('巳', '卯'), '癸': ('巳', '卯'),
    '辛': ('午', '寅')
}

def create_zhi_sequence(start_zhi):
    start_index = zhi_list.index(start_zhi)
    return [zhi_list[(start_index + i) % 12] for i in range(12)]

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
    user_input = input("연월일시를 입력하세요" + "\n" +
                       "예: 갑진년 임신월 사장 신유일 진시" + "\n" +
                       "예: 갑진년 임신월 유장 경신일 진시").strip()

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
    start_index = zhi_list.index(start_month_zang)
    month_zang_sequence = [zhi_list[(start_index + i) % 12] for i in range(12)]
    print("월장 순서=", month_zang_sequence)
    return month_zang_sequence

def determine_noble(day_gan, hour_zhi):
    if hour_zhi in ['卯', '辰', '巳', '午', '未', '申']:
        day_noble = noble_positions[day_gan][0]
        night_noble = noble_positions[day_gan][1]
    else:
        day_noble = noble_positions[day_gan][1]
        night_noble = noble_positions[day_gan][0]
    print("일간=", day_gan, ", 주야귀인=", day_noble, night_noble)
    return day_noble, night_noble

def determine_start_noble_position(day_gan, hour_zhi):
    day_noble, night_noble = determine_noble(day_gan, hour_zhi)
    return day_noble if hour_zhi in ['卯', '辰', '巳', '午', '未', '申'] else night_noble

def create_tianjiang_sequence(start_noble_zhi, month_zang_sequence):
    start_index = month_zang_sequence.index(start_noble_zhi)
    print("귀인 시작 인덱스=", start_index)
    arranged_tianjiang = []

    for i in range(12):
        pos_index = (i - start_index) % 12
        arranged_tianjiang.append(tianjiang_list[pos_index])
    print('천장 배열 = ', arranged_tianjiang)
    return arranged_tianjiang

def place_tianjiang(grid, tianjiang_sequence, positions):
    """
    천장 배열을 그리드에 배치하는 함수
    """
    # 지반의 위치 설정
    for i, zhi in enumerate(positions):
        x, y = positions[zhi]
        grid[x][y] = tianjiang_sequence[i]

def create_6x6_tianpan_and_tianjiang(month_zang_sequence, divination_hour, day_gan):
    """
    6x6 그리드에 천반과 천장을 배치하여 출력하는 함수
    """
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

    # 천장의 시작 지지 결정
    start_noble_zhi = determine_start_noble_position(day_gan, divination_hour)
    tianjiang_sequence = create_tianjiang_sequence(start_noble_zhi, month_zang_sequence)

    # 천장을 결합하여 6x6 배열의 바깥쪽 테두리에 배치
    place_tianjiang(combined_grid, tianjiang_sequence, tianpan_coords)

    # 6x6 그리드 출력
    print("\n6x6 천반 및 천장이 결합된 배열:")
    for row in combined_grid:
        print(' '.join(row))

def create_4x4_tianpan(month_zang_sequence, divination_hour):
    """
    4x4 그리드에 천반만 배치하여 출력하는 함수
    """
    tianpan_grid = [['  ' for _ in range(4)] for _ in range(4)]

    tianpan_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    tianpan_coords = {'巳': (0, 0), '午': (0, 1), '未': (0, 2), '申': (0, 3),
                      '酉': (1, 3), '戌': (2, 3), '亥': (3, 3), '子': (3, 2),
                      '丑': (3, 1), '寅': (3, 0), '卯': (2, 0), '辰': (1, 0)}

    start_index = tianpan_positions.index(divination_hour)
    for i in range(12):
        pos_index = (start_index + i) % 12
        x, y = tianpan_coords[tianpan_positions[pos_index]]
        tianpan_grid[x][y] = month_zang_sequence[i]

    print("\n4x4 천반 배열:")
    for row in tianpan_grid:
        print(' '.join(row))

def create_4x4_tianjiang(day_gan, divination_hour, month_zang_sequence):
    """
    4x4 그리드에 천장만 배치하여 출력하는 함수
    """
    # 4x4 천장 배열 초기화
    tianjiang_grid = [['  ' for _ in range(4)] for _ in range(4)]

    # 지반의 위치 설정
    diban_positions = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    diban_coords = {'巳': (0, 0), '午': (0, 1), '未': (0, 2), '申': (0, 3),
                    '酉': (1, 3), '戌': (2, 3), '亥': (3, 3), '子': (3, 2),
                    '丑': (3, 1), '寅': (3, 0), '卯': (2, 0), '辰': (1, 0)}

    # 천장의 시작 지지 결정
    start_noble_zhi = determine_start_noble_position(day_gan, divination_hour)
    tianjiang_sequence = create_tianjiang_sequence(start_noble_zhi, month_zang_sequence)

    # 천장을 결합하여 4x4 배열에 배치
    place_tianjiang(tianjiang_grid, tianjiang_sequence, diban_coords)

    print("\n4x4 천장 배열:")
    for row in tianjiang_grid:
        print(' '.join(row))

def main():
    # 사용자로부터 연, 월, 일, 시, 월장 입력받기
    year_gan, year_zhi, month_gan, month_zhi, month_zang, day_gan, day_zhi, hour_gan, hour_zhi = get_user_input()
    
    # 입력된 월장으로부터 12개의 월장 순서 생성
    month_zang_sequence = create_month_zang_sequence(month_zang)

    # 6x6 천반 및 천장 배열 출력
    create_6x6_tianpan_and_tianjiang(month_zang_sequence, hour_zhi, day_gan)

    # 4x4 천반 배열 출력
    create_4x4_tianpan(month_zang_sequence, hour_zhi)

    # 4x4 천장 배열 출력
    create_4x4_tianjiang(day_gan, hour_zhi, month_zang_sequence)

# 프로그램 실행
if __name__ == "__main__":
    main()
