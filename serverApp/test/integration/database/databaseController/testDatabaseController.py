import unittest
from network.network.network import Network
import constants.consts as consts
import json


# these integration tests require a running CAServer
# AS62ELRB5F0709LERPHZD06JWC0P8QSC should be a root key in the database
# DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3 should be a provider key in the database
class TestDatabaseController(unittest.TestCase):
    def test_sqlInjection(self):
        network = Network()
        key = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"

        no = {
            "error": consts.NO_ERROR,
            "command": "get",
            "table": consts.MEMBERS_TABLE,
            "key": key,
            "payload": "00000';DROP TABLE members;"
        }

        response = network.sendString(json.dumps(no))
        # unfinished

if __name__ == '__main__':
    unittest.main()
