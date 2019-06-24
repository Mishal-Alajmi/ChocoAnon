import json


# this class is what gets transferred over the network
class NetworkObject():
    def __init__(self, key=None, error=None, command=None, payload=None, table=None):
        self.error = error  # error codes are defined in consts.py
        self.command = command  # commands are also defined in consts.py
        self.table = table  # defined in consts.py
        self.key = key  # a unique access key, in hashed form
        self.payload = payload  # should be a dict

    """
    initialize this from a json string made with serialize()
    """
    def initialize(self, string):
        dictionary = json.loads(string)
        self.error = dictionary["error"]
        self.command = dictionary["command"]
        self.key = dictionary["key"]
        self.table = dictionary["table"]

        # load payload as a dict if it's json, otherwise load it as a string
        try:
            self.payload = json.loads(dictionary["payload"])
        except Exception:
            self.payload = dictionary["payload"]
    """
    convert to json string
    """
    def serialize(self):
        dictionary = {}
        dictionary["error"] = self.error
        dictionary["command"] = self.command
        dictionary["key"] = self.key
        dictionary["table"] = self.table

        if isinstance(self.payload, dict):
            dictionary["payload"] = json.dumps(self.payload)
        else:
            dictionary["payload"] = self.payload
        return json.dumps(dictionary)
