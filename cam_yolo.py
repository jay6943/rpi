import cv2
import ultralytics

model = ultralytics.YOLO('../yolo26n.pt')

cam = cv2.VideoCapture(0)

while cam.isOpened():
  success, frame = cam.read()
  if not success: break

  results = model(frame)
  annotated_frame = results[0].plot()
  cv2.imshow('frame', annotated_frame)

  if cv2.waitKey(1) in [27, 113]: break

cam.release()
cv2.destroyAllWindows()
