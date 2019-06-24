import json
import os.path
import sys
sys.path.append("..")
import constants.consts as consts
from dataProcessing.dataProcessing import DataProcessing
from network.networkController.networkController import NetworkController

#test key AS62ELRB5F0709LERPHZD06JWC0P8QSC
# gather username and password from user
##
class MenuInterface(DataProcessing):
    def __init__(self, nc=""):
        # initialize the parent class with a NetworkController Object
        if nc == "":
            nc = NetworkController()
        super().__init__(nc)
        # defaults variables
        self.key = "Default"

    def login(self):
        self.load_settings()

    def load_settings(self):
        if self.nc.validateKey(self.key).error == consts.ERROR_CONNECTION_FAILED:
            return
        if os.path.isfile("./manager_setting.json"):
            with open("./manager_setting.json") as input_file:
                settings = json.load(input_file)
                self.key = settings["key_01"]
                if self.nc.validateKey(self.key).payload != consts.KEY_ROOT:
                    input_file.close()
                    self.load_settings_validate()
                print("Logged in with key : " + self.nc.validateKey(self.key).payload)
                input_file.close()
                self._manager_main_menu()
        else:
            self.load_settings_validate()

    def load_settings_validate(self):
        if self.nc.validateKey(self.key).error == consts.ERROR_CONNECTION_FAILED:
            return
        self.key = input("You don't have a manager key, please enter your 32 digit key:")
        with open("./manager_setting.json", "w") as output_file:
            key_data = {"key_01": self.key}
            json.dump(key_data, output_file, sort_keys=True, indent=4)
            output_file.close()
            self.load_settings()

    def _manager_main_menu(self, user_input=""):
        print("-----Manager Main Menu-----")
        print("1. Report/Summary Menu")
        print("2. Member Management")
        print("3. Provider Management")
        print("4. Services Management")
        print("5. Services History")
        print("6. Keys Management")
        print("q. Exit")
        print(" ")
        if user_input == "":
            user_input = input()

        if user_input == "q":
            return "Exit"
        elif user_input == '1':
            self._report_menu()
        elif user_input == '2':
            self._member_management_menu()
        elif user_input == '3':
            self._provider_management_menu()
        elif user_input == "4":
            self._services_management_menu()
        elif user_input == "5":
            self._services_history_menu()
        elif user_input == "6":
            self._keys_management_menu()
        else:
            print("Invalid Input!")
        self._manager_main_menu("")



# Not ready for unit tests
    def _report_menu(self, user_input=""):
        print("-----Report Menu-----")
        print("1. Member reports")
        print("2. EFT reports")
        print("3. Summary reports")
        print("4. Provider reports")
        print("q. Exit")
        print(" ")
        if user_input == "":
            user_input = input()
        if user_input == "q":
            return "Exit"
        elif user_input == '1':
            self.member_report();
        elif user_input == '2':
            self.eft_report();
        elif user_input == "3":
            self.summary_report();
        elif user_input == "4":
            self.provider_report();
        else:
            print("Invalid Input!")
        self._report_menu("")

    def _member_management_menu(self, user_input=""):
        print("------Member Management-----")
        print("1. List All Members")
        print("2. Check Member Status")
        print("3. Add a Member")
        print("4. Update Member Info")
        print("5. Remove a Member")
        print("6. Delete All Members From Server")
        print("q. Exit")
        print(" ")
        if user_input == "":
            user_input = input()
        if user_input == "q":
            return "Exit"
        elif user_input == "1":
            self.list_all_members()
        elif user_input == "2":
            self.member_status()
        elif user_input == "3":
            self.add_member()
        elif user_input == "4":
            self.set_member()
        elif user_input == "5":
            self.remove_member()
        elif user_input == "6":
            self.delete_members_table()
        else:
            print("Invalid Input!")
        self._member_management_menu("")

    def _provider_management_menu(self, user_input=""):
        print("-----Provider Management-----")
        print("1. List Providers")
        print("2. Add a Provider")
        print("3. Remove a Provider")
        print("4. Update Provider info")
        print("q:Exit")
        print(" ")
        if user_input == "":
            user_input = input()

        if user_input == "q":
            return "Exit"
        elif user_input == "1":
            self.get_all_providers()
        elif user_input == "2":
            self.add_provider()
        elif user_input == "3":
            self.remove_provider()
        elif user_input == "4":
            self.set_provider()
        else:
            print("Invalid Input!")
        self._provider_management_menu("")

    def _services_history_menu(self, user_input=""):
        print("-----Services History Menu-----")
        print("1. List services history")
        print("2. Provide a service")
        print("3. Remove a provided service")
        print("4. Update a provided service info")
        print("q. Exit")
        print(" ")
        if user_input == "":
            user_input = input()
        if user_input == "q":
            return "Exit"
        elif user_input == '1':
            self.list_services_history()
        elif user_input == '2':
            self.provide_service()
        elif user_input == "3":
            self.remove_provided_service()
        elif user_input == "4":
            self.update_provided_service()
        else:
            print("Invalid Input!")
        self._services_history_menu()

    def _services_management_menu(self, user_input=""):
        print("------Services Management Menu-----")
        print("1. List all service offers")
        print("2. Add a service")
        print("3. Remove a service")
        print("4. Update a service")
        print("q. Exit")
        print(" ")
        if user_input == "":
            user_input = input()
        if user_input == "q":
            return "Exit"
        elif user_input == "1":
            self.list_all_service_offers()
        elif user_input == "2":
            self.add_a_service_offer()
        elif user_input == "3":
            self.remove_a_service_offer()
        elif user_input == "4":
            self.update_a_service_offer()
        else:
            print("Invalid Input!")
        self._services_management_menu()

    def _keys_management_menu(self, user_input=""):
        print("------Keys Management Menu-----")
        print("1. List keys")
        print("2. Update a key")
        print("3. Validate a key")
        print("4. Add a key")
        print("5. Remove a key")
        print("6. Remove all keys")
        print("q. Exit")
        print(" ")
        if user_input == "":
            user_input = input()
        if user_input == "q":
            return "Exit"
        elif user_input == "1":
            self.list_all_keys()
        elif user_input == "2":
            self.update_a_key()
        elif user_input == "3":
            self.validate_a_key()
        elif user_input == "4":
            self.add_a_key()
        elif user_input == "5":
            self.remove_a_key()
        elif user_input == "6":
            self.remove_all_keys()
        else:
            print("Invalid Input!")
        self._keys_management_menu()

