import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 이미지 로드 (그레이스케일)
img = cv2.imread('../data/sem/sem2.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. 노이즈 제거 (반도체 SEM 이미지의 미세한 노이즈 완화)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. 이진화 (Thresholding) - 오츠(Otsu) 알고리즘으로 최적의 임계값 자동 설정
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 4. 모폴로지 연산 (노이즈 제거 및 배경/전경 확실히 구분)
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# 확실한 배경 영역 추출 (Dilation)
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# 확실한 전경(물질 내부) 영역 추출 (Distance Transform)
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

# 알 수 없는 경계 영역 계산 (배경 - 전경)
unknown = cv2.subtract(sure_bg, sure_fg)

# 5. 마커 라벨링 (서로 다른 물질 영역에 고유 번호 부여)
_, markers = cv2.connectedComponents(sure_fg)

# 워터쉐드 알고리즘을 위해 라벨에 1을 더함 (배경을 0이 아닌 1로 만들기 위함)
markers = markers + 1
# 경계선(알 수 없는 영역)을 0으로 설정
markers[unknown == 255] = 0

# 6. 워터쉐드(Watershed) 알고리즘 적용 (경계선 기반 영역 분할)
markers = cv2.watershed(img, markers)

# 7. 무작위 색상 맵 생성 (물질 개수만큼 서로 다른 색상 배정)
num_labels = markers.max()
colors = np.random.randint(0, 255, size=(num_labels + 1, 3), dtype=np.uint8)
# 경계선(라벨 -1)은 빨간색으로 고정
colors[0] = [0, 0, 255] 

# 8. 마커 플래그에 맞게 색상 이미지 구성
# markers 결과값은 -1부터 시작하므로 인덱싱을 위해 1을 더해줍니다.
result_img = colors[markers + 1]

# 원본 이미지와 결과 이미지 시각화
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title("Original SEM Image")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Colored Material Segments")
plt.imshow(result_img)
plt.axis('off')

plt.tight_layout()
plt.show()
