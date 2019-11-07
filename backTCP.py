import os
import socket

from utils import log


class BTcpConnection:
    def __init__(self, mode, addr, port):
        # Create a TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.remote_addr = None

        if mode == 'send':
            self.remote_addr = addr, port
            self.sock.connect(self.remote_addr)
        elif mode == 'recv':
            self.sock.bind((addr, port))
            log('info', f"Listening on {addr} port {port}")
            self.sock.listen(1)
            self.conn, self.remote_addr = self.sock.accept()
            log('info', f"Accepted connection from {self.remote_addr[0]} port {self.remote_addr[1]}")
        else:
            raise ValueError(f"Unexpected mode {mode}")

    def __del__(self):
        try:
            self.sock.close()
        except Exception:
            pass


class BTcpPacket:
    def __init__(self, sport=None, dport=None, seq=None, ack=None, data_off=None, win_size=None, flag=0, data=b""):
        self.sport = sport
        self.dport = dport
        self.seq = seq
        self.ack = ack
        self.data_off = data_off
        self.win_size = win_size
        self.flag = flag
        self.data = data

    def __bytes__(self):
        return bytes([
            self.sport, self.dport, self.seq, self.ack,
            self.data_off, self.win_size, self.flag,
        ]) + bytes(self.data)


def send(data, addr, port):
    conn = BTcpConnection('send', addr, port)


def recv(addr, port):
    conn = BTcpConnection('recv', addr, port)
