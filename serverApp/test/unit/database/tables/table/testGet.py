import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import patch
from database.tables.table.table import Table


@patch("builtins.print")
@patch("database.tables.table.table.Table.create")
class TestGet(unittest.TestCase):
    def prepTable(self):
        self.mCursor = mock.Mock()
        self.mCursor.description = [["id", None, None, None, None, None, None], ["name", None, None, None, None, None, None], ["uak", None, None, None, None, None, None]]
        self.mCursor.fetchall.return_value = [["000000000", "jharod", "asdfhkgasdfasdfghkasdfghkasdfghkasdfghkasdfhk"]]
        self.mCursor.len.return_value = 1

        self.mConnection = mock.Mock()

        self.mLock = mock.Mock()

        Table.__abstractmethods__ = frozenset()

        self.table = Table(self.mConnection, self.mCursor, self.mLock, "members table")

    def test_get_good(self, mCreate, mPrint):
        self.prepTable()

        result = self.table.get("000000000")

        self.assertEqual(result, {"error": "No error", "result": {"id": "000000000", "name": "jharod", "uak": "asdfhkgasdfasdfghkasdfghkasdfghkasdfghkasdfhk"}})
        self.assertEqual(self.mCursor.execute.assert_has_calls([call("SELECT * FROM 'members table' WHERE id = ?1;", ("000000000", ))]), None)
        self.assertFalse(self.mConnection.commit.called)
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)

    def test_get_nonexistent(self, mCreate, mPrint):
        self.prepTable()
        self.mCursor.fetchall.return_value = []
        self.mCursor.len.return_value = 0

        result = self.table.get("000000000")

        self.assertEqual(result, {"error": "Error: unable to retrieve nonexistent entry from database", "result": None})
        self.assertEqual(self.mCursor.execute.assert_has_calls([call("SELECT * FROM 'members table' WHERE id = ?1;", ("000000000", ))]), None)
        self.assertFalse(self.mConnection.commit.called)
        self.assertTrue(self.mLock.acquire.called)
        self.assertTrue(self.mLock.release.called)
