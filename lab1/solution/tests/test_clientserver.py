import logging
import threading
import unittest
import json

from .. import server
from .. import client
from .context import lab_logging

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

    def test_server_get(self):  # each test_* function is a test
        msg = self.client.get("Ute")
        self.assertEqual(msg.get('type'), 'SUCCESS')
        self.assertEqual(msg.get('data'), {'Ute': 2860968})

    def test_server_get_all(self):  # each test_* function is a test
        msg = self.client.getall()
        self.assertEqual(msg, '2')

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop
        cls._server_thread.join()  # wait for server thread to terminate

if __name__ == '__main__':
    unittest.main()
