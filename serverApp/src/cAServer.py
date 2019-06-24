# this file need to be at project root

import socket
import ssl
from database.databaseController.databaseController import DatabaseController
from client.client import Client
import constants.consts as consts


class CAServer:
    def __init__(self):
        self.dbc = DatabaseController("chocan.db")

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((consts.TCP_IP, consts.TCP_PORT))
        sock.listen(1)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sockSsl = ssl.wrap_socket(sock, keyfile="network/certs/server.key", certfile="network/certs/serverCert.pem", server_side=True)

        threads = []
        print("Server active, waiting for client connection")
        while True:
            try:
                connection = None
                connection, addr = sockSsl.accept()

                newthread = Client(connection, self.dbc)
                newthread.start()
                threads.append(newthread)
            except Exception as e:
                print(e)

        for t in threads:
            t.join()


cas = CAServer()
cas.start()
