import constants.consts as consts
from database.tables.table.table import Table
import uuid
import hashlib


class KeysTable(Table):
    def __init__(self, connection, cursor, lock):
        super().__init__(connection, cursor, lock, consts.KEYS_TABLE)
        self.create()

    """
    Contains all of the keys authorized to access the database
    each entry has the following keys:
        id: hash of the unique access key
        level: KEY_ROOT or KEY_PROVIDER
        name: name of the person/org who owns this key
    """
    def create(self):
        self.lock.acquire()
        try:
            command = "CREATE TABLE IF NOT EXISTS '" + self.tableName + "' (" +\
                      "id TEXT PRIMARY KEY, " +\
                      "level TEXT, " +\
                      "name TEXT)"
            self.cursor.execute(command)
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": ""}
        finally:
            self.lock.release()

    # assumes id is an unhashed uak
    def add(self, entry):
        if "id" in entry:
            salt = uuid.uuid4().hex
            hash = hashlib.sha256(salt.encode() + entry["id"].encode()).hexdigest() + ':' + salt
            entry["id"] = hash
        return super(KeysTable, self).add(entry)

    # entryId can be an unhashed uak or a hashed id
    def get(self, entryId):
        entry = self.locateEntry(entryId)
        print(entry)

        if entry["error"] == consts.NO_ERROR:
            result = super(KeysTable, self).get(entry["result"]["id"])
        else:
            result = super(KeysTable, self).get(entryId)
        return result

    # because the primary key is hashed and salted, and entryId is unhashed, we have to retrieve all of the keys and iterate over them
    def locateEntry(self, unhashedUak):
        self.lock.acquire()
        try:
            # first figure out which entry in the table is the target one
            command = "SELECT * FROM '" + self.tableName + "';"
            self.cursor.execute(command)

            rows = self.cursor.fetchall()
            entry = {}
            found = False
            for i in range(len(rows)):
                password, salt = rows[i][0].split(":")
                if password == hashlib.sha256(salt.encode() + unhashedUak.encode()).hexdigest():
                    for j in range(len(rows[i])):
                        entry[self.cursor.description[j][0]] = rows[i][j]
                        found = True
            if not found:
                return {"error": consts.ERROR_NONEXISTENT_ENTRY, "result": {"id": ""}}
            else:
                return {"error": consts.NO_ERROR, "result": entry}
        finally:
            self.lock.release()

    # note that selector can be either a hashed id or an unhashed uak
    def remove(self, entryId):
        entry = self.locateEntry(entryId)
        if entry["error"] == consts.NO_ERROR:
            return super(KeysTable, self).remove(entry["result"]["id"])
        else:
            return super(KeysTable, self).remove(entryId)

    # entryId can be an unhashed uak or a hashed id
    def set(self, entryId, dict):
        # don't store unhashed keys
        if "id" in dict:
            salt = uuid.uuid4().hex
            hash = hashlib.sha256(salt.encode() + dict["id"].encode()).hexdigest() + ':' + salt
            dict.pop("id")
            dict["id"] = hash

        entry = self.locateEntry(entryId)
        if entry["error"] == consts.NO_ERROR:
            return super(KeysTable, self).set(entry["result"]["id"], dict)
        else:
            return super(KeysTable, self).set(entryId, dict)

    def validateKey(self, uak):
        self.lock.acquire()
        level = consts.KEY_INVALID
        try:
            if uak is not None and len(uak) != 0:
                command = "SELECT * FROM '" + self.tableName + "';"
                self.cursor.execute(command)
                rows = self.cursor.fetchall()

                if (len(rows) > 0):
                    for i in range(len(rows)):
                        password, salt = rows[i][0].split(":")
                        if password == hashlib.sha256(salt.encode() + uak.encode()).hexdigest():
                            level = rows[i][1]
        except Exception as e:
            print(e)
        finally:
            self.lock.release()
            return level
