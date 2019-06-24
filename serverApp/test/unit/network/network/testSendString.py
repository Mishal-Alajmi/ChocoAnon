import unittest
from unittest.mock import call
from unittest.mock import patch
from network.network.network import Network


@patch("ssl.wrap_socket")
@patch("socket.socket")
@patch("ssl.SSLSocket")
class TestSendString(unittest.TestCase):
    def test_sendString_good(self, mSslSocket, mSocket, mWrapSocket):
        mWrapSocket.return_value.recv.return_value = b'{"key": "v", "error": "w", "command": "x", "payload": "y", "table": "z"}\0'
        network = Network()

        result = network.sendString("asdf")

        self.assertEqual(mWrapSocket.return_value.send.assert_has_calls([call()(b"asdf\0")]), None)
        self.assertEqual(result.key, "v")
        self.assertEqual(result.error, "w")
        self.assertEqual(result.command, "x")
        self.assertEqual(result.payload, "y")
        self.assertEqual(result.table, "z")

    def test_sendString_connectionRefused(self, mSslSocket, mSocket, mWrapSocket):
        mWrapSocket.return_value.recv.side_effect = ConnectionRefusedError
        network = Network()

        result = network.sendString("asdf")

        self.assertTrue(network.noServer)
        self.assertEqual(result.key, None)
        self.assertEqual(result.error, "Error: could not establish a connection")
        self.assertEqual(result.command, None)
        self.assertEqual(result.payload, None)
        self.assertEqual(result.table, None)


if __name__ == '__main__':
    unittest.main()
