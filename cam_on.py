import cv2

cap = cv2.VideoCapture(1)

# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()

    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imshow("VideoFrame", frame)
    if cv2.waitKey(1) > 0:
        # print(frame.shape)
        break

cap.release()
cv2.destroyAllWindows()