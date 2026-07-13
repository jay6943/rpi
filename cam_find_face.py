import cv2
import msg
import time

cam = cv2.VideoCapture(0)

# OpenCV HOG 보행자(사람) 감지기 초기화
face_cascade = cv2.CascadeClassifier(
	cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

person_detected_start = None
cooldown_until = 0
cooldown_time = 60
set_time = 1

print('시스템 시작... 카메라 화면을 표시합니다.')
print('(종료하려면 화면에서 ESC키를 누르세요)')

while cam.isOpened():
  # 카메라에서 프레임 가져오기 (RGB 포맷)
  success, frame = cam.read()
  
  # HOG 처리를 위해 그레이스케일로 변환
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
  faces = face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

  if len(faces) > 0:
    current_time = time.time()
    
    if person_detected_start is None:
      person_detected_start = current_time
    else:
      elapsed_time = current_time - person_detected_start
      
      # 화면 좌상단에 타이머 텍스트 표시 (빨간색)
      cv2.putText(frame, f'Detecting: {elapsed_time:.1f}s',
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      
      # 5초 이상 지속적으로 감지되었고, 쿨다운 시간이 지났을 경우 캡처
      if elapsed_time > set_time and current_time > cooldown_until:
        filename = f'{time.strftime('%Y-%m-%d-%H%M%S')}.jpg'
        
        # 이미지 저장
        cv2.imwrite(f'../data/people/{filename}', frame)
        
        messages = f'방문자 {filename}'
        msg.send_message(messages)
        print(messages)
        
        cooldown_until = current_time + cooldown_time
        person_detected_start = None 
    
    # 감지된 사람의 영역에 초록색 사각형(바운딩 박스) 그리기
    for (x, y, w, h) in faces:
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
  else:
    # 프레임에 사람이 없으면 타이머 초기화
    person_detected_start = None

  # 화면에 프레임 출력
  cv2.imshow('Raspberry Pi 5 - Person Detection', frame)

  if cv2.waitKey(100) in [27, 113]: break

cam.release()
cv2.destroyAllWindows()
