import pickle
from collections import deque
import numpy as np
from sensors import *
from sympy import integrate
class VibrationDose():
    __instance = None
    def __init__(self, last_time, x, y, z):
        self.last_time = 0
        self.total = 0
        self.amr = []
        self.arep = 0
        self.are = 0
        self.aren = 0
        if len(last_time) > 0:
        
            self.total = 0
            self.last_time = last_time[-1]
            self.startx = x[-1]
            self.starty = y[-1]
            self.startz = z[-1]
            
    def sum_vibration(self, time, x, y, z, time_worked, n_repeated_action, time_experience):

        dtime = time[-1] - self.last_time
        st0_x = 0
        st0_y = 0
        st0_z = 0
        
        #for i in range(2, 22):
        #    print("X:" + str(x[i]))
        #    print("Y:" + str(y[i]))
        #    print("Z:" + str(z[i]))
        for i in x:
            #i = i * 9.8
            st0_x += i**2
        st1_x = st0_x / len(x)
        st2_x = st1_x / dtime
        rms_x = np.sqrt(st2_x)

        for i in y:
            #i = i * 9.8
            st0_y += i**2
        st1_y = st0_y / len(y)
        st2_y = st1_y / dtime
        rms_y = np.sqrt(st2_y)

        for i in z:
            #i = i * 9.8
            st0_z = i ** 2
        st1_z = st0_z / len(z)
        st2_z = st1_z / dtime
        rms_z = np.sqrt(st2_z)

        
        #self.total = (rms_x + rms_y + rms_z) / 3
        self.amr.append(np.sqrt((rms_x ** 2) + (rms_y ** 2) + (rms_z ** 2)))
        if len(self.amr) == 40:
            for i in self.amr:
                self.arep += i
            self.arep = self.arep / len(self.amr)
            print("AREP : " + str(self.arep))
            self.are = np.sqrt((n_repeated_action * (self.arep ** 2) * time_experience) / time_worked)
            print("ARE : " + str(self.are))
            self.aren = self.are * np.sqrt(time_worked / 480)
            print("AREN : " + str(self.aren))
            self.amr.clear()

        self.last_time = time[-1]

    def get_total(self):
        if self.aren >= 60:
            return 60
        return self.aren
        
    
