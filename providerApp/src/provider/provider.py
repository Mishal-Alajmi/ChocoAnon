import csv
import json
import os
import sys
import random
sys.path.append("..")
import constants.consts as consts
from network.networkController.networkController import NetworkController


class Provider():
    # Constructor: Initilize members
    def __init__(self, nc = ""):
        if nc =="":
            nc = NetworkController()
        self.nc = nc  # create an instance of the network controller passed in to the constructor
        self.key = 0  # key member will hold the provider key ID
        self.member_id = 0  # member_id will hold the member ID number
        # Sample provider = "DDPR0TG8EF760QR2J7IUF3UFIRXXL4E3" # testing provider ID
        # Sample Admin = "AS62ELRB5F0709LERPHZD06JWC0P8QSC"    # testing admin ID

    """
    The login function asks the user to enter a login key which then
    saves it into the key variable. It checks whether the key entered
    exists in the data base or not. If an error exists, it calls the function again
    """

    def login(self):
        self.key = input("Welcome.\nPlease enter your login key:\t")
        result = self.nc.validateKey(self.key)  # calling the validateKey function and storing the return into result

        # Error Checking: Check for the following errors
        if result.payload == consts.KEY_INVALID:
            print("\nError: Key is not valid.\n")
            self.login()

        elif result.payload == consts.KEY_PROVIDER:
            print("\nLogged in as a provider.\n")

        elif result.payload == consts.KEY_ROOT:
            print("\nError: Key is not authorized\n")
            self.login()

        if result.error == consts.ERROR_UNAUTHORIZED_OPERATION:
            print("\nError: Key is not authorized.\n")
            self.login()

        if result.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("\nError: Key not found.\n")
            self.login()

        if result.error == consts.ERROR_CONNECTION_FAILED:
            print("\nError: Server did not respond.\n")
            return

    """
    he customer_id_swipe asks the user to enter a customer ID.
    It saves the input into member_id and then checks whether
    it exists in the data base. If it returns no errors, then
    it will call the customer_menu() function. If an error is found,
    it will call itself again.
    """

    def customer_id_swipe(self):
        self.member_id = input("Please enter the customers' ID:\t")
        customer_id = self.nc.getMember(self.key,
                                        self.member_id)  # Saves the return value of 'getMember' into 'customer_id'

        # Error checking: Check for the following errors
        if customer_id.error == consts.ERROR_UNAUTHORIZED_OPERATION:
            print("\nError: Key is not authorized.\t")

        if customer_id.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("\nError: Customer not found.\n")

        if customer_id.error == consts.ERROR_CONNECTION_FAILED:
            print("\nError: Server did not respond.\t")

        if customer_id.error == consts.NO_ERROR:
            print("\nWelcome " + customer_id.payload.get('name') + "!")
            self.customer_menu()
        else:
            self.menu()
    """
     The display_one_service: asks the user to enter a code for the service
     that they would like to display. The input is stored in a local variable
     named 'code'. It checks whether the code exists in the data base. If it
     does, then it will display the information of that specific service. If
     not, then it will call itself again.
    """

    def display_one_service(self):
        code = input("Please enter the code of the service:\t")
        service_code = self.nc.getService(self.key, code)  # Saves the return value of 'getService' into 'service_code'

        # Error Checking: Check for the following errors
        if service_code.error == consts.ERROR_UNAUTHORIZED_OPERATION:
            print("\nError: Key is not authorized.\t")
            return

        if service_code.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("\nError: Invalid service code.\n")
            self.display_one_service()

        if service_code.error == consts.ERROR_CONNECTION_FAILED:
            print("\nError: Server did not respond.\t")
            return

        if service_code.error == consts.NO_ERROR:
            print("\nID: " + service_code.payload.get('id') +
                  "\nCode: " + service_code.payload.get('code') +
                  "\nprovider: " + service_code.payload.get('provider') +
                  "\nMember: " + service_code.payload.get('member') +
                  "\nDate: " + service_code.payload.get('date') +
                  "\nReceived: " + service_code.payload.get('received') +
                  "\nComment: " + service_code.payload.get('comment') +
                  "\nStatus: " + service_code.payload.get('status') + "\n")

        self.customer_services()

    """
    The display_all_services stores the return value of the getAllServices
    into a local variable called all_services. If no error occurs, the
    function will display all the services that the user is signed up for.
    """

    def display_all_services(self):

        all_services = self.nc.getAllServices(self.key) # Saves the return value of 'getAllServices' into 'all_services'
        customer_id = self.nc.getMember(self.key,self.member_id) # Saves the return value of 'getMember' into 'customer_id'

        # Error Checking: Check for the following errors
        if all_services.error == consts.ERROR_UNAUTHORIZED_OPERATION:
            print("\nError: Key is not authorized.\n")
            return

        if all_services.error == consts.ERROR_CONNECTION_FAILED:
            print("\nError: Server did not respond.\n")
            return

        if all_services.error == consts.NO_ERROR:
            print("Displaying all of " + customer_id.payload.get('name') + "'s services:\n")
            for x in range(len(all_services.payload)):
                print(all_services.payload[x])

        self.customer_services() # Call the customer_services function to return the customer_menu after display services

    """
     The member_information displays all the information about a specific
     member given a member ID.
    """
    def member_information(self):
        info = self.nc.getMember(self.key, self.member_id) # Saves the return value of 'getMember' into 'info'
        print("\nName: " + info.payload.get('name') +
              "\nAddress: " + info.payload.get('address') +
              "\nCity: " + info.payload.get('city') +
              "\nState: " + info.payload.get('state') +
              "\nZip: " + info.payload.get('zip'))

        self.customer_services()

    """
    The customer_services displays a menu to the user with options to choose from.
    All the options are related to the particular customer.
    """
    def customer_services(self):
        print("-----\tCustomer Services\t-----\n"
              "1. Display customer information\n"
              "2. Display all services\n"
              "3. Display one service\n"
              "4. Return to customer menu\n"
              "5. Return to main menu\n"
              "6. Exit\n")
        option = input()
        if option == "1":
            self.member_information()
        elif option == "2":
            self.display_all_services()
        elif option == "3":
            self.display_one_service()
        elif option == "4":
            self.customer_menu()
        elif option == "5":
            self.menu()
        elif option == "6":
            print("Thank you!")
            return
        else:
            print("Invalid Input")
            self.customer_services()

    """
    The add_service_id function asks the user to enter the service provider required.
    Afterwards, if the service request exists, it will return that service ID.
    """
    def add_service_id(self):
        p_id = input("Enter service provider id: ") # Store the service ID
        provider = self.nc.getProvider(self.key, p_id) # Saves the return value of 'getProvider' into 'provider'

        # check the error code to see if the provider exists
        if provider.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid provider id")
            return False
        else:
            return p_id

    """
    The add_service_member function asks the user to enter their memberID.
    Afterwards, if the member exists in the database, it will return that member ID.
    """
    def add_service_member(self):
        m_id = input("Enter member id: ")
        member = self.nc.getMember(self.key, m_id)
        # check the error code to see if the member exists
        if member.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Member id")
            return False
        else:
            return m_id

    """
    add_service_rest_info function takes the rest of the information from the user, 
    and returns them .
    """
    def add_service_rest_info(self):
        date = input("Enter service date (MM/DD/YYYY) : ")
        code = input("Enter 6 digit service code: ")
        comment = input("Please include comments on service: ")
        select = input("Was this service paid? (y/n): ")

        if select.lower() == "y":
            status = consts.STATUS_PAID # Sets the service to be marked as paid
        else:
            status = consts.STATUS_UNPAID # Sets the service to be marked as unpaid
        return date, code, comment, status

    """
    The add_service function asks the user to enter information required.
    Afterwards, if the service request exists, it will add that service to
    the customers' data.
    """
    def add_service(self):
        p_id = self.add_service_id() # Calls the add_service_id function to request a service ID
        if not p_id:
            return False

        m_id = self.add_service_member() # Calls the add_service_member function to request a member ID
        if not m_id:
            return False

        date, code, comment, status = self.add_service_rest_info() # Calls the add_service_rest_info function to store user input

        isValidId = False
        while not isValidId:
            id = ""
            for i in range(0, 9):
                id += str(random.choice("0123456789"))

            data = {
                "id": id,
                "code": code,
                "date": date,
                "provider": p_id,
                "member": m_id,
                "comment": comment,
                "status": status,
            }
            result = self.nc.addService(self.key, data)


            if result.error != consts.ERROR_DUPLICATE_ID:
                isValidId = True
                self.nc.getService(self.key, id)
                # print(result.serialize())

            print("New Service ID: " + id)

        self.customer_menu()

    """
    The customer_menu function displays options to select from. 
    """
    def customer_menu(self):
        print("-----\tCustomer Menu\t-----\n"
              "1. Existing services\n"
              "2. Add a service\n"
              "3. Return to main menu\n")
        option = input()
        if option == "1":
            self.customer_services()
        elif option == "2":
            self.add_service()
        elif option == "3":
            self.menu()
        else:
            print("Invalid Input.")
            self.customer_menu()

    """
    The services_offered function saves the return value of the
    getAllMenuItems function and if no error occurs, will display
    all the services offered in the data base.
    """
    def services_offered(self):
        display_menu = self.nc.getAllMenuItems(self.key) # Saves the return value of 'getAllMenuItems' into 'display_menu'

        # Error Checking: check for the following erros
        if display_menu.error == consts.ERROR_UNAUTHORIZED_OPERATION:
            print("\nError: Requires an ID with higher authorization.\n")
            self.services_offered()

        if display_menu.error == consts.NO_ERROR:
            print("\nDisplaying all services offered:\n")
            for x in range(len(display_menu.payload)):
                print(display_menu.payload[x])

        self.menu()

    """
    The generate_report function will ask the user to enter a member ID
    which will then be stored in a local variable called ID. Afterwards,
    it will check if the ID exists or not. If it does, then it will
    generate a report of that member and write it to a text file by calling
    the fileWrite function.
    """
    def generate_report(self):
        ID = input("Please enter a member ID:\t")
        self.member_dict = self.nc.getMember(self.key, ID)  # Saves the return value of 'getMember' into 'member_dict'

        # Error Checking: Check for the following errors
        #if no error has occured print the member info and then write to file in csv format
        if self.member_dict.error == consts.NO_ERROR:
            self.fileWrite(self.member_dict)
            print("\n----\tMember Information\t----\n",
                  "\nName:\t", self.member_dict.payload.get('name'),
                  "\nID:\t\t", self.member_dict.payload.get('id'),
                  "\nAddress:\t", self.member_dict.payload.get('address'),
                  "\nCity:\t\t", self.member_dict.payload.get('city'),
                  "\nState:\t\t", self.member_dict.payload.get('state'),
                  "\nZip Code:\t", self.member_dict.payload.get('zip'))
            self.menu()

        elif self.member_dict.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("\nError: Member does not exist\n")
            self.menu()

        elif self.member_dict.error == consts.ERROR_CONNECTION_FAILED:
            print("\nError: Connection to the server failed")

    """
    The fileWrite function will write infromation to a text file, 
    in csv format ordered by: 1-id 2-name 3-address 4-city 5-state 6-zip.
    The fileWrite() function will write from the member_dict pulled from the database
    """
    def fileWrite(self, member_info):
        try:
            with open('member_report.csv', 'a') as csv_file:
                filednames = ['id', 'name', 'address', 'city', 'state', 'zip']
                writer = csv.DictWriter(csv_file, fieldnames=filednames)
                # writer.writeheader()
                writer.writerow({'id': member_info.payload.get('id'), 'name': member_info.payload.get('name'),
                                 'address': member_info.payload.get('address'), 'city': member_info.payload.get('city'),
                                 'state': member_info.payload.get('state'), 'zip': member_info.payload.get('zip')})

        except FileNotFoundError as e:
            print(e)

        except Exception as e:
            print(e)

    def load_settings(self):
        if self.nc.validateKey(self.key).error == consts.ERROR_CONNECTION_FAILED:
            return
        if os.path.isfile("./provider_setting.json"):
            with open("./provider_setting.json") as input_file:
                settings = json.load(input_file)
                self.key = settings["key_01"]
                if self.nc.validateKey(self.key).payload != consts.KEY_PROVIDER:
                    input_file.close()
                    self.load_settings_validate()
                print("Logged in with key : " + self.nc.validateKey(self.key).payload)
                input_file.close()
                self.menu()
        else:
            self.load_settings_validate()

    def load_settings_validate(self):
        if self.nc.validateKey(self.key).error == consts.ERROR_CONNECTION_FAILED:
            return
        self.key = input("You don't have a provider key, please enter your 32 digit key:")
        with open("./provider_setting.json", "w") as output_file:
            key_data = {"key_01": self.key}
            json.dump(key_data, output_file, sort_keys=True, indent=4)
            output_file.close()
            self.load_settings()

    """
     The menu function will display the main menu to the user allowing them  to select an option
    """
    def menu(self):
        print("-----\tMain Menu\t-----\n"
              "1. Swipe Customer ID\n"
              "2. ChocAn Services Offered\n"
              "3. Generate Report\n"
              "4. Exit")
        option = input()

        if option == "1":
            self.customer_id_swipe()

        elif option == "2":
            self.services_offered()

        elif option == "3":
            self.generate_report()

        elif option == "4":
            print("Thank you!")
            return
        else:
            print("Invalid Input")
            self.menu()

'''
if __name__ == "__main__":
    nc = NetworkController()
    p = provider(nc)
    p.load_settings()
    # p.login() uncomment this code and the menu if you want to test both menu and login functions
    # p.menu()
'''