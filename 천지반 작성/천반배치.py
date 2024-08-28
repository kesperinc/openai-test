import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 한자 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # WSL의 나눔고딕 폰트 경로
fontprop = FontProperties(fname=font_path)

def create_tianpan_grid():
    # 천반 배치 리스트 (辰 위치에 巳를 시작으로 시계 방향으로 순환)
    tianpan_grid = [
        ['  ', '午', '未', '申', '酉', '  '],      
        ['  ', '巳', '午', '未', '申', '  '],
        ['巳', '辰', '  ', '  ', '酉', '戌'],
        ['辰', '卯', '  ', '  ', '戌', '亥'],
        ['  ', '寅', '丑', '子', '亥', '  '],
        ['  ', '卯', '寅', '丑', '子', '  '],        
    ]
    # 천반 지지 리스트 (진 시 기준으로 시계 방향으로)
    zhi_list = ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰']
    zhi_positions = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (5, 2), (5, 1), (4, 0), (3, 0), (2, 0)]

    fig, ax = plt.subplots(figsize=(6, 8))  # 세로로 긴 박스 생성
    
    # 각 텍스트의 위치를 사각형 형태로 배치
    for i in range(6):
        for j in range(4):
            if tianpan_grid[i][j].strip():  # 빈 공간은 텍스트를 그리지 않음
                ax.text(j + 0.5, 6 - i - 0.5, tianpan_grid[i][j], horizontalalignment='center', verticalalignment='center', fontsize=20, fontproperties=fontprop)
    
    # 천반 지지 위치에 텍스트 추가
    for idx, pos in enumerate(zhi_positions):
        x, y = pos
        ax.text(x + 0.5, 6 - y - 0.5, zhi_list[idx], horizontalalignment='center', verticalalignment='center', fontsize=20, fontproperties=fontprop, color='red')
    
    # 축 설정
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 6)
    ax.axis('off')  # 축 숨기기
    
    # 그래프를 파일로 저장
    plt.savefig("tianpan_grid.png")
    print("천반이 배치된 텍스트가 'tianpan_grid.png' 파일로 저장되었습니다.")

def main():
    # 텍스트 생성
    print("천반이 배치된 텍스트 생성 중...")
    create_tianpan_grid()

# 프로그램 실행
if __name__ == "__main__":
    main()
