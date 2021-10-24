import socket
import time
import argparse

HOST = 'localhost'
PORT = 5555
HEADER_SIZE = 2


class Client:
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._name = name
        self._client_socket = None

    def connect(self):
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._client_socket.connect((self._host, self._port))
        except ConnectionRefusedError as e:
            print("Cannot connect to the server!")
            return
        print(f"Client is connected to: {(HOST, PORT)}")
        self._send_name()

    def close(self):
        self._client_socket.close()
        print("Client is closed!")

    def _send_name(self):
        self._send(self._create_msg(self._name))

    def _send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self._client_socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def _send_all(self, msg):
        self._client_socket.sendall(msg)

    def _create_msg(self, msg):
        msg = bytearray(msg.encode())
        header = len(msg).to_bytes(HEADER_SIZE, byteorder='big')
        ba_header = bytearray(header)
        return ba_header + msg


def main():
    args = parse_args()
    client = Client(HOST, PORT, args.name)
    client.connect()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    return parser.parse_args()


if __name__ == "__main__":
    main()
