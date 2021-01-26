from sensors import *
import socket
import traceback
import sys
import numpy as np
import time
from resources import *


class ReadRoutine(object):
    __instance = None

    def __new__(cls):

        if ReadRoutine.__instance is None:
            ReadRoutine.__instance = object.__new__(cls)
            ReadRoutine.__instance.readers = []

        return ReadRoutine.__instance

    def add_connection(self, dest):
        reader = Reader()
        self.readers.append(reader)
        reader.connect(dest)
        return reader

    def close_at(self, i):
        self.readers[i].close()

    def read_values_at(self, i):
        self.readers[i].read_values()


class Reader:
    def __init__(self):
        self.sensors = Sensors(Sensors.MAX_X)
        self.sock = None

    def read_values(self):

        data = self.sock.recv(Sensors.WINDOWS_SIZE)
        while (len(data) != Sensors.WINDOWS_SIZE):
            data += self.sock.recv(Sensors.WINDOWS_SIZE-len(data))
        self.sensors.appendFromWindow(data)
        def get_bin(x, n): return format(x, 'b').zfill(n).replace("-", "1")

        # print(get_bin(self.sensors.a[0][-1], 16), get_bin(self.sensors.a[1]
        #                                                  [-1], 16), get_bin(self.sensors.a[2][-1], 16))

        #print(self.sensors.a[0][-1], self.sensors.a[1]
        #      [-1], self.sensors.a[2][-1])

       # print(np.sqrt(self.sensors.accGravity[0][-1]**2 + self.sensors.accGravity[1][-1]**2
        #           + self.sensors.accGravity[2][-1])**2)

    def connect(self, dest):
        # print("connecting...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(dest)

    def start(self):
        self.sock.send("start".encode())

    def close(self):
        self.sock.close()


def main():
    print(1)
    HOST = Resources().loadip()     # Endereco IP do Servidor
    PORT = 8001            # Porta que o Servidor esta
    ReadRoutine().connect((HOST, PORT))
    ReadRoutine().start()

    while True:
        try:

            ReadRoutine().read_values()
            print(ReadRoutine().sensors.rtc[-1])

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)

            sock.close()
            break


if __name__ == "__main__":
    main()
