import rpc
import logging

from context import lab_logging
import threading

def handle_append(result_list):
    print("Result: {}".format(result_list.value))

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, handle_append)

cl.stop()

