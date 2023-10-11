import logging
import socket

LOG = logging.getLogger(__name__)


class Client(object):
    def __init__(self, server_ip="0.0.0.0", port=8000, buffer=1024):
        self.host = socket.gethostbyname(socket.gethostname())
        # self.host = server_ip
        self.port = port
        self.buffer = buffer
        self.server = (server_ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_host(self):
        try:
            LOG.info("Connecting to server...")
            self.socket.connect((self.host, self.port))
            LOG.info(f"Connected to: {self.host}:{self.port}")
            return True
        except Exception as e:
            LOG.error(f"Connection failed: {e}")
            return False

    def send_to_server(self, message=""):
        result = None

        while True:
            self.socket.sendto(message.encode(), self.server)
            result = self.socket.recv(self.buffer).decode()
            break

        return result

    def close_connection(self):
        self.socket.close()
