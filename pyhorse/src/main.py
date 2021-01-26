# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

# main import for QT window
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

# connect bluetooth devices

from resources import *
from WifiConnection import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, screen):
        self.screen_size = screen.availableSize()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.screen_size.width(), self.screen_size.height())
        MainWindow.setStyleSheet("background-color: rgb(255,255,255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main Label
        self.main_label = QtWidgets.QLabel(self.centralwidget)
        w = 500
        h = 80
        self.main_label.setGeometry(QtCore.QRect(
            ((self.screen_size.width() * 0.5) - (w / 2)), (self.screen_size.height() * 0.2), w, h))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(65)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        self.main_label.setFont(font)
        self.main_label.setObjectName("main_label")

        # Full Name Label
        self.full_name_label = QtWidgets.QLabel(self.centralwidget)
        w = 336
        h = 20
        self.full_name_label.setGeometry(QtCore.QRect(
            ((self.screen_size.width() * 0.5) - ((w / 2) - 5)), (self.screen_size.height() * 0.31), w, h))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.full_name_label.setFont(font)
        self.full_name_label.setObjectName("full_name_label")

        # Bluetooth Label
        '''
        self.blue_label = QtWidgets.QLabel(self.centralwidget)
        self.blue_label.setGeometry(QtCore.QRect(420, 400, 366, 40))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(20)
        font.setItalic(False)
        self.blue_label.setFont(font)
        self.blue_label.setObjectName("blue_label")
        '''

        # Bluetooth Button
        self.blue_btn = QtWidgets.QPushButton(self.centralwidget)
        w = 290
        h = 60
        self.blue_btn.setGeometry(QtCore.QRect(
            ((self.screen_size.width() * 0.5) - (w / 2)), (self.screen_size.height() * 0.6), w, h))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(16)
        self.blue_btn.setFont(font)
        self.blue_btn.setObjectName("blue_btn")
        # print(MainWindow)

        # def blue():
        #    self.bluetoothPage(MainWindow)
        blue = WifiConnection()

        def f():
            MainWindow.close()
#
            self.window = QtWidgets.QMainWindow()
            choose = ChooseAppWindow()
            choose.setupUi(self.window,  self.screen_size)
            self.window.show()
            return blue.wifiConnect(
                Resources().loadip())

        self.blue_btn.clicked.connect(f)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.main_label.setText(_translate("MainWindow", "MUVmanco"))
        self.full_name_label.setText(_translate(
            "MainWindow", "Detector de Cavalo Manco"))
        #self.blue_label.setText(_translate("MainWindow", "Connect bluetooth"))
        self.blue_btn.setText(_translate(
            "MainWindow", "Procurar dispositivos"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, screen)
    MainWindow.show()
    sys.exit(app.exec_())
