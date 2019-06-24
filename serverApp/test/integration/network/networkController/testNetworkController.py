import unittest
from network.networkController.networkController import NetworkController
import constants.consts as consts


# these integration tests require a running CAServer
# AS62ELRB5F0709LERPHZD06JWC0P8QSC should be a root key in the database
# DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3 should be a provider key in the database
class TestNetworkController(unittest.TestCase):

    ############################################################################
    # Members API
    ############################################################################
    def test_truncateMembers_good(self):
        nc = NetworkController()
        key = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"

        response = nc.truncateMembers(key)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllMembers(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 0)

    def test_truncateMembers_unauthorized(self):
        nc = NetworkController()

        key = "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3"  # provider key
        response = nc.truncateMembers(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        key = "asd"  # invalid key
        response = nc.truncateMembers(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addMember_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 1)
        self.assertEqual(response.payload[0], {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED})

    def test_addMember_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMember("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMember("asdf", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addMember_incomplete(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e"}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA)

    def test_addMember_duplicate(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_getMember_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED})

    def test_getAllMembers_lots(self):
        nc = NetworkController()

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        for i in range(0, 9):
            nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": str(i), "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED})

        response = nc.getAllMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        print(response.serialize())

    def test_getMember_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getMember("asdf", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_getMember_nonexistent(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "b")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_setMember_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        nc.setMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"name": "c"})
        response = nc.getMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, {"id": "a", "name": "c", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED})

    def test_setMember_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.setMember("asdf", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.setMember("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_setMember_duplicate(self):
        nc = NetworkController()

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "aaaa", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED})
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "bbbb", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f", "status": consts.STATUS_UNBANNED})
        response = nc.setMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "aaaa", {"id": "bbbb"})
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_removeMember_good(self):
        nc = NetworkController()

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})
        response = nc.removeMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_removeMember_unauthorized(self):
        nc = NetworkController()

        nc.truncateMembers("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})
        response = nc.removeMember("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.removeMember("asd", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    ############################################################################
    # Keys API
    ############################################################################
    def test_truncateKeys_good(self):
        nc = NetworkController()
        key = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"

        response = nc.truncateKeys(key)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllKeys(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 0)

    def test_truncateKeys_unauthorized(self):
        nc = NetworkController()

        key = "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3"  # provider key
        response = nc.truncateKeys(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        key = "asd"  # invalid key
        response = nc.truncateKeys(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_validateKeyGood(self):
        nc = NetworkController()
        key = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"

        response = nc.validateKey(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, consts.KEY_ROOT)

        key = "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3"
        response = nc.validateKey(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, consts.KEY_PROVIDER)

        key = "asdfasdf"
        response = nc.validateKey(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, consts.KEY_INVALID)

    def test_addKey_good(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 1)

        self.assertEqual(response.payload[0]["level"], "b")
        self.assertEqual(response.payload[0]["name"], "c")

    def test_addKey_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addKey("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addKey("asdf", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addKey_incomplete(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA)

    def test_getKey_goodByUnhashedUak(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload["level"], "b")
        self.assertEqual(response.payload["name"], "c")

    def test_getKey_goodByHashedUak(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getAllKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")

        id = response.payload[0]["id"]
        response = nc.getKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", id)

        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload["level"], "b")
        self.assertEqual(response.payload["name"], "c")

    def test_getKey_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getKey("asdf", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_getKey_nonexistent(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "b")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_setKey_goodByUnhashedUak(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        nc.setKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"name": "c"})
        response = nc.getKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload["level"], "b")
        self.assertEqual(response.payload["name"], "c")

    def test_setKey_goodByHashedId(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        nc.setKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"name": "c"})

        response = nc.getAllKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        id = response.payload[0]["id"]
        response = nc.getKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", id)

        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload["level"], "b")
        self.assertEqual(response.payload["name"], "c")

    def test_setKey_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "level": "b", "name": "c"}

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.setKey("asdf", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.setKey("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_removeKey_goodByUak(self):
        nc = NetworkController()

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "level": "b", "name": "c"})

        response = nc.removeKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")

        self.assertEqual(response.error, consts.NO_ERROR)
        response = nc.getAllKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        self.assertEqual(len(response.payload), 0)

    def test_removeKey_goodByHash(self):
        nc = NetworkController()

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "level": "b", "name": "c"})

        response = nc.getAllKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        id = response.payload[0]["id"]
        response = nc.removeKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", id)

        self.assertEqual(response.error, consts.NO_ERROR)
        response = nc.getAllKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        self.assertEqual(len(response.payload), 0)



    def test_removeKey_unauthorized(self):
        nc = NetworkController()

        nc.truncateKeys("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addKey("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"uak": "a", "level": "b", "name": "c"})
        response = nc.removeKey("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.removeKey("asd", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    ############################################################################
    # Services API
    ############################################################################

    def test_truncateServices_good(self):
        nc = NetworkController()
        key = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"

        response = nc.truncateServices(key)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllServices(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 0)

    def test_truncateServices_unauthorized(self):
        nc = NetworkController()

        key = "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3"  # provider key
        response = nc.truncateServices(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        key = "asd"  # invalid key
        response = nc.truncateServices(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addService_good(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 1)
        response.payload[0].pop("received")  # no way to know what this ought to be
        self.assertEqual(response.payload[0], {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"})

    def test_addService_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addService("asdf", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addService_incomplete(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA)

    def test_addService_duplicate(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_getService_good(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        response.payload.pop("received")  # no way to know what this should be
        self.assertEqual(response.payload, {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"})

    def test_getService_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getService("asdf", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_getService_nonexistent(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "b")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_setService_good(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        nc.setService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"name": "c"})
        response = nc.getService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        response.payload.pop("received")  # no way to know what this should be
        self.assertEqual(response.payload, {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"})

    def test_setService_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"}

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.setService("asdf", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.setService("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_setService_duplicate(self):
        nc = NetworkController()

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"})
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "b", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"})
        response = nc.setService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"id": "b"})
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_removeService_good(self):
        nc = NetworkController()

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"})
        response = nc.removeService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_removeService_unauthorized(self):
        nc = NetworkController()

        nc.truncateServices("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addService("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "code": "b", "provider": "c", "member": "d", "comment": "e", "status": "f", "date": "g"})
        response = nc.removeService("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.removeService("asd", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    ############################################################################
    # MenuItems API
    ############################################################################
    def test_truncateMenuItems_good(self):
        nc = NetworkController()
        key = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"

        response = nc.truncateMenu(key)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllMenuItems(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 0)

    def test_addMenuItem_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllMenuItems("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 1)
        self.assertEqual(response.payload[0], {"id": "a", "name": "b", "fee": "100"})

    def test_addMenuItem_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMenuItem("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMenuItem("asdf", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addMenuItem_incomplete(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA)

    def test_addMenuItem_duplicate(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_getMenuItem_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, {"id": "a", "name": "b", "fee": "100"})

    def test_getMenuItem_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getMenuItem("asdf", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_getMenuItem_nonexistent(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "b")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_setMenuItem_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        nc.setMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"name": "c"})
        response = nc.getMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, {"id": "a", "name": "c", "fee": "100"})

    def test_setMenuItem_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "fee": "100"}

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.setMenuItem("asdf", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.setMenuItem("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_setMenuItem_duplicate(self):
        nc = NetworkController()

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "fee": "100"})
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "b", "name": "b", "fee": "100"})
        response = nc.setMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"id": "b"})
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_removeMenuItem_good(self):
        nc = NetworkController()

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "fee": "100"})
        response = nc.removeMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_removeMenuItem_unauthorized(self):
        nc = NetworkController()

        nc.truncateMenu("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addMenuItem("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "fee": "100"})
        response = nc.removeMenuItem("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.removeMenuItem("asd", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    ############################################################################
    # Providers API
    ############################################################################
    def test_truncateProviders_good(self):
        nc = NetworkController()
        key = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"

        response = nc.truncateProviders(key)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllProviders(key)
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 0)

    def test_truncateProviders_unauthorized(self):
        nc = NetworkController()

        key = "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3"  # provider key
        response = nc.truncateProviders(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        key = "asd"  # invalid key
        response = nc.truncateProviders(key)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addProvider_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getAllProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(len(response.payload), 1)
        self.assertEqual(response.payload[0], {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})

    def test_addProvider_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addProvider("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addProvider("asdf", data)
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_addProvider_incomplete(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        response = nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_FAILED_DATABASE_ADD_INCOMPLETE_DATA)

    def test_addProvider_duplicate(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_getProvider_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})

    def test_getProvider_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getProvider("asdf", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_getProvider_nonexistent(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.getProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "b")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_setProvider_good(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        nc.setProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"name": "c"})
        response = nc.getProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)
        self.assertEqual(response.payload, {"id": "a", "name": "c", "address": "c", "city": "d", "state": "e", "zip": "f"})

    def test_setProvider_unauthorized(self):
        nc = NetworkController()
        data = {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"}

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", data)
        response = nc.setProvider("asdf", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.setProvider("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a", {"name": "c"})
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

    def test_setProvider_duplicate(self):
        nc = NetworkController()

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "b", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})
        response = nc.setProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a", {"id": "b"})
        self.assertEqual(response.error, consts.ERROR_DUPLICATE_ID)

    def test_removeProvider_good(self):
        nc = NetworkController()

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})
        response = nc.removeProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.NO_ERROR)

        response = nc.getProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", "a")
        self.assertEqual(response.error, consts.ERROR_NONEXISTENT_ENTRY)

    def test_removeProvider_unauthorized(self):
        nc = NetworkController()

        nc.truncateProviders("AS62ELRB5F0709LERPHZD06JWC0P8QSC")
        nc.addProvider("AS62ELRB5F0709LERPHZD06JWC0P8QSC", {"id": "a", "name": "b", "address": "c", "city": "d", "state": "e", "zip": "f"})
        response = nc.removeProvider("DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)

        response = nc.removeProvider("asd", "a")
        self.assertEqual(response.error, consts.ERROR_UNAUTHORIZED_OPERATION)


if __name__ == '__main__':
    unittest.main()
