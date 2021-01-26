# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bluetooth_devices.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from bt_connection import *

class Ui_bluetooth_devices_window(object):
    
    def setupUi(self, bluetooth_devices_window, home_window, screen_size):
        bluetooth_devices_window.setObjectName("bluetooth_devices_window")
        bluetooth_devices_window.setWindowModality(QtCore.Qt.WindowModal)
        bluetooth_devices_window.resize(1200, 700)
        bluetooth_devices_window.setStyleSheet(
            "background-color: rgb(255,255,255)")

        self.centralwidget = QtWidgets.QWidget(bluetooth_devices_window)
        self.centralwidget.setObjectName("centralwidget")

        # Grid
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(400, 250, 400, 200))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        # Grid Layout
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        # Layout Spacers
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)

        # Submit Button
        self.submit_devices = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.submit_devices.setObjectName("submit_devices")
        self.gridLayout.addWidget(self.submit_devices, 4, 0, 1, 1)
        
        # Combo Box
        self.devices_combo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.devices_combo.setObjectName("devices_combo")
        self.gridLayout.addWidget(self.devices_combo, 2, 0, 1, 1)

        list_devices = self.mountComboBox()
        
        # Bluetooth configurations
        blue = btConnection()
        def f(x): return blue.connect_bt(list_devices, self.devices_combo.currentText(), bluetooth_devices_window, home_window, screen_size)
        self.submit_devices.clicked.connect(f)
        
        # Horizontal Grid
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 200, 1200, 60))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Main Label
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        bluetooth_devices_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(bluetooth_devices_window)
        QtCore.QMetaObject.connectSlotsByName(bluetooth_devices_window)

    def retranslateUi(self, bluetooth_devices_window):
        _translate = QtCore.QCoreApplication.translate
        bluetooth_devices_window.setWindowTitle(_translate("bluetooth_devices_window", "Bluetooth Devices"))
        self.submit_devices.setText(_translate("bluetooth_devices_window", "Select"))
        self.label.setText(_translate("bluetooth_devices_window", "Bluetooth devices available"))

    def mountComboBox(self):
        blue = btConnection()
        list_devices = blue.dicover_devices()
        listd = ['Nenhum']
        
        self.devices_combo.clear()
        for i in list_devices:
            listd.append(i[1])
        
        self.devices_combo.addItems(listd)
        return list_devices

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bluetooth_devices_window = QtWidgets.QMainWindow()
    ui = Ui_bluetooth_devices_window()
    ui.setupUi(bluetooth_devices_window)
    bluetooth_devices_window.show()
    sys.exit(app.exec_())
