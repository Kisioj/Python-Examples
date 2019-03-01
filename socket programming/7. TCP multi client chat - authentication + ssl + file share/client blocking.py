import socket
import threading

from shared.config import HOST, PORT
from shared.client import dispatch, context, authentication, chat_logic, connection_handler
from shared import client
from shared.clock import Clock

def main():
    connection = context.wrap_socket(socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM))
    connection.connect((HOST, PORT))

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
