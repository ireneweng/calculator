import socket

from calculator import Calculator


class Server(object):
    def __init__(self, port=8000, buffer=1024):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.buffer = buffer
        self.connection = None
        self.address = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.calculator = Calculator()

    def bind(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.connection, self.address = self.socket.accept()

    def run(self):
        self.bind()

        while True:
            # receive data
            data = self.connection.recv(self.buffer).decode()
            if not data:
                break
            print(f"Input: {data}")

            # compute calculation
            result, success = self.calculator.run(data)

            # print result to console
            console_msg = f"Output: {result}" if success else result
            print(console_msg)

            # send result to client
            self.connection.send(result.encode())

        # close connection
        print("Closing connection.")
        self.connection.close()


if __name__ == "__main__":
    server = Server()
    server.run()
