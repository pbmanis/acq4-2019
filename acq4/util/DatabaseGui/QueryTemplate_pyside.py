# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/util/DatabaseGui/QueryTemplate.ui',
# licensing of 'acq4/util/DatabaseGui/QueryTemplate.ui' applies.
#
# Created: Tue Jun 25 14:49:03 2019
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.queryText = QtWidgets.QLineEdit(Form)
        self.queryText.setObjectName("queryText")
        self.gridLayout.addWidget(self.queryText, 0, 0, 1, 1)
        self.queryBtn = FeedbackButton(Form)
        self.queryBtn.setObjectName("queryBtn")
        self.gridLayout.addWidget(self.queryBtn, 0, 1, 1, 1)
        self.queryTable = TableWidget(Form)
        self.queryTable.setObjectName("queryTable")
        self.queryTable.setColumnCount(0)
        self.queryTable.setRowCount(0)
        self.gridLayout.addWidget(self.queryTable, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.queryBtn.setText(QtWidgets.QApplication.translate("Form", "Query", None, -1))

from acq4.pyqtgraph import TableWidget, FeedbackButton
