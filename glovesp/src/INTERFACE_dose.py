# main import for QT window
from PyQt5 import QtCore, QtGui, QtWidgets

# imports to the graph works with the QT window
import sys
import time
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

# import for the highpass filter
from scipy import signal

# import for update dose bar
import time
import math

from vibration_dose import *

# import to test
import random

#imports to update the graph with the data from sensors
import os
import threading
from kpredictor import *
from read_routine import *
from save_routine import *

class Ui_dose(object):
    def setupUi(self, MainWindow, screen_size):
        MainWindow.setObjectName("MainWindow")
        max_height = screen_size.height() * 0.93
        MainWindow.resize(screen_size.width(), max_height)
        MainWindow.setStyleSheet("background-color: rgb(255,255,255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, screen_size.width(), max_height))
        self.centralwidget.setObjectName("centralwidget")

        self.v = VibrationDose(ReadRoutine().sensors.rtc, ReadRoutine().sensors.list_s[1].a[0],
                          ReadRoutine().sensors.list_s[1].a[1], ReadRoutine().sensors.list_s[1].a[2])

        # Setting the graphs dependencies
        self.list_canvas = []
        list_dynamic_canvas = []
        self.list__dynamic_ax = []
        self.gap = [0, 8]
        self.t = 1
        self.count_main_loop = 1

        # Drawing the graphs
        for i in range(3):
            self.list_canvas.append(QtWidgets.QVBoxLayout())
            self.list_canvas[i].setObjectName("canvas"+str(i))

            list_dynamic_canvas.append(
                FigureCanvas(Figure(figsize=(8, 2), dpi=90)))

            self.list_canvas[i].addWidget(list_dynamic_canvas[i])
            self.list__dynamic_ax.append(
                list_dynamic_canvas[i].figure.subplots())
            self._timer = list_dynamic_canvas[i].new_timer(0.01, [(self._update_canvas, (), {})])
        self._timer.start()
        
        # Left Layout definitions
        h = max_height * 0.32
        self.l1_Widget = QtWidgets.QWidget(self.centralwidget)
        self.l1_Widget.setGeometry(QtCore.QRect(
            10, 0, screen_size.width() * 0.5, h))
        self.l1_Widget.setObjectName("l1_Widget")
        self.l1_Layout = QtWidgets.QVBoxLayout(self.l1_Widget)
        self.l1_Layout.setContentsMargins(0, 0, 0, 0)
        self.l1_Layout.setObjectName("l1_Layout")

        self.l2_Widget = QtWidgets.QWidget(self.centralwidget)
        self.l2_Widget.setGeometry(QtCore.QRect(
            10, h + 1, screen_size.width() * 0.5, h))
        self.l2_Widget.setObjectName("l2_Widget")
        self.l2_Layout = QtWidgets.QVBoxLayout(self.l2_Widget)
        self.l2_Layout.setContentsMargins(0, 0, 0, 0)
        self.l2_Layout.setObjectName("l2_Layout")

        self.l3_Widget = QtWidgets.QWidget(self.centralwidget)
        self.l3_Widget.setGeometry(QtCore.QRect(
            10, h * 2 + 2, screen_size.width() * 0.5, h))
        self.l3_Widget.setObjectName("l3_Widget")
        self.l3_Layout = QtWidgets.QVBoxLayout(self.l3_Widget)
        self.l3_Layout.setContentsMargins(0, 0, 0, 0)
        self.l3_Layout.setObjectName("l3_Layout")

        # Inserting the graphs into the lines
        self.l1_Layout.addLayout(self.list_canvas[0])
        self.l2_Layout.addLayout(self.list_canvas[1])
        self.l3_Layout.addLayout(self.list_canvas[2])

        # Draw the background for the dose bar
        self.big_dose_bar_LayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.big_dose_bar_LayoutWidget.setGeometry(
            QtCore.QRect((screen_size.width() * 0.5) + 20, max_height * 0.05, screen_size.width() * 0.1, max_height * 0.90))
        self.big_dose_bar_LayoutWidget.setObjectName(
            "big_dose_bar_LayoutWidget")
        self.big_dose_bar_Layout = QtWidgets.QHBoxLayout(self.big_dose_bar_LayoutWidget)
        self.big_dose_bar_Layout.setContentsMargins(0, 0, 0, 0)
        self.big_dose_bar_Layout.setObjectName("big_dose_bar_Layout")

        # Draw the dose bar
        self.dose_bar_Layout = QtWidgets.QVBoxLayout()
        self.dose_bar_Layout.setObjectName("dose_bar_Layout")
        self.big_dose_bar_Layout.addLayout(self.dose_bar_Layout)

        # Set n_steps for n of lines in dose bar 'default = 60'
        self.levels_dose = []
        self.n_steps = 60

        for i in range((self.n_steps + 1)):
            self.levels_dose.append(QtWidgets.QFrame(
                self.big_dose_bar_LayoutWidget))

        # Draw the levels of dose
        for i in range(self.n_steps, 0, -1):
            self.levels_dose[i].setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.levels_dose[i].setFrameShadow(QtWidgets.QFrame.Raised)
            self.levels_dose[i].setObjectName("levels_dose"+str(i))
            self.dose_bar_Layout.addWidget(self.levels_dose[i])
            self.levels_dose[i].setStyleSheet(
                "background-color: rgb(222, 222, 222)")

        # Draw the label's column for dose
        self.dose_label_Layout = QtWidgets.QVBoxLayout()
        self.dose_label_Layout.setObjectName("dose_label_Layout")
        self.big_dose_bar_Layout.addLayout(self.dose_label_Layout)

        # Draw the labels

        # First spacer UP TO DOWN (100 - 73)
        spacer73 = QtWidgets.QSpacerItem(
            20, ((max_height*0.9) * 0.27), QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dose_label_Layout.addItem(spacer73)

        # Line 73%
        self.line73 = QtWidgets.QFrame(self.big_dose_bar_LayoutWidget)
        self.line73.setFrameShape(QtWidgets.QFrame.HLine)
        self.line73.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line73.setObjectName("line73")
        self.dose_label_Layout.addWidget(self.line73)

        # Label 73%
        self.label_73 = QtWidgets.QLabel(self.big_dose_bar_LayoutWidget)
        self.label_73.setObjectName("label_73")
        self.dose_label_Layout.addWidget(self.label_73)

        # Second spacer UP TO DOWN (73 - 60)
        spacer60 = QtWidgets.QSpacerItem(
            20, ((max_height*0.9) * 0.13), QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dose_label_Layout.addItem(spacer60)

        # Line 60%
        self.line60 = QtWidgets.QFrame(self.big_dose_bar_LayoutWidget)
        self.line60.setFrameShape(QtWidgets.QFrame.HLine)
        self.line60.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line60.setObjectName("line60")
        self.dose_label_Layout.addWidget(self.line60)

        # Label 60%
        self.label_60 = QtWidgets.QLabel(self.big_dose_bar_LayoutWidget)
        self.label_60.setObjectName("label_60")
        self.dose_label_Layout.addWidget(self.label_60)

        # Third spacer UP TO DOWN (60 - 33)
        spacer33 = QtWidgets.QSpacerItem(
            20, ((max_height*0.9) * 0.27), QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dose_label_Layout.addItem(spacer33)

        # Line 33%
        self.line33 = QtWidgets.QFrame(self.big_dose_bar_LayoutWidget)
        self.line33.setFrameShape(QtWidgets.QFrame.HLine)
        self.line33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line33.setObjectName("line33")
        self.dose_label_Layout.addWidget(self.line33)

        # Label 33%
        self.label_33 = QtWidgets.QLabel(self.big_dose_bar_LayoutWidget)
        self.label_33.setObjectName("label_33")
        self.dose_label_Layout.addWidget(self.label_33)

        # Third spacer UP TO DOWN (33 - 0)
        spacer0 = QtWidgets.QSpacerItem(
            20, ((max_height*0.9) * 0.33), QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dose_label_Layout.addItem(spacer0)


        # Draw the legend panel
        self.legendbox_LayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.legendbox_LayoutWidget.setGeometry(
            QtCore.QRect((screen_size.width() * 0.6) + 20, max_height * 0.05, screen_size.width() * 0.3, max_height * 0.10))
        self.legendbox_LayoutWidget.setObjectName(
            "legendbox_LayoutWidget")
        self.legendbox_Layout = QtWidgets.QHBoxLayout(
            self.legendbox_LayoutWidget)
        self.legendbox_Layout.setContentsMargins(0, 0, 0, 0)
        self.legendbox_Layout.setObjectName("legendbox_Layout")

        # Draw the controls line
        self.control_line = QtWidgets.QHBoxLayout()
        self.control_line.setObjectName("control_line")
        self.legendbox_Layout.addLayout(self.control_line)

        '''
        # Label AREN label
        self.label_aren_label = QtWidgets.QLabel(self.control_panel_LayoutWidget)
        self.label_aren_label.setObjectName("label_aren_label")
        self.control_panel_Layout.addWidget(self.label_aren_label)
        '''

        # AREN label
        self.aren_label = QtWidgets.QLabel(self.centralwidget)
        self.aren_label.setGeometry(QtCore.QRect((screen_size.width() * 0.8), max_height * 0.05, screen_size.width() * 0.05, max_height * 0.06))
        self.aren_label.setObjectName("aren_label")
        self.aren_label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                              "color: rgb(255, 255, 255);")
        
        # LEGENDA 
        
        '''
        # Method start update
        def start():
            self.count_main_loop += 1
    
        # Control button
        self.control_button = QtWidgets.QPushButton(self.control_panel_LayoutWidget)
        self.control_panel_Layout.addWidget(self.control_button)
        #self.control_button.clicked.connect(start)
        '''

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #def filter_highPass(self, ):

    '''
    def update_all(self):
        if (self.count_main_loop % 2) == 0:
            self.control_button.setText("Stop")
            while (self.count_main_loop % 2) == 0:
                self._update_canvas()
                print("Loop update")
    
    def setWhite(self):
        self.aren_label.setText("0 m/s²")
        self.control_button.setText("Start")
        for i in range(1, (self.n_steps + 1)):
            self.levels_dose[i].setStyleSheet(
                "background-color: rgb(222, 222, 222)")
    '''

    def calc_routine(self, *args):
        while len(ReadRoutine().sensors.rtc) == 0:
            time.sleep(0.01)
        #print(ReadRoutine().sensors.rtc)
        #print(ReadRoutine().sensors.list_s[1].a[0])

        #print(ReadRoutine().sensors.rtc.copy)
        self.v.sum_vibration(ReadRoutine().sensors.rtc.copy(), ReadRoutine().sensors.list_s[1].a[0].copy(
        ), ReadRoutine().sensors.list_s[1].a[1].copy(), ReadRoutine().sensors.list_s[1].a[2].copy(), 600, 24, 7)  # Change the 600 to the real jorney workerd

        #print (self.v.total)
        #print(round(v.total, 2))
        #print((round(v.total, 2)) * 10)
        self._update_dose_bar((round(self.v.get_total(), 2)))
        #time.sleep(0.01)

    def _update_dose_bar(self, value_dose):
        factor_x = 100
        value_dose = value_dose * factor_x
        #print("VALOR DA DOSE: " + str(value_dose))
        dose = math.floor((value_dose * self.n_steps) / 150)
        green_max = math.ceil(self.n_steps * 0.33333)
        yellow_max = math.ceil(self.n_steps * 0.6)
        orange_max = math.ceil(self.n_steps * 0.73333)
        self.aren_label.setText(str(value_dose / factor_x) + " m/s²")
        #self.aren_label.setText(str(value_dose) + " m/s²")

        for i in range(1, (dose + 1)):
            self.levels_dose[i].setStyleSheet(
                "background-color: rgb(0, 255, 0)")

        for i in range(dose, (self.n_steps + 1)):
            self.levels_dose[i].setStyleSheet(
                "background-color: rgb(222, 222, 222)")

        if dose >= green_max:
            for i in range(green_max, (dose + 1)):
                self.levels_dose[i].setStyleSheet(
                    "background-color: rgb(255, 255, 0)")

        if dose >= yellow_max:
            for i in range(yellow_max, (dose + 1)):
                self.levels_dose[i].setStyleSheet(
                    "background-color: rgb(255, 123, 0)")
        
        if dose >= orange_max:
            for i in range(orange_max, (dose + 1)):
                self.levels_dose[i].setStyleSheet(
                    "background-color: rgb(255, 0, 0)")

    
    # Method to get data to plot
    def getValues(self):
        value = []
        t = []
        for i in range(512):
            value.append(random.uniform(-1, 1))
            t.append(i)
        return t, value

    # Method to update the graphs
    def _update_canvas(self):
        for i in range(3):
            self.list__dynamic_ax[i].clear()

        t4, x = ReadRoutine().sensors.list_s[1].a[0].getxy(
            ReadRoutine().sensors.rtc)
        t5, y = ReadRoutine().sensors.list_s[1].a[1].getxy(
            ReadRoutine().sensors.rtc)
        t6, z = ReadRoutine().sensors.list_s[1].a[2].getxy(
            ReadRoutine().sensors.rtc)
        
        #print(ReadRoutine().sensors.list_s[1].a[0].last_acc_rate)

        '''
        t4, x = self.getValues()
        t5, y = self.getValues()
        t6, z = self.getValues()
        '''
        
        if len(t4) != 0:
            if t4[-1] >= self.gap[1]:
                self.gap[0] += 1
                self.gap[1] += 1

        self.list__dynamic_ax[0].plot(t4, x)
        self.list__dynamic_ax[0].set_ylabel('X-axis')

        self.list__dynamic_ax[1].plot(t5, y)
        self.list__dynamic_ax[1].set_ylabel('Y-axis')

        self.list__dynamic_ax[2].plot(t6, z)
        self.list__dynamic_ax[2].set_ylabel('Z-axis')

        for i in range(3):
            self.list__dynamic_ax[i].set_xlim([self.gap[0], self.gap[1]])
            #self.list__dynamic_ax[i].set_ylim([(-2), 2])
            self.list__dynamic_ax[i].figure.canvas.draw()
        #limit = random.randint(0, self.n_steps)
        t = threading.Thread(target = self.calc_routine(), args = ())
        t.start()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vibration Dose"))
        self.label_73.setText(_translate("MainWindow", "1.1 m/s²"))
        self.label_60.setText(_translate("MainWindow", "0.9 m/s²"))
        self.label_33.setText(_translate("MainWindow", "0.5 m/s²"))

        #self.label_aren_label.setText(_translate("MainWindow", "aren: "))
        self.aren_label.setText(_translate("MainWindow", "0 m/s²"))
        #self.control_button.setText(_translate("MainWindow", "Start"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_dose()
    screen_size = screen.availableSize()
    ui.setupUi(MainWindow, screen_size)
    MainWindow.show()
    sys.exit(app.exec_())
