import logging
import socket
import json

from . import constCS
from .context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class Client:
    logger = logging.getLogger("vs2lab.a1_layers.client.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constCS.HOST, constCS.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def get(self, name: str):
        self.logger.info("GET: " + name)
        return self.__handle_request("GET", name)

    def get_all(self):
        self.logger.info("GET_ALL")
        return self.__handle_request("GET_ALL", "")

    def __handle_request(self, request: str, name: str):
        msg = {
            "type": request,
            "name": name
        }
        self.sock.send(json.dumps(msg).encode('utf-8'))
        self.logger.info("sent Request: " + str(msg))
        data = self.sock.recv(1024)
        self.logger.info("received data: " + str(data))
        msg_out = json.loads(data.decode('utf-8'))
        return msg_out

    def close(self):
        self.sock.close()
        self.logger.info("Client down.")
