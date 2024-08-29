def circulate_12_zhi(start_zhi):
    # 12지지 리스트 정의
    zhi_list = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    # 시작 지지의 인덱스를 찾음
    start_index = zhi_list.index(start_zhi)
    
    # 순환하며 출력
    for i in range(len(zhi_list)):
        # 현재 순환 위치의 인덱스 계산
        current_index = (start_index + i) % len(zhi_list)
        # 지지 출력
        print(zhi_list[current_index], end=' ')

def main():
    # 사용자로부터 시작할 지지 입력받기
    start_zhi = input("시작할 지지를 입력하세요 (예: 사): ").strip()
    
    # 12지지 순환 출력
    if start_zhi in ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']:
        circulate_12_zhi(start_zhi)
    else:
        print("잘못된 입력입니다. 올바른 지지를 입력하세요.")

# 프로그램 실행
if __name__ == "__main__":
    main()
