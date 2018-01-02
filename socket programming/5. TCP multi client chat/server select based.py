#!/usr/bin/env python3
import select
import socket

from shared.config import HOST, PORT
from shared.server import setup, handle_packets, finish, clients, connection_to_client_map

if __name__ == "__main__":
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    with server:
        server.bind((HOST, PORT))
        server.listen(100)

        while True:
            rlist, wlist, xlist = select.select(list(connection_to_client_map) + [server], [], [], 0.03)

            for rconn in rlist:
                if rconn is server:
                    connection, client_address = server.accept()
                    setup(connection=connection, client_address=client_address)
                elif not handle_packets(connection=rconn):
                    finish(connection=rconn)

