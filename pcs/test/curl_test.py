from __future__ import (
    absolute_import,
    division,
    print_function,
)

# This module is intented to just test new Communicator/MultiringCommunicator
# classes which are using curllib

import os.path
import sys
import pprint
import logging

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PACKAGE_DIR)

from pcs.common.node_communicator import Request, RequestData, RequestTarget
from pcs import utils

logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger = logging.getLogger("old_cli")
logger.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)

global_target = RequestTarget(
    "TestServer", ["httpbin.org2", "httpbin.org"], port=443
)

pprint.pprint(global_target)

def get_request(timeout):
    return Request(global_target, RequestData("delay/{0}".format(timeout)))

lib_env = utils.get_lib_env()
# utils.pcs_options["--debug"] = True
request_list = [get_request((i + 1) * 2) for i in range(6)]
factory = lib_env.get_node_communicator_factory()
factory._request_timeout = 10
communicator = factory.get_multiring_communicator()
# communicator.add_requests([get_request(10)])
# response = list(communicator.start_loop())[0]
# pprint.pprint(response.to_report_item())
communicator.add_requests(request_list)
for response in communicator.start_loop():
    # print(80 * "-")
    # print(response.request.url)
    # print(response.data)
    # print(80 * "-")
    if response.request == request_list[2]:
        r = get_request(5)
        request_list.append(r)
        communicator.add_requests([r])
    if response.request == request_list[5]:
        r = get_request(10)
        request_list.append(r)
        communicator.add_requests([r])
    if len(request_list) == 8 and response.request == request_list[7]:
        r = get_request(15)
        communicator.add_requests([r])


