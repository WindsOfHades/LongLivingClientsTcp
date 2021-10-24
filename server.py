import socket
import time
from threading import Thread

HOST = 'localhost'
PORT = 5555
HEADER_SIZE = 2


class ClientDisconnected(Exception):
    pass


class Server:
    def __init__(self, host, port):
        self._server = None
        self._host = host
        self._port = port

    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self._host, self._port))
            server.listen()
            print("Server is listening")
            while True:
                conn, address = server.accept()
                print(f"Spawning thread for client {address}")
                handle_thread = Thread(target=self._handle_client,
                                       args=(conn, address))
                handle_thread.start()
        print("server is closed!")

    # def _handle_client(self, client_socket, address):
    #     with client_socket:
    #         print(f"{address} joined!")
    #         while True:
    #             data = client_socket.recv(1024)
    #             if not data:
    #                 break
    #             print(f"Received data from {address}: {data}")
    #     print(f"{address} left!")

    def _handle_client(self, client_socket, address):
        while True:
            try:
                msg = self._receive(client_socket, address)
            except ClientDisconnected:
                print(f"{address} left!", flush=True)
                break
            print(f"Client {address} sent: {msg}", flush=True)

    def _get_msg_size(self, client_socket):
        chunks = []
        while True:
            time.sleep(3)
            chunk = client_socket.recv(HEADER_SIZE)
            if not chunk:
                raise ClientDisconnected()
            if len(chunk) < HEADER_SIZE:
                chunks.append(chunk)
                continue
            break
        return int.from_bytes(chunk[:2], "big")

    def _receive(self, client_socket, address):
        msg_size = self._get_msg_size(client_socket)
        print(f"Total message size is {msg_size}")
        chunks = []
        bytes_recd = 0
        while bytes_recd < msg_size:
            chunk = client_socket.recv(min((msg_size - bytes_recd), 1024))
            if not chunk:
                raise ClientDisconnected()
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)


def main():
    server = Server('localhost', 5555)
    server.serve()


if __name__ == "__main__":
    main()
