import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import patch
from database.tables.table.table import Table


@patch("builtins.print")
@patch("database.tables.table.table.Table.create")
class TestSet(unittest.TestCase):
    def prepTable(self):
        self.mCursor = mock.Mock()
        self.mCursor.description = [["id"], ["name"], ["address"], ["city"], ["state"], ["zip"], ["status"]]
        self.mCursor.fetchall.return_value = [["000000000", "b", "c", "d", "e", "f"], ["7777777", "v", "w", "x", "y", "z"]]
        self.mCursor.len.return_value = 2

        self.mConnection = mock.Mock()

        self.mLock = mock.Mock()

        Table.__abstractmethods__ = frozenset()

        self.table = Table(self.mConnection, self.mCursor, self.mLock, "members table")

    def test_set_good(self, mCreate, mPrint):
        self.prepTable()

        result = self.table.set("000000000", {"id": "000000001", "name": "archive", "address": "addr", "city": "cat", "state": "dog", "zip": "lizard", "status": "banned"})

        expectedCalls = [call("SELECT * FROM 'members table';"),
                         call("UPDATE 'members table' SET id=:id, name=:name, address=:address, city=:city, state=:state, zip=:zip, status=:status WHERE id=:selectorId;", {'id': '000000001', 'name': 'archive', 'address': 'addr', 'city': 'cat', 'state': 'dog', 'zip': 'lizard', 'status': 'banned', 'selectorId': '000000000'})]
        self.assertEqual(result, {"error": "No error", "result": None})
        self.assertEqual(self.mCursor.execute.assert_has_calls(expectedCalls), None)
        self.assertTrue(self.mConnection.commit.called)
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)

    def test_set_duplicateId(self, mCreate, mPrint):
        self.prepTable()

        result = self.table.set("000000000", {"id": "000000000", "name": "archive", "address": "addr", "city": "cat", "state": "dog", "zip": "lizard", "status": "banned"})

        self.assertEqual(result, {"error": "Error: attempted to reuse a unique ID", "result": None})
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)

    def test_set_unknownError(self, mCreate, mPrint):
        self.prepTable()
        self.mCursor.execute.side_effect = Exception

        result = self.table.set("000000000", {"id": "000000001", "name": "archive", "address": "addr", "city": "cat", "state": "dog", "zip": "lizard", "status": "banned"})

        self.assertEqual(result, {"error": "Error: unknown error", "result": None})
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)
