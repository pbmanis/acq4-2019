# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/util/DirTreeWidget/DirTreeTemplate.ui',
# licensing of 'acq4/util/DirTreeWidget/DirTreeTemplate.ui' applies.
#
# Created: Tue Jun 25 14:49:01 2019
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(282, 285)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.titleLabel = QtWidgets.QLabel(Form)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 2)
        self.newBtn = QtWidgets.QPushButton(Form)
        self.newBtn.setObjectName("newBtn")
        self.gridLayout.addWidget(self.newBtn, 0, 2, 1, 1)
        self.loadBtn = QtWidgets.QPushButton(Form)
        self.loadBtn.setObjectName("loadBtn")
        self.gridLayout.addWidget(self.loadBtn, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(88, 77, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.saveBtn = QtWidgets.QPushButton(Form)
        self.saveBtn.setEnabled(False)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout.addWidget(self.saveBtn, 3, 2, 1, 1)
        self.saveAsBtn = QtWidgets.QPushButton(Form)
        self.saveAsBtn.setEnabled(True)
        self.saveAsBtn.setObjectName("saveAsBtn")
        self.gridLayout.addWidget(self.saveAsBtn, 4, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(88, 47, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 2, 1, 1)
        self.deleteBtn = QtWidgets.QPushButton(Form)
        self.deleteBtn.setEnabled(True)
        self.deleteBtn.setObjectName("deleteBtn")
        self.gridLayout.addWidget(self.deleteBtn, 7, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.currentTitleLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentTitleLabel.sizePolicy().hasHeightForWidth())
        self.currentTitleLabel.setSizePolicy(sizePolicy)
        self.currentTitleLabel.setObjectName("currentTitleLabel")
        self.horizontalLayout.addWidget(self.currentTitleLabel)
        self.currentLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentLabel.sizePolicy().hasHeightForWidth())
        self.currentLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.currentLabel.setFont(font)
        self.currentLabel.setText("")
        self.currentLabel.setObjectName("currentLabel")
        self.horizontalLayout.addWidget(self.currentLabel)
        self.gridLayout.addLayout(self.horizontalLayout, 8, 0, 1, 3)
        self.newDirBtn = QtWidgets.QPushButton(Form)
        self.newDirBtn.setObjectName("newDirBtn")
        self.gridLayout.addWidget(self.newDirBtn, 5, 2, 1, 1)
        self.fileTree = DirTreeWidget(Form)
        self.fileTree.setAcceptDrops(True)
        self.fileTree.setHeaderHidden(True)
        self.fileTree.setObjectName("fileTree")
        self.fileTree.headerItem().setText(0, "1")
        self.gridLayout.addWidget(self.fileTree, 1, 1, 7, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.titleLabel.setText(QtWidgets.QApplication.translate("Form", "Protocols", None, -1))
        self.newBtn.setText(QtWidgets.QApplication.translate("Form", "New", None, -1))
        self.loadBtn.setText(QtWidgets.QApplication.translate("Form", "Load", None, -1))
        self.saveBtn.setText(QtWidgets.QApplication.translate("Form", "Save", None, -1))
        self.saveAsBtn.setText(QtWidgets.QApplication.translate("Form", "Save As..", None, -1))
        self.deleteBtn.setText(QtWidgets.QApplication.translate("Form", "Delete", None, -1))
        self.currentTitleLabel.setText(QtWidgets.QApplication.translate("Form", "Current Protocol:", None, -1))
        self.newDirBtn.setText(QtWidgets.QApplication.translate("Form", "New Dir", None, -1))

from acq4.util.DirTreeWidget import DirTreeWidget
