from network.network.network import Network
from network.networkObject.networkObject import NetworkObject
import constants.consts as consts


# this class wraps Network to provide high-level functionality
# to other members of my group: instantiate a copy of this class to interface with the server
class NetworkController():
    def __init__(self):
        self.network = Network()

    ############################################################################
    # Members API
    ############################################################################

    """
    description: Add a member defined by dict to the server’s members table.
    arguments:
        key - an admin's unique access key
        dict - should contain values for the following keys: id (string, must be unique among all members),
name (string), address (string), city (string), state (string), zip (string).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA - dict was missing some data
        ERROR_DUPLICATE_ID - id was already used
        ERROR_CONNECTION_FAILED - server didn’t respond
        ERROR_UNKNOWN - something else went wrong
    """
    def addMember(self, key, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_ADD, dict, consts.MEMBERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve the member with id from the server’s members table.
    arguments:
        key - a provider or admin’s unique access key
        id - the 9 digit id of a member already in the database
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a dictionary
with the member’s information (id, name, address, city, state, zip), if no errors occurred. See Errors for more
information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_NONEXISTENT_ENTRY - database has no member with the given id
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getMember(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET, id, consts.MEMBERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Set dict’s fields of member defined by id. Dict does not have to contain all of a member’s fields.
    arguments:
        key - an admin’s unique access key
        dict - may contain values for the following keys: id (string, must be unique among all members), name
(string), address (string), city (string), state (string), zip (string).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_DUPLICATE_ID - attempted to set an id to an already existing id
        ERROR_CONNECTION_FAILED - server didn’t respond
        ERROR_UNKNOWN - something else went wrong
    """
    def setMember(self, key, id, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_SET, {"id": id, "data": dict}, consts.MEMBERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve all members from the server’s members table.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a list of
dictionaries, where each dictionary has a single member’s information (id, name, address, city, state, zip), if
no errors occurred. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
    """
    def getAllMembers(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET_ALL, "", consts.MEMBERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove all data from the server’s members table. Use with caution.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def truncateMembers(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_TRUNCATE, "", consts.MEMBERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove the member with id from the server’s members table.
    arguments:
        key - an admin’s unique access key
        id - the 9 digit id of a member already in the database
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def removeMember(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_REMOVE, id, consts.MEMBERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    ############################################################################
    # Keys API
    ############################################################################

    """
    description: Add a key defined by dict to the table.
    arguments:
        key - an admin’s unique access key
        dict - should contain values for the following keys: uak (string, must be unique among all keys), level
(string, either KEY_ROOT or KEY_PROVIDER), name (string, name of key owner).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA - dict was missing some data
        ERROR_DUPLICATE_ID - uak was already used
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def addKey(self, key, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_ADD, dict, consts.KEYS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve the key with uak from the server’s admins table.
    arguments:
        key - an admin’s unique access key
        uak - the uak field of an entry in the table
    returns: A NetworkObject whose error and result fields are set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_NONEXISTENT_ENTRY - database has no admin with the given id
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getKey(self, key, uak):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET, uak, consts.KEYS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Set dict’s fields of key defined by uak. Dict does not have to contain all of a key’s fields.
    arguments:
        key - an admin’s unique access key
        dict - may contain values for the following keys: uak (string, must be unique among all keys), level
(string, either KEY_ROOT or KEY_PROVIDER), name (string, key owner).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_DUPLICATE_ID - attempted to set an id to an already existing id
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def setKey(self, key, uak, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_SET, {"id": uak, "data": dict}, consts.KEYS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve all keys from the server’s admins table.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a list of
dictionaries, where each dictionary has a single keys’s information (uak, level, name) if no errors occurred.
See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getAllKeys(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET_ALL, "", consts.KEYS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove all data from the server’s keys table. Use with caution.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def truncateKeys(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_TRUNCATE, "", consts.KEYS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove the admin with uak from the server’s admins table.
    arguments:
        key - an admin’s unique access key
        uak - the uak field of an entry in the table
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def removeKey(self, key, uak):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_REMOVE, uak, consts.KEYS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Check whether key is valid or not.
    arguments:
        key - any string
    returns: A NetworkObject whose error and payload fields are set. The payload field will be of the format {”key”:
”result”} where result is KEY_PROVIDER, KEY_ROOT, or KEY_INVALID.
    errors:
        NO_ERROR - operation was successful
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def validateKey(self, key):
        networkObject = NetworkObject("", consts.NO_ERROR, consts.DBC_CMD_VALIDATE_KEY, key, consts.KEYS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    ############################################################################
    # Services API
    ############################################################################

    """
    description: Add a service defined by dict to the server’s saddServiceervices table. If key is a provider’s key, the server
will only use member, code, and comment from dict. All other fields will be auto-generated.
    arguments:
        key - a provider’s or admin’s unique access key
        dict - should contain values for the following keys: id (string, must be unique among all services), code
(string), provider (string, 9 digit id of the provider who sold the service), member (string, 9 digit ID of
the member who bought the service), comment (string), status (STATUS_PAID or STATUS_UNPAID)
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA - dict was missing some data
        ERROR_DUPLICATE_ID - id was already used
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def addService(self, key, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_ADD, dict, consts.SERVICES_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve the service with id from the server’s services table.
    arguments:
        key - a provider or admin’s unique access key
        id - the unique id of a service already in the database
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a dictionary
with the service’s information (id, code, provider, member, received, comment, status), if no errors occurred.
See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_NONEXISTENT_ENTRY - database has no service with the given id
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getService(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET, id, consts.SERVICES_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Set dict’s fields of service defined by id. Dict does not have to contain all of a service’s fields.
    arguments:
        key - an admin’s unique access key
        dict - may contain values for the following keys: id (string, must be unique among all services), code
(string), provider (string), member (string), received (string), comment (string), status (string, should
be STATUS_PAID or STATUS_UNPAID).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_DUPLICATE_ID - attempted to set an id to an already existing id
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def setService(self, key, id, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_SET, {"id": id, "data": dict}, consts.SERVICES_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve all services from the server’s service table.
    arguments:
        key - a provider or admin’s unique access key
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a list of
dictionaries, where each dictionary has a single service’s information (id, code, provider, member, received,
comment, status), if no errors occurred. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getAllServices(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET_ALL, "", consts.SERVICES_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response
    """
    description: Remove all data from the server’s services table. Use with caution.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def truncateServices(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_TRUNCATE, "", consts.SERVICES_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove the service with id from the server’s services table.
    arguments:
        key - an admin’s unique access key
        id - the 9 digit id of a service already in the database
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def removeService(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_REMOVE, id, consts.SERVICES_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    ############################################################################
    # Menu API
    ############################################################################

    """
    description: Add a menu service defined by dict to the server’s menu table.
    arguments:
        key - an admin’s unique access key
        dict - should contain values for the following keys: id (string, must be unique among all menu services),
name (string), fee (integer, in cents).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA - dict was missing some data
        ERROR_DUPLICATE_ID - id was already used
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def addMenuItem(self, key, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_ADD, dict, consts.MENU_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve the menu item with id from the server’s members table.
    arguments:
        key - a provider or admin’s unique access key
        id - the 6 digit id of a menu item in the database
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a dictionary
with the menu item’s information (id, name, fee), if no errors occurred. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_NONEXISTENT_ENTRY - database has no menu item with the given id
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getMenuItem(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET, id, consts.MENU_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Set dict’s fields of menu item defined by id. Dict does not have to contain all of a menu item’s fields.
    arguments:
        key - an admin’s unique access key
        dict - may contain values for the following keys: id (string, must be unique among all menu items),
name (string), fee (integer, in cents).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_DUPLICATE_ID - attempted to set an id to an already existing id
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def setMenuItem(self, key, id, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_SET, {"id": id, "data": dict}, consts.MENU_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve all menu items from the server’s menu table.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a list of
dictionaries, where each dictionary has a single menu item’s information (id, name, fee), if no errors occurred.
See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getAllMenuItems(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET_ALL, "", consts.MENU_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove all data from the server’s menu table. Use with caution.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def truncateMenu(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_TRUNCATE, "", consts.MENU_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove the menu item with id from the server’s menu table.
    arguments:
        key - an admin’s unique access key
        id - the 9 digit id of a menu item already in the database
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def removeMenuItem(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_REMOVE, id, consts.MENU_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    ############################################################################
    # Providers API
    ############################################################################

    """
    description: Add a provider defined by dict to the server’s provider table.
    arguments:
        key - an admin’s unique access key
        dict - should contain values for the following keys: id (string, must be unique among all menu services),
name (string), address (string), city (string), state (string), zip (string).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA - dict was missing some data
        ERROR_DUPLICATE_ID - id was already used
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def addProvider(self, key, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_ADD, dict, consts.PROVIDERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve the provider with id from the server’s provider table.
    arguments:
        key - an admin’s unique access key
        id - the 9 digit id of a provider already in the database
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a dictionary
with the provider’s information (id, name, address, city, state, zip), if no errors occurred. See Errors for more
information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_NONEXISTENT_ENTRY - database has no provider with the given id
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getProvider(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET, id, consts.PROVIDERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Set dict’s fields of provider defined by id. Dict does not have to contain all of a provider’s fields.
    arguments:
        key - an admin’s unique access key
        dict - may contain values for the following keys: id (string, must be unique among all providers), name
(string), address (string), city (string), state (string), zip (string)).
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_DUPLICATE_ID - attempted to set an id to an already existing id
        ERROR_UNKNOWN - something else went wrong
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def setProvider(self, key, id, dict):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_SET, {"id": id, "data": dict}, consts.PROVIDERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Retrieve all providers from the server’s provider table.
    arguments:
        key - an admin’s unique access key
        id - the 9 digit id of a provider already in the database
    returns: A NetworkObject whose error field and payload fields are set. The payload field will contain a list of
dictionaries, where each dictionary has a single provider’s information (id, name, address, city, state, zip), if
no errors occurred. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def getAllProviders(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_GET_ALL, "", consts.PROVIDERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove all data from the server’s providers table. Use with caution.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field is set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def truncateProviders(self, key):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_TRUNCATE, "", consts.PROVIDERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response

    """
    description: Remove the provider with id from the server’s provider table.
    arguments:
        key - an admin’s unique access key
    returns: A NetworkObject whose error field is are set. See Errors for more information.
    errors:
        NO_ERROR - operation was successful
        ERROR_UNAUTHORIZED_OPERATION - invalid key
        ERROR_CONNECTION_FAILED - server didn’t respond
    """
    def removeProvider(self, key, id):
        networkObject = NetworkObject(key, consts.NO_ERROR, consts.DBC_CMD_REMOVE, id, consts.PROVIDERS_TABLE)
        response = self.network.sendNetworkObject(networkObject)
        return response
