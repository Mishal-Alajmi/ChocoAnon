import unittest
from unittest import mock
from client.client import Client
from unittest.mock import patch


@patch("sys.stdout")
class TestInit(unittest.TestCase):
    def test_init(self, mStdout):
        mSocket = mock.Mock()
        mDbc = mock.Mock()

        Client(mSocket, mDbc)

        mStdout.assert_has_calls([
            mock.call.write("[+] Client connected"),
            mock.call.write('\n')
        ])


if __name__ == '__main__':
    unittest.main()
