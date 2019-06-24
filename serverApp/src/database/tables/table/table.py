from abc import ABC, abstractmethod
import constants.consts as consts
import sqlite3
import traceback


class Table(ABC):
    # cursor should be a database cursor made with sqlite3.connect(filepath).cursor()
    # lock should be a threading.lock()
    def __init__(self, connection, cursor, lock, tableName):
        super().__init__()
        self.connection = connection
        self.cursor = cursor
        self.lock = lock
        self.tableName = tableName

    # should create an empty table
    # remember to commit at the end with self.connection.commit()
    @abstractmethod
    def create(self):
        pass

    """
    use with caution, deletes the table's contents (but not the table itself)
    """
    def truncate(self):
        try:
            self.lock.acquire()
            self.cursor.execute("DROP TABLE IF EXISTS '" + self.tableName + "';")
            self.connection.commit()

        finally:
            self.lock.release()

        self.create()

        return {"error": consts.NO_ERROR, "result": None}

    """
    entry should be a dict with the appropriate keys
    """
    def add(self, entry):
        self.lock.acquire()
        try:
            # check that service has all the appropriate keys
            self.cursor.execute("SELECT * FROM '" + self.tableName + "'")
            for col in self.cursor.description:
                if col[0] not in entry:
                    raise KeyError

            # inefficient way to avoid having to throw sqlite3.IntegrityError in the unit tests (mahmoud)
            # IndexError is builtin to the language and thus doesn't require an import
            # whereas sqlite3.IntegrityError requires an import
            # remove if performance is necessary, replace with an exception check for sqlite3.IntegrityError
            # that error will be thrown on the self.cursor.execute call if a duplicate id is used
            rows = self.cursor.fetchall()
            if (len(rows) > 0):
                for i in range(0, len(rows)):
                    if len(rows[i]) > 0:
                        if entry["id"] == rows[i][0]:
                            raise IndexError

            keys = "("
            values = "("

            for key, value in entry.items():
                isValid = False
                for col in self.cursor.description:
                    if col[0] == key:
                        isValid = True
                if isValid:
                    keys += "'"
                    keys += key
                    keys += "', "

                    values += "'"
                    values += value
                    values += "', "

            # remove the extra commas
            keys = keys[0:len(keys) - 2]
            values = values[0:len(values) - 2]

            # and close them up
            keys += ")"
            values += ")"

            command = "INSERT INTO '" + self.tableName + "' " + keys + " VALUES " + values + ";"
            self.cursor.execute(command)
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": None}

        # graceful failure, whoever called this function can figure out what to do next
        except KeyError:
            return {"error": consts.ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA, "result": None}
        except IndexError:
            # traceback.print_exc()
            return {"error": consts.ERROR_DUPLICATE_ID, "result": None}
        except Exception as e:
            # print(e)
            # print("########################################################################")
            # traceback.print_exc()
            # print("########################################################################")
            return {"error": consts.ERROR_UNKNOWN, "result": None}
        finally:
            self.lock.release()

    """
    remove an entry by its id
    """
    def remove(self, entryId):
        self.lock.acquire()
        try:
            command = "DELETE FROM '" + self.tableName + "' WHERE id = ?1;"
            self.cursor.execute(command, (entryId,))
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": None}
        finally:
            self.lock.release()

    """
    get an entry by its id
    """
    def get(self, entryId):
        self.lock.acquire()
        try:
            command = "SELECT * FROM '" + self.tableName + "' WHERE id = ?1;"
            self.cursor.execute(command, (entryId,))

            rows = self.cursor.fetchall()
            entry = {}
            if (len(rows) > 0):
                for i in range(len(rows[0])):
                    entry[self.cursor.description[i][0]] = rows[0][i]
            else:
                return {"error": consts.ERROR_NONEXISTENT_ENTRY, "result": None}
            return {"error": consts.NO_ERROR, "result": entry}
        finally:
            self.lock.release()

    """
    modify an existing entry by overwriting it with entry dict's data
    """
    def set(self, id, dataDict):
        self.lock.acquire()
        try:
            # prepare the dictionary with all of the necessary keys, in case we got a partial dict
            # simultaneously generate the parameterized string, note that this part only uses clean data from self.cursor.description
            # rows = self.cursor.fetchall()

            # inefficient way to avoid having to throw sqlite3.IntegrityError in the unit tests (mahmoud)
            # IndexError is builtin to the language and thus doesn't require an import
            # whereas sqlite3.IntegrityError requires an import
            # remove if performance is necessary, replace with an exception check for sqlite3.IntegrityError
            # that error will be thrown on the self.cursor.execute call if a duplicate id is used
            if "id" in dataDict:
                self.cursor.execute("SELECT * FROM '" + self.tableName + "';")
                rows = self.cursor.fetchall()
                print("rows", rows)
                if (len(rows) > 0):
                    for i in range(0, len(rows)):
                        if len(rows[i]) > 0:
                            if dataDict["id"] == rows[i][0]:
                                raise IndexError
            else:
                self.cursor.execute("SELECT * FROM '" + self.tableName + "' WHERE id = ?1;", (id,))  # required to get cursor.description

            params = ""
            for i in range(len(self.cursor.description)):
                if self.cursor.description[i][0] in dataDict:
                    params += self.cursor.description[i][0] + "=:" + self.cursor.description[i][0] + ", "
                    print("C")

            if len(params) == 0:
                print(self.cursor.description)

            params = params[0:len(params) - 2]  # trim the extra ", "

            dataDict["selectorId"] = id
            command = "UPDATE '" + self.tableName + "' SET " + params + " WHERE id=:selectorId;"

            self.cursor.execute(command, dataDict)
            self.connection.commit()
            return {"error": consts.NO_ERROR, "result": None}
        except IndexError:
            return {"error": consts.ERROR_DUPLICATE_ID, "result": None}
        except Exception as e:
            # print("Exception:", e)
            # traceback.print_exc()
            return {"error": consts.ERROR_UNKNOWN, "result": None}
        finally:
            self.lock.release()

    """
    get all entries in this table, returning them as an array of dicts
    """
    def getAll(self):
        self.lock.acquire()
        try:
            command = "SELECT * FROM '" + self.tableName + "';"
            self.cursor.execute(command)

            rows = self.cursor.fetchall()
            entries = []
            entry = {}

            for i in range(0, len(rows)):
                for j in range(0, len(self.cursor.description)):
                    entry[self.cursor.description[j][0]] = rows[i][j]
                entries.append(entry)
                entry = {}
            return {"error": consts.NO_ERROR, "result": entries}
        finally:
            self.lock.release()
