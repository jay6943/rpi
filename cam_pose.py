import cv2
import ultralytics

model = ultralytics.YOLO('../data/yolo26n-pose.pt')

cam = cv2.VideoCapture(0)

while cam.isOpened():
  success, frame = cam.read()
  if not success: break
  
  results = model(frame, stream=True)
  for result in results:
    annotated_frame = result.plot()
    cv2.imshow('Pose track', annotated_frame)

  if cv2.waitKey(1) in [27, 113]: break

cam.release()
cv2.destroyAllWindows()
