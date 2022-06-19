import cv2


CAM_LEFT = 1
CAM_RIGHT = 2

CAM_HEIGHT = 420
CAM_WIDTH = 420

class StereoCamera:
    def __init__(self) -> None:
        self.cam_left = cv2.VideoCapture(CAM_LEFT,  cv2.CAP_DSHOW)
        self.cam_left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        self.cam_left.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)

        self.cam_right = cv2.VideoCapture(CAM_RIGHT,  cv2.CAP_DSHOW)
        self.cam_right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        self.cam_right.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)

    def isOpened(self) -> bool:
        return (self.cam_left.isOpened() and self.cam_right.isOpened())

    def release(self) -> None:
        self.cam_left.release()
        self.cam_right.release()
