import constants.consts as consts
from database.tables.table.table import Table
import datetime


class ServicesTable(Table):
    def __init__(self, connection, cursor, lock):
        super().__init__(connection, cursor, lock, consts.SERVICES_TABLE)
        self.create()

    """
    Contains all of the services that have been purchased
    services have the following key/value pairs:
        id: a unique string, serves as the entry's primary key
        code: the 6 digit service code
        date: date the service was purchased
        provider: the id of the provider who sold the service
        member: the id of the member who bought the service
        received: date and time the server received the purchase notification
        comment: arbitrary text
        status: consts.STATUS_PAID or consts.STATUS_UNPAID
    no other keys should be defined and all of these keys must be defined
    """
    def create(self):
        self.lock.acquire()
        try:
            command = "CREATE TABLE IF NOT EXISTS '" + consts.SERVICES_TABLE + "' (" +\
                      "id TEXT PRIMARY KEY, " +\
                      "code TEXT, " +\
                      "date TEXT, " +\
                      "provider TEXT, " +\
                      "member TEXT, " +\
                      "received TEXT, " +\
                      "comment TEXT, " +\
                      "status TEXT)"
            self.cursor.execute(command)
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": None}
        finally:
            self.lock.release()

    # inject a received timestamp
    def add(self, dict):
        dict["received"] = str(datetime.datetime.now())
        return super(ServicesTable, self).add(dict)
