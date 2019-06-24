import constants.consts as consts
from database.tables.table.table import Table
import hashlib


class AdminsTable(Table):
    def __init__(self, connection, cursor, lock):
        super().__init__(connection, cursor, lock, consts.ADMINS_TABLE)
        self.create()

    """
    Contains all of the admins authorized to read/write to all databases
    each entry has the following keys:
        id: guid
        uak: hash of the unique access key
        admin name
    """
    def create(self):
        self.lock.acquire()
        try:
            command = "CREATE TABLE IF NOT EXISTS '" + self.tableName + "' (" +\
                      "id TEXT PRIMARY KEY, " +\
                      "name TEXT, " +\
                      "uak TEXT)"
            self.cursor.execute(command)
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": ""}
        finally:
            self.lock.release()

    def validateKey(self, key):
        self.lock.acquire()
        try:
            if key is None:
                return False
            else:
                # get all of the hashed keys and check our key against them until a match is found
                command = "SELECT * from '" + self.tableName + "';"
                self.cursor.execute(command)
                results = self.cursor.fetchall()
                for result in results:
                    hashedKey = result[2]
                    password, salt = hashedKey.split(":")
                    if password == hashlib.sha256(salt.encode() + key.encode()).hexdigest():
                        return True
                if (len(results) >= 1):
                    return True
            return False

        finally:
            self.lock.release()
