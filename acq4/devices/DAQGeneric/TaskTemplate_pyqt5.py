# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/devices/DAQGeneric/TaskTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(770, 365)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.topSplitter = QtWidgets.QSplitter(Form)
        self.topSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.topSplitter.setObjectName("topSplitter")
        self.controlSplitter = QtWidgets.QSplitter(self.topSplitter)
        self.controlSplitter.setOrientation(QtCore.Qt.Vertical)
        self.controlSplitter.setObjectName("controlSplitter")
        self.plotSplitter = QtWidgets.QSplitter(self.topSplitter)
        self.plotSplitter.setOrientation(QtCore.Qt.Vertical)
        self.plotSplitter.setObjectName("plotSplitter")
        self.verticalLayout.addWidget(self.topSplitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

