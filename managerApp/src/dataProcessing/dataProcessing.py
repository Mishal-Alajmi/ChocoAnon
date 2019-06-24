import random
import string
import os
import sys
from datetime import datetime, timedelta, date
sys.path.append("..")
import constants.consts as consts


class DataProcessing(object):

    def __init__(self, nc):
        self.nc = nc

    # Report Menu
    def write_m_report(self, s_id):

        # get service info
        service = self.nc.getService(self.key, s_id)
        # get member info
        member = self.nc.getMember(self.key, service.payload["member"])
        # ger provider info
        provider = self.nc.getProvider(self.key, service.payload['provider'])

        # create report file/directory if doesnt already exist
        time = str(date.today())
        filename = ("./reports/member_report/" + member.payload["name"] + time + ".txt")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w+") as f:
            f.write("Name: " + member.payload["name"] + '\n')
            f.write("Member ID: " + member.payload['id'] + '\n')
            f.write("Address: : " + member.payload['address'] + '\n')
            f.write("City: " + member.payload['city'] + '\n')
            f.write("State: " + member.payload['state'] + '\n')
            f.write("Zip: " + member.payload['zip'] + '\n')
            f.write("Service Date: " + service.payload['date'] + '\n')
            f.write("Service Provider: " + provider.payload['name'] + '\n')
            f.write("Service Code: " + service.payload['code'] + '\n')
            f.close()
        return True

    def member_report(self):
        # get all services
        services = self.nc.getAllServices(self.key)

        # check for empty database
        if len(services.payload) == 0:
            print("Database is Empty")
            return False
        # check for service date and grab last 7 days

        for services_info in services.payload:
            if services_info["received"] >= str(datetime.now() - timedelta(days=7)):
                self.write_m_report(services_info["id"])

    def eft_report(self):
        # get all services
        services = self.nc.getAllServices(self.key)

        # check for empty database
        if len(services.payload) == 0:
            print("Database is Empty")
            return False
        # check for service date and grab last 7 days

        for services_info in services.payload:
            if services_info["received"] >= str(datetime.now() - timedelta(days=7)):
                self.write_eft_report(services_info["id"])

    def write_eft_report(self, s_id):

        # get service history info
        service = self.nc.getService(self.key, s_id)

        # get provider info
        provider = self.nc.getProvider(self.key, service.payload["provider"])

        # get menu item info
        item = self.nc.getMenuItem(self.key, service.payload["code"])

        # create report file/directory if doesnt already exist
        time = str(date.today())
        filename = ("./reports/eft_report/" + service.payload["id"] + "-" + time + ".txt")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write("Provider ID: " + service.payload['provider'] + '\n')
            f.write("Service Provider: " + provider.payload['name'] + '\n')
            f.write("Service Cost: " + item.payload['fee'] + '\n')
            f.close()
        return True

    def summary_report(self):
        # get all services
        services = self.nc.getAllServices(self.key)

        # get all providers
        providers = self.nc.getAllProviders(self.key)

        # check for empty database
        if len(services.payload) == 0:
            print("Database is Empty")
            return False

        # create report file/directory if doesnt already exist
        time = str(date.today())
        filename = ("./reports/summary_report/" + time + ".txt")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:

            total_sales = 0
            total_fee = 0
            # loop through all providers
            for providers_info in providers.payload:
                sales = 0
                fees = 0

                # check for service date and grab last 7 days
                for services_info in services.payload:
                    if services_info["received"] >= str(datetime.now() - timedelta(days=7)):
                        if services_info['provider'] == providers_info['id']:
                            sales += 1
                            # get service price
                            menuItem = self.nc.getMenuItem(self.key, services_info['code'])
                            fees += float(menuItem.payload['fee'])
                # increment totals
                if sales > 0:
                    total_sales += 1
                total_fee += fees

                # Write provider sales info to file
                f.write("Provider Name: " + providers_info['name'] + '\n')
                f.write("Provider id: " + providers_info["id"] + '\n')
                f.write("Services rendered :" + str(sales) + '\n')
                f.write("Total fees: " + str(fees) + '\n\n')
            # Write totals and close file
            f.write("Total number of providers with sales: " + str(total_sales) + '\n')
            f.write("Total cumulative fees (cents): " + str(total_fee) + '\n')
        f.close()
        return True

    def provider_report(self):
        # get all providers
        providers = self.nc.getAllProviders(self.key)

        # check for empty database
        if len(providers.payload) == 0:
            print("Database is Empty")
            return False

        for providers_info in providers.payload:
            self.write_provider_report(providers_info["id"])

    def write_provider_report(self, p_id):

        # get all services
        services = self.nc.getAllServices(self.key)

        # get provider info
        provider = self.nc.getProvider(self.key, p_id)

        # check for empty database
        if len(services.payload) == 0:
            print("Database is Empty")
            return False

        # create report file/directory if doesnt already exist
        time = str(date.today())
        filename = ("./reports/provider_report/" + provider.payload['name'] + time + ".txt")
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Write Provider info to file
        with open(filename, "w") as f:
            f.write("Provider Name: " + provider.payload['name'] + '\n')
            f.write("Provider id: " + provider.payload['id'] + '\n')
            f.write("Provider address: " + provider.payload['address'] + '\n')
            f.write("Provider city: " + provider.payload['city'] + '\n')
            f.write("Provider state: " + provider.payload['state'] + '\n')
            f.write("Provider zip: " + provider.payload['zip'] + '\n\n')
            # totals
            t_sales = 0
            t_fee = 0

            # look at services from last 7 days
            for services_info in services.payload:
                if services_info["received"] >= str(datetime.now() - timedelta(days=7)):
                    if services_info['provider'] == p_id:
                        # get member info
                        member = self.nc.getMember(self.key, services_info['member'])
                        # get menu item info
                        menuItem = self.nc.getMenuItem(self.key, services_info['code'])
                        # write service data to file
                        f.write("Service date: " + services_info['date'] + '\n')
                        f.write("Service received: " + services_info['received'] + '\n')
                        f.write("Member: " + member.payload['name'] + '\n')
                        f.write("Member id: " + services_info['member'] + '\n')
                        f.write("Service code: " + services_info['code'] + '\n')
                        f.write("Service fee (cents): " + menuItem.payload['fee'] + '\n\n')

                        # incriment totals
                        t_sales += 1
                        t_fee += float(menuItem.payload['fee'])
            f.write("Total sales: " + str(t_sales) + '\n')
            f.write("Total fees: " + str(t_fee) + '\n')
        f.close()

    # Services History Menu
    def list_services_history(self):
        # get all services network object payload and display a list of the data dictionary
        services = self.nc.getAllServices(self.key)
        if len(services.payload) == 0:
            print("Database is Empty")
            return False
        # Parse data and displays to the terminal
        else:
            print(
                "%-15s" % "Service id" + "%-10s" % "code" + "%-15s" % "Member id" + "%-15s" % "Provider id" + "status")
            for services_info in services.payload:
                print(
                    "%-15s" % services_info["id"] + "%-10s" % services_info["code"] + "%-15s" % services_info["member"]
                    + "%-15s" % services_info["provider"] + services_info["status"])

    def provider_ID(self):
        p_id = input("Enter service provider id: ")
        provider = self.nc.getProvider(self.key, p_id)
        # check the error code to see if the provider exists
        if provider.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Provider id")
            return False
        else:
            return p_id

    def provider_member(self):
        m_id = input("Enter member id: ")
        member = self.nc.getMember(self.key, m_id)
        # check the error code to see if the member exists
        if member.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Member id")
            return False
        else:
            return m_id

    def provide_service(self):

        p_id = self.provider_ID()
        if not p_id:
            return False

        m_id = self.provider_member()
        if not m_id:
            return False

        date = input("Enter service date (MM/DD/YYYY) : ")
        code = input("Enter 6 digit service code: ")
        comment = input("Please include comments on service: ")
        select = input("Was this service paid? (y/n): ")
        if select.lower() == "y":
            status = consts.STATUS_PAID
        else:
            status = consts.STATUS_UNPAID

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
            # print(result.serialize())

            if result.error != consts.ERROR_DUPLICATE_ID:
                isValidId = True
                self.nc.getService(self.key, id)
                # print(result.serialize())

            print("New Service ID: " + id)

    def update_provided_service_id_verify(self):
        id = input("Enter service id: ")

        service = self.nc.getService(self.key, id)
        # check the error code to see if the service exists
        if service.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Input")
            return False
        else:
            service_info = service.payload
            print(
                "%-15s" % "Service id" + "%-10s" % "code" + "%-15s" % "Member id" + "%-15s" % "Provider id" + "status")
            print("%-15s" % service_info["id"] + "%-10s" % service_info["code"] + "%-15s" % service_info["member"]
                  + "%-15s" % service_info["provider"] + service_info["status"])
            return id

    def update_provided_service_select_code(self):
        selectCode = input("Change service code? (y/n): ")
        if selectCode.lower() == "y":
            code = input("Enter service code: ")
            data = {"code": code}
            self.nc.setService(self.key, id, data)
        else:
            return False

    def update_provided_service_select_member(self):
        selectMember = input("Change member id? (y/n): ")
        if selectMember.lower() == "y":
            m_id = input("Enter member id: ")
            member = self.nc.getMember(self.key, m_id)
            # check the error code to see if the member exists
            if member.error == consts.ERROR_NONEXISTENT_ENTRY:
                print("Invalid Member id")
                return False
            else:
                data = {"member": m_id}
                self.nc.setService(self.key, id, data)
                return True

    def update_provided_service_select_provider(self):
        selectProvider = input("Change Provider id? (y/n): ")
        if selectProvider.lower() == "y":
            p_id = input("Enter provider id: ")
            provider = self.nc.getProvider(self.key, p_id)
            # check the error code to see if the member exists
            if provider.error == consts.ERROR_NONEXISTENT_ENTRY:
                print("Invalid provider id")
                return False
            else:
                data = {"provider": p_id}
                self.nc.setService(self.key, id, data)
                return True

    def update_provided_service_select_status(self):
        selectStatus = input("Change account status? (y/n): ")
        if selectStatus.lower() == "y":
            select = input("Was this service paid? (y/n): ")
            if select.lower() == "y":
                status = consts.STATUS_PAID
            else:
                status = consts.STATUS_UNPAID

            data = {"status": status}
            self.nc.setService(self.key, id, data)

    def update_provided_service(self):

        id = self.update_provided_service_id_verify()
        if not id:
            return False

        if not self.update_provided_service_select_code():
            return False

        if not self.update_provided_service_select_member():
            return False

        if not self.update_provided_service_select_provider():
            return False

        if not self.update_provided_service_select_status():
            return False

    def remove_provided_service(self):
        id = input("Enter service id: ")

        service = self.nc.getService(self.key, id)
        # check the error code to see if the member exists
        if service.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Input")
            return False
        else:
            service_info = service.payload
            print(
                "%-15s" % service_info["id"] + "%-10s" % service_info["code"] + "%-15s" % service_info["member"]
                + "%-15s" % service_info["provider"] + service_info["status"])
            select = input(" \nRemove this service? (Y/N): ")
            if select.lower() == 'y':
                self.nc.removeProvider(self.key, id)
                print("Service Removed")
                return True

    # Member Management Menu
    def list_all_members(self):
        # get all members network object payload and display a list of the data dictionary
        result = self.nc.getAllMembers(self.key)
        if len(result.payload) == 0:
            print("Database is Empty")
            return False
        # Parse data and displays to the terminal
        else:
            print("%-15s" % "Status" + "%-15s" % "Id" + "%-15s" % "Name" + "Address")
            for member_info in result.payload:
                if member_info["status"] == consts.STATUS_UNBANNED:
                    status = "Active"
                else:
                    status = "Banned"
                print("%-15s" % status + "%-15s" % member_info["id"] + "%-15s" % member_info["name"] +
                      member_info["address"] + " " + member_info["city"] + ", " + member_info["state"] + ", " + member_info[
                          "zip"])

    def member_status(self):
        # get user input to search for the member
        member_id = input("Member ID: ")
        # calls the get member function
        member = self.nc.getMember(self.key, member_id)
        # check the error code to see if the member exists
        if member.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Input")
            return False

        member_info = member.payload
        if member_info["status"] == consts.STATUS_UNBANNED:
            status = "Active"
        else:
            status = "Banned"
        print("%-15s" % "Status" + "%-15s" % "Id" + "%-15s" % "Name" + "Address")
        print("%-15s" % status + "%-15s" % member_info["id"] + "%-15s" % member_info["name"] + member_info["address"] + " " +
              member_info["city"] + ", " + member_info["state"] + ", " + member_info["zip"])

    def add_member(self):

        name = input("What is the name of the member? : ")
        address = input("What is the address? (Enter street address here): ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip Code: ")
        status = consts.STATUS_UNBANNED

        isValidId = False
        while not isValidId:
            id = ""
            for i in range(0, 9):
                id += str(random.choice("0123456789"))

            data = {
                "id": id,
                "name": name,
                "address": address,
                "city": city,
                "state": state,
                "zip": zip_code,
                "status": status,
            }
            result = self.nc.addMember(self.key, data)
            # print(result.serialize())
            print(result.error)
            if result.error != consts.ERROR_DUPLICATE_ID:
                isValidId = True
                self.nc.getMember(self.key, id)
                # print(result.serialize())

            print("New Member ID: " + id)

    def remove_member(self):
        # get user input to search for the member
        member_id = input("Member ID: ")
        # calls the get member function
        member = self.nc.getMember(self.key, member_id)
        # check the error code to see if the member exists
        if member.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Input")
            return False

        member_info = member.payload
        if member_info["status"] == consts.STATUS_UNBANNED:
            status = "Active"
        else:
            status = "Banned"
        print("%-15s" % "Status" + "%-15s" % "Id" + "%-15s" % "Name" + "Address")
        print("%-15s" % status + "%-15s" % member_info["id"] + "%-15s" % member_info["name"] + member_info["address"] + " " +
              member_info["city"] + ", " + member_info["state"] + ", " + member_info["zip"])

        user_input = input("Confirmation for deletion Y/N : ")
        if user_input == "Y":
            self.nc.removeMember(self.key, member_id)
            print("Successfully removed member : " + member_id + "\n")
        else:
            print("Invalid Input!" + "\n")
            return False

    def print_member(self, m_id):
        member = self.nc.getMember(self.key, m_id)
        member_info = member.payload
        if member_info["status"] == consts.STATUS_UNBANNED:
            status = "Active"
        else:
            status = "Banned"
        print("%-15s" % "Status" + "%-15s" % "Id" + "%-15s" % "Name" + "Address")
        print("%-15s" % status + "%-15s" % member_info["id"] + "%-15s" % member_info["name"] + member_info["address"] + " " +
              member_info["city"] + ", " + member_info["state"] + ", " + member_info["zip"])
        print("")
        print("")

    def check_member(self, m_id):
        member = self.nc.getMember(self.key, m_id)
        # check the error code to see if the member exists
        if member.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Member id")
            return False
        else:
            return True

    def change_m_id(self, m_id):
        isValidId = False
        while not isValidId:
            id_new = ""
            for i in range(0, 9):
                id_new += str(random.choice("0123456789"))
            data = {
                "id": id_new,
            }
            check = self.nc.setMember(self.key, m_id, data)
            if check.error != consts.ERROR_DUPLICATE_ID:
                isValidId = True
        return id_new

    def change_member_name(self, m_id):
        name = input("Enter Member name: ")
        data = {
            "name": name,
        }
        self.nc.setMember(self.key, m_id, data)

    def change_member_address(self, m_id):
        address = input("Enter Member's street address: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip Code: ")
        data = {
            "address": address,
            "city": city,
            "state": state,
            "zip": zip_code,
        }
        self.nc.setMember(self.key, m_id, data)

    def change_member_status(self, m_id):
        check = input("Is the member active? (Y/N): ")
        if check.lower() == "y":
            status = consts.STATUS_UNBANNED
        else:
            status = consts.STATUS_BANNED

        data = {
            "status": status
        }
        self.nc.setMember(self.key, m_id, data)

    def set_member(self):
        id = input("Enter member id: ")

        if not self.check_member(id):
            print("Invalid Input")
            return False

        else:
            self.print_member(id)

            select = input(" \nChange Member id? (Y/N): ")
            if select.lower() == 'y':
                id = self.change_m_id(id)

            select_name = input(" \nChange Member name? (Y/N): ")
            if select_name.lower() == 'y':
                self.change_member_name(id)

            select_address = input(" \nChange Member address? (Y/N): ")
            if select_address.lower() == 'y':
                self.change_member_address(id)

            select_status = input(" \nChange Member Status? (Y/N): ")
            if select_status.lower() == 'y':
                self.change_member_status(id)

    def delete_members_table(self):
        answer = input("Do you really want to delete all members information from the server? Y/N ")
        if answer == "Y":
            result = self.nc.truncateMembers(self.key)
            if result.error == consts.NO_ERROR:
                print("Successfully Deleted All Member Info")
        else:
            print("Canceled")
            return False

    # Provider Management Menu
    def check_provider(self, p_id):
        provider = self.nc.getProvider(self.key, p_id)
        # check the error code to see if the provider exists
        if provider.error == consts.ERROR_NONEXISTENT_ENTRY:
            print("Invalid Provider id")
            return False
        else:
            return True

    def add_provider(self):
        id = self.create_p_id()
        name = input("Enter Provider name: ")
        address = input("Enter Provider street address: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip Code: ")

        data = {
            "id": id,
            "name": name,
            "address": address,
            "city": city,
            "state": state,
            "zip": zip_code,
        }
        self.nc.addProvider(self.key, data)

    def change_p_id(self, p_id):
        isValidId = False
        while not isValidId:
            id_new = ""
            for i in range(0, 9):
                id_new += str(random.choice("0123456789"))
            data = {
                "id": id_new,
            }
            check = self.nc.setProvider(self.key, p_id, data)
            if check.error != consts.ERROR_DUPLICATE_ID:
                isValidId = True
            return id_new

    def change_provider_name(self, p_id):
        name = input("Enter Provider name: ")
        data = {
            "name": name,
        }
        self.nc.setProvider(self.key, p_id, data)

    def change_provider_address(self, p_id):
        address = input("Enter Provider street address: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip Code: ")
        data = {
            "address": address,
            "city": city,
            "state": state,
            "zip": zip_code,
        }
        self.nc.setProvider(self.key, p_id, data)

    def get_all_providers(self):
        # get all providers networkobject payload and display a list of the data dictionary
        providers = self.nc.getAllProviders(self.key)
        if len(providers.payload) == 0:
            print("Database is Empty")
            return
        # Parse data and displays to the terminal
        else:
            print("%-15s" % "Id" + "%-15s" % "Name" + "Address")
            for providers_info in providers.payload:
                print("%-15s" % providers_info["id"] + "%-15s" % providers_info["name"] + providers_info["address"] + " "
                      + providers_info["city"] + ", " + providers_info["state"] + ", " + providers_info["zip"])

    def create_s_id(self):

        isValidId = False
        while not isValidId:
            id = ""
            for i in range(0, 9):
                id += str(random.choice("0123456789"))
            check = self.nc.getService(self.key, id)
            if check.error == consts.ERROR_NONEXISTENT_ENTRY:
                isValidId = True
        return id

    def create_p_id(self):

        isValidId = False
        while not isValidId:
            id = ""
            for i in range(0, 9):
                id += str(random.choice("0123456789"))
            check = self.nc.getProvider(self.key, id)
            if check.error == consts.ERROR_NONEXISTENT_ENTRY:
                isValidId = True
        return id

    def set_provider(self):
        id = input("Enter Provider id: ")

        # check the error code to see if the provider exists
        if self.check_provider(id) == False:
            print("Invalid Input")
            return False
        else:
            self.print_provider(id)

            select = input(" \nChange Provider id? (Y/N): ")
            if select.lower() == 'y':
                id = self.change_p_id(id)

            select_name = input(" \nChange Provider name? (Y/N): ")
            if select_name.lower() == 'y':
                self.change_provider_name(id)

            select_address = input(" \nChange Provider address? (Y/N): ")
            if select_address.lower() == 'y':
                self.change_provider_address(id)

    def remove_provider(self):
        id = input("Enter Provider id: ")

        # check the error code to see if the member exists
        if self.check_provider(id) == False:
            print("Invalid Input")
            return False
        else:
            self.print_provider(id)
            select = input(" \nRemove this Provider? (Y/N): ")
            if select.lower() == 'y':
                self.nc.removeProvider(self.key, id)
                print("Provider Removed")
                return True

    def print_provider(self, p_id):
        provider = self.nc.getProvider(self.key, p_id)
        provider_info = provider.payload
        print("   Id     " + "         Name       " + "               Address              ")
        print("%-15s" % provider_info["id"] + "  " + "%-15s" % provider_info["name"] + " " + provider_info[
            "address"] + " " +
              provider_info["city"] + ", " + provider_info["state"] + ", " + provider_info["zip"])

    # Services Management Menu
    def list_all_service_offers(self):
        result = self.nc.getAllMenuItems(self.key)
        if len(result.payload) == 0:
            print("Database is empty")
        print("%-15s" % "Service Code" + "%-15s" % "Service Name" + "$%-15s" % "Fee")
        for item in result.payload:
            print("%-15s" % item["id"] + "%-15s" % item["name"] + "$%-15s" % item["fee"])

    def user_input_service_offer_id(self):
        id = input("\nWhat is the service offer id? 6 digits: ")
        return id

    def user_input_service_offer_name(self):
        name = input("\nWhat is the name of the service")
        return name

    def user_input_service_offer_fee(self):
        fee = input("\nWhat is the fee of the service? $:")
        return fee

    def add_a_service_offer(self):
        id = self.user_input_service_offer_id()
        name = self.user_input_service_offer_name()
        fee = self.user_input_service_offer_fee()
        print(fee)
        data ={
            "id": id,
            "name": name,
            "fee": fee
        }
        result = self.nc.addMenuItem(self.key, data)
        print(result.payload)
        print(result.error)

    def check_a_service_offer(self, serviceId):
        if not serviceId:
            return False
        if self.nc.getMenuItem(self.key, serviceId).error == consts.NO_ERROR:
            item = self.nc.getMenuItem(self.key, serviceId).payload
            print("%-15s" % item["id"] + "%-15s" % item["name"] + "$%-15s" % item["fee"])
            return True

    def remove_a_service_offer(self):
        id = self.user_input_service_offer_id()
        if self.check_a_service_offer(id):
            answer = input("\nDo you really want to remove this service offer? ID: " + id + " Y/N")
            if answer == "Y":
                result = self.nc.removeMenuItem(self.key, id)
                print("Successfully delete service Id: " + id)
        else:
            print("Invalid Id")

    def update_a_service_offer(self):
        id = self.user_input_service_offer_id()
        if self.check_a_service_offer(id):

            old_id = id
            service_offer = self.nc.getMenuItem(self.key, id).payload
            name = service_offer["name"]
            fee = service_offer["fee"]

            answerID = input("\nDo you want to change the service offer id? Y/N")
            if answerID == "Y":
                new_id = self.user_input_service_offer_id()
                id = new_id
                self.nc.setMenuItem(self.key, id, {"id": id})
            else:
                print("Invalid Input")

            answerName = input("\nDo you want to change the name of the service offer? Y/N ")
            if answerName == "Y":
                new_name = self.user_input_service_offer_name()
                name = new_name
                self.nc.setMenuItem(self.key, id, {"name": name})
            else:
                print("Invalid Input")

            answerFee = input("\nDo you want to change the fee of the service offer? Y/N ")
            if answerFee == "Y":
                new_fee = self.user_input_service_offer_fee()
                fee = new_fee
                self.nc.setMenuItem(self.key, id, {"fee": fee})
            else:
                print("Invalid Input")


        else:
            print("Invalid id")

    def remove_all_service_offers(self):
        answer = input("\nDo you really want to remove all service offers? Y/N")
        if answer == "Y":
            result = self.nc.truncateMenu(self.key)
            print("Successfully delete all offers")

    # Keys Management Menu
    def list_all_keys(self):
        keys = self.nc.getAllKeys(self.key)
        if len(keys.payload) == 0:
            print("Key Table is Empty")
            return False
        # Parse data and displays to the terminal
        print("%-15s" % "Name" + "%-15s" % "Level" + "%-15s" % "Hash (ID/Primary Key)")
        for key in keys.payload:
            print("%-15s" % key["name"] + "%-15s" % key["level"] + "%-15s" % key["id"])

    def update_key_modify_name(self):
        answer = input("Do you want to modify the name? Y/N")
        if answer.upper() == "Y":
            name = input("What is the new name?")
            self.nc.setKey(self.key, self.mykey, {"name": name})
            return True
        else:
            print("name not changed")
            return False

    def update_key_modify_level(self):
        answer = input("\nDo you want to change the access level of the key? Y/N")
        if answer.upper() == "Y":
            level = input("\nwhat is the level of the key? \n" + "1. Manager Key \n" + "2. Provider Key \n")
            if level == "1":
                level = consts.KEY_ROOT
                self.nc.setKey(self.key, self.mykey, {"level": level})
            elif level == "2":
                level = consts.KEY_PROVIDER
                self.nc.setKey(self.key, self.mykey, {"level": level})
            else:
                print("Access level not changed.")
        else:
            print("Access level not changed")

    def update_key_unique_key(self):
        answer = input("\nDo you want to change the unique access key? Y/N")
        if answer.upper() == "Y":
            newKey = "".join(random.choices(string.ascii_uppercase + string.digits, k=32))
            self.nc.setKey(self.key, self.mykey, {"uak": newKey})
            print("Your new unique access key is", newKey, ".")
        else:
            print("access key not changed")

    def update_a_key(self):
        self.mykey = input("\nWhat is the UAK that you want to modify?")
        result = self.nc.validateKey(self.mykey).payload
        if result == consts.KEY_ROOT or result == consts.KEY_PROVIDER:
            self.update_key_modify_name()
            self.update_key_modify_level()
            self.update_key_unique_key()
        else:
            print("Key is invalid")

    def validate_a_key(self):
        key = input("What is the key?: ")
        result = self.nc.validateKey(key)
        print("\n" + result.payload + "\n")

    def add_a_key(self):
        name = input("What is the name? ")
        newKey = "".join(random.choices(string.ascii_uppercase + string.digits, k=32))

        level = input("what is the level of the key? \n" + "1. Manager Key \n" + "2. Provider Key \n")
        if level == "1":
            level = consts.KEY_ROOT
        elif level == "2":
            level = consts.KEY_PROVIDER
        else:
            print("Invalid Input")
                
        data = {
            "id": newKey,
            "name": name,
            "level": level
        }
        print("Your new unique access key is", data["id"], ".")
        self.nc.addKey(self.key, data)

    def remove_a_key(self):
        key = input("\nWhat is the key you want to remove?: ")
        result = self.nc.validateKey(key).payload
        if result == consts.KEY_ROOT or result == consts.KEY_PROVIDER:
            answer = input("Do you really want to remove the key? Y/N")
            if answer.upper() == "Y":
                result = self.nc.removeKey(self.key, key)
                if result.error == consts.NO_ERROR:
                    print("Successfully deleted key from key table")
            else:
                print("Canceled")
        else:
            print("Canceled")

    def remove_all_keys(self):
        answer = input("\nDo you really want to delete all keys? Y/N :")
        if answer.upper() == "Y":
            result = self.nc.truncateKeys(self.key)
            if result.error == consts.NO_ERROR:
                print("Successfully Deleted All Keys")
            else:
                print(result.error)
        else:
            print("Canceled")
