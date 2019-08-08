# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/pyqtgraph/tests/uictest.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.widget = PlotWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 120, 80))
        self.widget.setObjectName("widget")
        self.widget_2 = ImageView(Form)
        self.widget_2.setGeometry(QtCore.QRect(10, 110, 120, 80))
        self.widget_2.setObjectName("widget_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

from pyqtgraph import ImageView, PlotWidget
