# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/devices/FilterWheel/FilterWheelTaskTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.sequenceCombo = QtWidgets.QComboBox(Form)
        self.sequenceCombo.setObjectName("sequenceCombo")
        self.gridLayout_2.addWidget(self.sequenceCombo, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.filterCombo = QtWidgets.QComboBox(Form)
        self.filterCombo.setObjectName("filterCombo")
        self.gridLayout_2.addWidget(self.filterCombo, 0, 1, 1, 1)
        self.sequenceListEdit = QtWidgets.QLineEdit(Form)
        self.sequenceListEdit.setObjectName("sequenceListEdit")
        self.gridLayout_2.addWidget(self.sequenceListEdit, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Sequence"))
        self.label.setText(_translate("Form", "Filter Wheel position"))

