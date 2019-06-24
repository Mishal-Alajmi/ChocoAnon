import unittest
from network.network.network import Network
from unittest import mock
from unittest.mock import call
from unittest.mock import patch


@patch("ssl.wrap_socket")
@patch("network.networkObject.networkObject.NetworkObject")
@patch("socket.socket")
@patch("ssl.SSLSocket")
@patch("network.network.network.Network.sendString")
class TestSendNetworkObject(unittest.TestCase):
    def test_sendNetworkObject_good(self, mSendString, mSslSocket, mSocket, mNetworkObject, mWrapSocket):
        mSendString.return_value = "abcde"
        no = mock.Mock()
        no.serialize.return_value = "asdf"
        network = Network()

        result = network.sendNetworkObject(no)

        expectedCalls = [call().sendString("asdf")]
        self.assertEqual(mSendString.assert_has_calls(expectedCalls), None)
        self.assertEqual(result, "abcde")


if __name__ == '__main__':
    unittest.main()
