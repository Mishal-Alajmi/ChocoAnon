import unittest
from unittest.mock import patch, MagicMock, call, ANY
import sys
sys.path.insert(0, "..")
from menu.menu import MenuInterface


class Test_Menu(unittest.TestCase):
    def setUp(self):
        nc = MagicMock()
        self.myClass = MenuInterface(nc)

    def tearDown(self):
        pass


@patch("menu.menu.MenuInterface.load_settings", autospec=True)
class Test_login(Test_Menu):
    def test_login(self, mockLoadSettings):
        #Actual
        self.myClass.login()
        #Verify
        mockLoadSettings.assert_called_once_with(self.myClass)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("menu.menu.MenuInterface._report_menu", autospec=True)
@patch("menu.menu.MenuInterface._member_management_menu", autospec=True)
@patch("menu.menu.MenuInterface._provider_management_menu", autospec=True)
@patch("menu.menu.MenuInterface._services_management_menu", autospec=True)
@patch("menu.menu.MenuInterface._services_history_menu", autospec=True)
@patch("menu.menu.MenuInterface._keys_management_menu", autospec=True)
class Test_manager_main_menu(Test_Menu):
    def test__manager_main_menu(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                mockprint, mockinput):
        #Setup
        mockinput.return_value = "q"
        #Actual
        result = self.myClass._manager_main_menu("")
        #Verify
        printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' ')]
        mockprint.assert_has_calls(printCalls)
        self.assertEqual(result, "Exit")

    def test__manager_main_menu1(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                 mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                 mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["1", "q"])
        #Actual
        self.myClass._manager_main_menu("")
        #Verify
        printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' ')]
        mockprint.assert_has_calls(printCalls)
        mock_report_menu.assert_called_once_with(self.myClass)

    def test__manager_main_menu2(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                 mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                 mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["2", "q"])
        #Actual
        self.myClass._manager_main_menu("")
        #Verify
        printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' ')]
        mockprint.assert_has_calls(printCalls)
        mock_member_management_menu.assert_called_once_with(self.myClass)

    def test__manager_main_menu3(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                 mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                 mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["3", "q"])
        #Actual
        self.myClass._manager_main_menu("")
        #Verify
        printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' ')]
        mockprint.assert_has_calls(printCalls)
        mock_provider_management_menu.assert_called_once_with(self.myClass)

    def test__manager_main_menu4(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                 mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                 mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["4", "q"])
        #Actual
        self.myClass._manager_main_menu("")
        #Verify
        printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' ')]
        mockprint.assert_has_calls(printCalls)
        mock_services_management_menu.assert_called_once_with(self.myClass)

    def test__manager_main_menu5(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                 mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                 mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["5", "q"])
        #Actual
        self.myClass._manager_main_menu("")
        #Verify
        printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' ')]
        mockprint.assert_has_calls(printCalls)
        mock_keys_menu.assert_called_once_with(self.myClass)

    def test__manager_main_menu6(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                 mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                 mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["6", "q"])
        #Actual
        self.myClass._manager_main_menu("")
        #Verify
        printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' ')]
        mockprint.assert_has_calls(printCalls)
        mock_admin_menu.assert_called_once_with(self.myClass)

    def test__manager_main_menu7(self, mock_admin_menu, mock_keys_menu, mock_services_management_menu,
                                 mock_provider_management_menu, mock_member_management_menu, mock_report_menu,
                                 mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["7", "q"])
        #Actual
        self.myClass._manager_main_menu("")
        #Verify
        printCalls = printCalls = [call("-----Manager Main Menu-----"), call("1. Report/Summary Menu"),
                      call("2. Member Management"), call("3. Provider Management"),
                      call("4. Services Management"), call("5. Services History"),
                      call("6. Keys Management"), call("q. Exit"), call(' '), call("Invalid Input!")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("menu.menu.MenuInterface.list_all_members", autospec=True)
@patch("menu.menu.MenuInterface.member_status", autospec=True)
@patch("menu.menu.MenuInterface.add_member", autospec=True)
@patch("menu.menu.MenuInterface.set_member", autospec=True)
@patch("menu.menu.MenuInterface.remove_member", autospec=True)
@patch("menu.menu.MenuInterface.delete_members_table", autospec=True)
class Test_member_management_menu(Test_Menu):
    def test_Test_Menu(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member, mockmember_status, mocklist_all_members, mockprint, mockinput):
        #Setup
        mockinput.return_value = "q"
        #Actual
        result = self.myClass._member_management_menu("")
        #Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" ")]
        mockprint.assert_has_calls(printCalls)
        self.assertEqual(result, "Exit")

    def test_Test_Menu1(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member,
                        mockmember_status, mocklist_all_members, mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["1", "q"])
        #Actual
        self.myClass._member_management_menu("")
        #Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" ")]
        mockprint.assert_has_calls(printCalls)
        mocklist_all_members.assert_called_once_with(self.myClass)

    def test_Test_Menu2(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member,
                        mockmember_status, mocklist_all_members, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["2", "q"])
        # Actual
        self.myClass._member_management_menu("")
        # Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" ")]
        mockprint.assert_has_calls(printCalls)
        mockmember_status.assert_called_once_with(self.myClass)

    def test_Test_Menu3(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member,
                        mockmember_status, mocklist_all_members, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["3", "q"])
        # Actual
        self.myClass._member_management_menu("")
        # Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" ")]
        mockprint.assert_has_calls(printCalls)
        mockadd_member.assert_called_once_with(self.myClass)

    def test_Test_Menu4(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member,
                        mockmember_status, mocklist_all_members, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["4", "q"])
        # Actual
        self.myClass._member_management_menu("")
        # Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" ")]
        mockprint.assert_has_calls(printCalls)
        mockset_member.assert_called_once_with(self.myClass)

    def test_Test_Menu5(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member,
                        mockmember_status, mocklist_all_members, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["5", "q"])
        # Actual
        self.myClass._member_management_menu("")
        # Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" ")]
        mockprint.assert_has_calls(printCalls)
        mockiremove_member.assert_called_once_with(self.myClass)

    def test_Test_Menu6(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member,
                        mockmember_status, mocklist_all_members, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["6", "q"])
        # Actual
        self.myClass._member_management_menu("")
        # Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" ")]
        mockprint.assert_has_calls(printCalls)
        mockdelete_members_table.assert_called_once_with(self.myClass)

    def test_Test_Menu7(self, mockdelete_members_table, mockiremove_member, mockset_member, mockadd_member,
                        mockmember_status, mocklist_all_members, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["7", "q"])
        # Actual
        self.myClass._member_management_menu("")
        # Verify
        printCalls = [call("------Member Management-----"), call("1. List All Members"),
                      call("2. Check Member Status"), call("3. Add a Member"),
                      call("4. Update Member Info"), call("5. Remove a Member"),
                      call("6. Delete All Members From Server"), call("q. Exit"),
                      call(" "), call("Invalid Input!")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("menu.menu.MenuInterface.get_all_providers", autospec=True)
@patch("menu.menu.MenuInterface.add_provider", autospec=True)
@patch("menu.menu.MenuInterface.remove_provider", autospec=True)
@patch("menu.menu.MenuInterface.set_provider", autospec=True)
class Test_provider_management_menu(Test_Menu):
    def test__provider_management_menu(self, mockset_provider, mockremove_provider, mockadd_provider,
                                       mockget_all_providers, mockprint, mockinput):
        #Setup
        mockinput.return_value = "q"
        #Actual
        result = self.myClass._provider_management_menu()
        #Verify
        printCalls = [call('-----Provider Management-----'), call('1. List Providers'),
                      call('2. Add a Provider'), call('3. Remove a Provider'),
                      call('4. Update Provider info'), call('q:Exit'),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        self.assertEqual(result, "Exit")

    def test__provider_management_menu1(self, mockset_provider, mockremove_provider, mockadd_provider,
                                        mockget_all_providers, mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["1", "q"])
        #Actual
        self.myClass._provider_management_menu("")
        #Verify
        printCalls = [call('-----Provider Management-----'), call('1. List Providers'),
                      call('2. Add a Provider'), call('3. Remove a Provider'),
                      call('4. Update Provider info'), call('q:Exit'),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockget_all_providers.assert_called_once_with(self.myClass)

    def test__provider_management_menu2(self, mockset_provider, mockremove_provider, mockadd_provider,
                                        mockget_all_providers, mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["2", "q"])
        #Actual
        self.myClass._provider_management_menu("")
        #Verify
        printCalls = [call('-----Provider Management-----'), call('1. List Providers'),
                      call('2. Add a Provider'), call('3. Remove a Provider'),
                      call('4. Update Provider info'), call('q:Exit'),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockadd_provider.assert_called_once_with(self.myClass)

    def test__provider_management_menu3(self, mockset_provider, mockremove_provider, mockadd_provider,
                                        mockget_all_providers, mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["3", "q"])
        #Actual
        self.myClass._provider_management_menu("")
        #Verify
        printCalls = [call('-----Provider Management-----'), call('1. List Providers'),
                      call('2. Add a Provider'), call('3. Remove a Provider'),
                      call('4. Update Provider info'), call('q:Exit'),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockremove_provider.assert_called_once_with(self.myClass)

    def test__provider_management_menu4(self, mockset_provider, mockremove_provider, mockadd_provider,
                                        mockget_all_providers, mockprint, mockinput):
        #Setup
        mockinput.side_effect = iter(["4", "q"])
        #Actual
        self.myClass._provider_management_menu()
        #Verify
        printCalls = [call('-----Provider Management-----'), call('1. List Providers'),
                      call('2. Add a Provider'), call('3. Remove a Provider'),
                      call('4. Update Provider info'), call('q:Exit'),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockset_provider.assert_called_once_with(self.myClass)

    def test__provider_management_menu5(self, mockset_provider, mockremove_provider, mockadd_provider,
                                        mockget_all_providers, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["7", "q"])
        # Actual
        self.myClass._provider_management_menu("")
        # Verify
        printCalls = [call('-----Provider Management-----'), call('1. List Providers'),
                      call('2. Add a Provider'), call('3. Remove a Provider'),
                      call('4. Update Provider info'), call('q:Exit'),
                      call(' '), call("Invalid Input!")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("menu.menu.MenuInterface.list_services_history", autospec=True)
@patch("menu.menu.MenuInterface.provide_service", autospec=True)
@patch("menu.menu.MenuInterface.remove_provided_service", autospec=True)
@patch("menu.menu.MenuInterface.update_provided_service", autospec=True)
class Test_services_history_menu(Test_Menu):
    def test__services_history_menu(self, mockset_service, mockremove_service, mockadd_service,
                                       mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.return_value = "q"
        # Actual
        result = self.myClass._services_history_menu("")
        # Verify
        printCalls = [call("-----Services History Menu-----"), call("1. List services history"),
                      call("2. Provide a service"),  call("3. Remove a provided service"),
                      call("4. Update a provided service info"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        self.assertEqual(result, "Exit")

    def test__services_history_menu1(self, mockset_service, mockremove_service, mockadd_service,
                                        mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["1", "q"])
        # Actual
        self.myClass._services_history_menu("")
        # Verify
        printCalls = [call("-----Services History Menu-----"), call("1. List services history"),
                      call("2. Provide a service"),  call("3. Remove a provided service"),
                      call("4. Update a provided service info"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockinglist_services.assert_called_once_with(self.myClass)

    def test__services_history_menu2(self, mockset_service, mockremove_service, mockadd_service,
                                        mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["2", "q"])
        # Actual
        self.myClass._services_history_menu("")
        # Verify
        printCalls = [call("-----Services History Menu-----"), call("1. List services history"),
                      call("2. Provide a service"),  call("3. Remove a provided service"),
                      call("4. Update a provided service info"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockadd_service.assert_called_once_with(self.myClass)

    def test__services_history_menu3(self, mockset_service, mockremove_service, mockadd_service,
                                        mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["3", "q"])
        # Actual
        self.myClass._services_history_menu("")
        # Verify
        printCalls = [call("-----Services History Menu-----"), call("1. List services history"),
                      call("2. Provide a service"), call("3. Remove a provided service"),
                      call("4. Update a provided service info"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockremove_service.assert_called_once_with(self.myClass)

    def test__services_history_menu4(self, mockset_service, mockremove_service, mockadd_service,
                                        mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["4", "q"])
        # Actual
        self.myClass._services_history_menu("")
        # Verify
        printCalls = [call("-----Services History Menu-----"), call("1. List services history"),
                      call("2. Provide a service"), call("3. Remove a provided service"),
                      call("4. Update a provided service info"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockset_service.assert_called_once_with(self.myClass)

    def test__services_history_menu5(self, mockset_service, mockremove_service, mockadd_service,
                                        mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["", "q"])
        # Actual
        self.myClass._services_history_menu("")
        # Verify
        printCalls = [call("-----Services History Menu-----"), call("1. List services history"),
                      call("2. Provide a service"), call("3. Remove a provided service"),
                      call("4. Update a provided service info"), call("q. Exit"),
                      call(' '), call("Invalid Input!")]
        mockprint.assert_has_calls(printCalls)


@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("menu.menu.MenuInterface.list_all_service_offers", autospec=True)
@patch("menu.menu.MenuInterface.add_a_service_offer", autospec=True)
@patch("menu.menu.MenuInterface.remove_a_service_offer", autospec=True)
@patch("menu.menu.MenuInterface.update_a_service_offer", autospec=True)
class Test_services_management_menu(Test_Menu):
    def test__services_management_menu(self, mockset_service, mockremove_service, mockadd_service,
                                        mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["", "q"])
        # Actual
        self.myClass._services_management_menu("")
        # Verify
        printCalls = [call("------Services Management Menu-----"), call("1. List all service offers"),
                      call("2. Add a service"), call("3. Remove a service"),
                      call("4. Update a service"), call("q. Exit"),
                      call(' '), call("Invalid Input!")]
        mockprint.assert_has_calls(printCalls)

    def test__services_management_menu1(self, mockupdate_service, mockremove_service, mockadd_service,
                                       mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["1", "q"])
        # Actual
        self.myClass._services_management_menu("")
        # Verify
        printCalls = [call("------Services Management Menu-----"), call("1. List all service offers"),
                      call("2. Add a service"), call("3. Remove a service"),
                      call("4. Update a service"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockinglist_services.assert_called_once_with(self.myClass)

    def test__services_management_menu2(self, mockupdate_service, mockremove_service, mockadd_service,
                                       mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["2", "q"])
        # Actual
        self.myClass._services_management_menu("")
        # Verify
        printCalls = [call("------Services Management Menu-----"), call("1. List all service offers"),
                      call("2. Add a service"), call("3. Remove a service"),
                      call("4. Update a service"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockadd_service.assert_called_once_with(self.myClass)

    def test__services_management_menu3(self, mockupdate_service, mockremove_service, mockadd_service,
                                       mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["3", "q"])
        # Actual
        self.myClass._services_management_menu("")
        # Verify
        printCalls = [call("------Services Management Menu-----"), call("1. List all service offers"),
                      call("2. Add a service"), call("3. Remove a service"),
                      call("4. Update a service"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockremove_service.assert_called_once_with(self.myClass)

    def test__services_management_menu4(self, mockupdate_service, mockremove_service, mockadd_service,
                                       mockinglist_services, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["4", "q"])
        # Actual
        self.myClass._services_management_menu("")
        # Verify
        printCalls = [call("------Services Management Menu-----"), call("1. List all service offers"),
                      call("2. Add a service"), call("3. Remove a service"),
                      call("4. Update a service"), call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mockupdate_service.assert_called_once_with(self.myClass)

@patch("builtins.input", autospec=True)
@patch("builtins.print", autospec=True)
@patch("menu.menu.MenuInterface.list_all_keys", autospec=True)
@patch("menu.menu.MenuInterface.update_a_key", autospec=True)
@patch("menu.menu.MenuInterface.validate_a_key", autospec=True)
@patch("menu.menu.MenuInterface.add_a_key", autospec=True)
@patch("menu.menu.MenuInterface.remove_a_key", autospec=True)
@patch("menu.menu.MenuInterface.remove_all_keys", autospec=True)
class Test_keys_management_menu(Test_Menu):
    def test__keys_management_menu(self,mRemove_all_keys, mRemove_a_key, mAdd_a_key, mValidate_a_key, mUpdate_a_key,
                                   mList_all_keys, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["", "q"])
        # Actual
        self.myClass._keys_management_menu("")
        # Verify
        printCalls = [call("------Keys Management Menu-----"), call("1. List keys"),
                      call("2. Update a key"), call("3. Validate a key"),
                      call("4. Add a key"), call("5. Remove a key"),
                      call("6. Remove all keys"),call("q. Exit"),
                      call(' '), call("Invalid Input!")]
        mockprint.assert_has_calls(printCalls)

    def test__keys_management_menu1(self,mRemove_all_keys, mRemove_a_key, mAdd_a_key, mValidate_a_key, mUpdate_a_key,
                                   mList_all_keys, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["1", "q"])
        # Actual
        self.myClass._keys_management_menu("")
        # Verify
        printCalls = [call("------Keys Management Menu-----"), call("1. List keys"),
                      call("2. Update a key"), call("3. Validate a key"),
                      call("4. Add a key"), call("5. Remove a key"),
                      call("6. Remove all keys"),call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mList_all_keys.assert_called_once_with(self.myClass)

    def test__keys_management_menu2(self,mRemove_all_keys, mRemove_a_key, mAdd_a_key, mValidate_a_key, mUpdate_a_key,
                                   mList_all_keys, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["2", "q"])
        # Actual
        self.myClass._keys_management_menu("")
        # Verify
        printCalls = [call("------Keys Management Menu-----"), call("1. List keys"),
                      call("2. Update a key"), call("3. Validate a key"),
                      call("4. Add a key"), call("5. Remove a key"),
                      call("6. Remove all keys"),call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mUpdate_a_key.assert_called_once_with(self.myClass)

    def test__keys_management_menu3(self,mRemove_all_keys, mRemove_a_key, mAdd_a_key, mValidate_a_key, mUpdate_a_key,
                                   mList_all_keys, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["3", "q"])
        # Actual
        self.myClass._keys_management_menu("")
        # Verify
        printCalls = [call("------Keys Management Menu-----"), call("1. List keys"),
                      call("2. Update a key"), call("3. Validate a key"),
                      call("4. Add a key"), call("5. Remove a key"),
                      call("6. Remove all keys"),call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mValidate_a_key.assert_called_once_with(self.myClass)

    def test__keys_management_menu4(self,mRemove_all_keys, mRemove_a_key, mAdd_a_key, mValidate_a_key, mUpdate_a_key,
                                   mList_all_keys, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["4", "q"])
        # Actual
        self.myClass._keys_management_menu("")
        # Verify
        printCalls = [call("------Keys Management Menu-----"), call("1. List keys"),
                      call("2. Update a key"), call("3. Validate a key"),
                      call("4. Add a key"), call("5. Remove a key"),
                      call("6. Remove all keys"),call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mAdd_a_key.assert_called_once_with(self.myClass)

    def test__keys_management_menu5(self,mRemove_all_keys, mRemove_a_key, mAdd_a_key, mValidate_a_key, mUpdate_a_key,
                                   mList_all_keys, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["5", "q"])
        # Actual
        self.myClass._keys_management_menu("")
        # Verify
        printCalls = [call("------Keys Management Menu-----"), call("1. List keys"),
                      call("2. Update a key"), call("3. Validate a key"),
                      call("4. Add a key"), call("5. Remove a key"),
                      call("6. Remove all keys"),call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mRemove_a_key.assert_called_once_with(self.myClass)

    def test__keys_management_menu6(self,mRemove_all_keys, mRemove_a_key, mAdd_a_key, mValidate_a_key, mUpdate_a_key,
                                   mList_all_keys, mockprint, mockinput):
        # Setup
        mockinput.side_effect = iter(["6", "q"])
        # Actual
        self.myClass._keys_management_menu("")
        # Verify
        printCalls = [call("------Keys Management Menu-----"), call("1. List keys"),
                      call("2. Update a key"), call("3. Validate a key"),
                      call("4. Add a key"), call("5. Remove a key"),
                      call("6. Remove all keys"),call("q. Exit"),
                      call(' ')]
        mockprint.assert_has_calls(printCalls)
        mRemove_all_keys.assert_called_once_with(self.myClass)


if __name__ == '__main__':
    unittest.main()
