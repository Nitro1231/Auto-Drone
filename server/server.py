import cv2
import receiver
import numpy as np


DISPLAY = True

cam_data = {
    'test_cam': {
        'index': 1,
        'host': '127.0.0.1',
        'port': 443,
        'resolution': (640, 480),
        'frame_rate': 60
    }
}

class Server:
    def __init__(self, camera_data: dict) -> None:
        self._camera_data = camera_data

        for name, data in self._camera_data.items():
            self._camera_data[name]['network'] = receiver.Receiver(
                host=data['host'],
                port=data['port'],
                data_size=data['resolution'][0] * data['resolution'][1] * 3
            )
            print(f'Scoket for {name} has been initialized on port {data["port"]}.')

    def stream(self) -> None:
        while True:
            for name, data in self._camera_data.items():
                print('!')
                image = np.frombuffer(
                    buffer=data['network'].receive_data(),
                    dtype=np.uint8
                ).reshape(data['resolution'][1], data['resolution'][0], 3)

                if DISPLAY:
                    self.display(name, image)

    def display(self, title, image) -> None:
        cv2.imshow(title, image)
        cv2.waitKey(1)

    def close(self) -> None:
        for data in self._camera_data:
            data['network'].close()
            data['camera'].release()


if __name__ == '__main__':
    c = Server(cam_data)
    c.stream()
