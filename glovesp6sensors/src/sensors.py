from collections import deque
import numpy as np
import struct
import ahrs
import time


class Sensors:
    TOTAL_S = 6
    TOTAL_P = 6
    GMAX = 2
    TO_DPS = 65.536
    TESLA = 1  # TODO
    RESIST = (2**(16-1))/GMAX
    MAX_Y_ACC = (2**(16-1))/RESIST
    MAX_Y_GYRO = (2**(16-1))/TO_DPS
    MAX_Y_MAG = 400
    MAX_X = 32768
    MAX_FFT = 10
    AXIS = 3
    WINDOWS_SIZE = 166
    WINDOW_SOCK_SIZE = WINDOWS_SIZE*TOTAL_S
    WINDOW_N_SIZE = 10
    STEP = 16
    STEPMAG = STEP+3*2
    def __init__(self, maxlen):

        self.a = []
        self.g = []
        self.m = []
        self.pitch = deque(maxlen=maxlen)
        self.roll = deque(maxlen=maxlen)
        self.yaw = deque(maxlen=maxlen)
        self.last_mag = [0, 0, 0]
        self.rtc = deque(maxlen=maxlen)
        self.Q = deque(maxlen=maxlen)
        self.Q.append([1., 0., 0., 0.])
        self.madgwick = ahrs.filters.Madgwick()
        self.accGravity = []
        self.gyroRad = []
        self.magNorm = []
        self.ref = {}
        self.ref["pitch"] = self.pitch
        self.ref["roll"] = self.roll
        self.ref["yaw"] = self.yaw
        for i in range(Sensors.AXIS):
            self.a.append(deque(maxlen=maxlen))
            self.g.append(deque(maxlen=maxlen))
            self.m.append(deque(maxlen=maxlen//10))
            self.accGravity.append(deque(maxlen=maxlen))
            self.gyroRad.append(deque(maxlen=maxlen))
            self.magNorm.append(deque(maxlen=maxlen//10))
            self.ref["a{}".format(i)] = self.a[-1]
            self.ref["g{}".format(i)] = self.g[-1]
            self.ref["accGravity{}".format(i)] = self.accGravity[-1]
            self.ref["gyroRad{}".format(i)] = self.gyroRad[-1]
            self.ref["magNorm{}".format(i)] = self.magNorm[-1]

    def shortToLong(self, shortInt):
        longInt = 0
        for i in range(len(shortInt)):
            mult = 256 ** i
            longInt += shortInt[i] * mult
        return longInt

    def append(self, timeRtc,  accLocal,  gyroLocal, magLocal):
        self.rtc.append(timeRtc/10)

        for i in range(Sensors.AXIS):
            self.a[i].append(accLocal[i])
            self.g[i].append(gyroLocal[i])
            self.accGravity[i].append(accLocal[i] / Sensors.RESIST)
            self.gyroRad[i].append(gyroLocal[i] / Sensors.TO_DPS)
            if magLocal:
                self.m[i].append(magLocal[i])
                self.magNorm[i].append(magLocal[i] / Sensors.TESLA)

        if magLocal:
            self.last_mag = magLocal

        self.Q.append(self.madgwick.updateMARG(
            self.Q[-1], ahrs.common.DEG2RAD * (np.array(gyroLocal)/Sensors.TO_DPS), accLocal, self.last_mag))
        angles = ahrs.common.Quaternion(
            self.Q[-1]).to_angles()*ahrs.common.RAD2DEG
        self.pitch.append(angles[0])
        self.roll.append(angles[1])
        self.yaw.append(angles[2])

    def getXY(self, sensor):
        y = list(self.ref[sensor])
        if "mag" in sensor:
            x = [self.rtc[i] for i in range(0, len(self.rtc), 10)]
        else:
            x = self.rtc
        x = list(x)[0:len(y)]
        return x, y

    def getAxis(self, ax):
        if ax == "x":
            pass
        if ax == "y":
            pass
        if ax == "z":
            pass
        return 0

    def getHip(self, x, y):
        return np.sqrt(x**2+y**2)

    def getXaxis(self):
        '''returns acrsin(y/hip) where hip = sqrt(y²+z²)'''
        z, y = self.a[2][-1], self.a[1][-1]
        return self.getAngle(z, y)

    def getYaxis(self):
        '''returns acrsin(z/hip) where hip = sqrt(z²+x²)'''
        x, z = self.a[0][-1], self.a[2][-1]
        return self.getAngle(z, x)

    def getAngle(self, xi1, xi2):
        hip = self.getHip(xi1, xi2)
        return np.rad2deg(np.arcsin(xi2/hip))

    def appendFromSliced(self, v, mag=False):
        time = self.shortToLong(v[0:4])

        accLocal = []
        gyroLocal = []
        magLocal = []

        for i in range(Sensors.AXIS):
            accLocal.append(struct.unpack(
                "<h", v[4 + 2 * i: 4 + 2 * i + 2])[0])
            gyroLocal.append(struct.unpack(
                "<h", v[10 + 2 * i: 10 + 2 * i + 2])[0])
            if mag:
                magLocal.append(struct.unpack(
                    "<h", v[16 + 2 * i: 16 + 2 * i + 2])[0])

        self.append(time, accLocal, gyroLocal, magLocal)

    def appendFromWindow(self, v):

        start = 0
        index = 0

        while start < Sensors.WINDOWS_SIZE - Sensors.STEP+1:

            if index == 0:

                self.appendFromSliced(
                    v[start: start + Sensors.STEPMAG], mag=True)
                start += Sensors.STEPMAG
            else:
                self.appendFromSliced(v[start: start + Sensors.STEP])
                start += Sensors.STEP

            index = (index+1) % 10

    def __repr__(self):
        return "\nax1: {}\n ax2: {}\n ax3: {}\n".format(
            self.a[0], self.a[1], self.a[2]
        )


class SensorsSet(list):
    def __init__(self, n_sensor, max_len):
        for i in range(n_sensor):
            self.append(Sensors(max_len))

    def add(self, data):
        for i in range(len(self)):
            start, end = i*Sensors.WINDOWS_SIZE, (i+1)*Sensors.WINDOWS_SIZE
            self[i].appendFromWindow(data[start:end])


def main():
    s1 = SensorsSet(6, Sensors.MAX_X)
    s1.append_at(2, [1, 2, 3])


if __name__ == "__main__":
    main()
