import socket
import ssl
import threading

from shared.clock import Clock
from shared.config import HOST, PORT
from shared.client import dispatch, context, authentication, chat_logic
from shared import client

def connection_handler(connection):
    clock = Clock(fps=30)
    while True:
        clock.tick()
        try:
            raw_data = connection.recv(1024).decode()

            if not raw_data:
                continue
            else:
                for json_data in raw_data.split('\x00'):
                    if json_data:
                        # print('json_data', json_data)
                        dispatch(connection, json_data)

        except ssl.SSLWantReadError:
            continue


def main():
    connection = context.wrap_socket(socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM))
    connection.connect((HOST, PORT))
    connection.setblocking(False)

    thread = threading.Thread(target=connection_handler, args=(connection,))
    thread.daemon = True  # exit the thread when the main thread terminates
    thread.start()

    authentication(connection)

    clock = Clock(fps=10)
    while not client.logged_in:
        clock.tick()

    chat_logic(connection)


if __name__ == '__main__':
    main()
