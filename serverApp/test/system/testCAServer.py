import os
import sys
# this is for app-relative absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/src")
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/src")
sys.path.append(os.getcwd())
from network.networkController.networkController import NetworkController
import threading
import unittest


def runClient():
    nc = NetworkController()
    data = nc.validateKey("asdf")


class TestCAServer(unittest.TestCase):
    def test_ddos(self):
        while (True):
            t = threading.Thread(target=runClient)
            t.start()


if __name__ == '__main__':
    unittest.main()
