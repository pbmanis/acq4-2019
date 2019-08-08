# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/util/imaging/contrast_ctrl_template.ui',
# licensing of 'acq4/util/imaging/contrast_ctrl_template.ui' applies.
#
# Created: Tue Jun 25 14:49:02 2019
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(176, 384)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.histogram = HistogramLUTWidget(Form)
        self.histogram.setObjectName("histogram")
        self.gridLayout.addWidget(self.histogram, 0, 0, 1, 2)
        self.btnAutoGain = QtWidgets.QPushButton(Form)
        self.btnAutoGain.setCheckable(True)
        self.btnAutoGain.setChecked(False)
        self.btnAutoGain.setObjectName("btnAutoGain")
        self.gridLayout.addWidget(self.btnAutoGain, 1, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.spinAutoGainSpeed = QtWidgets.QDoubleSpinBox(Form)
        self.spinAutoGainSpeed.setProperty("value", 2.0)
        self.spinAutoGainSpeed.setObjectName("spinAutoGainSpeed")
        self.gridLayout.addWidget(self.spinAutoGainSpeed, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.spinAutoGainCenterWeight = QtWidgets.QDoubleSpinBox(Form)
        self.spinAutoGainCenterWeight.setMaximum(1.0)
        self.spinAutoGainCenterWeight.setSingleStep(0.1)
        self.spinAutoGainCenterWeight.setObjectName("spinAutoGainCenterWeight")
        self.gridLayout.addWidget(self.spinAutoGainCenterWeight, 3, 1, 1, 1)
        self.zoomLiveBtn = QtWidgets.QPushButton(Form)
        self.zoomLiveBtn.setObjectName("zoomLiveBtn")
        self.gridLayout.addWidget(self.zoomLiveBtn, 6, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.alphaSlider = QtWidgets.QSlider(Form)
        self.alphaSlider.setMaximum(100)
        self.alphaSlider.setSingleStep(1)
        self.alphaSlider.setProperty("value", 100)
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setObjectName("alphaSlider")
        self.gridLayout.addWidget(self.alphaSlider, 4, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.btnAutoGain.setToolTip(QtWidgets.QApplication.translate("Form", "Determines the behavior of the white/black level sliders.\n"
"When enabled, the sliders maximum and minimum values are set\n"
"to the maximum and minimum intensity values in the image.\n"
"When disabled, the minimum is 0 and the maximum is the largest \n"
"possible intensity given the bit depth of the camera.", None, -1))
        self.btnAutoGain.setText(QtWidgets.QApplication.translate("Form", "Auto Gain", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Form", "Auto Gain Delay", None, -1))
        self.spinAutoGainSpeed.setToolTip(QtWidgets.QApplication.translate("Form", "Smooths out the auto gain control, prevents very\n"
"brief flashes from affecting the gain. Larger values\n"
"indicate more smoothing.\n"
"", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("Form", "Frame Center Weight", None, -1))
        self.spinAutoGainCenterWeight.setToolTip(QtWidgets.QApplication.translate("Form", "Weights the auto gain measurement to the center 1/3 of\n"
"the frame when set to 1.0. A value of 0.0 meters from \n"
"the entire frame.", None, -1))
        self.zoomLiveBtn.setText(QtWidgets.QApplication.translate("Form", "Zoom to Image", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Transparency", None, -1))

from acq4.pyqtgraph import HistogramLUTWidget
