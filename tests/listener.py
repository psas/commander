#!/usr/bin/env python
import socket
import time
from contextlib import closing


HOST = ''                 # Symbolic name meaning the local host
PORT = 2223              # Arbitrary non-privileged port

ports = 0

with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    while 1:
        conn, addr = s.accept()
        while 1:
            data = conn.recv(1024)
            if not data: continue
            print data


            if 'OFF' in data:
                ports = 127
            elif 'XFF' in data:
                ports = 0
            elif data[5] == 'O':
                ports |= int(data[6:])
            elif data[5] == 'X':
                ports &= ~int(data[6:])

            conn.send(str(ports))
            conn.close()
            break
