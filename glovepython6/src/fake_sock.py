import time
import sys
import threading
from read_routine import *
from charts import *
class FakeSock:
    def __init__(self,file):
        self.f=open(file,"rb")
        #self.content=f.read()
    
    def recv(self,n):
        time.sleep(0.0005)
        return self.f.read(n)

    def __connect(self,addr):
        while True:
            ReadRoutine().read_values(self)

    def connect(self):
        
        
        self.t=threading.Thread(target=self.__connect,args=("s"))
        self.t.start()

        c=charts()
        c.start_chart()
        c.update_chart()
    

if __name__=="__main__":
    fa=FakeSock("../log/log_file")
    fa.connect()
