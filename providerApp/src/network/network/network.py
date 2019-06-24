import socket
import ssl
import constants.consts as consts
from network.networkObject.networkObject import NetworkObject


# this class wraps basic socket functionality
# to other members of my group: don't use this class. use NetworkController instead
class Network():
    def __init__(self):
        self.ip = consts.TCP_IP
        self.port = consts.TCP_PORT
        self.bufferSize = consts.BUFFER_SIZE
        self.noServer = False

        # open a connection to the ca server
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sslSock = ssl.wrap_socket(self.socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs="network/certs/serverCert.pem")
            self.sslSock.connect((consts.TCP_IP, consts.TCP_PORT))
        except ConnectionRefusedError:
            self.noServer = True
            print("Connection was refused, probably because the server isn't running.")

    def __del__(self):
        try:
            self.sslSock.close()
        except AttributeError:
            pass
        finally:
            pass

    # send the string to the server and return the server's response
    def sendString(self, string):
        ret = NetworkObject()
        try:
            if self.noServer:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sslSock = ssl.wrap_socket(self.socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs="network/certs/serverCert.pem")
                self.sslSock.connect((consts.TCP_IP, consts.TCP_PORT))
                self.noServer = False

            self.sslSock.write(str.encode(string))
            response = self.sslSock.recv(self.bufferSize).decode()  # make sure to convert from aob to string
            ret.initialize(response)
        except ConnectionRefusedError:
            self.noServer = True
            ret.error = consts.ERROR_CONNECTION_FAILED
        finally:
            return ret

    def sendNetworkObject(self, networkObject):
        response = self.sendString(networkObject.serialize())
        return response
