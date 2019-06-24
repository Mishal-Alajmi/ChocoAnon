import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import patch
from database.tables.table.table import Table


@patch("builtins.print")
@patch("database.tables.table.table.Table.create")
class TestGetAll(unittest.TestCase):
    def prepTable(self):
        self.mCursor = mock.Mock()
        self.mCursor.fetchall.return_value = [["a", "b", "c", "d", "e", "f"], ["u", "v", "w", "x", "y", "z"]]
        self.mCursor.description = [["id"], ["name"], ["address"], ["city"], ["state"], ["zip"]]
        self.mCursor.len.return_value = 2

        self.mConnection = mock.Mock()

        self.mLock = mock.Mock()

        Table.__abstractmethods__ = frozenset()

        self.table = Table(self.mConnection, self.mCursor, self.mLock, "members table")

    def test_getAll_good(self, mCreate, mPrint):
        self.prepTable()

        result = self.table.getAll()

        self.assertEqual(result, {"error": "No error", "result": [{"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}, {"id": "u", "name": "v", "address": "w", "city": "x", "state": "y", "zip": "z"}]})
        self.assertEqual(self.mCursor.execute.assert_has_calls([call("SELECT * FROM 'members table';")]), None)
        self.assertFalse(self.mConnection.commit.called)
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)
