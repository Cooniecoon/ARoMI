import cv2


import numpy as np

def cali(source):

    rms = 0.438197
    fx = 458.049323
    fy = 458.049323
    cx = 320.000000
    cy = 240.000000
    k1 = -0.392772
    k2 = 0.165115
    p1 = 0.000704
    p2 = 0.000992

    hfov = 69.9
    vfov = 55.3

    # A (Intrinsic Parameters) [fc, skew*fx, cx], [0, fy, cy], [0, 0, 1]
    K = np.array([[fx, 0., cx],
                [0,  fy, cy],
                [0,   0,  1]])

    # Distortion Coefficients(kc) - 1st, 2nd
    d = np.array([k1, k2, p1, p2, 0]) # just use first two terms

    image = source
    img = cv2.resize(image, (640, 480), interpolation=cv2.INTER_LINEAR)
    h, w = img.shape[:2]

    # undistort
    newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (w,h), 0)
    newimg = cv2.undistort(img, K, d, None, newcamera)
    img = cv2.resize(newimg, (640, 480), interpolation=cv2.INTER_LINEAR)

    return img


cap = cv2.VideoCapture(0)

while True:
    _,img=cap.read()
    cv2.imshow("before_1", (img))
    cv2.imshow("after_1", cali(img))

    if cv2.waitKey(1) > 0: break

cap.release()
cv2.destroyAllWindows()