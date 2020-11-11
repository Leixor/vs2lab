import rpc
import logging

from context import lab_logging
import time


def handle_append(result_list):
    print("Result: {}".format(result_list.value))


lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, handle_append)
print("Append function called!")

for x in range(1, 15):
    time.sleep(1)
    print("%d seconds passed." % x)

cl.stop()

