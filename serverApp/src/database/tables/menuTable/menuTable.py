import constants.consts as consts
from database.tables.table.table import Table


class MenuTable(Table):
    def __init__(self, connection, cursor, lock):
        super().__init__(connection, cursor, lock, consts.MENU_TABLE)
        self.create()

    """
    Contains all of the services members can purchase
    services have the following key/value pairs:
        code: a unique string, serves as the entry's primary key
        name
        fee: integer, should be in cents
    no other keys should be defined and all of these keys must be defined
    """
    def create(self):
        self.lock.acquire()
        try:
            command = "CREATE TABLE IF NOT EXISTS '" + self.tableName + "' (" +\
                      "id TEXT PRIMARY KEY, " +\
                      "name TEXT, " +\
                      "fee TEXT)"
            self.cursor.execute(command)
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": None}
        finally:
            self.lock.release()
