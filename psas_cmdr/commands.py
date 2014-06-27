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
            sock.connect((self.ip, self.port))
        except:
            sock.close()
            print "connection error"
            return None

        try:
            sock.send(cmd)
        except socket.timeout:
            sock.close()
            print "timoute"
            return None
        except:
            sock.close()
            print "didnt send"
            return None

        try:
            data = sock.recv(512)
        except:
            sock.close()
            return None

        sock.close()
        return data



CONNECTIONS = {
    'TEST': {'TCP': TCP_Command('127.0.0.1', 2223)},
    'RNH':  {'TCP': TCP_Command('10.0.0.5',  23)},
    'FC':   {'TCP': TCP_Command('10.0.0.10', 23)},
    'IMU':  {'TCP': TCP_Command('10.0.0.20', 23)},
    'ROLL': {'TCP': TCP_Command('10.0.0.30', 23)},
}
