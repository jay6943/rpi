import cv2
from picamera2 import Picamera2

cam = Picamera2()
cfg = cam.create_video_configuration(main={'size':(640,480)})
cam.configure(cfg)
cam.start()

frame = cam.capture_array()
bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
roi = cv2.selectROI('Select Tracking Area', bgr, showCrosshair=True)
cv2.destroyWindow('Select Tracking Area')

tracker = cv2.TrackerCSRT.create()
tracker.init(bgr, roi)

while True:
  frame = cam.capture_array()
  bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  success, box = tracker.update(bgr)

  if success:
    x, y, w, h = [int(v) for v in box]
    ft = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(bgr, (x, y), (x + w, y + h), (0,255,0), 2)
    cv2.putText(bgr, 'Tracking', (x, y - 10), ft, 0.6, (0,255,0), 2)
  else:
    cv2.putText(bgr, 'Lost', (50, 50), ft, 1, (0,255,0), 2)

  cv2.imshow('Rasberry Pi Cam v3', bgr)
  if cv2.waitKey(1) in [27, 113]: break

cam.stop()
cv2.destroyAllWindows()
