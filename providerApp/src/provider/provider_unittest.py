import unittest
import tempfile
import sys
from unittest.mock import patch, MagicMock, call, ANY
sys.path.insert(0, "..")
from provider.provider import Provider


class TestProvider(unittest.TestCase):
    def setUp(self):
        nc = MagicMock()
        self.myClass = Provider(nc)
        self.myClass.key = MagicMock()
        self.myClass.member_id = MagicMock()

    def tearDown(self):
        pass


@patch("builtins.input", autospec=True)
class Testlogin(TestProvider):
    def test_login(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = None
        self.myClass.KEY_INVALID = "invalid"
        # Actual
        self.myClass.login()
        # Verify
        mockinput.assert_called_once_with("Welcome.\nPlease enter your login key:\t")

    def test_login1(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = ["invalid", "provider"]
        self.myClass.KEY_INVALID = "invalid"
        self.myClass.KEY_PROVIDER = "provider"
        # Actual
        self.myClass.login()
        # Verify
        mockinput.assert_called_once_with("Welcome.\nPlease enter your login key:\t")

    def test_login2(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = None
        self.myClass.KEY_INVALID = "invalid"
        self.myClass.KEY_PROVIDER = "provider"
        self.myClass.KEY_ROOT = "root"
        # Actual
        self.myClass.login()
        # Verify
        mockinput.assert_called_once_with("Welcome.\nPlease enter your login key:\t")

    def test_login3(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = None
        self.myClass.nc.validateKey.return_value.error = None
        self.myClass.KEY_INVALID = "invalid"
        self.myClass.KEY_PROVIDER = "provider"
        self.myClass.KEY_ROOT = "root"
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        # Actual
        self.myClass.login()
        # Verify
        mockinput.assert_called_once_with("Welcome.\nPlease enter your login key:\t")

    def test_login4(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = None
        self.myClass.nc.validateKey.return_value.error = None
        self.myClass.KEY_INVALID = "invalid"
        self.myClass.KEY_PROVIDER = "provider"
        self.myClass.KEY_ROOT = "root"
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        self.myClass.login()
        # Verify
        mockinput.assert_called_once_with("Welcome.\nPlease enter your login key:\t")

    def test_login5(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = None
        self.myClass.nc.validateKey.return_value.error = None
        self.myClass.KEY_INVALID = "invalid"
        self.myClass.KEY_PROVIDER = "provider"
        self.myClass.KEY_ROOT = "root"
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        # Actual
        self.myClass.login()
        # Verify
        mockinput.assert_called_once_with("Welcome.\nPlease enter your login key:\t")

@patch("provider.provider.Provider.menu", autospec=True)
@patch("builtins.input", autospec=True)
class Testcustomer_id_swipe(TestProvider):
    def test_customer_id_swipe(self, mockinput, mockmenu):
        # Setup
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        # Actual
        self.myClass.customer_id_swipe()
        # Verify
        mockinput.assert_called_once_with("Please enter the customers' ID:\t")
        mockmenu.assert_called_once_with(self.myClass)


    def test_customer_id_swipe1(self, mockinput, mockmenu):
        # Setup
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        self.myClass.customer_id_swipe()
        # Verify
        mockinput.assert_called_once_with("Please enter the customers' ID:\t")
        mockmenu.assert_called_once_with(self.myClass)

    def test_customer_id_swipe2(self, mockinput, mockmenu):
        # Setup
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        # Actual
        self.myClass.customer_id_swipe()
        # Verify
        mockinput.assert_called_once_with("Please enter the customers' ID:\t")
        mockmenu.assert_called_once_with(self.myClass)

    def test_customer_id_swipe3(self, mockinput, mockmenu):
        # Setup
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        self.myClass.NO_ERROR = "No error"
        # Actual
        self.myClass.customer_id_swipe()
        # Verify
        mockinput.assert_called_once_with("Please enter the customers' ID:\t")
        mockmenu.assert_called_once_with(self.myClass)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("provider.provider.Provider.customer_services", autospec=True)
class Testdisplay_one_service(TestProvider):
    def test_display_one_service(self, mockcustomer_services, mockprint, mockinput):
        # Setup
        self.myClass.nc.getService.return_value.error = "Error: operation requires higher authorization level"
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        # Actual
        result = self.myClass.display_one_service()
        # Verify
        mockinput.assert_called_once_with("Please enter the code of the service:\t")
        mockprint.assert_called_once_with("\nError: Key is not authorized.\t")
        self.assertEqual(result, None)

    def test_display_one_service1(self, mockcustomer_services, mockprint, mockinput):
        # Setup
        self.myClass.nc.getService.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        self.myClass.display_one_service()
        # Verify
        mockinput.assert_called_once_with("Please enter the code of the service:\t")

    def test_display_one_service2(self, mockcustomer_services, mockprint, mockinput):
        # Setup
        self.myClass.nc.getService.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        # Actual
        self.myClass.display_one_service()
        # Verify
        mockinput.assert_called_once_with("Please enter the code of the service:\t")

    def test_display_one_service3(self, mockcustomer_services, mockprint, mockinput):
        # Setup
        self.myClass.nc.getService.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        self.myClass.NO_ERROR = "No error"
        # Actual
        self.myClass.display_one_service()
        # Verify
        mockinput.assert_called_once_with("Please enter the code of the service:\t")

    def test_display_one_service4(self, mockcustomer_services, mockprint, mockinput):
        # Setup
        self.myClass.nc.getService.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        self.myClass.NO_ERROR = "No error"
        # Actual
        self.myClass.display_one_service()
        # Verify
        mockinput.assert_called_once_with("Please enter the code of the service:\t")
        mockcustomer_services.assert_called_once_with(self.myClass)


@patch("builtins.print", autospec=True)
@patch("provider.provider.Provider.customer_services", autospec=True)
class Testdisplay_all_services(TestProvider):
    def test_display_all_services(self, mockcustomer_services, mockprint):
        # Setup
        self.myClass.nc.getAllServices.return_value.error = "Error: operation requires higher authorization level"
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        # Actual
        result = self.myClass.display_all_services()
        # Verify
        mockprint.assert_called_once_with("\nError: Key is not authorized.\n")
        self.assertEqual(result, None)

    def test_display_all_services1(self, mockcustomer_services, mockprint):
        # Setup
        self.myClass.nc.getAllServices.return_value.error = "Error: could not establish a connection"
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        # Actual
        result = self.myClass.display_all_services()
        # Verify
        mockprint.assert_called_once_with("\nError: Server did not respond.\n")
        self.assertEqual(result, None)

    def test_display_all_services2(self, mockcustomer_services, mockprint):
        # Setup
        self.myClass.nc.getAllServices.return_value.error = "No error"
        self.myClass.nc.getAllServices.return_value.payload = ["service1"]
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        self.myClass.NO_ERROR = "No error"
        self.myClass.nc.getMember.return_value.payload = {"name": "myName"}
        # Actual
        result = self.myClass.display_all_services()
        # Verify
        printCalls = [call("Displaying all of myName's services:\n"), call("service1")]
        mockprint.assert_has_calls(printCalls)
        mockcustomer_services.assert_called_once_with(self.myClass)


@patch("builtins.print", autospec=True)
@patch("provider.provider.Provider.customer_services", autospec=True)
class Testmember_information(TestProvider):
    def test_member_information(self, mockcustomer_services, mockprint):
        # Setup
        self.myClass.nc.getMember.return_value.payload = {"name": "myName", "address": "myAddress", "city": "myCity", "state": "myState", "zip": "myZip"}
        # Actual
        self.myClass.member_information()
        # Verify
        mockprint.assert_called_once_with("\nName: myName\nAddress: myAddress\nCity: myCity\nState: myState\nZip: myZip")
        mockcustomer_services.assert_called_once_with(self.myClass)


@patch("builtins.print", autospec=True)
@patch("builtins.input", autospec=True)
@patch("provider.provider.Provider.member_information", autospec=True)
@patch("provider.provider.Provider.display_all_services", autospec=True)
@patch("provider.provider.Provider.display_one_service", autospec=True)
@patch("provider.provider.Provider.customer_menu", autospec=True)
@patch("provider.provider.Provider.menu", autospec=True)
class Testcustomer_services(TestProvider):
    def test_customer_services(self, mockmenu, mockcustomer_menu, mockdisplay_one_service, mockdisplay_all_services,
                               mockmember_information, mockinput, mockprint):
        # Setup
        mockinput.return_value = "1"
        # Actual
        self.myClass.customer_services()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Services\t-----\n"
                                          "1. Display customer information\n"
                                          "2. Display all services\n"
                                          "3. Display one service\n"
                                          "4. Return to customer menu\n"
                                          "5. Return to main menu\n"
                                          "6. Exit\n")
        mockmember_information.assert_called_once_with(self.myClass)

    def test_customer_services1(self, mockmenu, mockcustomer_menu, mockdisplay_one_service, mockdisplay_all_services,
                                mockmember_information, mockinput, mockprint):
        # Setup
        mockinput.return_value = "2"
        # Actual
        self.myClass.customer_services()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Services\t-----\n"
                                          "1. Display customer information\n"
                                          "2. Display all services\n"
                                          "3. Display one service\n"
                                          "4. Return to customer menu\n"
                                          "5. Return to main menu\n"
                                          "6. Exit\n")
        mockdisplay_all_services.assert_called_once_with(self.myClass)

    def test_customer_services2(self, mockmenu, mockcustomer_menu, mockdisplay_one_service, mockdisplay_all_services,
                                mockmember_information, mockinput, mockprint):
        # Setup
        mockinput.return_value = "3"
        # Actual
        self.myClass.customer_services()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Services\t-----\n"
                                          "1. Display customer information\n"
                                          "2. Display all services\n"
                                          "3. Display one service\n"
                                          "4. Return to customer menu\n"
                                          "5. Return to main menu\n"
                                          "6. Exit\n")
        mockdisplay_one_service.assert_called_once_with(self.myClass)

    def test_customer_services3(self, mockmenu, mockcustomer_menu, mockdisplay_one_service, mockdisplay_all_services,
                                mockmember_information, mockinput, mockprint):
        # Setup
        mockinput.return_value = "4"
        # Actual
        self.myClass.customer_services()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Services\t-----\n"
                                          "1. Display customer information\n"
                                          "2. Display all services\n"
                                          "3. Display one service\n"
                                          "4. Return to customer menu\n"
                                          "5. Return to main menu\n"
                                          "6. Exit\n")
        mockcustomer_menu.assert_called_once_with(self.myClass)

    def test_customer_services4(self, mockmenu, mockcustomer_menu, mockdisplay_one_service, mockdisplay_all_services,
                                mockmember_information, mockinput, mockprint):
        # Setup
        mockinput.return_value = "5"
        # Actual
        self.myClass.customer_services()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Services\t-----\n"
                                          "1. Display customer information\n"
                                          "2. Display all services\n"
                                          "3. Display one service\n"
                                          "4. Return to customer menu\n"
                                          "5. Return to main menu\n"
                                          "6. Exit\n")
        mockmenu.assert_called_once_with(self.myClass)

    def test_customer_services5(self, mockmenu, mockcustomer_menu, mockdisplay_one_service, mockdisplay_all_services,
                                mockmember_information, mockinput, mockprint):
        # Setup
        mockinput.return_value = "6"
        # Actual
        result = self.myClass.customer_services()
        # Verify
        printCalls = [call("-----\tCustomer Services\t-----\n"
                           "1. Display customer information\n"
                           "2. Display all services\n"
                           "3. Display one service\n"
                           "4. Return to customer menu\n"
                           "5. Return to main menu\n"
                           "6. Exit\n"), call("Thank you!")]
        mockprint.assert_has_calls(printCalls)
        self.assertEqual(result, None)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testadd_service_id(TestProvider):
    def test_add_service_id(self, mockprint, mockinput):
        # Setup
        self.myClass.nc.getProvider.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.add_service_id()
        # Verify
        mockinput.assert_called_once_with("Enter service provider id: ")
        mockprint.assert_called_once_with("Invalid provider id")
        self.assertFalse(result)

    def test_add_service_id1(self, mockprint, mockinput):
        # Setup
        self.myClass.nc.getProvider.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.add_service_id()
        # Verify
        mockinput.assert_called_once_with("Enter service provider id: ")
        self.assertTrue(result)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testadd_service_member(TestProvider):
    def test_add_service_member(self, mockprint, mockinput):
        # Setup
        self.myClass.nc.getMember.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.add_service_member()
        # Verify
        mockinput.assert_called_once_with("Enter member id: ")
        mockprint.assert_called_once_with("Invalid Member id")
        self.assertFalse(result)

    def test_add_service_member1(self, mockprint, mockinput):
        # Setup
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.add_service_member()
        # Verify
        mockinput.assert_called_once_with("Enter member id: ")
        self.assertTrue(result)


@patch("builtins.input", autospec=True)
class Testadd_service_rest_info(TestProvider):
    def test_add_service_rest_info(self, mockinput):
        # Setup
        mockinput.side_effect = iter(["1111", "123456", "no i won't", "Y"])
        # Actual
        result = self.myClass.add_service_rest_info()
        # Verify
        inputCalls = [call("Enter service date (MM/DD/YYYY) : "), call("Enter 6 digit service code: "),
                      call("Please include comments on service: "), call("Was this service paid? (y/n): ")]
        mockinput.assert_has_calls(inputCalls)
        self.assertEqual(result, ("1111", "123456", "no i won't", "paid"))

    def test_add_service_rest_info1(self, mockinput):
        # Setup
        mockinput.side_effect = iter(["1111", "123456", "no i won't", "n"])
        # Actual
        result = self.myClass.add_service_rest_info()
        # Verify
        inputCalls = [call("Enter service date (MM/DD/YYYY) : "), call("Enter 6 digit service code: "),
                      call("Please include comments on service: "), call("Was this service paid? (y/n): ")]
        mockinput.assert_has_calls(inputCalls)
        self.assertEqual(result, ("1111", "123456", "no i won't", "unpaid"))


@patch("provider.provider.Provider.add_service_id", autospec=True)
@patch("provider.provider.Provider.add_service_member", autospec=True)
@patch("random.choice")
@patch("provider.provider.Provider.add_service_rest_info", autospec=True)
@patch("builtins.print", autospec=True)
@patch("provider.provider.Provider.customer_menu", autospec=True)
class Testadd_service(TestProvider):
    def test_add_service(self, mockcustomer_menu, mockprint, mockadd_service_rest_info, mockrandon,
                         mockadd_service_member, mockadd_service_id):
        # Setup
        mockadd_service_id.return_value = True
        mockadd_service_member.return_value = True
        mockrandon.return_value = "9876543210"
        self.myClass.nc.addService.return_value.error = None
        self.myClass.ERROR_DUPLICATE_ID = "Error: attempted to reuse a unique ID"
        mockadd_service_rest_info.return_value = ("x", "y", "z", "X")
        # Actual
        self.myClass.add_service()
        # Verify
        mockadd_service_id.assert_called_once_with(self.myClass)
        mockadd_service_member.assert_called_once_with(self.myClass)
        mockadd_service_rest_info.assert_called_once_with(self.myClass)
        mockprint.assert_called_once_with("New Service ID: 987654321098765432109876543210987654321098765432109876543210987654321098765432109876543210")
        mockcustomer_menu.assert_called_once_with(self.myClass)


@patch("builtins.print", autospec=True)
@patch("builtins.input", autospec=True)
@patch("provider.provider.Provider.customer_services", autospec=True)
@patch("provider.provider.Provider.add_service", autospec=True)
@patch("provider.provider.Provider.menu", autospec=True)
class Testcustomer_menu(TestProvider):
    def test_customer_menu(self, mockmenu, mockadd_service, mockcustomer_services, mockinput, mockprint):
        # Setup
        mockinput.return_value = "1"
        # Actual
        self.myClass.customer_menu()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Menu\t-----\n"
                                          "1. Existing services\n"
                                          "2. Add a service\n"
                                          "3. Return to main menu\n")
        mockcustomer_services.assert_called_once_with(self.myClass)

    def test_customer_menu1(self, mockmenu, mockadd_service, mockcustomer_services, mockinput, mockprint):
        # Setup
        mockinput.return_value = "2"
        # Actual
        self.myClass.customer_menu()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Menu\t-----\n"
                                          "1. Existing services\n"
                                          "2. Add a service\n"
                                          "3. Return to main menu\n")
        mockadd_service.assert_called_once_with(self.myClass)

    def test_customer_menu2(self, mockmenu, mockadd_service, mockcustomer_services, mockinput, mockprint):
        # Setup
        mockinput.return_value = "3"
        # Actual
        self.myClass.customer_menu()
        # Verify
        mockprint.assert_called_once_with("-----\tCustomer Menu\t-----\n"
                                          "1. Existing services\n"
                                          "2. Add a service\n"
                                          "3. Return to main menu\n")
        mockmenu.assert_called_once_with(self.myClass)


@patch("builtins.print", autospec=True)
@patch("provider.provider.Provider.menu", autospec=True)
class Testservices_offered(TestProvider):
    def test_services_offered(self, mockmenu, mockprint):
        # Setup
        self.myClass.nc.getAllMenuItems.return_value.error = None
        self.myClass.ERROR_UNAUTHORIZED_OPERATION = "Error: operation requires higher authorization level"
        # Actual
        self.myClass.services_offered()
        # Verify
        mockmenu.assert_called_once_with(self.myClass)

    def test_services_offered1(self, mockmenu, mockprint):
        # Setup
        self.myClass.nc.getAllMenuItems.return_value.error = "No error"
        self.myClass.nc.getAllMenuItems.return_value.payload = ["myName", "myService"]
        self.myClass.NO_ERROR = "No error"
        # Actual
        self.myClass.services_offered()
        # Verify
        printCalls = [call("\nDisplaying all services offered:\n"), call("myName"), call("myService")]
        mockprint.assert_has_calls(printCalls)
        mockmenu.assert_called_once_with(self.myClass)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("provider.provider.Provider.menu", autospec=True)
class Testgenerate_report(TestProvider):
    def test_generate_report(self, mockmenu, mockprint, mockinput):
        # Setup
        self.myClass.nc.getMember.return_value.error = "No error"
        self.myClass.nc.getMember.return_value.payload = {"name": "myName", "id": "myID", "address": "myAddress",
                                                          "city": "myCity", "state": "myState", "zip": "myZip"}
        self.myClass.NO_ERROR = "No error"
        # Actual
        self.myClass.generate_report()
        # Verify
        mockinput.assert_called_once_with("Please enter a member ID:\t")
        mockprint.assert_called_once_with('\n----\tMember Information\t----\n', '\nName:\t', 'myName',
                                           '\nID:\t\t', 'myID', '\nAddress:\t', 'myAddress', '\nCity:\t\t',
                                           'myCity', '\nState:\t\t', 'myState', '\nZip Code:\t', 'myZip')
        mockmenu.assert_called_once_with(self.myClass)


    def test_generate_report1(self, mockmenu, mockprint, mockinput):
        # Setup
        self.myClass.nc.getMember.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.NO_ERROR = "No error"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        self.myClass.generate_report()
        # Verify
        mockprint.assert_called_once_with("\nError: Member does not exist\n")
        mockmenu.assert_called_once_with(self.myClass)

    def test_generate_report2(self, mockmenu, mockprint, mockinput):
        # Setup
        self.myClass.nc.getMember.return_value.error = "Error: could not establish a connection"
        self.myClass.NO_ERROR = "No error"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_CONNECTION_FAILED = "Error: could not establish a connection"
        # Actual
        self.myClass.generate_report()
        # Verify
        mockprint.assert_called_once_with("\nError: Connection to the server failed")


@patch("builtins.print", autospec=True)
@patch("builtins.input", autospec=True)
@patch("provider.provider.Provider.customer_id_swipe", autospec=True)
@patch("provider.provider.Provider.services_offered", autospec=True)
@patch("provider.provider.Provider.generate_report", autospec=True)
class Testmenu(TestProvider):
    def test_menu(self, mockgenerate_report, mockservices_offered, mockcustomer_id_swipe, mockinput, mockprint):
        # Setup
        mockinput.return_value = "1"
        # Actual
        self.myClass.menu()
        # Verify
        mockprint.assert_called_once_with("-----\tMain Menu\t-----\n"
                                          "1. Swipe Customer ID\n"
                                          "2. ChocAn Services Offered\n"
                                          "3. Generate Report\n"
                                          "4. Exit")
        mockinput.assert_called_once_with()
        mockcustomer_id_swipe.assert_called_once_with(self.myClass)



    def test_menu1(self, mockgenerate_report, services_offered, mockcustomer_id_swipe, mockinput, mockprint):
        # Setup
        mockinput.return_value = "2"
        # Actual
        self.myClass.menu()
        # Verify
        mockprint.assert_called_once_with("-----\tMain Menu\t-----\n"
                                          "1. Swipe Customer ID\n"
                                          "2. ChocAn Services Offered\n"
                                          "3. Generate Report\n"
                                          "4. Exit")
        mockinput.assert_called_once_with()
        services_offered.assert_called_once_with(self.myClass)

    def test_menu2(self, mockgenerate_report, services_offered, mockcustomer_id_swipe, mockinput, mockprint):
        # Setup
        mockinput.return_value = "3"
        # Actual
        self.myClass.menu()
        # Verify
        mockprint.assert_called_once_with("-----\tMain Menu\t-----\n"
                                          "1. Swipe Customer ID\n"
                                          "2. ChocAn Services Offered\n"
                                          "3. Generate Report\n"
                                          "4. Exit")
        mockinput.assert_called_once_with()
        mockgenerate_report.assert_called_once_with(self.myClass)

    def test_menu3(self, mockgenerate_report, services_offered, mockcustomer_id_swipe, mockinput, mockprint):
        # Setup
        mockinput.return_value = "4"
        # Actual
        self.myClass.menu()
        # Verify
        printCalls = [call("-----\tMain Menu\t-----\n"
                           "1. Swipe Customer ID\n"
                           "2. ChocAn Services Offered\n"
                           "3. Generate Report\n"
                           "4. Exit"), call("Thank you!")]
        mockprint.assert_has_calls(printCalls)
        mockinput.assert_called_once_with()



if __name__ == "__main__":
    unittest.main()
