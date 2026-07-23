import cv2

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

while True:
  ret, frame = cap.read()
  if not ret: break
  cv2.imshow('Camera', frame)
  if cv2.waitKey(1) == 27: break

cap.release()
cv2.destroyAllWindows()
