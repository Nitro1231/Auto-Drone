import socket

HEAD = b'StartOfStream'
BUFFER = 512

class Sender:
    def __init__(self, host: str, port: int) -> None:
        self._receiver = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data: bytes) -> None:
        self._socket.sendto(HEAD, self._receiver)
        send_data = data.tostring()
        for i in range(0, len(send_data), BUFFER):
            self._socket.sendto(send_data[i:i+BUFFER], self._receiver)

    def close(self) -> None:
        self._socket.close()
