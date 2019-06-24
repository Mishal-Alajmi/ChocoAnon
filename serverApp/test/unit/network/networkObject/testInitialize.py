import unittest
from network.networkObject.networkObject import NetworkObject


class TestInitialize(unittest.TestCase):
    def test_initialize_withStrPayload(self):
        no = NetworkObject("a", "b", "c", "d", "e")

        no.initialize('{"key": "v", "error": "w", "command": "x", "payload": "y", "table": "z"}')

        self.assertEqual(no.key, "v")
        self.assertEqual(no.error, "w")
        self.assertEqual(no.command, "x")
        self.assertEqual(no.payload, "y")
        self.assertEqual(no.table, "z")

    def test_initialize_withDictPayload(self):
        no = NetworkObject("a", "b", "c", "d", "e")

        no.initialize('{"key": "v", "error": "w", "command": "x", "payload": {"aKey":"aVal", "bKey":"bVal"}, "table": "z"}')

        self.assertEqual(no.key, "v")
        self.assertEqual(no.error, "w")
        self.assertEqual(no.command, "x")
        self.assertEqual(no.payload, {"aKey": "aVal", "bKey": "bVal"})
        self.assertEqual(no.table, "z")


if __name__ == '__main__':
    unittest.main()
