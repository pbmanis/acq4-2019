# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/devices/MultiClamp/TaskTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(330, 97)
        Form.setAutoFillBackground(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.layoutWidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.vcModeRadio = QtWidgets.QRadioButton(self.frame_2)
        self.vcModeRadio.setObjectName("vcModeRadio")
        self.horizontalLayout_2.addWidget(self.vcModeRadio)
        self.i0ModeRadio = QtWidgets.QRadioButton(self.frame_2)
        self.i0ModeRadio.setChecked(True)
        self.i0ModeRadio.setObjectName("i0ModeRadio")
        self.horizontalLayout_2.addWidget(self.i0ModeRadio)
        self.icModeRadio = QtWidgets.QRadioButton(self.frame_2)
        self.icModeRadio.setObjectName("icModeRadio")
        self.horizontalLayout_2.addWidget(self.icModeRadio)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.holdingCheck = QtWidgets.QCheckBox(self.frame_2)
        self.holdingCheck.setObjectName("holdingCheck")
        self.horizontalLayout_6.addWidget(self.holdingCheck)
        self.holdingSpin = SpinBox(self.frame_2)
        self.holdingSpin.setEnabled(False)
        self.holdingSpin.setMinimum(-1000000.0)
        self.holdingSpin.setMaximum(1000000.0)
        self.holdingSpin.setObjectName("holdingSpin")
        self.horizontalLayout_6.addWidget(self.holdingSpin)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_6)
        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.primarySignalCheck = QtWidgets.QCheckBox(self.layoutWidget)
        self.primarySignalCheck.setObjectName("primarySignalCheck")
        self.gridLayout.addWidget(self.primarySignalCheck, 0, 0, 1, 1)
        self.secondarySignalCheck = QtWidgets.QCheckBox(self.layoutWidget)
        self.secondarySignalCheck.setObjectName("secondarySignalCheck")
        self.gridLayout.addWidget(self.secondarySignalCheck, 1, 0, 1, 1)
        self.primarySignalCombo = QtWidgets.QComboBox(self.layoutWidget)
        self.primarySignalCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.primarySignalCombo.sizePolicy().hasHeightForWidth())
        self.primarySignalCombo.setSizePolicy(sizePolicy)
        self.primarySignalCombo.setMinimumSize(QtCore.QSize(40, 0))
        self.primarySignalCombo.setObjectName("primarySignalCombo")
        self.primarySignalCombo.addItem("")
        self.gridLayout.addWidget(self.primarySignalCombo, 0, 1, 1, 1)
        self.secondarySignalCombo = QtWidgets.QComboBox(self.layoutWidget)
        self.secondarySignalCombo.setEnabled(False)
        self.secondarySignalCombo.setMinimumSize(QtCore.QSize(40, 0))
        self.secondarySignalCombo.setObjectName("secondarySignalCombo")
        self.secondarySignalCombo.addItem("")
        self.gridLayout.addWidget(self.secondarySignalCombo, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 2, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.secondaryGainCheck = QtWidgets.QCheckBox(self.layoutWidget)
        self.secondaryGainCheck.setObjectName("secondaryGainCheck")
        self.horizontalLayout_7.addWidget(self.secondaryGainCheck)
        self.secondaryGainSpin = QtWidgets.QSpinBox(self.layoutWidget)
        self.secondaryGainSpin.setEnabled(False)
        self.secondaryGainSpin.setMaximum(100000)
        self.secondaryGainSpin.setObjectName("secondaryGainSpin")
        self.horizontalLayout_7.addWidget(self.secondaryGainSpin)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.primaryGainCheck = QtWidgets.QCheckBox(self.layoutWidget)
        self.primaryGainCheck.setObjectName("primaryGainCheck")
        self.horizontalLayout_5.addWidget(self.primaryGainCheck)
        self.primaryGainSpin = QtWidgets.QSpinBox(self.layoutWidget)
        self.primaryGainSpin.setEnabled(False)
        self.primaryGainSpin.setMaximum(100000)
        self.primaryGainSpin.setObjectName("primaryGainSpin")
        self.horizontalLayout_5.addWidget(self.primaryGainSpin)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.frame = QtWidgets.QFrame(self.layoutWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.waveGeneratorLabel = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waveGeneratorLabel.sizePolicy().hasHeightForWidth())
        self.waveGeneratorLabel.setSizePolicy(sizePolicy)
        self.waveGeneratorLabel.setObjectName("waveGeneratorLabel")
        self.verticalLayout.addWidget(self.waveGeneratorLabel)
        self.waveGeneratorWidget = StimGenerator(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waveGeneratorWidget.sizePolicy().hasHeightForWidth())
        self.waveGeneratorWidget.setSizePolicy(sizePolicy)
        self.waveGeneratorWidget.setObjectName("waveGeneratorWidget")
        self.verticalLayout.addWidget(self.waveGeneratorWidget)
        self.verticalLayout_2.addWidget(self.frame)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.topPlotWidget = PlotWidget(self.splitter)
        self.topPlotWidget.setObjectName("topPlotWidget")
        self.bottomPlotWidget = PlotWidget(self.splitter)
        self.bottomPlotWidget.setObjectName("bottomPlotWidget")
        self.verticalLayout_3.addWidget(self.splitter_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.vcModeRadio.setText(_translate("Form", "VC"))
        self.i0ModeRadio.setText(_translate("Form", "I=0"))
        self.icModeRadio.setText(_translate("Form", "IC"))
        self.holdingCheck.setText(_translate("Form", "Holding"))
        self.primarySignalCheck.setText(_translate("Form", "Primary:"))
        self.secondarySignalCheck.setText(_translate("Form", "Secondary:"))
        self.primarySignalCombo.setItemText(0, _translate("Form", "MembranePotential"))
        self.secondarySignalCombo.setItemText(0, _translate("Form", "MembraneCurrent"))
        self.secondaryGainCheck.setText(_translate("Form", "Set Gain"))
        self.primaryGainCheck.setText(_translate("Form", "Set Gain"))
        self.waveGeneratorLabel.setText(_translate("Form", "Command Function (A)"))

from acq4.pyqtgraph import PlotWidget, SpinBox
from acq4.util.generator.StimGenerator import StimGenerator
