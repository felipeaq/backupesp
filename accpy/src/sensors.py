from collections import deque
import numpy as np


class dequeSensor(deque):
    def __init__(self, iterable=(), maxlen=None):
        deque.__init__(self, iterable=iterable, maxlen=maxlen)
        self.real_len=0
        self.yffts = deque(maxlen=Sensors.MAX_FFT)
        self.xffts = deque(maxlen=Sensors.MAX_FFT)
        self.last_acc_rate=1

    def get_last_fft(self):
        if len(self.yffts)>0:
            return self.yffts[-1]
        return None
    def append(self,val):
        deque.append(self,val)
        self.real_len+=1

    def getxy(self,x):
        if not (len(self) < Sensors.MAX_X):
            delta_t = x[-1]-x[0]
            acc_rate = Sensors.MAX_X/delta_t
            self.last_acc_rate = acc_rate
        
        return np.array([list(x)[-len(self):],self])
    
    def getxyFFT(self,x):
        if len(self)<Sensors.MAX_X:
            return [0,0],[0,0]
        y=self.getFFT()
        
        delta_t=x[-1]-x[0]
        acc_rate=Sensors.MAX_X/delta_t
        self.last_acc_rate=acc_rate
        x = np.linspace(0.0, 1.0/(2.0*1/acc_rate), Sensors.MAX_X/2+1)
        self.xffts.append(x)
        self.yffts.append(y)
        x_new = np.mean(self.xffts, axis=0)
        y_new = np.mean(self.yffts, axis=0)
        return x_new[1:], y_new[1:]
        

    def getFFT(self):
        if len(self)<Sensors.MAX_X:
            return np.fft.fft([0,0])
        else:
            fft = np.fft.rfft(self)
            X = np.sqrt(fft.real**2+fft.imag**2)/(Sensors.MAX_X/2)
            X[0] /= 2
            X[-1] /= 2
            return X

    def get_real_FFT(self):
        v=self.getFFT()
        return np.concatenate((v.imag,v.real))

class Sensors:
    TOTAL_S=6
    TOTAL_P=6
    TO_RAD = 10430.3783505
    RESIST = 16384
    MAX_X = 2048
    MAX_FFT = 10
    def __init__(self,maxlen):
        
        self.a=[]
       
        for i in range (Sensors.TOTAL_P//2):
            self.a.append(dequeSensor(maxlen=maxlen))
    
    def append(self,a):
        for p,d in zip(a,self.a):
            d.append(p/Sensors.RESIST)
      
    def __repr__(self):
        return "\nax1: {}\n ax2: {}\n ax3: {}\n".format(
            self.a[0],self.a[1],self.a[2]
        )

class SensorsSet():
    def __init__(self,ns,maxlen):
        self.list_s=[]
        self.dic_s={}
        for i in range(ns):
            sensor=Sensors(maxlen)
            self.list_s.append(sensor)
            self.dic_s["sensor"+str(i+1)]=sensor
        self.rtc=dequeSensor(maxlen=maxlen)

    def __repr__(self):
        s=""
        for i in self.dic_s.items():
            s+=str(i)+"\n"
        s+="('rtc', "+str(self.rtc)+")"+"\n"
        return s

    def append_at(self,i,a):
        self.list_s[i].append(a)


    
def main():
    s1=SensorsSet(6,Sensors.MAX_X)
    s1.append_at(2,[1,2,3])


if __name__=="__main__":
    main()

