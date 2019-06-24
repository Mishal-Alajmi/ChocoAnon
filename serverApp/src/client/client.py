from threading import Thread
import constants.consts as consts
import errno
import socket
from network.networkObject.networkObject import NetworkObject
import time


class Client(Thread):
    def __init__(self, connection, dbc):
        Thread.__init__(self)
        self.connection = connection
        self.dbc = dbc

        print("[+] Client connected")

    def run(self):
        try:
            while True:
                # retrieve the data sent by the client and check that they actually sent something (including "")
                # data = self.connection.recv(consts.BUFFER_SIZE).decode()  # note that the string is encoded as an aob

                oldTime = int(round(time.time() * 1000000))
                # reading = True
                # frags = []
                # while reading:
                #     chunk = self.connection.recv(4096).decode()
                #     if chunk[len(chunk) - 1:len(chunk)] == '\0':
                #         reading = False
                #         frags.append(chunk[0:len(chunk) - 1])  # remove the null, it'll mess up NetworkObject.initialize()
                #     else:
                #         frags.append(chunk)
                # data = ''.join(frags)

                # data = self.connection.recv(4096).decode()
                reading = True
                frags = []
                while reading:
                    chunk = self.connection.recv(4096).decode()

                    # recv can continuously return empty strings, depending on what the client does, without the check it'll go into an infinite loop
                    # this is fixable clientside, but that opens the server up to XSS, better to fix it here and let the client do w/e
                    if chunk[len(chunk) - 1:len(chunk)] == '\0' or chunk == "":
                        reading = False
                        frags.append(chunk[0:len(chunk) - 1])  # remove the null, it'll mess up NetworkObject.initialize()
                    else:
                        frags.append(chunk)
                data = "".join(frags)

                # data = data[0:len(data) - 1]
                print("Time elapsed:", int(round(time.time() * 1000000)) - oldTime)

                if not data:
                    self.connection.send(str.encode(consts.ERROR_UNKNOWN + '\0'))
                else:
                    networkObject = NetworkObject()
                    networkObject.initialize(data)

                    result = self.parseNetworkObject(networkObject)

                    self.connection.send(str.encode(result.serialize() + '\0'))  # send result back
        except socket.error as e:
            if (e.errno == errno.EPIPE):  # broken pipe error, not sure where this is defined
                print("[-] Client disconnected.")
            else:
                raise
        except Exception as e:
            print(e)
        finally:
            self.connection.close()

    """
    Execute the instruction contained in the network object
    Then return a new network object with the exec's error and result
    """
    def parseNetworkObject(self, networkObject):
        responseError = consts.ERROR_INVALID_COMMAND  # no news is bad news because this should be set in one of the if blocks
        responseCommand = consts.NO_CMD
        responsePayload = {}
        responseTable = consts.NO_TABLE
        response = self.dbc.execute(networkObject.table, networkObject.command, networkObject.payload, networkObject.key)
        if response["error"] == consts.NO_ERROR:
            responsePayload = response["result"]
            responseError = consts.NO_ERROR
        else:
            responseError = response["error"]

        return NetworkObject("", responseError, responseCommand, responsePayload, responseTable)
