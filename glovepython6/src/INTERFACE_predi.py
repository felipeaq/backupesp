# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'predi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

# main import for the QT window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox
# imports to the graph works with the QT window
import sys
import time
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure

# imports to update the graph with the data from sensors
import os
import threading
from kpredictor import *
from read_routine import *
from save_routine import *

# import to the slide window of the canvas work
from collections import deque

from demo import *  # TODO remover


class Ui_MainWindow(object):

    def setupUi(self, MainWindow, screen_size):

        # Graphs settings
        self.firstChange = True
        self.list_canvas = []
        # list_toolbar = []
        list_dynamic_canvas = []
        self.list__dynamic_ax = []
        self.min_fft = [0, 0, 0]
        self.max_fft = [0, 0, 0]
        self.min_axis = [0, 0, 0, 0, 0, 0]
        self.max_axis = [0, 0, 0, 0, 0, 0]
        self.gap = [0, 8]

        # Save button settings
        self.state_button = True

        MainWindow.setObjectName("MainWindow")
        max_height = screen_size.height() * 0.93
        MainWindow.resize(screen_size.width(), max_height)
        MainWindow.setStyleSheet("background-color: rgb(255,255,255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Graphs first configurations
        for i in range(6):

            self.list_canvas.append(QtWidgets.QVBoxLayout())
            self.list_canvas[i].setObjectName("canvas"+str(i))

            list_dynamic_canvas.append(
                FigureCanvas(Figure(figsize=(8, 2), dpi=90)))

            # list_toolbar.append(NavigationToolbar2QT(list_dynamic_canvas[i], MainWindow))
            # self.list_canvas[i].addWidget(list_toolbar[i])

            self.list_canvas[i].addWidget(list_dynamic_canvas[i])
            self.list__dynamic_ax.append(
                list_dynamic_canvas[i].figure.subplots())
            self._timer = list_dynamic_canvas[i].new_timer(
                0.01, [(self._update_canvas, (), {})])

        for i in range(3):
            pass
        for i in range(3, 6):
            self.list__dynamic_ax[i].set_ylim(
                [-Sensors.MAX_Y_ACC, Sensors.MAX_Y_ACC])

        self._timer.start()

        # Setting the layout of the lateral menu
        w = screen_size.width() * 0.14
        self.lateralMenuLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.lateralMenuLayoutWidget.setGeometry(
            QtCore.QRect(screen_size.width() * 0.005, 1, w, max_height))
        self.lateralMenuLayoutWidget.setObjectName("lateralMenuLayoutWidget")
        self.lateralMenuLayout = QtWidgets.QVBoxLayout(
            self.lateralMenuLayoutWidget)
        self.lateralMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.lateralMenuLayout.setObjectName("lateralMenuLayout")

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem)

        # chart settings
        self.cb = []
        for i in range(6):
            cb = QCheckBox('Sensor '+str(i+1),
                           self.lateralMenuLayoutWidget)

            self.cb.append(cb)
            self.cb[i].move(20, 30+i*20)
            self.cb[i].toggle()
        # cb.stateChanged.connect(self.changeTitle)

        # INPUT section
        self.txtlineLayout = QtWidgets.QHBoxLayout()
        self.txtlineLayout.setObjectName("txtlineLayout")

        self.txtlineLayout2 = QtWidgets.QHBoxLayout()
        self.txtlineLayout2.setObjectName("txtlineLayout2")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")

        self.txt_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        self.txt_label.setObjectName("txt_label")

        self.txtlineLayout.addWidget(self.txt_label)
        self.txtlineLayout2.addWidget(self.textEdit)

        self.lateralMenuLayout.addLayout(self.txtlineLayout)
        self.lateralMenuLayout.addLayout(self.txtlineLayout2)

        # SAVE section
        self.savelineLayout = QtWidgets.QHBoxLayout()
        self.savelineLayout.setObjectName("savelineLayout")

        self.save_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.save_label.setFont(font)
        self.save_label.setObjectName("save_label")

        self.save_button = QtWidgets.QPushButton(self.lateralMenuLayoutWidget)
        self.save_button.setObjectName("save_button")
        self.save_button.setStyleSheet("background-color: rgb(0, 255, 0);")

        self.savelineLayout.addWidget(self.save_label)
        self.savelineLayout.addWidget(self.save_button)

        self.lateralMenuLayout.addLayout(self.savelineLayout)

        def save():
            if self.state_button == True:
                self.state_button = False
                self.changetoSTOP()
                textboxValue = self.textEdit.toPlainText()
                SaveRoutine().start(textboxValue)
                self.textEdit.clear()
            else:
                self.state_button = True
                self.changetoSTART()
                SaveRoutine().stop()

        self.save_button.clicked.connect(save)

        spacerItemSave = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItemSave)

        #######################################################################################################
        # Graphs things
        w = screen_size.width() * 0.85
        w_ini = screen_size.width() * 0.15
        h = max_height * 0.33

        self.firstLineLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.firstLineLayoutWidget.setGeometry(QtCore.QRect(w_ini, 1, w, h))
        self.firstLineLayoutWidget.setObjectName("firstLineLayoutWidget")
        self.firstLineLayout = QtWidgets.QHBoxLayout(
            self.firstLineLayoutWidget)
        self.firstLineLayout.setContentsMargins(0, 0, 0, 0)
        self.firstLineLayout.setObjectName("firstLineLayout")

        self.secondLineLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.secondLineLayoutWidget.setGeometry(
            QtCore.QRect(w_ini, h + 1, w, h))
        self.secondLineLayoutWidget.setObjectName("secondLineLayoutWidget")
        self.secondLineLayout = QtWidgets.QHBoxLayout(
            self.secondLineLayoutWidget)
        self.secondLineLayout.setContentsMargins(0, 0, 0, 0)
        self.secondLineLayout.setObjectName("secondLineLayout")

        self.thirdLineLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.thirdLineLayoutWidget.setGeometry(
            QtCore.QRect(w_ini, h * 2, w, h))
        self.thirdLineLayoutWidget.setObjectName("thirdLineLayoutWidget")
        self.thirdLineLayout = QtWidgets.QHBoxLayout(
            self.thirdLineLayoutWidget)
        self.thirdLineLayout.setContentsMargins(0, 0, 0, 0)
        self.thirdLineLayout.setObjectName("thirdLineLayout")

        self.firstLineLayout.addLayout(self.list_canvas[0])
        self.firstLineLayout.addLayout(self.list_canvas[3])
        self.secondLineLayout.addLayout(self.list_canvas[1])
        self.secondLineLayout.addLayout(self.list_canvas[4])
        self.thirdLineLayout.addLayout(self.list_canvas[2])
        self.thirdLineLayout.addLayout(self.list_canvas[5])

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 58, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _update_canvas(self):
        for i in range(6):
            self.list__dynamic_ax[i].clear()

        for i in range(6):
            if self.cb[i].isChecked():
                t1, gx = ReadRoutine().sensors.getXY(i, "gyroRad0")
                t2, gy = ReadRoutine().sensors.getXY(i, "gyroRad1")
                t3, gz = ReadRoutine().sensors.getXY(i, "gyroRad2")
                t4, ax = ReadRoutine().sensors.getXY(i, "accGravity0")
                t5, ay = ReadRoutine().sensors.getXY(i, "accGravity1")
                t6, az = ReadRoutine().sensors.getXY(i, "accGravity2")

                # print(np.diff(t6))
                # print("mean={}, std={}".format(np.mean(np.diff(t6)), np.std(np.diff(t6))))
                if len(t4) != 0:
                    if t4[-1] >= self.gap[1]:
                        self.gap[0] = int(ReadRoutine().sensors.rtc[0])
                        self.gap[1] = int(ReadRoutine().sensors.rtc[-1])

                self.list__dynamic_ax[0].plot(t1, gx)
                self.list__dynamic_ax[0].set_ylabel('X gyroscope')
                self.list__dynamic_ax[1].plot(t2, gy)
                self.list__dynamic_ax[1].set_ylabel('Y gyroscope')
                self.list__dynamic_ax[2].plot(t3, gz)
                self.list__dynamic_ax[2].set_ylabel('Z gyroscope')

                self.list__dynamic_ax[3].plot(t4, ax)
                self.list__dynamic_ax[3].set_ylabel('X accelerometer')
                self.list__dynamic_ax[4].plot(t5, ay)
                self.list__dynamic_ax[4].set_ylabel('Y accelerometer')
                self.list__dynamic_ax[5].plot(t6, az)
                self.list__dynamic_ax[5].set_ylabel('Z accelerometer')

        list_ylim = [Sensors.MAX_Y_GYRO] * 3 + [Sensors.MAX_Y_ACC]*3
        for i in range(6):
            self.list__dynamic_ax[i].set_xlim([self.gap[0], self.gap[1]])
            self.list__dynamic_ax[i].set_ylim([-list_ylim[i], list_ylim[i]])
            self.list__dynamic_ax[i].figure.canvas.draw()

    def changetoSTART(self):
        self.save_button.setText("START")
        self.save_button.setStyleSheet("background-color: rgb(0, 255, 0);")

    def changetoSTOP(self):
        self.save_button.setText("STOP")
        self.save_button.setStyleSheet("background-color: rgb(255, 0, 0);")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.save_label.setText(_translate("MainWindow", "Press to: "))
        self.save_button.setText(_translate("MainWindow", "SAVE"))

        self.txt_label.setText(_translate("MainWindow", "Insert a name"))
