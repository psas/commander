""" PSAS Command definitions.
"""
import socket

class TCP_Command(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send(self, cmd):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', 0))
            sock.settimeout(2)
            sock.connect((self.ip, self.port))
        except:
            sock.close()
            return None, "Connection error"

        try:
            sock.send(cmd)
        except socket.timeout:
            sock.close()
            return None, "Send timeout"
        except:
            sock.close()
            return None, "Send failed"

        try:
            data = sock.recv(512)
            data = data.rstrip(" \t\n\r\0")
        except:
            sock.close()
            return None, "Response timeout"

        sock.close()
        return 1, data


CONNECTIONS = {
    'TEST': {'TCP': TCP_Command('127.0.0.1', 2223)},
    'RNH':  {'TCP': TCP_Command('10.10.10.5',  23)},
    'FC':   {'TCP': TCP_Command('10.10.10.10', 23)},
    'IMU':  {'TCP': TCP_Command('10.10.10.20', 23)},
    'ROLL': {'TCP': TCP_Command('10.10.10.30', 23)},
}
