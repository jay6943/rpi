import cv2
import picamera2
import ultralytics

model = ultralytics.YOLO('../data/yolo26n-pose.pt')

cam = picamera2.Picamera2()
# cam.preview_configuration.main.size = (1280, 720)
cam.preview_configuration.main.format = 'RGB888'
cam.preview_configuration.align()
cam.configure('preview')
cam.start()

while True:
  frame = cam.capture_array()
  
  results = model(frame, stream=True)
  for result in results:
    annotated_frame = result.plot()
    cv2.imshow('Rasberry Pi Cam v3', annotated_frame)

  if cv2.waitKey(1) in [27, 113]: break

cam.stop()
cv2.destroyAllWindows()
