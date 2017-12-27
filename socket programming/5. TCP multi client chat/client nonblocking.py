#!/usr/bin/env python3
import socket
import threading
import errno
from shared.clock import Clock
from shared.config import HOST, PORT
from shared.client import dispatch, send_loop


def connection_handler(connection):
    clock = Clock(fps=30)
    while True:
        clock.tick()
        try:
            raw_data = connection.recv(1024).decode()

            if not raw_data:
                continue
            else:
                for json_data in raw_data.split('\n'):
                    if json_data:
                        # print('json_data', json_data)
                        dispatch(connection, json_data)

        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK:
                continue
            raise


def main():
    connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    connection.connect((HOST, PORT))
    connection.setblocking(0)

    thread = threading.Thread(target=connection_handler, args=(connection,))
    thread.daemon = True  # exit the thread when the main thread terminates
    thread.start()

    send_loop(connection)

if __name__ == '__main__':
    main()
