import unittest
from unittest import mock
from unittest.mock import call
from database.tables.keysTable.keysTable import KeysTable


class KTTestValidateKey(unittest.TestCase):
    def test_validateKey_root(self):
        mConnection = mock.Mock()
        mCursor = mock.Mock()
        mCursor.description = [["uak"], ["level"], "name"]
        mCursor.fetchall.return_value = [["9f3d425479559f2bf31686637433b2d7de38db19a86415b1441bab7ce08c6124:2a29ec68220047978d0091bb08aec2f6", "root", "jharod"]]
        mCursor.len.return_value = 1
        mLock = mock.Mock()
        # don't call create on construction
        with mock.patch("database.tables.keysTable.keysTable.KeysTable.create"):
            table = KeysTable(mConnection, mCursor, mLock)

        result = table.validateKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC")

        self.assertEqual(result, "root")
        self.assertEqual(mCursor.execute.assert_has_calls([call("SELECT * FROM 'keys';")]), None)
        self.assertFalse(mConnection.commit.called)
        self.assertTrue(mLock.acquire.called)
        self.assertTrue(mLock.release.called)


if __name__ == '__main__':
    unittest.main()
