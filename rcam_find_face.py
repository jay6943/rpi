import cv2
import time
from picamera2 import Picamera2

# Picamera2 초기화 및 해상도 설정 (처리 속도 및 화면 출력을 위해 640x480으로 설정)
cam = Picamera2()
# cfg = cam.create_video_configuration(main={'size': (640, 480)})
cfg = cam.create_video_configuration()
cam.configure(cfg)
cam.start()

# OpenCV HOG 보행자(사람) 감지기 초기화
face_cascade = cv2.CascadeClassifier(
	cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

person_detected_start = None
cooldown_until = 0
cooldown_time = 60
set_time = 1

print('시스템 시작... 카메라 화면을 표시합니다.')
print('(종료하려면 화면에서 ESC키를 누르세요)')

while True:
  # 카메라에서 프레임 가져오기 (RGB 포맷)
  frame = cam.capture_array()
  
  # OpenCV 화면 출력 및 저장을 위해 RGB를 BGR로 변환
  bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  # HOG 처리를 위해 그레이스케일로 변환
  gray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
  
  faces = face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

  if len(faces) > 0:
    current_time = time.time()
    
    if person_detected_start is None:
      person_detected_start = current_time
    else:
      elapsed_time = current_time - person_detected_start
      
      # 화면 좌상단에 타이머 텍스트 표시 (빨간색)
      cv2.putText(bgr_frame,
        f'Detecting: {elapsed_time:.1f}s', (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      
      # 5초 이상 지속적으로 감지되었고, 쿨다운 시간이 지났을 경우 캡처
      if elapsed_time > set_time and current_time > cooldown_until:
        timestamp = time.strftime('%Y-%m-%d-%H%M%S')
        filename = f'../data/people/{timestamp}.jpg'
        
        # 이미지 저장
        cv2.imwrite(filename, bgr_frame)
        print(f'[알림] 사람이 {set_time}초 이상 감지되어 캡처되었습니다. ({filename})')
        
        cooldown_until = current_time + cooldown_time
        person_detected_start = None 
    
    # 감지된 사람의 영역에 초록색 사각형(바운딩 박스) 그리기
    for (x, y, w, h) in faces:
      cv2.rectangle(bgr_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
  else:
    # 프레임에 사람이 없으면 타이머 초기화
    person_detected_start = None

  # 화면에 프레임 출력
  cv2.imshow('Raspberry Pi 5 - Person Detection', bgr_frame)

  if cv2.waitKey(100) in [27, 113]: break

cam.stop()
cv2.destroyAllWindows()