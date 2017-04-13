#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading


def send(conn):
    while True:
        msg = input()
        conn.send(msg.encode())


def main():
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    print('Started listening on port 8080')
    server.listen(1)
    conn, address = server.accept()
    thread = threading.Thread(target=send, args=(conn,))
    thread.start()
    while True:
        msg = conn.recv(1024).decode()
        print('server:', msg)


if __name__ == '__main__':
    main()
