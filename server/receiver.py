import socket


HEADER = b'StartOfStream'
BUFFER = 512
# data_size = width * height * 3

class Receiver:
    def __init__(self, host: str, port: int, data_size: int) -> None:
        self._server = (host, port)
        self._chunks = data_size / BUFFER
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(self._server)

    def receive_data(self) -> bytes:
        chunks = []
        new_data = False
        while len(chunks) < self._chunks:
            chunk, _ = self._socket.recvfrom(BUFFER)
            if new_data:
                chunks.append(chunk)
            elif chunk.startswith(HEADER):
                new_data = True

        return b''.join(chunks)

    def close(self) -> None:
        self._socket.close()
