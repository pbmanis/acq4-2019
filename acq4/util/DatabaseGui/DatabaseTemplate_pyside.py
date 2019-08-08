# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/util/DatabaseGui/DatabaseTemplate.ui',
# licensing of 'acq4/util/DatabaseGui/DatabaseTemplate.ui' applies.
#
# Created: Tue Jun 25 14:49:03 2019
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(274, 39)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dbLabel = QtWidgets.QLabel(Form)
        self.dbLabel.setObjectName("dbLabel")
        self.horizontalLayout.addWidget(self.dbLabel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.tableArea = QtWidgets.QWidget(Form)
        self.tableArea.setObjectName("tableArea")
        self.gridLayout = QtWidgets.QGridLayout(self.tableArea)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addWidget(self.tableArea, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Database:", None, -1))
        self.dbLabel.setText(QtWidgets.QApplication.translate("Form", "[ no DB loaded ]", None, -1))

