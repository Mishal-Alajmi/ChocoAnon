import unittest
from unittest import mock
from database.tables.servicesTable.servicesTable import ServicesTable
import constants.consts as consts


class STTestCreate(unittest.TestCase):
    def test_create(self):
        mConnection = mock.Mock()
        mCursor = mock.Mock()
        mLock = mock.Mock()
        # don't call create on construction
        with mock.patch("database.tables.servicesTable.servicesTable.ServicesTable.create"):
            table = ServicesTable(mConnection, mCursor, mLock)

        table.create()

        self.assertTrue(mCursor.execute.called)
        self.assertEqual(mCursor.execute.assert_called_with("CREATE TABLE IF NOT EXISTS 'services' (id TEXT PRIMARY KEY, code TEXT, date TEXT, provider TEXT, member TEXT, received TEXT, comment TEXT, status TEXT)"), None)
        self.assertTrue(mConnection.commit.called)
        self.assertTrue(mLock.acquire.called)
        self.assertTrue(mLock.release.called)


if __name__ == '__main__':
    unittest.main()
