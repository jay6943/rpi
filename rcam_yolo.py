import cv2
import picamera2
import ultralytics

# YOLO 모델 로드 (사용하려는 가중치 파일 경로 입력)
model = ultralytics.YOLO('../yolo26n.pt') 

cam = picamera2.Picamera2()
# YOLO 추론 속도를 높이고 메모리를 아끼기 위해 메인 스트림 해상도를 적절하게 조절합니다.
# (YOLO Nano 모델은 기본적으로 640x640 크기 내외에서 효율적입니다.)
# cam.preview_configuration.main.size = (640, 480)
# cam.preview_configuration.main.size = (1280, 720)
# YOLO와 OpenCV 처리를 위해 RGB 포맷 설정
cam.preview_configuration.main.format = 'RGB888'
cam.preview_configuration.align()
# 설정 적용 및 카메라 시작
cam.configure('preview')
cam.start()

while True:
  # 카메라로부터 실시간 프레임을 NumPy 배열(RGB)로 캡처
  frame = cam.capture_array()
  
  # YOLO 모델로 객체 감지 수행 (imgsz를 지정하면 내부 리사이징으로 성능 최적화 가능)
  results = model(frame, imgsz=320, verbose=False)
  
  # 감지된 결과 레이블 및 박스가 그려진 시각화 프레임 가져오기
  annotated_frame = results[0].plot()
  
  cv2.imshow('Picamera2 + YOLO Detection', annotated_frame)
  if cv2.waitKey(1) in [27, 113]: break

cam.stop()
cv2.destroyAllWindows()
