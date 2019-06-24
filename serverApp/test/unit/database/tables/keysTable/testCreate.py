import unittest
from unittest import mock
from unittest.mock import patch
from database.tables.keysTable.keysTable import KeysTable


class KTTestCreate(unittest.TestCase):
    def test_create(self):
        mConnection = mock.Mock()
        mCursor = mock.Mock()
        mLock = mock.Mock()
        # don't call create on construction, needs to be context manager so create() can be called later
        with mock.patch("database.tables.keysTable.keysTable.KeysTable.create"):
            table = KeysTable(mConnection, mCursor, mLock)

        table.create()

        self.assertEqual(mCursor.execute.assert_called_with("CREATE TABLE IF NOT EXISTS 'keys' (id TEXT PRIMARY KEY, level TEXT, name TEXT)"), None)
        self.assertTrue(mConnection.commit.called)
        self.assertTrue(mLock.acquire.called)
        self.assertTrue(mLock.release.called)


if __name__ == '__main__':
    unittest.main()
