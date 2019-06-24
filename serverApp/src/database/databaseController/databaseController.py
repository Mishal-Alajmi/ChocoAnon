import sqlite3
import threading
from database.tables.membersTable.membersTable import MembersTable
from database.tables.menuTable.menuTable import MenuTable
from database.tables.servicesTable.servicesTable import ServicesTable
from database.tables.providersTable.providersTable import ProvidersTable
from database.tables.keysTable.keysTable import KeysTable
import constants.consts as consts
import traceback


class DatabaseController:
    def __init__(self, filepath):
        # allow sharing of the same sqlite3 objects
        # this is safe because we're using a lock
        # but if you write new methods, make sure to lock them too!
        self.connection = sqlite3.connect(filepath, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.lock = threading.Lock()  # all tables need to share the same lock object

        self.authTable = {consts.KEY_ROOT: [
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_ADD, True],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_GET, True],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_SET, True],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_TRUNCATE, True],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_REMOVE, True],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_VALIDATE_KEY, False],

            [consts.MEMBERS_TABLE, consts.DBC_CMD_ADD, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_GET, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_SET, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_TRUNCATE, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_REMOVE, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_VALIDATE_KEY, False],

            [consts.SERVICES_TABLE, consts.DBC_CMD_ADD, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_GET, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_SET, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_TRUNCATE, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_REMOVE, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_VALIDATE_KEY, True],

            [consts.KEYS_TABLE, consts.DBC_CMD_ADD, True],
            [consts.KEYS_TABLE, consts.DBC_CMD_GET, True],
            [consts.KEYS_TABLE, consts.DBC_CMD_SET, True],
            [consts.KEYS_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.KEYS_TABLE, consts.DBC_CMD_TRUNCATE, True],
            [consts.KEYS_TABLE, consts.DBC_CMD_REMOVE, True],
            [consts.KEYS_TABLE, consts.DBC_CMD_VALIDATE_KEY, True],

            [consts.MENU_TABLE, consts.DBC_CMD_ADD, True],
            [consts.MENU_TABLE, consts.DBC_CMD_GET, True],
            [consts.MENU_TABLE, consts.DBC_CMD_SET, True],
            [consts.MENU_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.MENU_TABLE, consts.DBC_CMD_TRUNCATE, True],
            [consts.MENU_TABLE, consts.DBC_CMD_REMOVE, True],
            [consts.MENU_TABLE, consts.DBC_CMD_VALIDATE_KEY, False]
        ], consts.KEY_PROVIDER: [
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_ADD, False],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_GET, False],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_SET, False],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_GET_ALL, False],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_TRUNCATE, False],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_REMOVE, False],
            [consts.PROVIDERS_TABLE, consts.DBC_CMD_VALIDATE_KEY, False],

            [consts.MEMBERS_TABLE, consts.DBC_CMD_ADD, False],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_GET, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_SET, False],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_TRUNCATE, False],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_REMOVE, False],
            [consts.MEMBERS_TABLE, consts.DBC_CMD_VALIDATE_KEY, False],

            [consts.SERVICES_TABLE, consts.DBC_CMD_ADD, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_GET, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_SET, False],
            [consts.SERVICES_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.SERVICES_TABLE, consts.DBC_CMD_TRUNCATE, False],
            [consts.SERVICES_TABLE, consts.DBC_CMD_REMOVE, False],
            [consts.SERVICES_TABLE, consts.DBC_CMD_VALIDATE_KEY, False],

            [consts.KEYS_TABLE, consts.DBC_CMD_ADD, False],
            [consts.KEYS_TABLE, consts.DBC_CMD_GET, False],
            [consts.KEYS_TABLE, consts.DBC_CMD_SET, False],
            [consts.KEYS_TABLE, consts.DBC_CMD_GET_ALL, False],
            [consts.KEYS_TABLE, consts.DBC_CMD_TRUNCATE, False],
            [consts.KEYS_TABLE, consts.DBC_CMD_REMOVE, False],
            [consts.KEYS_TABLE, consts.DBC_CMD_VALIDATE_KEY, True],

            [consts.MENU_TABLE, consts.DBC_CMD_ADD, False],
            [consts.MENU_TABLE, consts.DBC_CMD_GET, True],
            [consts.MENU_TABLE, consts.DBC_CMD_SET, False],
            [consts.MENU_TABLE, consts.DBC_CMD_GET_ALL, True],
            [consts.MENU_TABLE, consts.DBC_CMD_TRUNCATE, False],
            [consts.MENU_TABLE, consts.DBC_CMD_REMOVE, False],
            [consts.MENU_TABLE, consts.DBC_CMD_VALIDATE_KEY, False]

        ], consts.KEY_INVALID: [
            [consts.KEYS_TABLE, consts.DBC_CMD_VALIDATE_KEY, True]
        ]}

        self.tables = {}

        self.tables[consts.MEMBERS_TABLE] = MembersTable(self.connection, self.cursor, self.lock)
        self.tables[consts.MENU_TABLE] = MenuTable(self.connection, self.cursor, self.lock)
        self.tables[consts.SERVICES_TABLE] = ServicesTable(self.connection, self.cursor, self.lock)
        self.tables[consts.PROVIDERS_TABLE] = ProvidersTable(self.connection, self.cursor, self.lock)
        self.tables[consts.KEYS_TABLE] = KeysTable(self.connection, self.cursor, self.lock)

        # create empty tables in the database if they don't already exist
        for table in self.tables:
            self.tables[table].create()

        # # admin key, remove later, only for testing
        # salt = uuid.uuid4().hex
        # key = hashlib.sha256(salt.encode() + "AS62ELRB5F0709LERPHZD06JWC0P8QSC".encode()).hexdigest() + ':' + salt
        # self.tables[consts.KEYS_TABLE].add({"uak": key, "name": "jharod", "level": consts.KEY_ROOT})

        # # provider key, remove later, only for testing
        # salt = uuid.uuid4().hex
        # key = hashlib.sha256(salt.encode() + "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3".encode()).hexdigest() + ':' + salt
        # self.tables[consts.KEYS_TABLE].add({"uak": key, "name": "axiom", "level": consts.KEY_PROVIDER})

    """
    execute command on table, if key has sufficient auth level
    data should be a dict, its contents depend on the specific command
    will return a dict with "error" and "result" keys
    """
    def execute(self, table, command, data, key):
        retError = consts.ERROR_UNAUTHORIZED_OPERATION
        retResult = {}

        try:
            keyState = self.checkKey(key)

            authorizedOperation = False
            for case in self.authTable[keyState]:
                if table == case[0] and command == case[1] and case[2]:
                    authorizedOperation = True

            if authorizedOperation:
                print("Exec", command, "on", table, "with key level:", keyState, "and data:", data)

                if command == consts.DBC_CMD_ADD:
                    response = self.tables[table].add(data)
                elif command == consts.DBC_CMD_GET:
                    response = self.tables[table].get(data)
                elif command == consts.DBC_CMD_SET:
                    response = self.tables[table].set(data["id"], data["data"])
                elif command == consts.DBC_CMD_REMOVE:
                    response = self.tables[table].remove(data)
                elif command == consts.DBC_CMD_GET_ALL:
                    response = self.tables[table].getAll()
                elif command == consts.DBC_CMD_TRUNCATE:
                    response = self.tables[table].truncate()
                elif command == consts.DBC_CMD_VALIDATE_KEY:
                    # this is to fake an entry in the database for testing (a backdoor)
                    # don't remove it
                    if table == consts.KEYS_TABLE:
                        response = {"error": consts.NO_ERROR, "result": self.checkKey(data)}
                        print(response)
                    else:
                        response = self.tables[table].validateKey(data)
                else:
                    response = {"error": consts.ERROR_INVALID_COMMAND, "result": {}}
                retError = response["error"]
                retResult = response["result"]
            else:
                print("Exec failed, unauthorized key:", key)
        except Exception as e:
            print("************************************************************************************************************************************************")
            print("Exception:", e)
            traceback.print_exc()
            print("Response:", response)
            retError = consts.ERROR_UNKNOWN
        finally:
            return {"error": retError, "result": retResult}

    def checkKey(self, key):
        ########################################################################
        # !!FOR TESTING ONLY - REMOVE BEFORE RELEASE!!
        ########################################################################
        if key == "AS62ELRB5F0709LERPHZD06JWC0P8QSC":
            return consts.KEY_ROOT
        elif key == "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3":
            return consts.KEY_PROVIDER

        ########################################################################
        # !!FOR TESTING ONLY - REMOVE BEFORE RELEASE!!
        ########################################################################

        return self.tables[consts.KEYS_TABLE].validateKey(key)
