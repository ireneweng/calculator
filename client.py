import logging
import socket

LOG = logging.getLogger(__name__)


class Client(object):
    """Simple client class."""

    def __init__(
        self, server_ip: str = "0.0.0.0", port: int = 8000, buffer: int = 1024
    ):
        # self.host = socket.gethostbyname(socket.gethostname())
        self.host = server_ip
        self.port = port
        self.buffer = buffer
        self.server = (server_ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_host(self) -> None:
        """Attempts a connection to the server."""
        try:
            LOG.info("Connecting to server...")
            self.socket.connect((self.host, self.port))
            LOG.info(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            LOG.error(f"Connection failed: {e}")
            return False

    def send_to_server(self, message: str) -> str:
        """Sends the given message to the server and receives a return message."""
        result = None

        while True:
            LOG.info(f"Sending: {message}")
            self.socket.sendall(message.encode())
            result = self.socket.recv(self.buffer).decode()
            break

        LOG.info(f"Received: {result}")
        return result

    def close_connection(self) -> None:
        """Closes the socket connection."""
        self.socket.close()
        LOG.info("Closed connection")
