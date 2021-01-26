"""
This file is part of the pyquaternion python module
Author:         Kieran Wynn
Website:        https://github.com/KieranWynn/pyquaternion
Documentation:  http://kieranwynn.github.io/pyquaternion/
Version:         1.0.0
License:         The MIT License (MIT)
Copyright (c) 2015 Kieran Wynn
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
demo.py - Demo of pyquaternion using matplotlib
"""

import numpy as np

from pyquaternion import Quaternion

# import matplotlib
# matplotlib.use('TKAgg')

from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from read_routine import *
from save_routine import *
import time
import threading


class Ob3D:
    def __init__(self):
        self.fig, self.ax, self.lines = self.setup()

    def init(self):
        for line in self.lines:
            line.set_data([], [])
            line.set_3d_properties([])

        return self.lines

    # animation function.  This will be called sequentially with the frame number

    def setup(self):
        fig = plt.figure()

        ax = fig.add_axes([0, 0, 1, 1], projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # prepare the axes limits
        ax.set_xlim((-1, 1))
        ax.set_ylim((-1, 1))
        ax.set_zlim((-1, 1))
        # set point-of-view: specified by (altitude degrees, azimuth degrees)
        ax.view_init(30, 0)
        # initialization function: plot the background of each frame
        # ax.axis('off')
        # use a different color for each axis
        colors = ['r', 'g', 'b']
        # set up lines and points
        lines = sum([ax.plot([], [], [], c=c)
                     for c in colors], [])

        return fig, ax, lines

    def animate(self, i):
        print(i)
        begin = time.time()
        # we'll step two time-steps per frame.  This leads to nice results.
        # i = (2 * i) % x_t.shape[1]

        startpoints = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        endpoints = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        while ReadRoutine().sensors[0].Q == []:
            print("esperando ...")
            time.sleep(0.1)
        q = Quaternion(ReadRoutine().sensors[0].Q[-1])
        # print("q:", q)

        for line, start, end in zip(self.lines, startpoints, endpoints):
            # end *= 5
            start = q.rotate(start)
            end = q.rotate(end)

            line.set_data([start[0], end[0]], [start[1], end[1]])
            line.set_3d_properties([start[2], end[2]])

            # pt.set_data(x[-1:], y[-1:])
            # pt.set_3d_properties(z[-1:])

        # ax.view_init(30, 0.6 * i)
        self.fig.canvas.draw()
        return self.lines

    def start(self):
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                       frames=500, interval=30, blit=False)

        plt.show()


def connect(addr):
    # print (addr)
    # Create the client socket
    # self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # self.sock.connect((addr, self.port))
    # self.sock.settimeout(10)
    try:
        ReadRoutine().connect(addr)
    except:
        print("impossible to connect")
    try:
        ReadRoutine().start()

    except:
        pass
    while True:
        try:
            ReadRoutine().read_values()
            SaveRoutine().save_routine()
        except bluetooth.btcommon.BluetoothError:
            # print ("exceção no bluetooth")
            ReadRoutine().close()

            return -2
        except KeyboardInterrupt:
            # print ("finalizando conexão...")
            ReadRoutine().close()
            return 1
    # sock.close()
    return 0


if __name__ == "__main__":
    obj = Ob3D()
    addr = ('192.168.0.110', 8001)

    t = threading.Thread(target=connect, args=(addr,))
    t.start()

    obj.start()
    # instantiate the animator.
