import unittest
from unittest import mock
from client.client import Client
from unittest.mock import patch


@patch("builtins.print")
@patch("socket.socket")
@patch("database.databaseController.databaseController.DatabaseController")
@patch("network.networkObject.networkObject.NetworkObject")
class TestParseNetworkObject(unittest.TestCase):
    def test_parseNetworkObject_noError(self, mSocket, mDbc, mNo, mPrint):
        mDbc.execute.return_value = {"error": "No error", "result": "test result"}
        client = Client(mSocket, mDbc)

        no = client.parseNetworkObject(mNo)

        self.assertEqual(no.error, "No error")
        self.assertEqual(no.command, "no command")
        self.assertEqual(no.table, "no table")
        self.assertEqual(no.key, "")
        self.assertEqual(no.payload, "test result")

    def test_parseNetworkObject_errorUnknown(self, mSocket, mDbc, mNo, mPrint):
        mDbc.execute.return_value = {"error": "Error unknown", "result": ""}
        client = Client(mSocket, mDbc)

        no = client.parseNetworkObject(mNo)

        self.assertEqual(no.error, "Error unknown")
        self.assertEqual(no.command, "no command")
        self.assertEqual(no.table, "no table")
        self.assertEqual(no.key, "")
        self.assertEqual(no.payload, {})

    def test_parseNetworkObject_invalidCommand(self, mSocket, mDbc, mNo, mPrint):
        mDbc.execute.return_value = {"error": "Error: invalid command", "result": "test result"}
        client = Client(mSocket, mDbc)

        no = client.parseNetworkObject(mNo)

        self.assertEqual(no.error, "Error: invalid command")
        self.assertEqual(no.command, "no command")
        self.assertEqual(no.table, "no table")
        self.assertEqual(no.key, "")
        self.assertEqual(no.payload, {})

    def test_parseNetworkObject_unauthorizedOperation(self, mSocket, mDbc, mNo, mPrint):
        mDbc.execute.return_value = {"error": "Error: operation requires higher authorization level", "result": "test result"}
        client = Client(mSocket, mDbc)

        no = client.parseNetworkObject(mNo)

        self.assertEqual(no.error, "Error: operation requires higher authorization level")
        self.assertEqual(no.command, "no command")
        self.assertEqual(no.table, "no table")
        self.assertEqual(no.key, "")
        self.assertEqual(no.payload, {})


if __name__ == '__main__':
    unittest.main()
