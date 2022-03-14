import cv2
import camera
import sender


DISPLAY = True

cam_data = {
    'test_cam': {
        'index': 1,
        'host': '127.0.0.1',
        'port': 6666,
        'resolution': (960, 720),
        'frame_rate': 60
    }
}

class Client:
    def __init__(self, camera_data: dict) -> None:
        self._camera_data = camera_data

        for name, data in self._camera_data.items():
            self._camera_data[name]['network'] = sender.Sender(
                host=data['host'],
                port=data['port']
            )
            self._camera_data[name]['camera'] = camera.Camera(
                index=data['index'],
                resolution=data['resolution'],
                frame_rate=data['frame_rate']
            )

    def stream(self) -> None:
        while True:
            for name, data in self._camera_data.items():
                _, image = data['camera'].read()
                data['network'].send_data(image)

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
    c = Client(cam_data)
    c.stream()
