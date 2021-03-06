#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading


def send(conn):
    while True:
        msg = input()
        conn.send(msg.encode())


def main():
    conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    conn.connect(('127.0.0.1', 8080))
    thread = threading.Thread(target=send, args=(conn,))
    thread.start()
    while True:
        msg = conn.recv(1024).decode()
        print('server:', msg)

if __name__ == '__main__':
    main()
