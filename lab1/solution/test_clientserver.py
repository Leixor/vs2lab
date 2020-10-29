import logging
import threading
import unittest

import server
import client
from context import lab_logging
from database import dictionaryList

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    _server = server.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = client.Client()  # create new client for each test

    def test_server_get(self):
        name = "Ute"

        msg = self.client.get(name)

        data = msg.get('data')
        type = msg.get('type')

        self.assertEqual(type, 'SUCCESS')

        self.assertEqual(list(data.keys())[0], name)
        self.assertEqual(dictionaryList.get(name), data.get(name))

    def test_server_get_all(self):
        msg = self.client.get_all()
        self.assertEqual(msg.get('data'), dictionaryList)

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop
        cls._server_thread.join()  # wait for server thread to terminate

if __name__ == '__main__':
    unittest.main()
