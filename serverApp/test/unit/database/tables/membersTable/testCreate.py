import unittest
from unittest import mock
from database.tables.membersTable.membersTable import MembersTable


class MTTestCreate(unittest.TestCase):
    def test_create(self):
        mConnection = mock.Mock()
        mCursor = mock.Mock()
        mLock = mock.Mock()
        # don't call create on construction
        with mock.patch("database.tables.membersTable.membersTable.MembersTable.create"):
            table = MembersTable(mConnection, mCursor, mLock)

        table.create()

        self.assertTrue(mConnection.commit.called)
        self.assertEqual(mCursor.execute.assert_called_with("CREATE TABLE IF NOT EXISTS 'members' (id TEXT PRIMARY KEY, name TEXT, address TEXT, city TEXT, state TEXT, zip TEXT, status TEXT)"), None)
        self.assertTrue(mLock.acquire.called)
        self.assertTrue(mLock.release.called)


if __name__ == '__main__':
    unittest.main()
