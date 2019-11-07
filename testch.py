#!/usr/bin/python3

import sys
import os
import argparse
import random
import threading

import backTCP
from utils import *


def pass_through(from_socket, to_socket):
    def handler(from_socket, to_socket):
        while True:
            if from_socket.sock is None:
                # Closed - don't waste CPU
                break
            try:
                # Blindly forward packets
                p = from_socket.recv()
                to_socket.send(p)
            except Exception:
                pass

    # Run in background and don't worry anymore
    t = threading.Thread(target=handler, args=(from_socket, to_socket), daemon=True)
    t.start()
    return t


def btMITM(out_addr, out_port, in_addr, in_port):
    # This is going to be challenging: listen and send at the same time while manipulating packets
    in_sock = backTCP.BTcpConnection('recv', in_addr, in_port)
    out_sock = backTCP.BTcpConnection('send', out_addr, out_port)

    # We're not going to manipulate server responses
    pass_through(out_sock, in_sock)

    packets = []

    while True:
        p = in_sock.recv()
        if p is None:
            p.close()
            return
        packets.append(p)

        # TODO: Shuffle and drop randomly
        # XXX: When to perform this action?
        if len(packets) >= 0:
            for p in packets:
                out_sock.send(p)
            packets = []


def parse_args():
    parser = argparse.ArgumentParser(description="starts a backTCP test channel", epilog="This program is created by iBug")
    parser.add_argument('-a', '--out-addr', '--address', metavar="addr", help="address of receiver", default="127.0.0.1")
    parser.add_argument('-p', '--out-port', '--port', metavar="port", type=int, help="port of receiver", default=6666)
    parser.add_argument('-A', '--in-addr', metavar="addr", help="address to listen for sender", default="0.0.0.0")
    parser.add_argument('-P', '--in-port', metavar="port", type=int, help="port to listen for sender", default=6667)
    parser.add_argument('-l', '--log-level', metavar="level", help="logging level", default=LOG_WARNING)
    return parser.parse_args()


def main():
    global log_level
    args = parse_args()
    log_level = validate_log_level(args.log_level)

    btMITM(args.address, args.port, args.in_addr, args.in_port)


if __name__ == '__main__':
    main()
