# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/analysis/modules/PSPReversal/resultsTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ResultsDialogBox(object):
    def setupUi(self, ResultsDialogBox):
        ResultsDialogBox.setObjectName("ResultsDialogBox")
        ResultsDialogBox.resize(350, 468)
        font = QtGui.QFont()
        font.setPointSize(11)
        ResultsDialogBox.setFont(font)
        self.label = QtWidgets.QLabel(ResultsDialogBox)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName("label")
        self.resultsPSPReversal_text = QtWidgets.QTextEdit(ResultsDialogBox)
        self.resultsPSPReversal_text.setGeometry(QtCore.QRect(10, 30, 331, 431))
        self.resultsPSPReversal_text.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.resultsPSPReversal_text.setReadOnly(True)
        self.resultsPSPReversal_text.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.resultsPSPReversal_text.setObjectName("resultsPSPReversal_text")

        self.retranslateUi(ResultsDialogBox)
        QtCore.QMetaObject.connectSlotsByName(ResultsDialogBox)

    def retranslateUi(self, ResultsDialogBox):
        _translate = QtCore.QCoreApplication.translate
        ResultsDialogBox.setWindowTitle(_translate("ResultsDialogBox", "Dialog"))
        self.label.setText(_translate("ResultsDialogBox", "PSP Reversal Results"))

