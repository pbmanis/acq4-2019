# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/devices/ThorlabsFilterWheel/FilterWheelTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FilterWheelWidget(object):
    def setupUi(self, FilterWheelWidget):
        FilterWheelWidget.setObjectName("FilterWheelWidget")
        FilterWheelWidget.resize(207, 226)
        self.gridLayout = QtWidgets.QGridLayout(FilterWheelWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.FastButton = QtWidgets.QRadioButton(FilterWheelWidget)
        self.FastButton.setObjectName("FastButton")
        self.SpeedButtonGroup = QtWidgets.QButtonGroup(FilterWheelWidget)
        self.SpeedButtonGroup.setObjectName("SpeedButtonGroup")
        self.SpeedButtonGroup.addButton(self.FastButton)
        self.gridLayout.addWidget(self.FastButton, 0, 2, 1, 1)
        self.inputTrigButton = QtWidgets.QRadioButton(FilterWheelWidget)
        self.inputTrigButton.setObjectName("inputTrigButton")
        self.TriggerButtonGroup = QtWidgets.QButtonGroup(FilterWheelWidget)
        self.TriggerButtonGroup.setObjectName("TriggerButtonGroup")
        self.TriggerButtonGroup.addButton(self.inputTrigButton)
        self.gridLayout.addWidget(self.inputTrigButton, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(FilterWheelWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(FilterWheelWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.SlowButton = QtWidgets.QRadioButton(FilterWheelWidget)
        self.SlowButton.setObjectName("SlowButton")
        self.SpeedButtonGroup.addButton(self.SlowButton)
        self.gridLayout.addWidget(self.SlowButton, 0, 1, 1, 1)
        self.outputTrigButton = QtWidgets.QRadioButton(FilterWheelWidget)
        self.outputTrigButton.setObjectName("outputTrigButton")
        self.TriggerButtonGroup.addButton(self.outputTrigButton)
        self.gridLayout.addWidget(self.outputTrigButton, 1, 2, 1, 1)
        self.PositionGroup = QtWidgets.QGroupBox(FilterWheelWidget)
        self.PositionGroup.setObjectName("PositionGroup")
        self.PositionGridLayout = QtWidgets.QGridLayout(self.PositionGroup)
        self.PositionGridLayout.setObjectName("PositionGridLayout")
        self.gridLayout.addWidget(self.PositionGroup, 3, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(FilterWheelWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.sensorOffButton = QtWidgets.QRadioButton(FilterWheelWidget)
        self.sensorOffButton.setObjectName("sensorOffButton")
        self.gridLayout.addWidget(self.sensorOffButton, 2, 1, 1, 1)
        self.sensorOnButton = QtWidgets.QRadioButton(FilterWheelWidget)
        self.sensorOnButton.setObjectName("sensorOnButton")
        self.gridLayout.addWidget(self.sensorOnButton, 2, 2, 1, 1)

        self.retranslateUi(FilterWheelWidget)
        QtCore.QMetaObject.connectSlotsByName(FilterWheelWidget)

    def retranslateUi(self, FilterWheelWidget):
        _translate = QtCore.QCoreApplication.translate
        FilterWheelWidget.setWindowTitle(_translate("FilterWheelWidget", "Form"))
        self.FastButton.setText(_translate("FilterWheelWidget", "fast"))
        self.inputTrigButton.setText(_translate("FilterWheelWidget", "input"))
        self.label_3.setText(_translate("FilterWheelWidget", "Trigger Mode"))
        self.label.setText(_translate("FilterWheelWidget", "Speed"))
        self.SlowButton.setText(_translate("FilterWheelWidget", "slow"))
        self.outputTrigButton.setText(_translate("FilterWheelWidget", "output"))
        self.PositionGroup.setTitle(_translate("FilterWheelWidget", "Current Position"))
        self.label_2.setText(_translate("FilterWheelWidget", "Sensor Mode"))
        self.sensorOffButton.setText(_translate("FilterWheelWidget", "off"))
        self.sensorOnButton.setText(_translate("FilterWheelWidget", "on"))

