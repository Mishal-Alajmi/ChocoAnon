# this is for app-relative absolute imports
import os
import sys
os.chdir("../src")
sys.path.append(os.getcwd())
import unittest

################################################################################
# UNIT TESTS
################################################################################

# Network
from unit.network.network.testSendString import TestSendString  # noqa: F401
from unit.network.network.testSendNetworkObject import TestSendNetworkObject  # noqa: F401

# NetworkObject
from unit.network.networkObject.testInitialize import TestInitialize  # noqa: F401
from unit.network.networkObject.testSerialize import TestSerialize  # noqa: F401

# Client
from unit.client.testInit import TestInit  # noqa: F401
from unit.client.testParseNetworkObject import TestParseNetworkObject  # noqa: F401

# Table
from unit.database.tables.table.testAdd import TestAdd  # noqa: F401
from unit.database.tables.table.testGet import TestGet  # noqa: F401
from unit.database.tables.table.testGetAll import TestGetAll  # noqa: F401
from unit.database.tables.table.testRemove import TestRemove  # noqa: F401
from unit.database.tables.table.testSet import TestSet  # noqa: F401
from unit.database.tables.table.testTruncate import TestTruncate  # noqa: F401

# KeysTable
from unit.database.tables.keysTable.testCreate import KTTestCreate  # noqa: F401
from unit.database.tables.keysTable.testValidateKey import KTTestValidateKey  # noqa: F401

# MembersTable
from unit.database.tables.membersTable.testCreate import MTTestCreate  # noqa: F401

# ProvidersTable
from unit.database.tables.providersTable.testCreate import PTTestCreate  # noqa: F401

# MenuTable
from unit.database.tables.menuTable.testCreate import MenuTableTestCreate  # noqa: F401

# ServicesTable
from unit.database.tables.servicesTable.testCreate import STTestCreate  # noqa: F401


################################################################################
# INTEGRATION TESTS
################################################################################

# DatabaseController
from integration.database.databaseController.testDatabaseController import TestDatabaseController  # noqa: F401

# NetworkController
from integration.network.networkController.testNetworkController import TestNetworkController  # noqa: F401



if __name__ == '__main__':
    unittest.main()
