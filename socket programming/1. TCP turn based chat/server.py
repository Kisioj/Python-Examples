#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import socket

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8080))
print('Started listening on port 8080')
server.listen(1)
conn, address = server.accept()
while True:
    msg = conn.recv(1024).decode()
    print('client:', msg)
    msg = input('> ')
    conn.send(msg.encode())
