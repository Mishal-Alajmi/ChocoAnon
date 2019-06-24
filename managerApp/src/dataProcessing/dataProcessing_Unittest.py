import unittest
import sys
sys.path.insert(0, "..")
from unittest.mock import patch, MagicMock, call, ANY

from dataProcessing.dataProcessing import DataProcessing


class TestdataProcessing(unittest.TestCase):
    def setUp(self):
        nc = MagicMock()
        self.myClass = DataProcessing(nc)

    def tearDown(self):
        pass
@patch("datetime.date", autospec=True)
@patch("os.makedirs", autospec=True)
@patch("builtins.open", create=True)
class Testwrite_m_report(TestdataProcessing):
    def test_write_m_report(self, mockopen, mockmakedirs, mocktoday):
        # Setup
        self.myClass.key = MagicMock()
        mocktoday.return_value = "12:00"
        self.myClass.nc.getMember.return_value.payload = {"name": "myName", "id": "myID", "address": "myAddress",
                                                          "city": "myCity", "state": "myState", "zip": "myZip"}
        self.myClass.nc.getProvider.return_value.payload = {"name": "myName"}
        self.myClass.nc.getService.return_value.payload = {"member": "myMember", "provider": "myProvider", "date": "myDate", "code": "myCode"}
        mockopen.side_effect = [mockopen(read_data="A").return_value]
        # Actual
        result = self.myClass.write_m_report("s_id")
        # Verify
        openCalls = [call(read_data='A'),
                    call('./reports/member_report/myName2018-06-06.txt', 'w+'),
                    call()().__enter__(),
                    call()().__enter__().write('Name: myName\n'),
                    call()().__enter__().write('Member ID: myID\n'),
                    call()().__enter__().write('Address: : myAddress\n'),
                    call()().__enter__().write('City: myCity\n'),
                    call()().__enter__().write('State: myState\n'),
                    call()().__enter__().write('Zip: myZip\n'),
                    call()().__enter__().write('Service Date: myDate\n'),
                    call()().__enter__().write('Service Provider: myName\n'),
                    call()().__enter__().write('Service Code: myCode\n'),
                    call()().__enter__().close(),
                    call()().__exit__(None, None, None)]
        mockopen.assert_has_calls(openCalls)
        mockmakedirs.assert_called_once_with('./reports/member_report', exist_ok=True)
        self.assertTrue(result)


@patch("builtins.print", autospec=True)
class Testmember_report(TestdataProcessing):
    def test_member_report(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllServices.return_value.payload = []
        # Actual
        result = self.myClass.member_report()
        # Verify
        mockprint.assert_called_once_with("Database is Empty")
        self.assertFalse(result)


@patch("datetime.date", autospec=True)
@patch("os.makedirs", autospec=True)
@patch("builtins.open", create=True)
class Testwrite_eft_report(TestdataProcessing):
    def test_write_eft_report(self, mockopen, mockmakedirs, mocktoday):
        # Setup
        self.myClass.key = MagicMock()
        mocktoday.return_value = "12:00"
        self.myClass.nc.getMenuItem.return_value.payload = {"fee": "myFee"}
        self.myClass.nc.getProvider.return_value.payload = {"name": "myName"}
        self.myClass.nc.getService.return_value.payload = {"member": "myMember", "provider": "myProvider",
                                                           "date": "myDate", "code": "myCode", "id": "myID"}
        mockopen.side_effect = [mockopen(read_data="A").return_value]
        # Actual
        result = self.myClass.write_eft_report("s_id")
        # Verify
        openCalls = [call(read_data='A'),
                     call('./reports/eft_report/myID-2018-06-06.txt', 'w'),
                     call()().__enter__(),
                     call()().__enter__().write('Provider ID: myProvider\n'),
                     call()().__enter__().write('Service Provider: myName\n'),
                     call()().__enter__().write('Service Cost: myFee\n'),
                     call()().__enter__().close(),
                     call()().__exit__(None, None, None)]
        mockopen.assert_has_calls(openCalls)
        mockmakedirs.assert_called_once_with('./reports/eft_report', exist_ok=True)
        self.assertTrue(result)


@patch("builtins.print", create=True)
@patch("dataProcessing.dataProcessing.DataProcessing.write_provider_report")
class Testprovider_report(TestdataProcessing):
    def test_provider_report(self, mockwrite_provider_report, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllProviders.return_value.payload = {}
        # Actual
        result = self.myClass.provider_report()
        # Verify
        mockprint.assert_called_once_with("Database is Empty")
        self.assertFalse(result)

    def test_provider_report1(self, mockwrite_provider_report, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllProviders.return_value.payload = [{"id": "100000000"}]
        # Actual
        self.myClass.provider_report()
        # Verify
        mockwrite_provider_report.assert_called_once_with("100000000")


@patch("builtins.print", autospec=True)
class Testlist_services_history(TestdataProcessing):
    def test_list_services_history(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllServices.return_value.payload = []
        # Actual
        self.myClass.list_services_history()
        # Verify
        mockprint.assert_called_once_with("Database is Empty")

    def test_list_services_history1(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllServices.return_value.payload = [{"id": "1", "code": "2", "provider": "3", "member": "4",
                                                                "received": "5", "comment": '6', "status": "7"},
                                                               {"id": "1", "code": "2", "provider": "3", "member": "4",
                                                                "received": "5", "comment": '6', "status": "7"}]
        # Actual
        self.myClass.list_services_history()
        # Verify
        printCalls = [call('Service id     code      Member id      Provider id    status'),
                      call('1              2         4              3              7'),
                      call('1              2         4              3              7')]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testprovider_ID(TestdataProcessing):
    def test_provider_ID(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getProvider.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.provider_ID()
        # Verify
        mockinput.assert_called_once_with("Enter service provider id: ")
        mockprint.assert_called_once_with("Invalid Provider id")
        self.assertEqual(result, False)

    def test_provider_ID1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getProvider.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        mockinput.return_value = "x"
        # Actual
        result = self.myClass.provider_ID()
        # Verify
        mockinput.assert_called_once_with("Enter service provider id: ")
        self.assertEqual(result, "x")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testprovider_member(TestdataProcessing):
    def test_provider_member(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.provider_member()
        # Verify
        mockinput.assert_called_once_with("Enter member id: ")
        mockprint.assert_called_once_with("Invalid Member id")
        self.assertEqual(result, False)

    def test_provider_member1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        mockinput.return_value = "x"
        # Actual
        result = self.myClass.provider_member()
        # Verify
        mockinput.assert_called_once_with("Enter member id: ")
        self.assertEqual(result, "x")


@patch("dataProcessing.dataProcessing.DataProcessing.provider_ID")
@patch("dataProcessing.dataProcessing.DataProcessing.provider_member")
@patch("builtins.input", autospec=True)
@patch("random.choice")
@patch("builtins.print", autospec=True)
class Testprovide_service(TestdataProcessing):
    def test_provide_service(self, mockprint, mockrandom, mockinput, mockprovider_member, mockprovider_ID):
        # Setup
        mockprovider_ID.return_value = False
        # Actual
        result = self.myClass.provide_service()
        # Verify
        mockprovider_ID.assert_called_once_with()
        self.assertEqual(result, False)

    def test_provide_service1(self, mockprint, mockrandom, mockinput, mockprovider_member, mockprovider_ID):
        # Setup
        mockprovider_ID.return_value = "123"
        mockprovider_member.return_value = False
        # Actual
        result = self.myClass.provide_service()
        # Verify
        mockprovider_ID.assert_called_once_with()
        mockprovider_member.assert_called_once_with()
        self.assertEqual(result, False)

    def test_provide_service2(self, mockprint, mockrandom, mockinput, mockprovider_member, mockprovider_ID):
        # Setup
        self.myClass.key = MagicMock()
        mockprovider_ID.return_value = "123"
        mockprovider_member.return_value = "456"
        mockinput.side_effect = iter(["x", "y", "z", "Y"])
        self.myClass.STATUS_PAID = "paid"
        self.myClass.isValidId = False
        mockrandom.return_value = "9876543210"
        self.myClass.ERROR_DUPLICATE_ID = "Error: attempted to reuse a unique ID"
        self.myClass.nc.addService.return_value.error = None
        # Actual
        result = self.myClass.provide_service()
        # Verify
        mockprovider_ID.assert_called_once_with()
        mockprovider_member.assert_called_once_with()
        inputCalls = [call("Enter service date (MM/DD/YYYY) : "), call("Enter 6 digit service code: "),
                      call("Please include comments on service: "), call("Was this service paid? (y/n): ")]
        mockinput.assert_has_calls(inputCalls)
        mockprint.assert_called_once_with(
            "New Service ID: 987654321098765432109876543210987654321098765432109876543210987654321098765432109876543210")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testupdate_provided_service_id_verify(TestdataProcessing):
    def test_update_provided_service_id_verify(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getService.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        self.myClass.update_provided_service_id_verify()
        # Verify
        mockinput.assert_called_once_with("Enter service id: ")
        mockprint.assert_called_once_with("Invalid Input")

    def test_update_provided_service_id_verify1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getService.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        self.myClass.update_provided_service_id_verify()
        # Verify
        mockinput.assert_called_once_with("Enter service id: ")
        printCalls = [call("Service id     code      Member id      Provider id    status")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
class Testupdate_provided_service_select_code(TestdataProcessing):
    def test_update_provided_service_select_code(self, mockinput):
        # Setup
        mockinput.return_value = "Y"
        self.myClass.key = MagicMock()
        # Actual
        self.myClass.update_provided_service_select_code()
        # Verify
        inputCalls = [call("Change service code? (y/n): "), call("Enter service code: ")]
        mockinput.assert_has_calls(inputCalls)

    def test_update_provided_service_select_code1(self, mockinput):
        # Setup
        mockinput.return_value = "n"
        self.myClass.key = MagicMock()
        # Actual
        result = self.myClass.update_provided_service_select_code()
        # Verify
        mockinput.assert_called_once_with("Change service code? (y/n): ")
        self.assertEqual(result, False)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testupdate_provided_service_select_member(TestdataProcessing):
    def test_update_provided_service_select_member(self, mockprint, mockinput):
        # Setup
        mockinput.return_value = "Y"
        self.myClass.key = MagicMock()
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.nc.getMember.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.update_provided_service_select_member()
        # Verify
        inputCalls = [call('Change member id? (y/n): '), call('Enter member id: ')]
        mockinput.assert_has_calls(inputCalls)
        mockprint.assert_called_once_with("Invalid Member id")
        self.assertFalse(result)

    def test_update_provided_service_select_member1(self, mockprint, mockinput):
        # Setup
        mockinput.return_value = "Y"
        self.myClass.key = MagicMock()
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.nc.getMember.return_value.error = None
        # Actual
        result = self.myClass.update_provided_service_select_member()
        # Verify
        inputCalls = [call('Change member id? (y/n): '), call('Enter member id: ')]
        mockinput.assert_has_calls(inputCalls)
        self.assertTrue(result)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testupdate_provided_service_select_provider(TestdataProcessing):
    def test_update_provided_service_select_provider(self, mockprint, mockinput):
        # Setup
        mockinput.return_value = "Y"
        self.myClass.key = MagicMock()
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.nc.getProvider.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.update_provided_service_select_provider()
        # Verify
        inputCalls = [call("Change Provider id? (y/n): "), call("Enter provider id: ")]
        mockinput.assert_has_calls(inputCalls)
        mockprint.assert_called_once_with("Invalid provider id")
        self.assertFalse(result)

    def test_update_provided_service_select_provider1(self, mockprint, mockinput):
        # Setup
        mockinput.return_value = "Y"
        self.myClass.key = MagicMock()
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.nc.getProvider.return_value.error = None
        # Actual
        result = self.myClass.update_provided_service_select_provider()
        # Verify
        inputCalls = [call("Change Provider id? (y/n): "), call("Enter provider id: ")]
        mockinput.assert_has_calls(inputCalls)
        self.assertTrue(result)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testupdate_provided_service_select_status(TestdataProcessing):
    def test_update_provided_service_select_status(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.return_value = "Y"
        # Actual
        self.myClass.update_provided_service_select_status()
        # Verify
        inputCalls = [call("Change account status? (y/n): "), call("Was this service paid? (y/n): ")]
        mockinput.assert_has_calls(inputCalls)


@patch("dataProcessing.dataProcessing.DataProcessing.update_provided_service_id_verify")
@patch("dataProcessing.dataProcessing.DataProcessing.update_provided_service_select_code")
@patch("dataProcessing.dataProcessing.DataProcessing.update_provided_service_select_member")
@patch("dataProcessing.dataProcessing.DataProcessing.update_provided_service_select_provider")
@patch("dataProcessing.dataProcessing.DataProcessing.update_provided_service_select_status")
class Testupdate_provided_service(TestdataProcessing):
    def test_update_provided_service(self, mockupdate_provided_service_select_status,
                                     mockupdate_provided_service_select_provider,
                                     mockupdate_provided_service_select_member,
                                     mockupdate_provided_service_select_code, mockupdate_provided_service_id_verify):
        # Setup
        mockupdate_provided_service_id_verify.return_value = True
        mockupdate_provided_service_select_code.return_value = True
        mockupdate_provided_service_select_member.return_value = True
        mockupdate_provided_service_select_provider.return_value = True
        mockupdate_provided_service_select_status.return_value = True
        # Actual
        self.myClass.update_provided_service()
        # Verify
        mockupdate_provided_service_id_verify.assert_called_once_with()
        mockupdate_provided_service_select_code.assert_called_once_with()
        mockupdate_provided_service_select_member.assert_called_once_with()
        mockupdate_provided_service_select_provider.assert_called_once_with()
        mockupdate_provided_service_select_status.assert_called_once_with()

    def test_update_provided_service1(self, mockupdate_provided_service_select_status,
                                      mockupdate_provided_service_select_provider,
                                      mockupdate_provided_service_select_member,
                                      mockupdate_provided_service_select_code, mockupdate_provided_service_id_verify):
        # Setup
        mockupdate_provided_service_id_verify.return_value = False
        mockupdate_provided_service_select_code.return_value = True
        mockupdate_provided_service_select_member.return_value = True
        mockupdate_provided_service_select_provider.return_value = True
        mockupdate_provided_service_select_status.return_value = True
        # Actual
        self.myClass.update_provided_service()
        # Verify
        mockupdate_provided_service_id_verify.assert_called_once_with()

    def test_update_provided_service2(self, mockupdate_provided_service_select_status,
                                      mockupdate_provided_service_select_provider,
                                      mockupdate_provided_service_select_member,
                                      mockupdate_provided_service_select_code, mockupdate_provided_service_id_verify):
        # Setup
        mockupdate_provided_service_id_verify.return_value = True
        mockupdate_provided_service_select_code.return_value = False
        mockupdate_provided_service_select_member.return_value = True
        mockupdate_provided_service_select_provider.return_value = True
        mockupdate_provided_service_select_status.return_value = True
        # Actual
        self.myClass.update_provided_service()
        # Verify
        mockupdate_provided_service_id_verify.assert_called_once_with()
        mockupdate_provided_service_select_code.assert_called_once_with()

    def test_update_provided_service3(self, mockupdate_provided_service_select_status,
                                      mockupdate_provided_service_select_provider,
                                      mockupdate_provided_service_select_member,
                                      mockupdate_provided_service_select_code, mockupdate_provided_service_id_verify):
        # Setup
        mockupdate_provided_service_id_verify.return_value = True
        mockupdate_provided_service_select_code.return_value = True
        mockupdate_provided_service_select_member.return_value = False
        mockupdate_provided_service_select_provider.return_value = True
        mockupdate_provided_service_select_status.return_value = True
        # Actual
        self.myClass.update_provided_service()
        # Verify
        mockupdate_provided_service_id_verify.assert_called_once_with()
        mockupdate_provided_service_select_code.assert_called_once_with()
        mockupdate_provided_service_select_member.assert_called_once_with()

    def test_update_provided_service4(self, mockupdate_provided_service_select_status,
                                      mockupdate_provided_service_select_provider,
                                      mockupdate_provided_service_select_member,
                                      mockupdate_provided_service_select_code, mockupdate_provided_service_id_verify):
        # Setup
        mockupdate_provided_service_id_verify.return_value = True
        mockupdate_provided_service_select_code.return_value = True
        mockupdate_provided_service_select_member.return_value = True
        mockupdate_provided_service_select_provider.return_value = False
        mockupdate_provided_service_select_status.return_value = True
        # Actual
        self.myClass.update_provided_service()
        # Verify
        mockupdate_provided_service_id_verify.assert_called_once_with()
        mockupdate_provided_service_select_code.assert_called_once_with()
        mockupdate_provided_service_select_member.assert_called_once_with()
        mockupdate_provided_service_select_provider.assert_called_once_with()

    def test_update_provided_service5(self, mockupdate_provided_service_select_status,
                                      mockupdate_provided_service_select_provider,
                                      mockupdate_provided_service_select_member,
                                      mockupdate_provided_service_select_code, mockupdate_provided_service_id_verify):
        # Setup
        mockupdate_provided_service_id_verify.return_value = True
        mockupdate_provided_service_select_code.return_value = True
        mockupdate_provided_service_select_member.return_value = True
        mockupdate_provided_service_select_provider.return_value = True
        mockupdate_provided_service_select_status.return_value = False
        # Actual
        self.myClass.update_provided_service()
        # Verify
        mockupdate_provided_service_id_verify.assert_called_once_with()
        mockupdate_provided_service_select_code.assert_called_once_with()
        mockupdate_provided_service_select_member.assert_called_once_with()
        mockupdate_provided_service_select_provider.assert_called_once_with()
        mockupdate_provided_service_select_status.assert_called_once_with()


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testremove_provided_service(TestdataProcessing):
    def test_remove_provided_service(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getService.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.remove_provided_service()
        # Verify
        mockinput.assert_called_once_with("Enter service id: ")
        mockprint.assert_called_once_with("Invalid Input")
        self.assertFalse(result)

    def test_remove_provided_service1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.side_effect = iter(["123", "Y"])
        self.myClass.nc.getService.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.remove_provided_service()
        # Verify
        inputCalls = [call("Enter service id: "), call(" \nRemove this service? (Y/N): ")]
        mockinput.assert_has_calls(inputCalls)
        printCalls = [call("Service Removed")]
        mockprint.assert_has_calls(printCalls)
        self.assertTrue(result)


@patch("builtins.print", autospec=True)
class Testlist_all_members(TestdataProcessing):
    def test_list_all_members(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllMembers.return_value.payload = []
        # Actual
        result = self.myClass.list_all_members()
        # Verify
        mockprint.assert_called_once_with("Database is Empty")
        self.assertFalse(result)

    def test_list_all_members1(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllMembers.return_value.payload = [{"status": "STATUS_UNBANNED", "id": "2", "name": "3",
                                                               "address": "4", "city": "5", "state": '6', "zip": "7"}]
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        # Actual
        result = self.myClass.list_all_members()
        # Verify
        printCall = [call('Status         Id             Name           Address'),
                     call('Active         2              3              45, 6, 7')]
        mockprint.assert_has_calls(printCall)

    def test_list_all_members2(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllMembers.return_value.payload = [{"status": "BANNED", "id": "2", "name": "3",
                                                               "address": "4", "city": "5", "state": '6', "zip": "7"}]
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        # Actual
        result = self.myClass.list_all_members()
        # Verify
        printCall = [call('Status         Id             Name           Address'),
                     call('Banned         2              3              45, 6, 7')]
        mockprint.assert_has_calls(printCall)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testmember_status(TestdataProcessing):
    def test_member_status(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.member_status()
        # Verify
        mockinput.assert_called_once_with("Member ID: ")
        mockprint.assert_called_once_with("Invalid Input")
        self.assertFalse(result)

    def test_member_status1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.nc.getMember.return_value.payload = {"status": "STATUS_UNBANNED", "id": "2", "name": "3",
                                                          "address": "4", "city": "5", "state": '6', "zip": "7"}
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        # Actual
        self.myClass.member_status()
        # Verify
        mockinput.assert_called_once_with("Member ID: ")
        printCall = [call('Status         Id             Name           Address'),
                     call('Active         2              3              45, 6, 7')]
        mockprint.assert_has_calls(printCall)

    def test_member_status2(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.nc.getMember.return_value.payload = {"status": "BANNED", "id": "2", "name": "3",
                                                          "address": "4", "city": "5", "state": '6', "zip": "7"}
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        # Actual
        self.myClass.member_status()
        # Verify
        mockinput.assert_called_once_with("Member ID: ")
        printCall = [call('Status         Id             Name           Address'),
                     call('Banned         2              3              45, 6, 7')]
        mockprint.assert_has_calls(printCall)


@patch("builtins.input", autospec=True)
@patch("random.choice")
@patch("builtins.print", autospec=True)
class Testadd_member(TestdataProcessing):
    def test_add_member(self, mockprint, mockrandom, mockinput):
        # Setup
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        mockrandom.return_value = "9876543210"
        self.myClass.key = MagicMock()
        self.myClass.nc.addMember.return_value.error = None
        self.myClass.ERROR_DUPLICATE_ID = "Error: attempted to reuse a unique ID"
        # Actual
        self.myClass.add_member()
        # Verify
        inputCalls = [call("What is the name of the member? : "),
                      call("What is the address? (Enter street address here): "),
                      call("City: "), call("State: "), call("Zip Code: ")]
        mockinput.assert_has_calls(inputCalls)
        mockprint.assert_has_calls([call(
            "New Member ID: 987654321098765432109876543210987654321098765432109876543210987654321098765432109876543210")])


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testremove_member(TestdataProcessing):
    def test_remove_member(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.remove_member()
        # Verify
        mockinput.assert_called_once_with("Member ID: ")
        mockprint.assert_called_once_with("Invalid Input")
        self.assertFalse(result)

    def test_remove_member1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.side_effect = iter(["x", "Y"])
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        self.myClass.nc.getMember.return_value.payload = {"status": "BANNED", "id": "2", "name": "3",
                                                          "address": "4", "city": "5", "state": '6', "zip": "7"}
        # Actual
        self.myClass.remove_member()
        # Verify
        inputCalls = [call("Member ID: "), call("Confirmation for deletion Y/N : ")]
        mockinput.assert_has_calls(inputCalls)
        printCalls = [call('Status         Id             Name           Address'),
                      call('Banned         2              3              45, 6, 7'),
                      call("Successfully removed member : x\n")]
        mockprint.assert_has_calls(printCalls)

    def test_remove_member2(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.side_effect = iter(["x", "Y"])
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        self.myClass.nc.getMember.return_value.payload = {"status": "STATUS_UNBANNED", "id": "2", "name": "3",
                                                          "address": "4", "city": "5", "state": '6', "zip": "7"}
        # Actual
        self.myClass.remove_member()
        # Verify
        inputCalls = [call("Member ID: "), call("Confirmation for deletion Y/N : ")]
        mockinput.assert_has_calls(inputCalls)
        printCalls = [call('Status         Id             Name           Address'),
                      call('Active         2              3              45, 6, 7'),
                      call("Successfully removed member : x\n")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.print", autospec=True)
class Testprint_member(TestdataProcessing):
    def test_print_member(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.payload = {"status": "STATUS_UNBANNED", "id": "2", "name": "3",
                                                          "address": "4", "city": "5", "state": '6', "zip": "7"}
        self.myClass.STATUS_UNBANNED = "STATUS_UNBANNED"
        # Actual
        self.myClass.print_member("123")
        # Verify
        printCalls = [call('Status         Id             Name           Address'),
                      call('Active         2              3              45, 6, 7'),
                      call(""), call("")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.print", autospec=True)
class Testcheck_member(TestdataProcessing):
    def test_check_member(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.check_member("123")
        # Verify
        mockprint.assert_called_once_with("Invalid Member id")
        self.assertFalse(result)

    def test_check_member1(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMember.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.check_member("123")
        # Verify
        self.assertTrue(result)


@patch("random.choice")
class Testchange_m_id(TestdataProcessing):
    def test_change_m_id(self, mockrandom):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.setMember.return_value.error = None
        self.myClass.ERROR_DUPLICATE_ID = "Error: attempted to reuse a unique ID"
        mockrandom.return_value = "9876543210"
        # Actual
        result = self.myClass.change_m_id("123")
        # verify
        self.assertTrue(result)


@patch("builtins.input", autospec=True)
class Testchange_member_name(TestdataProcessing):
    def test_change_member_name(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        # Actual
        result = self.myClass.change_member_name("")
        # Verify
        mockinput.assert_called_once_with("Enter Member name: ")
        self.assertEqual(result, None)


@patch("builtins.input", autospec=True)
class Testchange_member_address(TestdataProcessing):
    def test_change_member_address(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        # Actual
        self.myClass.change_member_address("123")
        # verify
        inputCalls = [call("Enter Member's street address: "), call("City: "), call("State: "), call("Zip Code: ")]
        mockinput.assert_has_calls(inputCalls)


@patch("builtins.input", autospec=True)
class Testchange_member_status(TestdataProcessing):
    def test_change_member_status(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.return_value = "Y"
        # Actual
        self.myClass.change_member_status("123")
        # Verify
        mockinput.assert_called_once_with("Is the member active? (Y/N): ")


@patch("builtins.input", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.check_member")
@patch("builtins.print", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.print_member")
@patch("dataProcessing.dataProcessing.DataProcessing.change_m_id")
@patch("dataProcessing.dataProcessing.DataProcessing.change_member_name")
@patch("dataProcessing.dataProcessing.DataProcessing.change_member_address")
@patch("dataProcessing.dataProcessing.DataProcessing.change_member_status")
class Testset_member(TestdataProcessing):
    def test_set_member(self, mockchange_member_status, mockchange_member_address, mockchange_member_name,
                        mockchange_m_id, mockprint_member, mockprint, mockcheck_member, mockinput):
        # Setup
        mockcheck_member.return_value = False
        mockinput.return_value = "123"
        # Actual
        result = self.myClass.set_member()
        # Verify
        mockinput.assert_called_once_with("Enter member id: ")
        mockcheck_member.assert_called_once_with("123")
        mockprint.assert_called_once_with("Invalid Input")
        self.assertFalse(result)

    def test_set_member1(self, mockchange_member_status, mockchange_member_address, mockchange_member_name,
                         mockchange_m_id, mockprint_member, mockprint, mockcheck_member, mockinput):
        # Setup
        mockcheck_member.return_value = True
        mockchange_m_id.return_value = "456"
        mockinput.side_effect = iter(["123", "Y", "Y", "Y", "Y"])
        # Actual
        self.myClass.set_member()
        # Verify
        inputCalls = [call('Enter member id: '), call(' \nChange Member id? (Y/N): '),
                      call(' \nChange Member name? (Y/N): '), call(' \nChange Member address? (Y/N): '),
                      call(' \nChange Member Status? (Y/N): ')]
        mockinput.assert_has_calls(inputCalls)
        mockcheck_member.assert_called_once_with("123")
        mockprint_member.assert_called_once_with("123")
        mockchange_m_id.assert_called_once_with("123")
        mockchange_member_name.assert_called_once_with("456")
        mockchange_member_address.assert_called_once_with("456")
        mockchange_member_status.assert_called_once_with("456")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testdelete_members_table(TestdataProcessing):
    def test_delete_members_table(self, mockprint, mockinput):
        # Setup
        mockinput.return_value = "Y"
        self.myClass.key = MagicMock()
        self.myClass.nc.truncateMembers.return_value.error = "No error"
        self.myClass.NO_ERROR = "No error"
        # Actual
        self.myClass.delete_members_table()
        # Verify
        mockprint.assert_called_once_with("Successfully Deleted All Member Info")

    def test_delete_members_table1(self, mockprint, mockinput):
        # Setup
        mockinput.return_value = "n"
        # Actual
        result = self.myClass.delete_members_table()
        # Verify
        mockprint.assert_called_once_with("Canceled")
        self.assertFalse(result)


@patch("builtins.print", autospec=True)
class Testcheck_provider(TestdataProcessing):
    def test_check_provider(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getProvider.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.check_provider("123")
        # Verify
        mockprint.assert_called_once_with("Invalid Provider id")
        self.assertFalse(result)

    def test_check_provider1(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getProvider.return_value.error = None
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        # Actual
        result = self.myClass.check_provider("123")
        # Verify
        self.assertTrue(result)


@patch("dataProcessing.dataProcessing.DataProcessing.create_p_id")
@patch("builtins.input", autospec=True)
class Testadd_provider(TestdataProcessing):
    def test_add_provider(self, mockinput, mockcreate_p_id):
        # Setup
        self.myClass.key = MagicMock()
        # Actual
        self.myClass.add_provider()
        # Verify
        mockcreate_p_id.assert_called_once_with()
        inputCalls = [call("Enter Provider name: "), call("Enter Provider street address: "),
                      call("City: "), call("State: "), call("Zip Code: ")]
        mockinput.assert_has_calls(inputCalls)


@patch("random.choice")
class Testchange_p_id(TestdataProcessing):
    def test_change_p_id(self, mockrandom):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.setProvider.return_value.error = None
        self.myClass.ERROR_DUPLICATE_ID = "Error: attempted to reuse a unique ID"
        mockrandom.return_value = "9876543210"
        # Actual
        result = self.myClass.change_p_id("123")
        # Verify
        self.assertTrue(result)


@patch("builtins.input", autospec=True)
class Testchange_provider_name(TestdataProcessing):
    def test_change_provider_name(self, mockinput):
        self.myClass.key = MagicMock()
        # Actual
        result = self.myClass.change_provider_name("123")
        # Verify
        mockinput.assert_called_once_with("Enter Provider name: ")
        self.assertEqual(result, None)


@patch("builtins.input", autospec=True)
class Testchange_provider_address(TestdataProcessing):
    def test_change_provider_address(self, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        # Actual
        self.myClass.change_provider_address("123")
        # Verify
        inputCalls = [call("Enter Provider street address: "), call("City: "), call("State: "), call("Zip Code: ")]
        mockinput.assert_has_calls(inputCalls)


@patch("builtins.print", autospec=True)
class Testget_all_providers(TestdataProcessing):
    def test_get_all_providers(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllProviders.return_value.payload = []
        # Actual
        result = self.myClass.get_all_providers()
        # Verify
        mockprint.assert_called_once_with("Database is Empty")
        self.assertFalse(result)

    def test_get_all_providers1(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllProviders.return_value.payload = [{"status": "STATUS_UNBANNED", "id": "2", "name": "3",
                                                                 "address": "4", "city": "5", "state": '6', "zip": "7"}]
        # Actual
        result = self.myClass.get_all_providers()
        # Verify
        printCalls = [call('Id             Name           Address'),
                      call('2              3              45, 6, 7')]
        mockprint.assert_has_calls(printCalls)
        self.assertFalse(result)


@patch("random.choice")
class Testcreate_s_id(TestdataProcessing):
    def test_create_s_id(self, mockrandom):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getService.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        mockrandom.return_value = "9876543210"
        # Actual
        result = self.myClass.create_s_id()
        # Verify
        self.assertEqual(result,
                         "987654321098765432109876543210987654321098765432109876543210987654321098765432109876543210")


@patch("random.choice")
class Testcreate_p_id(TestdataProcessing):
    def test_create_p_id(self, mockrandom):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getProvider.return_value.error = "Error: unable to retrieve nonexistent entry from database"
        self.myClass.ERROR_NONEXISTENT_ENTRY = "Error: unable to retrieve nonexistent entry from database"
        mockrandom.return_value = "9876543210"
        # Actual
        result = self.myClass.create_p_id()
        # Verify
        self.assertEqual(result,
                         "987654321098765432109876543210987654321098765432109876543210987654321098765432109876543210")


@patch("builtins.input", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.check_provider")
@patch("builtins.print", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.print_provider")
@patch("dataProcessing.dataProcessing.DataProcessing.change_p_id")
@patch("dataProcessing.dataProcessing.DataProcessing.change_provider_name")
@patch("dataProcessing.dataProcessing.DataProcessing.change_provider_address")
class Testset_provider(TestdataProcessing):
    def test_set_provider(self, mockchange_provider_address, mockchange_provider_name, mockchange_p_id,
                          mockprint_provider, mockprint, mockcheck_provider, mockinput):
        # Setup
        mockinput.return_value = "123"
        mockcheck_provider.return_value = False
        # Actual
        result = self.myClass.set_provider()
        # Verify
        mockinput.assert_called_once_with("Enter Provider id: ")
        mockcheck_provider.assert_called_once_with("123")
        mockprint.assert_called_once_with("Invalid Input")
        self.assertFalse(result)

    def test_set_provider1(self, mockchange_provider_address, mockchange_provider_name, mockchange_p_id,
                           mockprint_provider, mockprint, mockcheck_provider, mockinput):
        # Setup
        mockinput.side_effect = iter(["123", "Y", "Y", "Y"])
        mockcheck_provider.return_value = True
        mockchange_p_id.return_value = "456"
        # Actual
        result = self.myClass.set_provider()
        # Verify
        inputCalls = [call("Enter Provider id: "), call(" \nChange Provider id? (Y/N): "),
                      call(" \nChange Provider name? (Y/N): "), call(" \nChange Provider address? (Y/N): ")]
        mockinput.assert_has_calls(inputCalls)
        mockcheck_provider.assert_called_once_with("123")
        mockprint_provider.assert_called_once_with("123")
        mockchange_provider_name.assert_called_once_with("456")
        mockchange_provider_address.assert_called_once_with("456")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.check_provider", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.print_provider", autospec=True)
class Testremove_provider(TestdataProcessing):
    def test_remove_provider(self, mockprint_provider, mockcheck_provider, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockcheck_provider.return_value = False
        mockinput.return_value = "123"
        # Actual
        result = self.myClass.remove_provider()
        # Verify
        mockcheck_provider.assert_called_once_with(self.myClass, "123")
        mockinput.assert_called_once_with("Enter Provider id: ")
        mockprint.assert_called_once_with("Invalid Input")
        self.assertFalse(result)

    def test_remove_provider1(self, mockprint_provider, mockcheck_provider, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockcheck_provider.return_value = True
        mockinput.side_effect = iter(["123", "Y"])
        # Actual
        result = self.myClass.remove_provider()
        # Verify
        mockcheck_provider.assert_called_once_with(self.myClass, "123")
        inputCalls = [call("Enter Provider id: "), call(" \nRemove this Provider? (Y/N): ")]
        mockinput.assert_has_calls(inputCalls)
        mockprint_provider.assert_called_once_with(self.myClass, "123")
        mockprint.assert_called_once_with("Provider Removed")
        self.assertTrue(result)


@patch("builtins.print", autospec=True)
class Testprint_provider(TestdataProcessing):
    def test_print_provider(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getProvider.return_value.payload = {"status": "STATUS_UNBANNED", "id": "2", "name": "3",
                                                            "address": "4", "city": "5", "state": '6', "zip": "7"}
        # Actual
        self.myClass.print_provider("123")
        # Verify
        printCalls = [call('   Id              Name                      Address              '),
                      call('2                3               4 5, 6, 7')]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.print", autospec=True)
class Testlist_all_service_offers(TestdataProcessing):
    def test_list_all_service_offers(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllMenuItems.return_value.payload = []
        # Actual
        self.myClass.list_all_service_offers()
        # Verify
        mockprint.assert_called_once_with("Database is empty")

    def test_list_all_service_offers1(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllMenuItems.return_value.payload = [{"id": "1", "name": "2", "fee": "123"}]
        # Actual
        self.myClass.list_all_service_offers()
        # Verify
        mockprint.assert_called_once_with("1              2              $123            ")

    def test_list_all_service_offers2(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllMenuItems.return_value.payload = [{"id": "1", "name": "2", "fee": "123"},
                                                                {"id": "1", "name": "2", "fee": "123"}]
        # Actual
        self.myClass.list_all_service_offers()
        # Verify
        printCalls = [call("1              2              $123            "),
                      call("1              2              $123            ")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
class Testuser_input_service_offer_id(TestdataProcessing):
    def test_user_input_service_offer_id(self, mockinput):
        # Setup
        mockinput.return_value = "i do not know"
        # Actual
        result = self.myClass.user_input_service_offer_id()
        # Verify
        mockinput.assert_called_once_with("\nWhat is the service offer id? 6 digits: ")
        self.assertEqual(result, "i do not know")


@patch("builtins.input", autospec=True)
class Testuser_input_service_offer_name(TestdataProcessing):
    def test_user_input_service_offer_name(self, mockinput):
        # Setup
        mockinput.return_value = "i do not know"
        # Actual
        result = self.myClass.user_input_service_offer_name()
        # Verify
        mockinput.assert_called_once_with("\nWhat is the name of the service")
        self.assertEqual(result, "i do not know")


@patch("builtins.input", autospec=True)
class Testuser_input_service_offer_fee(TestdataProcessing):
    def test_user_input_service_offer_fee(self, mockinput):
        # Setup
        mockinput.return_value = "i do not know"
        # Actual
        result = self.myClass.user_input_service_offer_fee()
        # Verify
        mockinput.assert_called_once_with("\nWhat is the fee of the service? in cents:")
        self.assertEqual(result, "i do not know")


@patch("dataProcessing.dataProcessing.DataProcessing.user_input_service_offer_id", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.user_input_service_offer_name", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.user_input_service_offer_fee", autospec=True)
class Testadd_a_service_offer(TestdataProcessing):
    def test_add_a_service_offer(self, mockuser_input_service_offer_fee, mockuser_input_service_offer_name,
                                 mockuser_input_service_offer_id):
        # Setup
        self.myClass.key = MagicMock()
        # Actual
        self.myClass.add_a_service_offer()
        # Verify
        mockuser_input_service_offer_id.assert_called_once_with(self.myClass)
        mockuser_input_service_offer_name.assert_called_once_with(self.myClass)
        mockuser_input_service_offer_fee.assert_called_once_with(self.myClass)


class Testcheck_a_service_offer(TestdataProcessing):
    def test_check_a_service_offer(self):
        # Actual
        result = self.myClass.check_a_service_offer("")
        # Verify
        self.assertFalse(result)

    def test_check_a_service_offer1(self):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMenuItem.return_value.error = "No error"
        self.myClass.NO_ERROR = "No error"
        # Actual
        result = self.myClass.check_a_service_offer("123")
        # Verify
        self.assertTrue(result)

    def test_check_a_service_offer2(self):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getMenuItem.return_value.error = None
        self.myClass.NO_ERROR = "No error"
        # Actual
        result = self.myClass.check_a_service_offer("123")
        # Verify
        self.assertEqual(result, None)


@patch("dataProcessing.dataProcessing.DataProcessing.user_input_service_offer_id", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.check_a_service_offer", autospec=True)
@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testremove_a_service_offer(TestdataProcessing):
    def test_remove_a_service_offer(self, mockprint, mockinput, mockcheck_a_service_offer,
                                    mockuser_input_service_offer_id):
        # Setup
        self.myClass.key = MagicMock()
        mockcheck_a_service_offer.return_value = True
        mockuser_input_service_offer_id.return_value = "123"
        mockinput.return_value = "Y"
        # Actual
        self.myClass.remove_a_service_offer()
        # Verify
        mockuser_input_service_offer_id.assert_called_once_with(self.myClass)
        mockcheck_a_service_offer.assert_called_once_with(self.myClass, "123")
        mockinput.assert_called_once_with("\nDo you really want to remove this service offer? ID: 123 Y/N")
        mockprint.assert_called_once_with("Successfully delete service Id: 123")

    def test_remove_a_service_offer1(self, mockprint, mockinput, mockcheck_a_service_offer,
                                     mockuser_input_service_offer_id):
        # Setup
        self.myClass.key = MagicMock()
        mockcheck_a_service_offer.return_value = False
        # Actual
        self.myClass.remove_a_service_offer()
        # Verify
        mockuser_input_service_offer_id.assert_called_once_with(self.myClass)
        mockprint.assert_called_once_with("Invalid Id")


'''
@patch("dataProcessing.dataProcessing.DataProcessing.user_input_service_offer_id", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.check_a_service_offer", autospec=True)
@patch("builtins.input", autospec=True)
class Testupdate_a_service_offer(TestdataProcessing):
    def test_update_a_service_offer(self, mockinput, mockcheck_a_service_offer, mockuser_input_service_offer_id):
        # Setup
        self.myClass.key = MagicMock()
        mockuser_input_service_offer_id.side_effect = iter(["123", "456"])
        mockcheck_a_service_offer.return_value = True
        mockinput.side_effect = iter(["Y", "y", "Y"])
        self.myClass.nc.getMenuItem.return_value.payload = {"Name": "myName", "Fee": "myFee"}
        # Actual
        self.myClass.update_a_service_offer()
        # Verify
        inputCalls = [call("\nDo you want to change the service offer id? Y/N"),
                      call("\nDo you want to change the name of the service offer? Y/N "),
                      call("\nDo you want to change the fee of the service offer? Y/N ")]
        mockinput.assert_has_calls(inputCalls)

'''


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testremove_all_service_offers(TestdataProcessing):
    def test_remove_all_service_offers(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.return_value = "Y"
        # Actual
        self.myClass.remove_all_service_offers()
        # Verify
        mockinput.assert_called_once_with("\nDo you really want to remove all service offers? Y/N")
        mockprint.assert_called_once_with("Successfully delete all offers")

    def test_remove_all_service_offers1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.return_value = "n"
        # Actual
        result = self.myClass.remove_all_service_offers()
        # Verify
        mockinput.assert_called_once_with("\nDo you really want to remove all service offers? Y/N")
        self.assertEqual(result, None)


@patch("builtins.print", autospec=True)
class Testlist_all_keys(TestdataProcessing):
    def test_list_all_keys(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllKeys.return_value.payload = []
        # Actual
        result = self.myClass.list_all_keys()
        # Verify
        mockprint.assert_called_once_with("Key Table is Empty")
        self.assertEqual(result, False)

    def test_list_all_keys1(self, mockprint):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.getAllKeys.return_value.payload = [{"name": "myname", "level": "mylevel", "id": "myid"}]
        # Actual
        self.myClass.list_all_keys()
        # Verify
        printCalls = [call('Name           Level          Hash (ID/Primary Key)'),
                      call('myname         mylevel        myid           ')]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testupdate_key_modify_name(TestdataProcessing):
    def test_update_key_modify_name(self, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["y", "Li"])
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        result = self.myClass.update_key_modify_name()
        # Verify
        inputCall = [call("Do you want to modify the name? Y/N"), call("What is the new name?")]
        mockinput.assert_has_calls(inputCall)
        self.assertTrue(result)

    def test_update_key_modify_name1(self, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["n", "Li"])
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        result = self.myClass.update_key_modify_name()
        # Verify
        mockinput.assert_called_once_with("Do you want to modify the name? Y/N")
        mockprint.assert_called_once_with("name not changed")
        self.assertFalse(result)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testupdate_key_modify_level(TestdataProcessing):
    def test_update_key_modify_level(self, mockprint, mockInput):
        # Setup
        mockInput.side_effect = iter(["y", "1"])
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        self.myClass.update_key_modify_level()
        # Verify
        inputCalls = [call("\nDo you want to change the access level of the key? Y/N"),
                      call("\nwhat is the level of the key? \n" + "1. Manager Key \n" + "2. Provider Key \n")]
        mockInput.assert_has_calls(inputCalls)

    def test_update_key_modify_level1(self, mockprint, mockInput):
        # Setup
        mockInput.side_effect = iter(["y", "2"])
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        self.myClass.update_key_modify_level()
        # Verify
        inputCalls = [call("\nDo you want to change the access level of the key? Y/N"),
                      call("\nwhat is the level of the key? \n" + "1. Manager Key \n" + "2. Provider Key \n")]
        mockInput.assert_has_calls(inputCalls)

    def test_update_key_modify_level2(self, mockprint, mockInput):
        # Setup
        mockInput.side_effect = iter(["y", "Li"])
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        self.myClass.update_key_modify_level()
        # Verify
        inputCalls = [call("\nDo you want to change the access level of the key? Y/N"),
                      call("\nwhat is the level of the key? \n" + "1. Manager Key \n" + "2. Provider Key \n")]
        mockprint.assert_called_once_with("Access level not changed.")
        mockInput.assert_has_calls(inputCalls)

    def test_update_key_modify_level3(self, mockprint, mockInput):
        # Setup
        mockInput.return_value = "n"
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        self.myClass.update_key_modify_level()
        # Verify
        mockInput.assert_called_once_with("\nDo you want to change the access level of the key? Y/N")
        mockprint.assert_called_once_with("Access level not changed")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("random.choices", autospec=True)
class Testupdate_key_unique_key(TestdataProcessing):
    def test_update_key_unique_key(self, mockrandom, mockprint, mockinput):
        # Setup
        mockinput.return_value = "y"
        mockrandom.return_value = "0987654321"
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        self.myClass.update_key_unique_key()
        # Verify
        mockinput.assert_called_once_with("\nDo you want to change the unique access key? Y/N")
        mockprint.assert_called_once_with('Your new unique access key is', '0987654321', '.')

    def test_update_key_unique_key1(self, mockrandom, mockprint, mockinput):
        # Setup
        mockinput.return_value = "n"
        mockrandom.return_value = "0987654321"
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        # Actual
        self.myClass.update_key_unique_key()
        # Verify
        mockinput.assert_called_once_with("\nDo you want to change the unique access key? Y/N")
        mockprint.assert_called_once_with("access key not changed")


@patch("builtins.input", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.update_key_modify_name", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.update_key_modify_level", autospec=True)
@patch("dataProcessing.dataProcessing.DataProcessing.update_key_unique_key", autospec=True)
@patch("builtins.print", autospec=True)
class Testupdate_a_key(TestdataProcessing):
    def test_update_a_key(self, mockprint, mockupdate_key_unique_key, mockupdate_key_modify_level, mockupdate_key_modify_name, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = "provider"
        self.myClass.KEY_PROVIDER = "provider"
        # Actual
        self.myClass.update_a_key()
        # Verify
        mockinput.assert_called_once_with("\nWhat is the UAK that you want to modify?")
        mockupdate_key_modify_name.assert_called_once_with(self.myClass)
        mockupdate_key_modify_level.assert_called_once_with(self.myClass)
        mockupdate_key_unique_key.assert_called_once_with(self.myClass)

    def test_update_a_key1(self, mockprint, mockupdate_key_unique_key, mockupdate_key_modify_level, mockupdate_key_modify_name, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.mykey = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = None
        self.myClass.KEY_PROVIDER = "provider"
        # Actual
        self.myClass.update_a_key()
        # Verify
        mockinput.assert_called_once_with("\nWhat is the UAK that you want to modify?")
        mockprint.assert_called_once_with("Key is invalid")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testvalidate_a_key(TestdataProcessing):
    def test_validate_a_key(self, mockinput, mocinput):
        # Setup
        self.myClass.key = MagicMock()
        self.myClass.nc.validateKey.return_value.payload = "x"
        # Actaul
        self.myClass.validate_a_key()
        # verify
        mocinput.assert_called_once_with("What is the key?: ")
        mockinput.assert_called_once_with("\nx\n")


@patch("builtins.input", autospec=True)
@patch("random.choices", autospec=True)
@patch("builtins.print", autospec=True)
class Testadd_a_key(TestdataProcessing):
    def test_add_a_key(self, mockprint, mockrandom, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockrandom.return_value = "9876543210"
        mockinput.return_value = "1"
        # Actual
        self.myClass.add_a_key()
        # Verify
        inputCalls = [call("What is the name? "),
                      call("what is the level of the key? \n" + "1. Manager Key \n" + "2. Provider Key \n")]
        mockinput.assert_has_calls(inputCalls)
        mockprint.assert_called_once_with("Your new unique access key is", "9876543210", ".")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testremove_a_key(TestdataProcessing):
    def test_remove_a_key(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.side_effect = iter(["key", "y"])
        self.myClass.KEY_ROOT = "root"
        self.myClass.NO_ERROR = "No error"
        self.myClass.nc.validateKey.return_value.payload = "root"
        self.myClass.nc.removeKey.return_value.error = "No error"
        # Actual
        self.myClass.remove_a_key()
        # Verify
        inputCalls = [call("\nWhat is the key you want to remove?: "),
                      call("Do you really want to remove the key? Y/N")]
        mockinput.assert_has_calls(inputCalls)
        mockprint.assert_called_once_with("Successfully deleted key from key table")

    def test_remove_a_key1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.side_effect = iter(["key", "n"])
        self.myClass.KEY_ROOT = "root"
        self.myClass.NO_ERROR = "No error"
        self.myClass.nc.validateKey.return_value.payload = "root"
        self.myClass.nc.removeKey.return_value.error = None
        # Actual
        self.myClass.remove_a_key()
        # Verify
        inputCalls = [call("\nWhat is the key you want to remove?: "),
                      call("Do you really want to remove the key? Y/N")]
        mockinput.assert_has_calls(inputCalls)
        mockprint.assert_called_once_with("Canceled")

    def test_remove_a_key2(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.side_effect = iter(["key", "n"])
        self.myClass.KEY_ROOT = "root"
        self.myClass.nc.validateKey.return_value.payload = None
        # Actual
        self.myClass.remove_a_key()
        # Verify
        mockinput.assert_called_once_with("\nWhat is the key you want to remove?: ")
        mockprint.assert_called_once_with("Canceled")


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
class Testremove_all_keys(TestdataProcessing):
    def test_remove_all_keys(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.return_value = "y"
        self.myClass.NO_ERROR = "No error"
        self.myClass.nc.truncateKeys.return_value.error = "No error"
        # Actual
        self.myClass.remove_all_keys()
        # Verify
        mockinput.assert_called_once_with("\nDo you really want to delete all keys? Y/N :")
        mockprint.assert_called_once_with("Successfully Deleted All Keys")

    def test_remove_all_keys1(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.return_value = "y"
        self.myClass.NO_ERROR = "no error"
        self.myClass.nc.truncateKeys.return_value.error = "an error occurred"
        # Actual
        self.myClass.remove_all_keys()
        # Verify
        mockinput.assert_called_once_with("\nDo you really want to delete all keys? Y/N :")
        mockprint.assert_called_once_with("an error occurred")

    def test_remove_all_keys2(self, mockprint, mockinput):
        # Setup
        self.myClass.key = MagicMock()
        mockinput.return_value = "n"
        self.myClass.NO_ERROR = "no error"
        self.myClass.nc.truncateKeys.return_value.error = "an error occurred"
        # Actual
        self.myClass.remove_all_keys()
        # Verify
        mockinput.assert_called_once_with("\nDo you really want to delete all keys? Y/N :")
        mockprint.assert_called_once_with("Canceled")


if __name__ == '__main__':
    unittest.main()
