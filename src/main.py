#!/usr/bin/python3
import argparse
from server import *
from client import *

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Online Bingo Game')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' network the client sends to')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='ZMQ REQ port')
    parser.add_argument('-s', metavar='port', type=int, default=2060,
                        help='ZMQ SUB port')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p, args.s)
