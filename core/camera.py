import cv2


class Camera:
    def __init__(self, index: int, resolution: tuple, frame_rate: int) -> None:
        self._index = index
        self._resolution = resolution
        self._frame_rate = frame_rate

        self._capture = cv2.VideoCapture(index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self._capture.set(cv2.CAP_PROP_FPS, frame_rate)

    def read(self) -> tuple:
        return self._capture.read()

    def release(self) -> None:
        self._capture.release()
