import socket

import sympy


class Server(object):
    def __init__(self, port=8000, buffer=1024):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.buffer = buffer
        self.connection = None
        self.address = None

    def instantiate_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.instantiate_socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.connection, self.address = self.socket.accept()

    def run(self):
        self.bind()

        while True:
            data = self.connection.recv(self.buffer).decode()
            print("Input: ", data)
            if not data:
                break
            result = float(sympy.sympify(str(data)))
            self.connection.send(str(result).encode())

        self.connection.close()


if __name__ == "__main__":
    server = Server()
    server.run()
