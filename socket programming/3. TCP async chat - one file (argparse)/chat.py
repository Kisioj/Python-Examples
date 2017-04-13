#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import socket
import threading


def send(conn):
    while True:
        msg = input()
        conn.send(msg.encode())


def main():
    parser = argparse.ArgumentParser(description='Python chat')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--client', action='store_true', help='Join existing server')
    group.add_argument('-s', '--server', action='store_true', help='Host new server')
    parser.add_argument('--ip', help='IP address of the server', default='127.0.0.1')
    parser.add_argument('--port', type=int, help='Port of the server', default=8080)
    args = parser.parse_args()

    ip, port = args.ip, args.port
    address = (ip, port)

    if args.server:
        talk_to = 'client'
        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        server.bind(address)
        print('Started listening on port {}'.format(port))
        server.listen(1)
        conn, address = server.accept()
    else:
        talk_to = 'server'
        conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        conn.connect(address)
        print('Joined server on {}:{}'.format(ip, port))
    thread = threading.Thread(target=send, args=(conn,))
    thread.start()
    while True:
        msg = conn.recv(1024).decode()
        print('{}: {}'.format(talk_to, msg))


if __name__ == '__main__':
    main()
