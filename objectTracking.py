import cv2
from imutils.video import VideoStream

class ObjectTracker:

    def __init__(self, mask_values, video):
        self.greenLower = mask_values[:3]
        self.greenUpper = mask_values[3:]
        
        if video:
            self.cap = cv2.VideoCapture(video)

        else:
            self.cap = VideoStream(src=0).start()

    def __del__(self):
        self.cap.release()

    def startTracking(mask_values, video="None"):

        while True:

            ret, frame = cap.read()

            if ret:
                yield frame

            cv2.waitKey(0)

