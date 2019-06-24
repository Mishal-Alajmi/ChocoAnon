# ============================ TABLES AND DATABASES ============================
MEMBERS_TABLE = "members"
MENU_TABLE = "menu"
SERVICES_TABLE = "services"
PROVIDERS_TABLE = "providers"
KEYS_TABLE = "keys"
NO_TABLE = "no table"

STATUS_PAID = "paid"
STATUS_UNPAID = "unpaid"
STATUS_BANNED = "STATUS_BANNED"
STATUS_UNBANNED = "STATUS_UNBANNED"

#
# ===================================== ERRORS =================================
ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA = "Error: failed to add entry to database due to incomplete data"
ERROR_UNKNOWN = "Error: unknown error"
ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
ERROR_DUPLICATE_ID = "Error: attempted to reuse a unique ID"
NO_ERROR = "No error"
ERROR_INVALID_COMMAND = "Error: invalid command"
ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
ERROR_CONNECTION_FAILED = "Error: could not establish a connection"

#
# ========================= SERVER/CLIENT COMMUNICATION ========================
TCP_IP = '127.0.0.1'
TCP_PORT = 2048
BUFFER_SIZE = 1024

NO_CMD = "no command"
DBC_CMD_ADD = "add"
DBC_CMD_GET = "get"
DBC_CMD_SET = "set"
DBC_CMD_GET_ALL = "get all"
DBC_CMD_TRUNCATE = "truncate"
DBC_CMD_REMOVE = "remove"
DBC_CMD_VALIDATE_KEY = "validate key"

KEY_ROOT = "root"
KEY_PROVIDER = "provider"
KEY_INVALID = "invalid"
