# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './lib/util/pyqtgraph/plotConfigTemplate.ui'
#
# Created: Wed Aug 17 13:49:55 2011
#      by: pyside-uic 0.2.11 running on PySide 1.0.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(250, 340)
        Form.setMaximumSize(QtCore.QSize(250, 350))
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.xManualRadio = QtGui.QRadioButton(self.groupBox)
        self.xManualRadio.setObjectName("xManualRadio")
        self.gridLayout.addWidget(self.xManualRadio, 0, 0, 1, 1)
        self.xMinText = QtGui.QLineEdit(self.groupBox)
        self.xMinText.setObjectName("xMinText")
        self.gridLayout.addWidget(self.xMinText, 0, 1, 1, 1)
        self.xMaxText = QtGui.QLineEdit(self.groupBox)
        self.xMaxText.setObjectName("xMaxText")
        self.gridLayout.addWidget(self.xMaxText, 0, 2, 1, 1)
        self.xAutoRadio = QtGui.QRadioButton(self.groupBox)
        self.xAutoRadio.setChecked(True)
        self.xAutoRadio.setObjectName("xAutoRadio")
        self.gridLayout.addWidget(self.xAutoRadio, 1, 0, 1, 1)
        self.xAutoPercentSpin = QtGui.QSpinBox(self.groupBox)
        self.xAutoPercentSpin.setEnabled(True)
        self.xAutoPercentSpin.setMinimum(1)
        self.xAutoPercentSpin.setMaximum(100)
        self.xAutoPercentSpin.setSingleStep(1)
        self.xAutoPercentSpin.setProperty("value", 100)
        self.xAutoPercentSpin.setObjectName("xAutoPercentSpin")
        self.gridLayout.addWidget(self.xAutoPercentSpin, 1, 1, 1, 2)
        self.xLinkCombo = QtGui.QComboBox(self.groupBox)
        self.xLinkCombo.setObjectName("xLinkCombo")
        self.gridLayout.addWidget(self.xLinkCombo, 2, 1, 1, 2)
        self.xMouseCheck = QtGui.QCheckBox(self.groupBox)
        self.xMouseCheck.setChecked(True)
        self.xMouseCheck.setObjectName("xMouseCheck")
        self.gridLayout.addWidget(self.xMouseCheck, 3, 1, 1, 1)
        self.xLogCheck = QtGui.QCheckBox(self.groupBox)
        self.xLogCheck.setObjectName("xLogCheck")
        self.gridLayout.addWidget(self.xLogCheck, 3, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.yManualRadio = QtGui.QRadioButton(self.groupBox_2)
        self.yManualRadio.setObjectName("yManualRadio")
        self.gridLayout_2.addWidget(self.yManualRadio, 0, 0, 1, 1)
        self.yMinText = QtGui.QLineEdit(self.groupBox_2)
        self.yMinText.setObjectName("yMinText")
        self.gridLayout_2.addWidget(self.yMinText, 0, 1, 1, 1)
        self.yMaxText = QtGui.QLineEdit(self.groupBox_2)
        self.yMaxText.setObjectName("yMaxText")
        self.gridLayout_2.addWidget(self.yMaxText, 0, 2, 1, 1)
        self.yAutoRadio = QtGui.QRadioButton(self.groupBox_2)
        self.yAutoRadio.setChecked(True)
        self.yAutoRadio.setObjectName("yAutoRadio")
        self.gridLayout_2.addWidget(self.yAutoRadio, 1, 0, 1, 1)
        self.yAutoPercentSpin = QtGui.QSpinBox(self.groupBox_2)
        self.yAutoPercentSpin.setEnabled(True)
        self.yAutoPercentSpin.setMinimum(1)
        self.yAutoPercentSpin.setMaximum(100)
        self.yAutoPercentSpin.setSingleStep(1)
        self.yAutoPercentSpin.setProperty("value", 100)
        self.yAutoPercentSpin.setObjectName("yAutoPercentSpin")
        self.gridLayout_2.addWidget(self.yAutoPercentSpin, 1, 1, 1, 2)
        self.yLinkCombo = QtGui.QComboBox(self.groupBox_2)
        self.yLinkCombo.setObjectName("yLinkCombo")
        self.gridLayout_2.addWidget(self.yLinkCombo, 2, 1, 1, 2)
        self.yMouseCheck = QtGui.QCheckBox(self.groupBox_2)
        self.yMouseCheck.setChecked(True)
        self.yMouseCheck.setObjectName("yMouseCheck")
        self.gridLayout_2.addWidget(self.yMouseCheck, 3, 1, 1, 1)
        self.yLogCheck = QtGui.QCheckBox(self.groupBox_2)
        self.yLogCheck.setObjectName("yLogCheck")
        self.gridLayout_2.addWidget(self.yLogCheck, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.powerSpectrumGroup = QtGui.QGroupBox(self.tab_2)
        self.powerSpectrumGroup.setCheckable(True)
        self.powerSpectrumGroup.setChecked(False)
        self.powerSpectrumGroup.setObjectName("powerSpectrumGroup")
        self.verticalLayout_2.addWidget(self.powerSpectrumGroup)
        self.decimateGroup = QtGui.QGroupBox(self.tab_2)
        self.decimateGroup.setCheckable(True)
        self.decimateGroup.setObjectName("decimateGroup")
        self.gridLayout_4 = QtGui.QGridLayout(self.decimateGroup)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.manualDecimateRadio = QtGui.QRadioButton(self.decimateGroup)
        self.manualDecimateRadio.setChecked(True)
        self.manualDecimateRadio.setObjectName("manualDecimateRadio")
        self.gridLayout_4.addWidget(self.manualDecimateRadio, 0, 0, 1, 1)
        self.downsampleSpin = QtGui.QSpinBox(self.decimateGroup)
        self.downsampleSpin.setMinimum(1)
        self.downsampleSpin.setMaximum(100000)
        self.downsampleSpin.setProperty("value", 1)
        self.downsampleSpin.setObjectName("downsampleSpin")
        self.gridLayout_4.addWidget(self.downsampleSpin, 0, 1, 1, 1)
        self.autoDecimateRadio = QtGui.QRadioButton(self.decimateGroup)
        self.autoDecimateRadio.setChecked(False)
        self.autoDecimateRadio.setObjectName("autoDecimateRadio")
        self.gridLayout_4.addWidget(self.autoDecimateRadio, 1, 0, 1, 1)
        self.maxTracesCheck = QtGui.QCheckBox(self.decimateGroup)
        self.maxTracesCheck.setObjectName("maxTracesCheck")
        self.gridLayout_4.addWidget(self.maxTracesCheck, 2, 0, 1, 1)
        self.maxTracesSpin = QtGui.QSpinBox(self.decimateGroup)
        self.maxTracesSpin.setObjectName("maxTracesSpin")
        self.gridLayout_4.addWidget(self.maxTracesSpin, 2, 1, 1, 1)
        self.forgetTracesCheck = QtGui.QCheckBox(self.decimateGroup)
        self.forgetTracesCheck.setObjectName("forgetTracesCheck")
        self.gridLayout_4.addWidget(self.forgetTracesCheck, 3, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.decimateGroup)
        self.averageGroup = QtGui.QGroupBox(self.tab_2)
        self.averageGroup.setCheckable(True)
        self.averageGroup.setChecked(False)
        self.averageGroup.setObjectName("averageGroup")
        self.gridLayout_5 = QtGui.QGridLayout(self.averageGroup)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.avgParamList = QtGui.QListWidget(self.averageGroup)
        self.avgParamList.setObjectName("avgParamList")
        self.gridLayout_5.addWidget(self.avgParamList, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.averageGroup)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.alphaGroup = QtGui.QGroupBox(self.tab_3)
        self.alphaGroup.setCheckable(True)
        self.alphaGroup.setObjectName("alphaGroup")
        self.horizontalLayout = QtGui.QHBoxLayout(self.alphaGroup)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.autoAlphaCheck = QtGui.QCheckBox(self.alphaGroup)
        self.autoAlphaCheck.setChecked(False)
        self.autoAlphaCheck.setObjectName("autoAlphaCheck")
        self.horizontalLayout.addWidget(self.autoAlphaCheck)
        self.alphaSlider = QtGui.QSlider(self.alphaGroup)
        self.alphaSlider.setMaximum(1000)
        self.alphaSlider.setProperty("value", 1000)
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setObjectName("alphaSlider")
        self.horizontalLayout.addWidget(self.alphaSlider)
        self.verticalLayout_3.addWidget(self.alphaGroup)
        self.gridGroup = QtGui.QGroupBox(self.tab_3)
        self.gridGroup.setCheckable(True)
        self.gridGroup.setChecked(False)
        self.gridGroup.setObjectName("gridGroup")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gridGroup)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridAlphaSlider = QtGui.QSlider(self.gridGroup)
        self.gridAlphaSlider.setMaximum(255)
        self.gridAlphaSlider.setProperty("value", 70)
        self.gridAlphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.gridAlphaSlider.setObjectName("gridAlphaSlider")
        self.verticalLayout_4.addWidget(self.gridAlphaSlider)
        self.verticalLayout_3.addWidget(self.gridGroup)
        self.pointsGroup = QtGui.QGroupBox(self.tab_3)
        self.pointsGroup.setCheckable(True)
        self.pointsGroup.setObjectName("pointsGroup")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.pointsGroup)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.autoPointsCheck = QtGui.QCheckBox(self.pointsGroup)
        self.autoPointsCheck.setChecked(True)
        self.autoPointsCheck.setObjectName("autoPointsCheck")
        self.verticalLayout_5.addWidget(self.autoPointsCheck)
        self.verticalLayout_3.addWidget(self.pointsGroup)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_7 = QtGui.QGridLayout(self.tab_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        spacerItem1 = QtGui.QSpacerItem(59, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.saveSvgBtn = QtGui.QPushButton(self.tab_4)
        self.saveSvgBtn.setObjectName("saveSvgBtn")
        self.gridLayout_6.addWidget(self.saveSvgBtn, 0, 0, 1, 1)
        self.saveImgBtn = QtGui.QPushButton(self.tab_4)
        self.saveImgBtn.setObjectName("saveImgBtn")
        self.gridLayout_6.addWidget(self.saveImgBtn, 1, 0, 1, 1)
        self.saveMaBtn = QtGui.QPushButton(self.tab_4)
        self.saveMaBtn.setObjectName("saveMaBtn")
        self.gridLayout_6.addWidget(self.saveMaBtn, 2, 0, 1, 1)
        self.saveCsvBtn = QtGui.QPushButton(self.tab_4)
        self.saveCsvBtn.setObjectName("saveCsvBtn")
        self.gridLayout_6.addWidget(self.saveCsvBtn, 3, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(59, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 211, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem3, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "X Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.xManualRadio.setText(QtGui.QApplication.translate("Form", "Manual", None, QtGui.QApplication.UnicodeUTF8))
        self.xMinText.setText(QtGui.QApplication.translate("Form", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.xMaxText.setText(QtGui.QApplication.translate("Form", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.xAutoRadio.setText(QtGui.QApplication.translate("Form", "Auto", None, QtGui.QApplication.UnicodeUTF8))
        self.xAutoPercentSpin.setSuffix(QtGui.QApplication.translate("Form", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.xMouseCheck.setText(QtGui.QApplication.translate("Form", "Mouse", None, QtGui.QApplication.UnicodeUTF8))
        self.xLogCheck.setText(QtGui.QApplication.translate("Form", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Link with:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.yManualRadio.setText(QtGui.QApplication.translate("Form", "Manual", None, QtGui.QApplication.UnicodeUTF8))
        self.yMinText.setText(QtGui.QApplication.translate("Form", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.yMaxText.setText(QtGui.QApplication.translate("Form", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.yAutoRadio.setText(QtGui.QApplication.translate("Form", "Auto", None, QtGui.QApplication.UnicodeUTF8))
        self.yAutoPercentSpin.setSuffix(QtGui.QApplication.translate("Form", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.yMouseCheck.setText(QtGui.QApplication.translate("Form", "Mouse", None, QtGui.QApplication.UnicodeUTF8))
        self.yLogCheck.setText(QtGui.QApplication.translate("Form", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Link with:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "Scale", None, QtGui.QApplication.UnicodeUTF8))
        self.powerSpectrumGroup.setTitle(QtGui.QApplication.translate("Form", "Power Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.decimateGroup.setTitle(QtGui.QApplication.translate("Form", "Downsample", None, QtGui.QApplication.UnicodeUTF8))
        self.manualDecimateRadio.setText(QtGui.QApplication.translate("Form", "Manual", None, QtGui.QApplication.UnicodeUTF8))
        self.autoDecimateRadio.setText(QtGui.QApplication.translate("Form", "Auto", None, QtGui.QApplication.UnicodeUTF8))
        self.maxTracesCheck.setToolTip(QtGui.QApplication.translate("Form", "If multiple curves are displayed in this plot, check this box to limit the number of traces that are displayed.", None, QtGui.QApplication.UnicodeUTF8))
        self.maxTracesCheck.setText(QtGui.QApplication.translate("Form", "Max Traces:", None, QtGui.QApplication.UnicodeUTF8))
        self.maxTracesSpin.setToolTip(QtGui.QApplication.translate("Form", "If multiple curves are displayed in this plot, check \"Max Traces\" and set this value to limit the number of traces that are displayed.", None, QtGui.QApplication.UnicodeUTF8))
        self.forgetTracesCheck.setToolTip(QtGui.QApplication.translate("Form", "If MaxTraces is checked, remove curves from memory after they are hidden (saves memory, but traces can not be un-hidden).", None, QtGui.QApplication.UnicodeUTF8))
        self.forgetTracesCheck.setText(QtGui.QApplication.translate("Form", "Forget hidden traces", None, QtGui.QApplication.UnicodeUTF8))
        self.averageGroup.setToolTip(QtGui.QApplication.translate("Form", "Display averages of the curves displayed in this plot. The parameter list allows you to choose parameters to average over (if any are available).", None, QtGui.QApplication.UnicodeUTF8))
        self.averageGroup.setTitle(QtGui.QApplication.translate("Form", "Average", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.alphaGroup.setTitle(QtGui.QApplication.translate("Form", "Alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.autoAlphaCheck.setText(QtGui.QApplication.translate("Form", "Auto", None, QtGui.QApplication.UnicodeUTF8))
        self.gridGroup.setTitle(QtGui.QApplication.translate("Form", "Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.pointsGroup.setTitle(QtGui.QApplication.translate("Form", "Points", None, QtGui.QApplication.UnicodeUTF8))
        self.autoPointsCheck.setText(QtGui.QApplication.translate("Form", "Auto", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Form", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.saveSvgBtn.setText(QtGui.QApplication.translate("Form", "SVG", None, QtGui.QApplication.UnicodeUTF8))
        self.saveImgBtn.setText(QtGui.QApplication.translate("Form", "Image", None, QtGui.QApplication.UnicodeUTF8))
        self.saveMaBtn.setText(QtGui.QApplication.translate("Form", "MetaArray", None, QtGui.QApplication.UnicodeUTF8))
        self.saveCsvBtn.setText(QtGui.QApplication.translate("Form", "CSV", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))

