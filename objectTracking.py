import cv2


def trackObject(mask_values, video="None"):

    cap = None

    if video:
        cap = cv2.VideoCapture(video)

    else:
        cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if ret:
            yield frame

        cv2.waitKey(0)

    cap.release()
