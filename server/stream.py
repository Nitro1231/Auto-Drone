import cv2
import numpy as np
from receiver import Receiver


class Stream:
    def __init__(self, name: str, data: dict, display = False) -> None:
        self._name = name
        self._data = data
        self._res = data['resolution']
        self._display = display
        self._receiver = Receiver(
            host=data['host'],
            port=data['port'],
            data_size=self._res[0] * self._res[1] * 3
        )
        print(f'Scoket for {name} has been initialized on port {data["port"]}.')

    def __call__(self) -> None:
        image = np.frombuffer(
            buffer=self._receiver.receive_data(),
            dtype=np.uint8
        ).reshape(self._res[1], self._res[0], 3)

        if self._display:
            self.display(self._name, image)

    def display(self, title, image) -> None:
        cv2.imshow(title, image)
        cv2.waitKey(1)

    def close(self) -> None:
        self._receiver.close()
