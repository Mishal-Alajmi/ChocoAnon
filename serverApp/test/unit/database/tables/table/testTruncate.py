import unittest
from unittest import mock
from unittest.mock import patch
from database.tables.table.table import Table


@patch("builtins.print")
@patch("database.tables.table.table.Table.create")
class TestTruncate(unittest.TestCase):
    def prepTable(self):
        self.mCursor = mock.Mock()
        self.mCursor.description = [["id"], ["name"], ["address"], ["city"], ["state"], ["zip"], ["status"]]

        self.mConnection = mock.Mock()

        self.mLock = mock.Mock()

        Table.__abstractmethods__ = frozenset()

        self.table = Table(self.mConnection, self.mCursor, self.mLock, "members table")

    def test_truncate(self, mCreate, mPrint):
        self.prepTable()

        result = self.table.truncate()

        self.assertEqual(result, {"error": "No error", "result": None})
        self.assertEqual(self.mCursor.execute.assert_called_with("DROP TABLE IF EXISTS 'members table';"), None)
        self.assertTrue(self.mConnection.commit.called)
        self.assertTrue(mCreate.called)
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)
