import cv2
from camera import Camera
from sender import Sender


class Stream:
    def __init__(self, name: str, data: dict, display = False) -> None:
        self._name = name
        self._info = data
        self._display = display
        self._camera = Camera(
            index=data['index'],
            resolution=data['resolution'],
            frame_rate=data['frame_rate']
        )
        self._sender = Sender(
            host=data['host'],
            port=data['port']
        )

    def __call__(self) -> None:
        _, image = self._camera.read()
        self._sender.send_data(image)

        if self._display:
            self.display(self._name, image)

    def display(self, title, image) -> None:
        cv2.imshow(title, image)
        cv2.waitKey(1)

    def close(self) -> None:
        self._sender.close()
        self._camera.release()
