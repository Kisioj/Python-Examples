#!/usr/bin/env python3
import socket

from shared.clock import Clock
from shared.config import HOST, PORT
from shared.server import setup, handle, finish, clients


def client_listener():
    clock = Clock(fps=30)
    while True:
        clock.tick()
        try:
            connection, client_address = server.accept()
            connection.setblocking(0)
            setup(connection=connection, client_address=client_address)
        except BlockingIOError:
            pass

        for client in clients:
            try:
                handle(connection=client.connection)
                finish(connection=client.connection)
            except BlockingIOError:
                continue


if __name__ == "__main__":
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    with server:
        server.bind((HOST, PORT))
        server.listen(100)
        server.setblocking(0)

        client_listener()
