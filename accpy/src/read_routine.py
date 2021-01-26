from sensors import *

class ReadRoutine(object):
    __instance = None
    def __new__(cls):
        if ReadRoutine.__instance is None:
            total_s=6
            ReadRoutine.__instance = object.__new__(cls)
            ReadRoutine.__instance.sensors=SensorsSet(total_s,Sensors.MAX_X)
            ReadRoutine.__instance.cycle_past=0
            ReadRoutine.__instance.n_s=6
            ReadRoutine.__instance.active_sensors=[False]*total_s
            ReadRoutine.__instance.sensor_pos=[]
            ReadRoutine.__instance.FRTC=32768.0
            
        return ReadRoutine.__instance

    def sync(self,sock):
        sync_sensor=False

        while not sync_sensor:
            #print ("a")
            cod1 =int.from_bytes(sock.recv(1),"little")
            #print ("cod1:"+str(cod1))
            if cod1==255:
                
                cod2=int.from_bytes(sock.recv(1),"little")
                #print ("cod2:"+str(cod2))
                if (cod2 == 127 or cod2==255):
                    sync_sensor=True
                    if cod2==255:
                        cod3=int.from_bytes(sock.recv(1),"little")
                        #print ("cod3:"+str(cod3))
                        if cod3!=127:
                            sync_sensor=False
                    

    def read_values(self,sock):
        
        active_sensors = [False]*self.n_s
        n_s=int.from_bytes(sock.recv(1),"little")
        sock.recv(1)#garbage    
        rtc=int.from_bytes(sock.recv(1)+sock.recv(1),"little")
        buffer=[]

        sensor_pos=[]

        for i in range(n_s):

            pos=int.from_bytes(sock.recv(1),"little")-1
            sock.recv(1) #garbage
            
            if (pos>=6 or pos<0):
                print("erro na sincronização lido posição:",pos,i)
                
                return
            
            active_sensors[pos]=True
            sensor_pos.append(pos)
            buffer.append([])
            for j in range (3): 
                buffer[i].append(int.from_bytes(sock.recv(1)+sock.recv(1),"little",signed=True))
        self.update_time(rtc)
        for i in range (n_s):
            #g=buffer[i][0:3]
            a=buffer[i][0:3]
            self.sensors.list_s[sensor_pos[i]].append(a)
        
        self.active_sensors=active_sensors
        self.sensor_pos=sensor_pos
        #print (self.active_sensors)
        
    def update_time(self,cycle):
        
        deltaCycle=0
        if (cycle>=self.cycle_past):
            delta_cycle=cycle-self.cycle_past
        else:
            delta_cycle=2**16-self.cycle_past+cycle
        
        delta_time=delta_cycle/self.FRTC
        
        if not self.sensors.rtc:
            self.sensors.rtc.append(delta_time)
        else:
            self.sensors.rtc.append(delta_time+self.sensors.rtc[-1])
        self.cycle_past=cycle
        


def main():
    
    ReadRoutine().read_values("a")
    ReadRoutine().update_time(2)
    ReadRoutine().update_time(4)
    ReadRoutine().update_time(2**15-1)
    ReadRoutine().update_time(1)
    #print (ReadRoutine().sensors)



if __name__=="__main__":
    main()
