import json
import random
import string
import os

# make sure to uncomment this if you want to load the data into the database
# from network.networkController.networkController import NetworkController


def randStr(chars):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=chars))


numEntries = 10
with open("initDbData.json", "w") as file:
    dict = {}

    dict["members"] = []
    for i in range(1, numEntries):
        id = randStr(9)
        name = randStr(7)
        address = randStr(3)
        city = randStr(4)
        state = randStr(9)
        zip = randStr(5)
        dict["members"].append({"id": id, "name": name, "address": address, "city": city, "state": state, "zip": zip})

    dict["admins"] = []
    for i in range(1, numEntries):
        id = randStr(9)
        name = randStr(7)
        uak = randStr(32)
        dict["admins"].append({"id": id, "name": name, "uak": uak})

    dict["services"] = []
    for i in range(1, numEntries):
        id = randStr(9)
        code = randStr(6)
        provider = randStr(9)
        member = randStr(9)
        comment = randStr(500)
        status = randStr(7)
        dict["services"].append({"id": id, "code": code, "provider": provider, "member": member, "comment": comment, "status": status})

    dict["menu"] = []
    for i in range(1, numEntries):
        id = randStr(6)
        name = randStr(6)
        fee = randStr(5)
        dict["menu"].append({"id": id, "name": name, "fee": fee})

    dict["providers"] = []
    for i in range(1, numEntries):
        id = randStr(6)
        address = randStr(6)
        city = randStr(5)
        state = randStr(8)
        zip = randStr(5)
        uak = randStr(32)
        dict["providers"].append({"id": id, "address": address, "city": city, "state": state, "zip": zip, "uak": uak})

    file.write(json.dumps(dict))


# this code will load the data into the database from the file that was just made
"""
data = json.load(open("initDbData.json"))
nc = NetworkController()

for i in range(0, len(data["members"])):
    member = data["members"][i]
    nc.addMember("AS62ELRB5F0709LERPHZD06JWC0P8QSC", member)

for i in range(0, len(data["admins"])):
    admin = data["admins"][i]
    nc.addAdmin("AS62ELRB5F0709LERPHZD06JWC0P8QSC", member)

for i in range(0, len(data["menu"])):
    menu = data["menu"][i]
    nc.addAdmin("AS62ELRB5F0709LERPHZD06JWC0P8QSC", menu)

for i in range(0, len(data["services"])):
    service = data["services"][i]
    nc.addAdmin("AS62ELRB5F0709LERPHZD06JWC0P8QSC", service)

for i in range(0, len(data["providers"])):
    provider = data["providers"][i]
    nc.addAdmin("AS62ELRB5F0709LERPHZD06JWC0P8QSC", provider)
"""
