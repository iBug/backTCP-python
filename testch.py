#!/usr/bin/python3

import sys
import os
import argparse
import random
import threading

import backTCP
from utils import *


# Actions: What to do for a stream of incoming packets
#   0: Do nothing and forward
#   1: Drop unless retransmitted
#   2: Swap two packets
#   3: Randomly order 3 packets and maybe drop one and maybe duplicate one
#
# You can configure the following list to change the possibility of each action
ACTIONS = [0] * 7 + [1] * 5 + [2] * 5 + [3] * 3


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
        action = random.choice(ACTIONS)
        log('debug', f"Action: {action}")
        packet_needed = max(1, action)
        packet_count = 0

        while packet_count < packet_needed:
            p = in_sock.recv()
            if p is None:
                # The last ones aren't manipulated
                for p in packets:
                    out_sock.send(p)
                out_sock.send(None)  # Tell the receiver to close
                in_sock.close()
                out_sock.close()
                return
            packet_count += 1
            packets.append(p)

        if action == 0:
            pass # through
        elif action == 1:
            if not packets[0].flag & 1:
                # Packet loss
                packets.pop()
        elif action == 2:
            # Swap packets
            packets = packets[::-1]
        else:
            # Shuffle three packets ...
            random.shuffle(packets)
            for i in range(len(packets)):
                if random.random() >= 0.8:
                    # ... and maybe duplicate one ...
                    packets.append(random.choice(packets))
                    break
                if not packets[i].flag & 1 and random.random() >= 0.5:
                    # ... or drop up to 1 at random
                    packets.pop(i)
                    break

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
    args = parse_args()
    set_log_level(args.log_level)

    btMITM(args.out_addr, args.out_port, args.in_addr, args.in_port)


if __name__ == '__main__':
    main()
