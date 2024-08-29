import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 한자 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # WSL의 나눔고딕 폰트 경로
fontprop = FontProperties(fname=font_path)

def create_text_grid():
    # 텍스트 리스트
    earth_text_grid = [
        ['巳', '午', '未', '申',],
        ['辰', '  ', '  ', '酉',],
        ['卯', '  ', '  ', '戌',],
        ['寅', '丑', '子', '亥',]
    ]

    fig, ax = plt.subplots(figsize=(6, 6))  # 정사각형 형태의 그래프 생성
    
    # 각 텍스트의 위치를 사각형 형태로 배치
    for i in range(4):
        for j in range(4):
            if text_grid[i][j].strip():  # 빈 공간은 텍스트를 그리지 않음
                ax.text(j + 0.5, 4 - i - 0.5, text_grid[i][j], horizontalalignment='center', verticalalignment='center', fontsize=20, fontproperties=fontprop)

    # 축 설정
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')  # 축 숨기기
    
    # 그래프를 파일로 저장
    plt.savefig("text_grid.png")
    print("사각형으로 배치된 텍스트가 'text_grid.png' 파일로 저장되었습니다.")

def main():
    # 텍스트 생성
    print("사각형으로 배치된 텍스트 생성 중...")
    create_text_grid()

# 프로그램 실행
if __name__ == "__main__":
    main()
