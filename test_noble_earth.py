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
    """
    시작 월장으로부터 12지지 순서를 생성하는 함수
    """
    start_index = zhi_list.index(start_month_zang)
    month_zang_sequence = [zhi_list[(start_index + i) % 12] for i in range(12)]
    print("월장 순서 =", month_zang_sequence)
    return month_zang_sequence

def determine_noble(day_gan, hour_zhi):
    """
    천간과 시에 따른 주야 귀인을 결정하는 함수
    """
    if hour_zhi in ['卯', '辰', '巳', '午', '未', '申']:
        day_noble = noble_positions[day_gan][0]
        night_noble = noble_positions[day_gan][1]
    else:
        day_noble = noble_positions[day_gan][1]
        night_noble = noble_positions[day_gan][0]
    print("일간=", day_gan, ", 주야귀인=", day_noble, night_noble)
    return day_noble, night_noble

def determine_start_noble_position(day_gan, hour_zhi):
    """
    귀인의 시작 위치를 결정하는 함수
    """
    day_noble, night_noble = determine_noble(day_gan, hour_zhi)
    print('귀인 위치=', day_noble, night_noble)
    return day_noble, night_noble

def create_tianjiang_sequence(start_noble_zhi, month_zang_sequence):
    """
    시작 귀인 위치와 월장 순서에 따라 천장 배열을 생성하는 함수
    """
    start_index = month_zang_sequence.index(start_noble_zhi)
    print(start_index)
    arranged_tianjiang = []
    
    for i in range(12):
        pos_index = (i - start_index) % 12
        arranged_tianjiang.append(tianjiang_list[pos_index])
    print('천장 배열 = ', arranged_tianjiang)
    return arranged_tianjiang

def find_noble_start_index(day_gan, hour_zhi, month_zang_sequence):
    """
    천간과 시에 따른 귀인의 시작 인덱스를 찾는 함수
    """
    day_noble, night_noble = determine_start_noble_position(day_gan, hour_zhi)
    # 시간대에 따라 올바른 귀인 선택
    start_noble_zhi = day_noble if hour_zhi in ['卯', '辰', '巳', '午', '未', '申'] else night_noble
    start_index = month_zang_sequence.index(start_noble_zhi)
    print('귀인 시작 인덱스=', start_index, "월장=", month_zang_sequence)
    return start_index

def main():
    # 사용자로부터 연, 월, 일, 시, 월장 입력받기
    year_gan, year_zhi, month_gan, month_zhi, month_zang, day_gan, day_zhi, hour_gan, hour_zhi = get_user_input()
    
    # 입력된 월장으로부터 12개의 월장 순서 생성
    month_zang_sequence = create_month_zang_sequence(month_zang)

    # 천장 배열 생성
    start_noble_zhi = determine_start_noble_position(day_gan, hour_zhi)[0]  # 낮 귀인으로 기본 설정
    tianjiang_sequence = create_tianjiang_sequence(start_noble_zhi, month_zang_sequence)

    # 나머지 코드 실행

if __name__ == "__main__":
    main()
