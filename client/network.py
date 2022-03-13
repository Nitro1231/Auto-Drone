import socket
import struct


class Network:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self, data: bytes) -> None:
        # Use 'L' for larger data.
        self._socket.sendall(struct.pack('H', len(data)) + data)

    def connect(self) -> None:
        self._socket.connect(self._host, self._port)

    def close(self) -> None:
        self._socket.close()
