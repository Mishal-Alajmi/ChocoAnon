import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import patch
from database.tables.table.table import Table


@patch("builtins.print")
@patch("database.tables.table.table.Table.create")
class TestRemove(unittest.TestCase):
    def prepTable(self):
        self.mCursor = mock.Mock()

        self.mConnection = mock.Mock()

        self.mLock = mock.Mock()

        Table.__abstractmethods__ = frozenset()

        self.table = Table(self.mConnection, self.mCursor, self.mLock, "members table")

    def test_remove(self, mCreate, mPrint):
        self.prepTable()

        result = self.table.remove("000000000")

        self.assertEqual(result, {"error": "No error", "result": None})
        self.assertEqual(self.mCursor.execute.assert_has_calls([call("DELETE FROM 'members table' WHERE id = ?1;", ("000000000", ))]), None)
        self.assertTrue(self.mConnection.commit.called)
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)
