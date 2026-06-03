import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# 1. Picamera2 카메라 초기화 및 설정
picam2 = Picamera2()

# YOLO 추론 속도를 높이고 메모리를 아끼기 위해 메인 스트림 해상도를 적절하게 조절합니다.
# (YOLO Nano 모델은 기본적으로 640x640 크기 내외에서 효율적입니다.)
picam2.preview_configuration.main.size = (640, 480)
# YOLO와 OpenCV 처리를 위해 RGB 포맷 설정
picam2.preview_configuration.main.format = 'RGB888'
picam2.preview_configuration.align()

# 설정 적용 및 카메라 시작
picam2.configure('preview')
picam2.start()

# 2. YOLO 모델 로드 (사용하려는 가중치 파일 경로 입력)
# 여기서는 예시로 일반적인 yolov8n.pt를 타겟팅합니다. 
# 본인의 파일명(예: yolo26n.pt 등)으로 변경하여 사용하세요.
# model = YOLO('../data/yolov8n.pt') 
model = YOLO('../data/yolo26n.pt') 

print('YOLO 객체 감지를 시작합니다. 종료하려면 이미지 창에서 q를 누르세요.')

try:
  while True:
    # 3. 카메라로부터 실시간 프레임을 NumPy 배열(RGB)로 캡처
    frame = picam2.capture_array()
    
    # OpenCV는 BGR 순서를 사용하므로 RGB에서 BGR로 색상 채널 변환
    # frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # 4. YOLO 모델로 객체 감지 수행 (imgsz를 지정하면 내부 리사이징으로 성능 최적화 가능)
    # results = model(frame_bgr, imgsz=320, verbose=False)
    results = model(frame, imgsz=320, verbose=False)
    
    # 감지된 결과 레이블 및 박스가 그려진 시각화 프레임 가져오기
    annotated_frame = results[0].plot()
    
    # 5. 화면에 실시간 결과 출력
    cv2.imshow('Picamera2 + YOLO Detection', annotated_frame)
    
    # 'q' 키를 누르면 루프 탈출
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

finally:
  # 6. 자원 해제 및 종료
  picam2.stop()
  cv2.destroyAllWindows()
  print('프로그램이 안전하게 종료되었습니다.')