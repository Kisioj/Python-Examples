#!/usr/bin/env python3
import select
import socket
import threading

from shared.config import HOST, PORT
from shared.server import setup, handle_packets, finish, clients, connection_to_client_map


def new_client_listener():
    while True:
        connection, client_address = server.accept()
        setup(connection=connection, client_address=client_address)


if __name__ == "__main__":
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    with server:
        server.bind((HOST, PORT))
        server.listen(100)

        thread = threading.Thread(target=new_client_listener)
        thread.start()

        while True:
            rlist, wlist, xlist = select.select(connection_to_client_map, [], [], 0.03)

            for connection in rlist:
                if not handle_packets(connection=connection):
                    finish(connection=connection)
