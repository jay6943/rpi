import cv2
from picamera2 import Picamera2

cam = Picamera2()
# cfg = cam.create_video_configuration(main={'size':(640,480)})
# cfg = cam.create_video_configuration(main={'size':(1280,720)})
# cfg = cam.create_video_configuration(main={'size':(1920,1080)})
cfg = cam.create_video_configuration()
cam.configure(cfg)
cam.start()

while True:
  frame = cam.capture_array()
  bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  cv2.imshow('Rasberry Pi Cam v3', bgr)
  if cv2.waitKey(1) in [27, 113]: break

cam.stop()
cv2.destroyAllWindows()
