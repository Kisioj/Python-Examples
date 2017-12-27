# https://stackoverflow.com/questions/8582766/adding-ssl-support-to-socketserver
import socketserver
# import threading

from shared.config import HOST, PORT
from shared.server import setup, handle, finish


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        setup(connection=self.request, client_address=self.client_address)

    def handle(self):
        handle(connection=self.request)

    def finish(self):
        finish(connection=self.request)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        server.serve_forever()

    # server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    # thread = threading.Thread(target=server.serve_forever)
    # thread.daemon = True  # Exit the server thread when the main thread terminates
    # thread.start()
    # with server:
    #     while True:
    #         input()  # GAME LOGIC
