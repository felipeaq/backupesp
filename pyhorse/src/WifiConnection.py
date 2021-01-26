import sys
import uuid
import threading
import time
from read_routine import *
from save_routine import *
from enum import Enum


from PyQt5 import QtWidgets
from INTERFACE_choose_app import Ui_MainWindow as ChooseAppWindow


class Status(Enum):
    STOP = 0
    WORKING = 1
    FINDPROBLEM = -1
    FINISHED = -2
    CONNECTING = 2


class WifiConnection:
    def __init__(self, name="ACELEROMETROS", port=8001):
        self.name = name
        self.sock = None
        self.port = port
        self.status = Status.STOP
        self.t = None

    def __connect(self, addr):
        # try:
        reader = ReadRoutine().add_connection(addr)
        # except:
        #    print("impossible to connect")
        #   return
        try:
            reader.start()
            self.status = Status.WORKING
        except:
            print("impossible to send")
            self.status = Status.FINISHED

        while True:
            try:

                reader.read_values()
                # reader.save_routine()

            except KeyboardInterrupt:
                # print ("finalizando conexão...")
                reader.close()
                self.status = Status.FINISHED
                return 1

        self.sock.close()
        return 0

    def wifiConnect(self, ips):

        for ip in ips:

            addr = (ip, 8001)
            self.t = threading.Thread(target=self.__connect, args=(addr,))
            self.t.start()

        return 0


if __name__ == "__main__":
    w = WifiConnection()
    print("a")
    w.wifiConnect(["192.168.0.101"])
    print("b")
    time.sleep(1)
    print("c")
    while True:
        print(ReadRoutine().readers[0].sensors.a)
