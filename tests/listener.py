#!/usr/bin/env python
import socket
import time

HOST = ''                 # Symbolic name meaning the local host
PORT = 2223              # Arbitrary non-privileged port


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        if not data: continue
        print data
        conn.send("Unknown")
        conn.close()
        break
