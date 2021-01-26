import bluetooth
import sys
import uuid
import threading
import time
from charts import *
from read_routine import *
from save_routine import *
from enum import Enum
from kpredictor import *

from PyQt5 import QtWidgets
from INTERFACE_choose_app import Ui_MainWindow as ChooseAppWindow


class Status(Enum):
    STOP = 0
    WORKING = 1
    FINDPROBLEM = -1
    FINISHED = -2
    CONNECTING = 2


class btConnection:
    def __init__(self, name="ACELEROMETROS", port=0x1001):
        self.name = name
        self.sock = None
        self.port = port
        self.status = Status.STOP
        self.t = None

    def close(self, bluetooth_devices_window):
        bluetooth_devices_window.close()

    def dicover_devices(self, duration=3):

        #print("performing inquiry...")
        nearby_devices = bluetooth.discover_devices(
            duration=duration, lookup_names=True, flush_cache=True, lookup_class=False)
        #print (nearby_devices)

        #print("found %d devices" % len(nearby_devices))
        return nearby_devices

    def __connect(self, addr):
        #print (addr)

        # Create the client socket
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr, self.port))
        self.sock.settimeout(10)

        #print("connected.  type stuff")
        try:
            self.sock.send("U".encode())
            self.status = Status.WORKING
        except:
            self.status = Status.FINISHED

        while True:
            try:
                # ReadRoutine().sync(self.sock)
                ReadRoutine().read_values(self.sock)
                SaveRoutine().save_routine()
            except bluetooth.btcommon.BluetoothError:
                #print ("exceção no bluetooth")
                self.sock.close()
                self.status = Status.FINISHED
                return -2

            except KeyboardInterrupt:
                #print ("finalizando conexão...")
                self.sock.close()
                self.status = Status.FINISHED
                return 1

        self.sock.close()
        return 0

    def connect(self, addr):
        #print (addr)

        # Create the client socket
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr, self.port))
        self.sock.settimeout(10)

        #print("connected.  type stuff")
        try:
            self.sock.send("U".encode())
            self.status = Status.WORKING
        except:
            self.status = Status.FINISHED

        return self.sock

    def connect_bt(self, list_devices, name, bluetooth_devices_window, home_window, screen_size):
        # print(self)
        # print(list_devices)
        # print(name)
        # nearby_devices=self.dicover_devices()
        try:
            #print ("select device...")
            for i, name_local, in zip(range(len(list_devices)), list_devices):
                #print(i, name_local[1], name, name_local == name)
                if name_local[1] == name:
                    break

            # i=int(input())
            self.status = Status.CONNECTING
        except IndexError:
            return -1
        addr = list_devices[i][0]
        self.t = threading.Thread(target=self.__connect, args=(addr,))
        self.t.start()
        self.close(bluetooth_devices_window)

        self.close(home_window)

        self.window = QtWidgets.QMainWindow()
        choose = ChooseAppWindow()
        choose.setupUi(self.window, screen_size)
        self.window.show()
        return 0


def test_sync_points(b):
    #print (b.status)
    while b.status == Status.CONNECTING:
        time.sleep(0.01)

    #print ("start test sync")

    while b.status == Status.WORKING:
        time.sleep(0.1)
        ok = True
        n = len(ReadRoutine().sensors.rtc)
        for i in range(6):
            for j in range(3):
                #ok=ok and len(ReadRoutine().sensors.list_s[i].g[j]) == n
                ok = ok and len(ReadRoutine().sensors.list_s[i].a[j]) == n

        # if not ok:
        #    for i in range (6):
        #        for j in range (3):
        #            #print ("a [{}][{}]".format(i,j),len(ReadRoutine().sensors.list_s[i].g[j]))
                #print ("g [{}][{}]".format(i,j),len(ReadRoutine().sensors.list_s[i].a[j]))
            #print ("rtc",len(ReadRoutine().sensors.rtc))


def test_graph(b):
    #print (b.status)
    while b.status == Status.CONNECTING:
        time.sleep(0.01)
    SaveRoutine().start()
    c = charts()
    time.sleep(1)
    #print (print (ReadRoutine().sensors.list_s[0].g))
    c.start_chart()
    c.update_chart()
    #print ("start test sync")


def test_save_routine(b):
    #print (b.status)
    while b.status == Status.CONNECTING:
        time.sleep(0.01)

    c = charts()
    x = input("valor")
    SaveRoutine().start(x)
    #print ("a")
    c.start_chart()
    #print ("b")
    c.update_chart()
    #print ("c")


def test_acsition(b):
    while b.status == Status.CONNECTING:
        time.sleep(0.01)

    #print ("start test sync")
    time.sleep(1)
    # start=ReadRoutine().sensors.rtc[0]
    # while b.status==Status.WORKING:
    #    print (len(ReadRoutine().sensors.rtc)/(ReadRoutine().sensors.rtc[-1]-ReadRoutine().sensors.rtc[0]))


def test_kpred(b):
    while True:
        time.sleep(0.1)
        if len(ReadRoutine().sensors.list_s[0].a[1]) >= Sensors.MAX_X:
            KPredictior().append_predict(
                ReadRoutine().sensors.list_s[0].a[1].get_real_FFT())
            #print (KPredictior().values)
        else:
            print("dsada")


def main():
    b = btConnection()
    list_devices = b.dicover_devices()
    b.connect_bt(list_devices, "ACELEROMETROS", open("gambiarra_close", "w"))
    test_save_routine(b)
    # test_acsition(b)


if __name__ == "__main__":
    main()
