import constants.consts as consts
from database.tables.table.table import Table


class MembersTable(Table):
    def __init__(self, connection, cursor, lock):
        super().__init__(connection, cursor, lock, consts.MEMBERS_TABLE)
        self.create()

    """
    Contains all of the members registered with ChocAn
    members have the following key/value pairs:
        id: a unique string, serves as the entry's primary key
        name
        address
        city
        state
        zip
        status (either consts.STATUS_BANNED or consts.STATUS_UNBANNED)
    no other keys should be defined and all of these keys must be defined
    """
    def create(self):
        self.lock.acquire()
        try:
            command = "CREATE TABLE IF NOT EXISTS '" + self.tableName + "' (" +\
                      "id TEXT PRIMARY KEY, " +\
                      "name TEXT, " +\
                      "address TEXT, " +\
                      "city TEXT, " +\
                      "state TEXT, " +\
                      "zip TEXT, " +\
                      "status TEXT)"
            self.cursor.execute(command)
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": None}
        finally:
            self.lock.release()
