import unittest
from network.networkObject.networkObject import NetworkObject


class TestSerialize(unittest.TestCase):
    def test_serialize_withStrPayload(self):
        no = NetworkObject("a", "b", "c", "d", "e")

        result = no.serialize()

        self.assertEqual(result, '{"error": "b", "command": "c", "key": "a", "table": "e", "payload": "d"}')

    def test_serialize_withDictPayload(self):
        no = NetworkObject("a", "b", "c", {"aKey": "aVal"}, "e")

        result = no.serialize()

        # don't know why the double backslashes are present, but the test doesn't function without them
        self.assertEqual(result, '{"error": "b", "command": "c", "key": "a", "table": "e", "payload": "{\\"aKey\\": \\"aVal\\"}"}')


if __name__ == '__main__':
    unittest.main()
