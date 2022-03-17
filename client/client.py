from stream import Stream


DISPLAY = True

cam_data = {
    'test_cam': {
        'index': 1,
        'host': '127.0.0.1',
        'port': 6666,
        'resolution': (640, 480),
        'frame_rate': 60
    }
}

class Client:
    def __init__(self, stream_data: dict) -> None:
        self._stream_data = stream_data
        self._stream = dict()
        
        for name, data in self._stream_data.items():
            self._stream[name] = Stream(name, data, DISPLAY)

    def main_loop(self) -> None:
        while True:
            for stream in self._stream.values():
                stream()


if __name__ == '__main__':
    c = Client(cam_data)
    c.main_loop()
