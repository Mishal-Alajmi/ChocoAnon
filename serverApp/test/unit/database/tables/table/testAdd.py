import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import patch
from database.tables.table.table import Table


@patch("database.tables.table.table.Table.create")
@patch("database.tables.table.table.Table.create")
class TestAdd(unittest.TestCase):
    def prepTable(self):
        self.mCursor = mock.Mock()
        self.mCursor.description = [["id"], ["name"], ["address"], ["city"], ["state"], ["zip"], ["status"]]
        self.mCursor.fetchall.return_value = [["88888888", "b", "c", "d", "e", "f"], ["7777777", "v", "w", "x", "y", "z"]]
        self.mCursor.len.return_value = 2

        self.mConnection = mock.Mock()

        self.mLock = mock.Mock()

        Table.__abstractmethods__ = frozenset()

        self.table = Table(self.mConnection, self.mCursor, self.mLock, "members table")

    def test_add_good(self, tableCreate, mStdOutWrite):
        self.prepTable()

        result = self.table.add({"id": "000000000", "name": "jharod", "address": "asd", "city": "port", "state": "or", "zip": "12345", "status": "banned"})

        self.assertEqual(result, {"error": "No error", "result": None})
        self.assertEqual(self.mCursor.execute.assert_has_calls([call("SELECT * FROM 'members table'"), call("INSERT INTO 'members table' ('id', 'name', 'address', 'city', 'state', 'zip', 'status') VALUES ('000000000', 'jharod', 'asd', 'port', 'or', '12345', 'banned');")]), None)
        self.assertTrue(self.mConnection.commit.called)
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)

    def test_add_incomplete(self, tableCreate, mStdOutWrite):
        self.prepTable()
        self.mCursor.execute.side_effect = KeyError

        result = self.table.add({"id": "000000000", "name": "jharod", "address": "asd", "city": "port", "state": "or", "zip": "12345", "status": "banned"})

        self.assertEqual(result, {"error": "Error: failed to add entry to database due to incomplete data", "result": None})
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)

    def test_add_duplicate(self, tableCreate, mStdOutWrite):
        self.prepTable()

        result = self.table.add({"id": "88888888", "name": "jharod", "address": "asd", "city": "port", "state": "or", "zip": "12345", "status": "banned"})

        self.assertEqual(result, {"error": "Error: attempted to reuse a unique ID", "result": None})
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)

    def test_add_unknownError(self, tableCreate, mStdOutWrite):
        self.prepTable()
        self.mCursor.execute.side_effect = Exception

        result = self.table.add({"id": "000000000", "name": "jharod", "address": "asd", "city": "port", "state": "or", "zip": "12345", "status": "banned"})

        self.assertEqual(result, {"error": "Error: unknown error", "result": None})
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)
