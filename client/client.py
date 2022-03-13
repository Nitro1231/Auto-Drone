import camera
import pickle
import network


DISPLAY = True

cam_data = {
    'test_cam': {
        'index': 1,
        'host': '127.0.0.1',
        'port': 6666,
        'resolution': (1920, 1080),
        'frame_rate': 60
    }
}

class Client:
    def __init__(self, camera_data: dict) -> None:
        self._camera_data = camera_data

        for name, data in self._camera_data.items():
            self._camera_data[name]['network'] = network.Network(
                host=data['host'],
                port=data['port']
            )
            self._camera_data[name]['camera'] = camera.Camera(
                index=data['index'],
                resolution=data['resolution'],
                frame_rate=data['frame_rate']
            )

    def connect(self) -> None:
        for data in self._camera_data.values():
            data['network'].connect()

    def close(self) -> None:
        for data in self._camera_data.values():
            data['network'].close()

    def stream(self) -> None:
        while True:
            for name, data in self._camera_data.items():
                _, image = data['camera'].read()
                image_data = pickle.dumps(image)
                data['network'].send_data(image_data)

                if DISPLAY:
                    data['camera'].show(name, image)

    def image_to_bytes(image: object) -> bytes:
        return pickle.dumps(image)


if __name__ == '__main__':
    c = Client(cam_data)
    c.stream()
