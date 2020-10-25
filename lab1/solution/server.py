import logging
import socket
import json
import traceback

import constCS
import database

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class Server:
    logger = logging.getLogger("vs2lab.a1_layers.server.Server")
    _serving = True

    def __init__(self, port=None):
        print(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((constCS.HOST, port or constCS.PORT))
        self.sock.settimeout(3)

    def serve(self):
        self.sock.listen(1)
        while self._serving:
            self.logger.info("new serve loop")
            try:
                (connection, address) = self.sock.accept()
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break

                    self.logger.info("received data: " + str(data))

                    msg_obj = json.loads(data.decode('utf-8'))
                    msg_type = msg_obj["type"]
                    name = msg_obj["name"]

                    reply = {}
                    if msg_type == "GET_ALL":
                        self.__handle_get_all(reply)
                    elif msg_type == "GET":
                        self.__handle_get(name, reply)

                    self.logger.info("reply: " + str(reply))
                    connection.send(json.dumps(reply).encode('utf-8'))
                    self.logger.info("reply sent")
                connection.close()
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self.logger.info("Server down")

    @staticmethod
    def __handle_get_all(reply):
        reply["type"] = "SUCCESS"
        reply["data"] = database.find_all()

    @staticmethod
    def __handle_get(name, reply):
        if not name:
            reply["type"] = "ERROR"
            reply["msg"] = "No name provided"
            return

        answer = database.find(name)
        if answer:
            reply["type"] = "SUCCESS"
        else:
            reply["type"] = "ERROR"
            reply["msg"] = "Name not found in Database"

        reply["data"] = answer

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    Server(12312).serve()