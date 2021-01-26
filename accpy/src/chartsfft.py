import matplotlib.pyplot as plt
import numpy as np
import time
from read_routine import *
from sensors import *
import random

class charts:
    def __init__(self):
        self.fig,self.ax = plt.subplots(2,3)
        self.la=[]
        self.lg=[]

    def start_chart(self):
        #TODO verificar se os tamanhos de x e y são iguais
        #for j in range (3):
        #    self.lg.append([])
        #    for i in range (1):
        #        
        #        l,=self.ax[0][j].plot(ReadRoutine().sensors.rtc,ReadRoutine().sensors.list_s[i].g[j])
        #        self.lg[j].append(l)
        #    self.ax[0][j].relim()
        #    self.ax[0][j].set_ylim(-(2**15/Sensors.TO_RAD*1.1),(2**15/Sensors.TO_RAD*1.1))
        #    self.ax[0][j].set_xlim(0,50)
        #    self.ax[0][j].autoscale_view(True,True,True)
            
        

        for j in range (3):
            self.la.append([])
            for i in range(1):
                x, y = ReadRoutine().sensors.list_s[i].a[j].getxyFFT()
                
                l1,=self.ax[1][j].plot(x.real,y.real)
                l2, = self.ax[1][j].plot(x.imag, y.imag)
                self.la[j].append(l1)
                self.la[j].append(l2)
            self.ax[1][j].relim()
            self.ax[1][j].set_ylim(-100,100)
            self.ax[1][j].set_xlim(-1,1)
            self.ax[1][j].autoscale_view(True,True,True)

        
        self.fig.canvas.draw()
        plt.show(block=False)


    def update_chart(self):
        while len(ReadRoutine().sensors.rtc)<2:
            time.sleep(0.01)
        #print (len(ReadRoutine().sensors.rtc))
        while True:
            try:
                self.__update_chart()
                self.fig.canvas.draw()
                plt.pause(0.03)
            except KeyboardInterrupt:
                break

    def __update_chart(self):
        #TODO verificar se os tamanhos de x e y são iguais
        
        #for j in range (3):
        #    for i in range (1):
        #        if ReadRoutine().active_sensors[i]:
        #            self.lg[j][i].set_xdata(ReadRoutine().sensors.rtc)
        #            self.lg[j][i].set_ydata(ReadRoutine().sensors.list_s[i].g[j])
        #    self.ax[0][j].set_xlim(ReadRoutine().sensors.rtc[0],ReadRoutine().sensors.rtc[-1])
        
        for j in range (3):
            for i in range (1):
                if ReadRoutine().active_sensors[i]:
                    x, y = ReadRoutine().sensors.list_s[i].a[j].getxyFFT()
                    self.la[j][i].set_xdata(x.real)
                    self.la[j][i].set_ydata(y.real)
                    self.la[j][i+1].set_xdata(x.imag)
                    self.la[j][i+1].set_ydata(y.imag)
            #self.ax[1][j].set_xlim(ReadRoutine().sensors.rtc[0],ReadRoutine().sensors.rtc[-1])


def main():

    fig,ax = plt.subplots(2,3)
    #ax = fig.add_subplot(111)

    # some X and Y data
    x = deque(maxlen=1000)
    y = deque(maxlen=1000)
    y2=deque(maxlen=1000)
    la, =ax[0][0].plot(x,y)
    li, = ax[0][1].plot(x, y2)

    # draw and show it
    ax[0][0].relim() 
    ax[0][0].set_ylim(-3,3)
    ax[0][0].set_xlim(0,1000)
    ax[0][1].relim() 
    ax[0][1].autoscale_view(True,True,True)
    fig.canvas.draw()
    plt.show(block=False)
    i=0

    # loop to update the data
    while True:
        try:
            y.append(random.random())
            y2.append(random.random())
            x.append(i)
            #y[-10:] = np.random.randn(10)
            #y2[:-10] = y2[10:]
            #y2[-10:] = np.random.randn(10)

            # set the new data
            li.set_ydata(y)
            li.set_xdata(x)
            la.set_ydata(y2)
            la.set_xdata(x)
            fig.canvas.draw()
            print ("a")
            plt.pause(0.03)
            i+=1
        except KeyboardInterrupt:
            break
