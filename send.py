#!/usr/bin/python3

import sys
import os
import argparse

import backTCP
from utils import *


def parse_args():
    parser = argparse.ArgumentParser(description="send a file via backTCP", epilog="This program is created by iBug")
    parser.add_argument('filename', metavar="file", help="the name of the file to send")
    parser.add_argument('-a', '-A', '--address', metavar="addr", help="address of target to send", default="127.0.0.1")
    parser.add_argument('-p', '--port', metavar="port", type=int, help="port of target to send", default=6666)
    parser.add_argument('-l', '--log-level', metavar="level", help="logging level", default=LOG_WARNING)
    return parser.parse_args()


def main():
    args = parse_args()
    set_log_level(args.log_level)

    with open(args.filename, "rb") as f:
        data = f.read()
    backTCP.send(data, args.address, args.port)


if __name__ == '__main__':
    main()
