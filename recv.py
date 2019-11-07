#!/usr/bin/python3

import sys
import os
import argparse

import backTCP
from utils import *


def parse_args():
    parser = argparse.ArgumentParser(description="receive a file from backTCP", epilog="This program is created by iBug")
    parser.add_argument('filename', metavar="file", help="the name to save received file as")
    parser.add_argument('-a', '-A', '--address', metavar="addr", help="address to listen for", default="0.0.0.0")
    parser.add_argument('-p', '--port', metavar="port", type=int, help="port to listen on", default=6666)
    parser.add_argument('-l', '--log-level', metavar="level", help="logging level", default=LOG_WARNING)
    return parser.parse_args()


def main():
    args = parse_args()
    set_log_level(args.log_level)

    with open(args.filename, "wb") as f:
        f.write(backTCP.recv(args.address, args.port))


if __name__ == '__main__':
    main()
