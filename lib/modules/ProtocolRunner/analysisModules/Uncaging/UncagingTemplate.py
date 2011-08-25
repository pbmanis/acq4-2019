# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './lib/modules/ProtocolRunner/analysisModules/Uncaging/UncagingTemplate.ui'
#
# Created: Wed Aug 17 13:49:55 2011
#      by: pyside-uic 0.2.11 running on PySide 1.0.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(240, 287)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.cameraModCombo = QtGui.QComboBox(Form)
        self.cameraModCombo.setObjectName("cameraModCombo")
        self.gridLayout.addWidget(self.cameraModCombo, 1, 1, 1, 2)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.clampDevCombo = QtGui.QComboBox(Form)
        self.clampDevCombo.setObjectName("clampDevCombo")
        self.gridLayout.addWidget(self.clampDevCombo, 4, 1, 1, 2)
        self.protList = QtGui.QListWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.protList.sizePolicy().hasHeightForWidth())
        self.protList.setSizePolicy(sizePolicy)
        self.protList.setObjectName("protList")
        self.gridLayout.addWidget(self.protList, 5, 0, 1, 3)
        self.deleteBtn = QtGui.QPushButton(Form)
        self.deleteBtn.setObjectName("deleteBtn")
        self.gridLayout.addWidget(self.deleteBtn, 6, 0, 1, 1)
        self.alphaSlider = QtGui.QSlider(Form)
        self.alphaSlider.setMaximum(255)
        self.alphaSlider.setPageStep(10)
        self.alphaSlider.setProperty("value", 150)
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setObjectName("alphaSlider")
        self.gridLayout.addWidget(self.alphaSlider, 6, 1, 1, 2)
        self.scannerDevCombo = QtGui.QComboBox(Form)
        self.scannerDevCombo.setObjectName("scannerDevCombo")
        self.gridLayout.addWidget(self.scannerDevCombo, 3, 1, 1, 2)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.clampStopSpin = QtGui.QLabel(Form)
        self.clampStopSpin.setObjectName("clampStopSpin")
        self.gridLayout.addWidget(self.clampStopSpin, 9, 0, 1, 1)
        self.enabledCheck = QtGui.QCheckBox(Form)
        self.enabledCheck.setObjectName("enabledCheck")
        self.gridLayout.addWidget(self.enabledCheck, 0, 1, 1, 1)
        self.clampBaseStartSpin = QtGui.QDoubleSpinBox(Form)
        self.clampBaseStartSpin.setMaximum(100000.0)
        self.clampBaseStartSpin.setObjectName("clampBaseStartSpin")
        self.gridLayout.addWidget(self.clampBaseStartSpin, 8, 1, 1, 1)
        self.clampTestStartSpin = QtGui.QDoubleSpinBox(Form)
        self.clampTestStartSpin.setMaximum(100000.0)
        self.clampTestStartSpin.setProperty("value", 400.0)
        self.clampTestStartSpin.setObjectName("clampTestStartSpin")
        self.gridLayout.addWidget(self.clampTestStartSpin, 9, 1, 1, 1)
        self.clampTestStopSpin = QtGui.QDoubleSpinBox(Form)
        self.clampTestStopSpin.setMaximum(100000.0)
        self.clampTestStopSpin.setProperty("value", 450.0)
        self.clampTestStopSpin.setObjectName("clampTestStopSpin")
        self.gridLayout.addWidget(self.clampTestStopSpin, 9, 2, 1, 1)
        self.clampBaseStopSpin = QtGui.QDoubleSpinBox(Form)
        self.clampBaseStopSpin.setMaximum(100000.0)
        self.clampBaseStopSpin.setProperty("value", 380.0)
        self.clampBaseStopSpin.setObjectName("clampBaseStopSpin")
        self.gridLayout.addWidget(self.clampBaseStopSpin, 8, 2, 1, 1)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)
        self.pspToleranceSpin = QtGui.QDoubleSpinBox(Form)
        self.pspToleranceSpin.setProperty("value", 4.0)
        self.pspToleranceSpin.setObjectName("pspToleranceSpin")
        self.gridLayout.addWidget(self.pspToleranceSpin, 10, 1, 1, 2)
        self.recomputeBtn = QtGui.QPushButton(Form)
        self.recomputeBtn.setObjectName("recomputeBtn")
        self.gridLayout.addWidget(self.recomputeBtn, 17, 1, 1, 1)
        self.displayImageCheck = QtGui.QCheckBox(Form)
        self.displayImageCheck.setChecked(True)
        self.displayImageCheck.setObjectName("displayImageCheck")
        self.gridLayout.addWidget(self.displayImageCheck, 13, 1, 1, 2)
        self.spotToleranceSpin = QtGui.QDoubleSpinBox(Form)
        self.spotToleranceSpin.setMinimum(0.01)
        self.spotToleranceSpin.setMaximum(100000000.0)
        self.spotToleranceSpin.setSingleStep(0.1)
        self.spotToleranceSpin.setProperty("value", 1000.0)
        self.spotToleranceSpin.setObjectName("spotToleranceSpin")
        self.gridLayout.addWidget(self.spotToleranceSpin, 15, 1, 1, 1)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 15, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 14, 0, 1, 1)
        self.frame1Spin = QtGui.QSpinBox(Form)
        self.frame1Spin.setObjectName("frame1Spin")
        self.gridLayout.addWidget(self.frame1Spin, 14, 1, 1, 1)
        self.frame2Spin = QtGui.QSpinBox(Form)
        self.frame2Spin.setObjectName("frame2Spin")
        self.gridLayout.addWidget(self.frame2Spin, 14, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Camera Module:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Clamp Device:", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteBtn.setText(QtGui.QApplication.translate("Form", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Scanner Device:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Clamp Baseline", None, QtGui.QApplication.UnicodeUTF8))
        self.clampStopSpin.setText(QtGui.QApplication.translate("Form", "Clamp Test", None, QtGui.QApplication.UnicodeUTF8))
        self.enabledCheck.setText(QtGui.QApplication.translate("Form", "Enabled", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "PSP Tolerance", None, QtGui.QApplication.UnicodeUTF8))
        self.recomputeBtn.setText(QtGui.QApplication.translate("Form", "Recompute", None, QtGui.QApplication.UnicodeUTF8))
        self.displayImageCheck.setText(QtGui.QApplication.translate("Form", "Display images", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Spot Cutoff", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Frame:", None, QtGui.QApplication.UnicodeUTF8))

