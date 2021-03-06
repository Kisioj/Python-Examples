import socket
import threading

from shared.config import HOST, PORT
from shared.server import setup, handle, finish, context


def client_thread(connection, client_address):
    setup(connection=connection, client_address=client_address)
    handle(connection=connection)
    finish(connection=connection)


def client_listener():
    while True:
        connection, client_address = server.accept()
        thread = threading.Thread(target=client_thread, args=(connection, client_address))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    server = context.wrap_socket(
        socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM),
        server_side=True
    )

    server.bind((HOST, PORT))
    server.listen(100)

    thread = threading.Thread(target=client_listener)
    thread.daemon = True
    thread.start()

    input()
    server.close()
