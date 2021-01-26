import bluetooth
import sys
import uuid
import threading
import time
from charts import *
from read_routine import *
from save_routine import *
from enum import Enum
class Status(Enum):
    STOP=0
    WORKING=1
    FINDPROBLEM=-1
    FINISHED=-2
    CONNECTING=2
class btConnection:
    def __init__(self,name="ACELEROMETROS",port=0x1001):
        self.name=name
        self.sock=None
        self.port = port
        self.status=Status.STOP
        self.t=None

    def dicover_devices(self,duration=3):

        print("performing inquiry...")
        nearby_devices = bluetooth.discover_devices(
            duration=duration, lookup_names=True, flush_cache=True, lookup_class=False)
        print (nearby_devices)
        
        print("found %d devices" % len(nearby_devices))
        return nearby_devices
        print ("no threads found")
        self.status=Status.FINDPROBLEM
        return None

    def __connect(self,addr):
        print (addr)
        
        
        # Create the client socket
        self.sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr, self.port))
        self.sock.settimeout(10)
        
        print("connected.  type stuff")
        try:
            self.sock.send("U".encode())
            self.status=Status.WORKING
        except:
            self.status=Status.FINISHED
        
        while True:
            try:
                f=open("../log/log_file",'ab')
                f.write(self.sock.recv(1))
                f.close()
                #ReadRoutine().sync(self.sock)
                #ReadRoutine().read_values(self.sock)
                #SaveRoutine().save_routine()
            except bluetooth.btcommon.BluetoothError:
                print ("exceção no bluetooth")
                self.sock.close()
                self.status=Status.FINISHED
                return -2

            except KeyboardInterrupt:
                print ("finalizando conexão...")
                self.sock.close()
                self.status=Status.FINISHED
                return 1
            
        self.sock.close()
        return 0

    def connect(self):
        
        nearby_devices=self.dicover_devices()
        try:
            print ("select device...")
            for i,name, in zip(range(len(nearby_devices)),nearby_devices):
                print (str(i)+": "+name[1])
            i=int(input())
            self.status=Status.CONNECTING
        except IndexError:
            return -1    
        addr=nearby_devices[i][0]
        
        self.t=threading.Thread(target=self.__connect,args=(addr,))
        self.t.start()

def test_sync_points(b):
    print (b.status)
    while b.status==Status.CONNECTING:
        time.sleep(0.01)

    print ("start test sync")    

    while b.status==Status.WORKING:
        time.sleep(0.1)
        ok=True
        n=len(ReadRoutine().sensors.rtc)
        for i in range (6):
                for j in range (3):
                    ok=ok and len(ReadRoutine().sensors.list_s[i].g[j]) == n
                    ok=ok and len(ReadRoutine().sensors.list_s[i].a[j]) == n
                    
        
        #if not ok:
        #    for i in range (6):
        #        for j in range (3):
        #            print ("a [{}][{}]".format(i,j),len(ReadRoutine().sensors.list_s[i].g[j]))
        #            print ("g [{}][{}]".format(i,j),len(ReadRoutine().sensors.list_s[i].a[j]))
        #    print ("rtc",len(ReadRoutine().sensors.rtc))
        

def test_graph(b):
    #print (b.status)
    while b.status==Status.CONNECTING:
        time.sleep(0.01)
    c=charts()
    time.sleep(1)
    #print (print (ReadRoutine().sensors.list_s[0].g))
    c.start_chart()
    c.update_chart()
    print ("start test sync")  

def test_save_routine(b):
    print (b.status)
    while b.status==Status.CONNECTING:
        time.sleep(0.01)

    
    SaveRoutine().start()
    time.sleep(1)
    SaveRoutine().stop()
    time.sleep(1)
    SaveRoutine().start()

def main():
    b=btConnection()
    k=b.connect()
    test_save_routine(b)
    #test_sync_points(b)
        #print (ReadRoutine().sensors.rtc,len(ReadRoutine().sensors.rtc)/(ReadRoutine().sensors.rtc[-1]-ReadRoutine().sensors.rtc[0]))

if __name__=="__main__":
    main()