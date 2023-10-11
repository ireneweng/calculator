import socket

from calculator import Calculator


class Server(object):
    """Simple server class."""

    def __init__(self, port: int = 8000, buffer: int = 1024):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.buffer = buffer
        self.connection = None
        self.address = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self) -> None:
        """Binds the socket and waits for an incoming connection."""
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.connection, self.address = self.socket.accept()

    def run(self, class_inst: object) -> None:
        """
        Runs the given class on the server.
        Assumes the class includes a run() function and accepts a string input.
        """
        self.bind()

        while True:
            # receive data
            data = self.connection.recv(self.buffer).decode()
            if not data:
                break
            print(f"Received: {data}")

            # execute class - assumes there is a run function
            result = class_inst.run(data)

            # send result to client
            self.connection.send(str(result).encode())
            print(f"Sent: {result}")

        # close connection
        self.connection.close()
        print("Closed connection")


def main():
    server = Server()
    server.run(Calculator())


if __name__ == "__main__":
    main()
