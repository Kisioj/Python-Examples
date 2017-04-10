#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import socket

conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
conn.connect(('127.0.0.1', 8080))
while True:
    msg = input('> ')
    conn.send(msg.encode())
    msg = conn.recv(1024).decode()
    print('server:', msg)
