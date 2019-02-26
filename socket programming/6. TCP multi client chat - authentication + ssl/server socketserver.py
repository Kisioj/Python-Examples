import socketserver

from shared.config import HOST, PORT
from shared.server import setup, handle, finish, context


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        setup(connection=self.request, client_address=self.client_address)

    def handle(self):
        handle(connection=self.request)

    def finish(self):
        finish(connection=self.request)


class SSLThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def get_request(self):
        sock, addr = self.socket.accept()
        ssock = context.wrap_socket(sock, server_side=True)
        return ssock, addr


if __name__ == "__main__":
    with SSLThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        server.serve_forever()

    # server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    # thread = threading.Thread(target=server.serve_forever)
    # thread.daemon = True  # Exit the server thread when the main thread terminates
    # thread.start()
    # with server:
    #     while True:
    #         input()  # GAME LOGIC
