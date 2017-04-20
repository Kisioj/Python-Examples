#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import functools
import os
import pickle
import re
import socket


connection = None


def network(func):
    @functools.wraps(func)
    def inner(player, *args, **kwargs):
        if player.is_remote:
            return pickle.loads(connection.recv(1024))
        else:
            result = func(player, *args, **kwargs)
            if connection:
                connection.send(pickle.dumps(result))
            return result
    return inner


class Player(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.is_remote = False

    def play(self):
        x, y = self.coord_input('Enter coordinates to draw there symbol %s (np. A2):' % self.symbol, '^[ABC][123]$')
        fields[y][x] = self.symbol

    @property
    def is_winner(self):
        horizontal = [''.join(row) for row in fields]
        vertical = [''.join(row) for row in zip(*fields)]
        diagonal = [''.join(fields[i][i] for i in range(3)), ''.join(fields[i][2 - i] for i in range(3))]
        return (self.symbol * 3) in (horizontal + vertical + diagonal)

    @network
    def coord_input(self, msg, regexp):
        validator = re.compile(regexp)
        print(msg, end=' ')
        while True:
            result = input()
            if not validator.match(result):
                print('Incorrect coordinates, enter again:', end=' ')
            else:
                x, y = result
                x = ord(x) - ord('A')
                y = int(y) - 1
                if fields[y][x] != '.':
                    print('There already is something on this field, choose other:', end=' ')
                else:
                    return x, y


def is_draw():
    return all(map(lambda field: field != '.', (field for row in fields for field in row)))


def play():
    while True:
        for player in players:
            os.system('cls')
            print("It's now turn of player with symbol", player.symbol)
            print('  A B C')
            print('\n'.join('%d ' % (i+1) + ' '.join(row) for i, row in enumerate(fields)))

            player.play()
            if player.is_winner or is_draw():
                os.system('cls')
                print('End of the game')
                print('  A B C')
                print('\n'.join('%d ' % (i+1) + ' '.join(row) for i, row in enumerate(fields)))
                if player.is_winner:
                    print('Player with symbol', player.symbol, 'won!')
                else:
                    print('Draw!')
                return


def host(string):
    regexp = re.compile(r'^[0-9]+(?:\.[0-9]+){3}$')
    if not regexp.match(string):
        raise argparse.ArgumentTypeError("%r is not correct ip" % string)
    return string


def main():
    global connection
    parser = argparse.ArgumentParser(description='Tick tack toe Multiplayer')
    parser.add_argument('--server', action="store_true", help="create new server")
    parser.add_argument('--client', action="store_true", help="join existing server")
    parser.add_argument('--host', type=host, help="host", default="127.0.0.1")
    parser.add_argument('--port', type=int, help="port", default=12345)
    args = parser.parse_args()
    if args.server:
        print('Listening on port {}'.format(args.port))
        s = socket.socket()
        s.bind((args.host, args.port))
        s.listen(1)
        c, addr = s.accept()
        connection = c
        p2.is_remote = True
    elif args.client:
        s = socket.socket()
        s.connect((args.host, args.port))
        connection = s
        p1.is_remote = True

    play()
    if connection:
        connection.close()

if __name__ == '__main__':
    p1, p2 = Player('O'), Player('X')
    players = (p1, p2)

    width, height = 3, 3
    fields = [['.' for x in range(width)] for y in range(height)]

    main()
