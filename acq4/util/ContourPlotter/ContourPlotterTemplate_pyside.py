# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/util/ContourPlotter/ContourPlotterTemplate.ui',
# licensing of 'acq4/util/ContourPlotter/ContourPlotterTemplate.ui' applies.
#
# Created: Tue Jun 25 14:49:01 2019
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.drawBtn = QtWidgets.QPushButton(Form)
        self.drawBtn.setObjectName("drawBtn")
        self.gridLayout.addWidget(self.drawBtn, 2, 0, 1, 1)
        self.tree = TreeWidget(Form)
        self.tree.setObjectName("tree")
        self.tree.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tree, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.drawBtn.setText(QtWidgets.QApplication.translate("Form", "Draw", None, -1))
        self.tree.headerItem().setText(0, QtWidgets.QApplication.translate("Form", "Param", None, -1))
        self.tree.headerItem().setText(1, QtWidgets.QApplication.translate("Form", "Threshold", None, -1))
        self.tree.headerItem().setText(2, QtWidgets.QApplication.translate("Form", "% of max", None, -1))
        self.tree.headerItem().setText(3, QtWidgets.QApplication.translate("Form", "Color", None, -1))
        self.tree.headerItem().setText(4, QtWidgets.QApplication.translate("Form", "Remove", None, -1))

from pyqtgraph import TreeWidget
