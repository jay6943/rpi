import cv2
import ultralytics


model = ultralytics.YOLO('../data/yolo26n.pt')


def cam():
  cap = cv2.VideoCapture(0)

  while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow('frame', annotated_frame)

    if cv2.waitKey(1) in [27, 113]: break

  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__': cam()
