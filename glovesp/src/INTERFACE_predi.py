# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'predi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

# main import for the QT window
from PyQt5 import QtCore, QtGui, QtWidgets

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

        # CORRECT probability line
        self.line0Layout = QtWidgets.QHBoxLayout()
        self.line0Layout.setObjectName("line0Layout")

        self.correct_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        # self.correct_label.setGeometry(QtCore.QRect(
        #    w * 0.1, max_height * 0.02, w * 0.4, max_height * 0.02))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(66)
        self.correct_label.setFont(font)
        self.correct_label.setObjectName("correct_label")

        self.prob_correct_value = QtWidgets.QLabel(
            self.lateralMenuLayoutWidget)
        # self.prob_correct_value.setGeometry(QtCore.QRect(
        #    w * 0.5, max_height * 0.02, w * 0.4, max_height * 0.04))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(70)
        self.prob_correct_value.setFont(font)
        self.prob_correct_value.setObjectName("prob_correct_value")

        self.line0Layout.addWidget(self.correct_label)
        self.line0Layout.addWidget(self.prob_correct_value)

        self.lateralMenuLayout.addLayout(self.line0Layout)

        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem2)

        # unbalance probability line
        self.line1Layout = QtWidgets.QHBoxLayout()
        self.line1Layout.setObjectName("line1Layout")

        self.unbalance_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        # self.unbalance_label.setGeometry(QtCore.QRect(
        #    w * 0.1, max_height * 0.02, w * 0.4, max_height * 0.02))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(66)
        self.unbalance_label.setFont(font)
        self.unbalance_label.setObjectName("unbalance_label")

        self.prob_unbalance_value = QtWidgets.QLabel(
            self.lateralMenuLayoutWidget)
        # self.prob_unbalance_value.setGeometry(QtCore.QRect(
        #    w * 0.5, max_height * 0.02, w * 0.4, max_height * 0.04))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(70)
        self.prob_unbalance_value.setFont(font)
        self.prob_unbalance_value.setObjectName("prob_unbalance_value")

        self.line1Layout.addWidget(self.unbalance_label)
        self.line1Layout.addWidget(self.prob_unbalance_value)

        self.lateralMenuLayout.addLayout(self.line1Layout)

        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem3)

        # FRICTION probability line
        self.line2Layout = QtWidgets.QHBoxLayout()
        self.line2Layout.setObjectName("line2Layout")

        self.friction_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        # self.friction_label.setGeometry(QtCore.QRect(
        #    w * 0.1, max_height * 0.02, w * 0.4, max_height * 0.02))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(66)
        self.friction_label.setFont(font)
        self.friction_label.setObjectName("friction_label")

        self.prob_friction_value = QtWidgets.QLabel(
            self.lateralMenuLayoutWidget)
        # self.prob_friction_value.setGeometry(QtCore.QRect(
        #    w * 0.5, max_height * 0.02, w * 0.4, max_height * 0.04))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(70)
        self.prob_friction_value.setFont(font)
        self.prob_friction_value.setObjectName("prob_friction_value")

        self.line2Layout.addWidget(self.friction_label)
        self.line2Layout.addWidget(self.prob_friction_value)

        self.lateralMenuLayout.addLayout(self.line2Layout)

        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem3)

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

        t1, xfft = ReadRoutine().sensors.getXY("gyroRad0")
        t2, yfft = ReadRoutine().sensors.getXY("gyroRad1")
        t3, zfft = ReadRoutine().sensors.getXY("gyroRad2")
        t4, x = ReadRoutine().sensors.getXY("accGravity0")
        t5, y = ReadRoutine().sensors.getXY("accGravity1")
        t6, z = ReadRoutine().sensors.getXY("accGravity2")
        t7, magx = ReadRoutine().sensors.getXY("magNorm0")
        t8, magy = ReadRoutine().sensors.getXY("magNorm1")
        t9, magz = ReadRoutine().sensors.getXY("magNorm2")
        t10, pitch = ReadRoutine().sensors.getXY("pitch")
        t11, roll = ReadRoutine().sensors.getXY("roll")
        t12, yaw = ReadRoutine().sensors.getXY("yaw")

        # print(np.diff(t6))
        # print("mean={}, std={}".format(np.mean(np.diff(t6)), np.std(np.diff(t6))))
        if len(t4) != 0:
            if t4[-1] >= self.gap[1]:
                self.gap[0] = int(ReadRoutine().sensors.rtc[0])
                self.gap[1] = int(ReadRoutine().sensors.rtc[-1])

        self.list__dynamic_ax[0].plot(t1, xfft)
        self.list__dynamic_ax[0].set_ylabel('X-FFT')
        self.list__dynamic_ax[0].plot(t2, yfft)
        self.list__dynamic_ax[0].set_ylabel('Y-FFT')
        self.list__dynamic_ax[0].plot(t3, zfft)
        self.list__dynamic_ax[0].set_ylabel('Z-FFT')

        self.list__dynamic_ax[1].plot(t4, x)
        self.list__dynamic_ax[1].set_ylabel('X-axis')
        self.list__dynamic_ax[1].plot(t5, y)
        self.list__dynamic_ax[1].set_ylabel('Y-axis')
        self.list__dynamic_ax[1].plot(t6, z)
        self.list__dynamic_ax[1].set_ylabel('Z-axis')

        self.list__dynamic_ax[2].plot(t7, magx)
        self.list__dynamic_ax[2].set_ylabel('X-axis')
        self.list__dynamic_ax[2].plot(t8, magy)
        self.list__dynamic_ax[2].set_ylabel('Y-axis')
        self.list__dynamic_ax[2].plot(t9, magz)
        self.list__dynamic_ax[2].set_ylabel('Z-axis')

        self.list__dynamic_ax[3].plot(t10, pitch)
        self.list__dynamic_ax[3].set_ylabel('X-axis')
        self.list__dynamic_ax[4].plot(t11, roll)
        self.list__dynamic_ax[4].set_ylabel('Y-axis')
        self.list__dynamic_ax[5].plot(t12, yaw)
        self.list__dynamic_ax[5].set_ylabel('Z-axis')

        list_ylim = [Sensors.MAX_Y_GYRO] + \
            [Sensors.MAX_Y_ACC]+[Sensors.MAX_Y_MAG]+[180]*3
        for i in range(6):
            self.list__dynamic_ax[i].set_xlim([self.gap[0], self.gap[1]])
            self.list__dynamic_ax[i].set_ylim([-list_ylim[i], list_ylim[i]])
            self.list__dynamic_ax[i].figure.canvas.draw()

        self.firstChange = False
        self.probCorrect()
        self.probunbalance()
        self.probFriction()
        if KPredictior().values:
            print(KPredictior().values[-1])

    def changetoSTART(self):
        self.save_button.setText("START")
        self.save_button.setStyleSheet("background-color: rgb(0, 255, 0);")

    def changetoSTOP(self):
        self.save_button.setText("STOP")
        self.save_button.setStyleSheet("background-color: rgb(255, 0, 0);")

    def probCorrect(self):
        self.prob_correct_value.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                              "color: rgb(0, 0, 0);")

        self.prob_correct_value.setText(
            str(0)+"%")

    def probunbalance(self):
        self.prob_unbalance_value.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                "color: rgb(0, 0, 0);")
        self.prob_unbalance_value.setText(
            str(round(ReadRoutine().sensors.getAxis("y"), 1))+"º")

    def probFriction(self):
        self.prob_friction_value.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                               "color: rgb(0, 0, 0);")
        self.prob_friction_value.setText(
            str(round(ReadRoutine().sensors.getAxis("x"), 1))+"º")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.correct_label.setText(_translate("MainWindow", "Correct: "))
        self.prob_correct_value.setText(_translate("MainWindow", "0%"))

        self.unbalance_label.setText(_translate("MainWindow", "Unbalance: "))
        self.prob_unbalance_value.setText(_translate("MainWindow", "0%"))

        self.friction_label.setText(_translate("MainWindow", "Friction: "))
        self.prob_friction_value.setText(_translate("MainWindow", "0%"))

        self.save_label.setText(_translate("MainWindow", "Press to: "))
        self.save_button.setText(_translate("MainWindow", "SAVE"))

        self.txt_label.setText(_translate("MainWindow", "Insert a name"))
