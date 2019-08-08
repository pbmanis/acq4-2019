# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/util/ColorMapper/CMTemplate.ui',
# licensing of 'acq4/util/ColorMapper/CMTemplate.ui' applies.
#
# Created: Tue Jun 25 14:49:04 2019
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(264, 249)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.fileCombo = QtWidgets.QComboBox(Form)
        self.fileCombo.setEditable(True)
        self.fileCombo.setMaxVisibleItems(20)
        self.fileCombo.setObjectName("fileCombo")
        self.horizontalLayout.addWidget(self.fileCombo)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.saveBtn = FeedbackButton(Form)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout.addWidget(self.saveBtn, 1, 0, 1, 1)
        self.saveAsBtn = FeedbackButton(Form)
        self.saveAsBtn.setObjectName("saveAsBtn")
        self.gridLayout.addWidget(self.saveAsBtn, 1, 1, 1, 1)
        self.deleteBtn = FeedbackButton(Form)
        self.deleteBtn.setObjectName("deleteBtn")
        self.gridLayout.addWidget(self.deleteBtn, 1, 2, 1, 1)
        self.tree = TreeWidget(Form)
        self.tree.setRootIsDecorated(False)
        self.tree.setObjectName("tree")
        self.gridLayout.addWidget(self.tree, 2, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Color Scheme:", None, -1))
        self.saveBtn.setText(QtWidgets.QApplication.translate("Form", "Save", None, -1))
        self.saveAsBtn.setText(QtWidgets.QApplication.translate("Form", "Save As..", None, -1))
        self.deleteBtn.setText(QtWidgets.QApplication.translate("Form", "Delete", None, -1))
        self.tree.headerItem().setText(0, QtWidgets.QApplication.translate("Form", "arg", None, -1))
        self.tree.headerItem().setText(1, QtWidgets.QApplication.translate("Form", "op", None, -1))
        self.tree.headerItem().setText(2, QtWidgets.QApplication.translate("Form", "min", None, -1))
        self.tree.headerItem().setText(3, QtWidgets.QApplication.translate("Form", "max", None, -1))
        self.tree.headerItem().setText(4, QtWidgets.QApplication.translate("Form", "colors", None, -1))
        self.tree.headerItem().setText(5, QtWidgets.QApplication.translate("Form", "remove", None, -1))

from acq4.pyqtgraph import FeedbackButton, TreeWidget
