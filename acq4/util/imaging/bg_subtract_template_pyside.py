# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/util/imaging/bg_subtract_template.ui',
# licensing of 'acq4/util/imaging/bg_subtract_template.ui' applies.
#
# Created: Tue Jun 25 14:49:02 2019
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(162, 90)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.bgBlurSpin = QtWidgets.QDoubleSpinBox(Form)
        self.bgBlurSpin.setProperty("value", 0.0)
        self.bgBlurSpin.setObjectName("bgBlurSpin")
        self.gridLayout.addWidget(self.bgBlurSpin, 2, 1, 1, 1)
        self.bgTimeSpin = QtWidgets.QDoubleSpinBox(Form)
        self.bgTimeSpin.setDecimals(1)
        self.bgTimeSpin.setSingleStep(1.0)
        self.bgTimeSpin.setProperty("value", 3.0)
        self.bgTimeSpin.setObjectName("bgTimeSpin")
        self.gridLayout.addWidget(self.bgTimeSpin, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.collectBgBtn = QtWidgets.QPushButton(Form)
        self.collectBgBtn.setCheckable(True)
        self.collectBgBtn.setObjectName("collectBgBtn")
        self.gridLayout.addWidget(self.collectBgBtn, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.subtractBgBtn = QtWidgets.QPushButton(Form)
        self.subtractBgBtn.setCheckable(True)
        self.subtractBgBtn.setAutoExclusive(False)
        self.subtractBgBtn.setObjectName("subtractBgBtn")
        self.horizontalLayout.addWidget(self.subtractBgBtn)
        self.divideBgBtn = QtWidgets.QPushButton(Form)
        self.divideBgBtn.setCheckable(True)
        self.divideBgBtn.setAutoExclusive(False)
        self.divideBgBtn.setObjectName("divideBgBtn")
        self.horizontalLayout.addWidget(self.divideBgBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.contAvgBgCheck = QtWidgets.QCheckBox(Form)
        self.contAvgBgCheck.setObjectName("contAvgBgCheck")
        self.horizontalLayout_2.addWidget(self.contAvgBgCheck)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.bgBlurSpin.setToolTip(QtWidgets.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Blurs the background frame before dividing it from the current frame.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Large blur values may cause performance to degrade.</span></p></body></html>", None, -1))
        self.bgTimeSpin.setToolTip(QtWidgets.QApplication.translate("Form", "Sets the approximate number of frames to be averaged for\n"
"background division.", None, -1))
        self.bgTimeSpin.setSuffix(QtWidgets.QApplication.translate("Form", " s", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "Blur Background", None, -1))
        self.collectBgBtn.setText(QtWidgets.QApplication.translate("Form", "Collect Background", None, -1))
        self.subtractBgBtn.setText(QtWidgets.QApplication.translate("Form", "Subtract", None, -1))
        self.divideBgBtn.setToolTip(QtWidgets.QApplication.translate("Form", "Enables background division. \n"
"Either a set of static background frames need to have already by collected\n"
"(by pressing \'Static\' above) or \'Continuous\' needs to be pressed.", None, -1))
        self.divideBgBtn.setText(QtWidgets.QApplication.translate("Form", "Divide", None, -1))
        self.contAvgBgCheck.setText(QtWidgets.QApplication.translate("Form", "Continuous Average", None, -1))

