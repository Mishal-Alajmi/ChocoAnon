import unittest
from unittest import mock
from database.tables.providersTable.providersTable import ProvidersTable


class PTTestCreate(unittest.TestCase):
    def test_create(self):
        mConnection = mock.Mock()
        mCursor = mock.Mock()
        mLock = mock.Mock()
        # don't call create on construction
        with mock.patch("database.tables.providersTable.providersTable.ProvidersTable.create"):
            table = ProvidersTable(mConnection, mCursor, mLock)
        table.create()

        self.assertTrue(mCursor.execute.called)
        self.assertEqual(mCursor.execute.assert_called_with("CREATE TABLE IF NOT EXISTS 'providers' (id TEXT PRIMARY KEY, name TEXT, address TEXT, city TEXT, state TEXT, zip TEXT)"), None)
        self.assertTrue(mConnection.commit.called)
        self.assertTrue(mLock.acquire.called)
        self.assertTrue(mLock.release.called)


if __name__ == '__main__':
    unittest.main()
