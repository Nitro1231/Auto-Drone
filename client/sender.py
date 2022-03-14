import socket


BUFFER = 512
HEADER = ('StartOfStream' + (BUFFER - len('StartOfStream')) * 'a').encode('utf-8')

class Sender:
    def __init__(self, host: str, port: int) -> None:
        self._receiver = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data: bytes) -> None:
        self._socket.sendto(HEADER, self._receiver)
        send_data = data.tobytes()
        for i in range(0, len(send_data), BUFFER):
            self._socket.sendto(send_data[i:i+BUFFER], self._receiver)

    def close(self) -> None:
        self._socket.close()
