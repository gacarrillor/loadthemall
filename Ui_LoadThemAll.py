# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_LoadThemAll.ui'
#
# Created: Sun Jan 18 11:07:18 2015
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LoadThemAll(object):
    def setupUi(self, LoadThemAll):
        LoadThemAll.setObjectName(_fromUtf8("LoadThemAll"))
        LoadThemAll.resize(400, 514)
        self.verticalLayout = QtGui.QVBoxLayout(LoadThemAll)
        self.verticalLayout.setMargin(9)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(LoadThemAll)
        self.tabWidget.setMaximumSize(QtCore.QSize(382, 16777215))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabVector = QtGui.QWidget()
        self.tabVector.setObjectName(_fromUtf8("tabVector"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tabVector)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.stackedWidgetVector = QtGui.QStackedWidget(self.tabVector)
        self.stackedWidgetVector.setMinimumSize(QtCore.QSize(0, 345))
        self.stackedWidgetVector.setObjectName(_fromUtf8("stackedWidgetVector"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.stackedWidgetVector.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.stackedWidgetVector.addWidget(self.page_2)
        self.gridLayout_6.addWidget(self.stackedWidgetVector, 0, 0, 1, 1)
        self.groupBoxGeometryTypeFilter = QtGui.QGroupBox(self.tabVector)
        self.groupBoxGeometryTypeFilter.setCheckable(True)
        self.groupBoxGeometryTypeFilter.setChecked(False)
        self.groupBoxGeometryTypeFilter.setObjectName(_fromUtf8("groupBoxGeometryTypeFilter"))
        self.gridLayout = QtGui.QGridLayout(self.groupBoxGeometryTypeFilter)
        self.gridLayout.setContentsMargins(9, 9, -1, 9)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkPolygon = QtGui.QCheckBox(self.groupBoxGeometryTypeFilter)
        self.chkPolygon.setObjectName(_fromUtf8("chkPolygon"))
        self.gridLayout.addWidget(self.chkPolygon, 0, 3, 1, 1)
        self.chkPoint = QtGui.QCheckBox(self.groupBoxGeometryTypeFilter)
        self.chkPoint.setObjectName(_fromUtf8("chkPoint"))
        self.gridLayout.addWidget(self.chkPoint, 0, 1, 1, 1)
        self.chkLine = QtGui.QCheckBox(self.groupBoxGeometryTypeFilter)
        self.chkLine.setObjectName(_fromUtf8("chkLine"))
        self.gridLayout.addWidget(self.chkLine, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBoxGeometryTypeFilter, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabVector, _fromUtf8(""))
        self.tabRaster = QtGui.QWidget()
        self.tabRaster.setObjectName(_fromUtf8("tabRaster"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabRaster)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.stackedWidgetRaster = QtGui.QStackedWidget(self.tabRaster)
        self.stackedWidgetRaster.setMinimumSize(QtCore.QSize(0, 345))
        self.stackedWidgetRaster.setObjectName(_fromUtf8("stackedWidgetRaster"))
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.stackedWidgetRaster.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.stackedWidgetRaster.addWidget(self.page_4)
        self.verticalLayout_5.addWidget(self.stackedWidgetRaster)
        self.groupBoxRasterTypeFilter = QtGui.QGroupBox(self.tabRaster)
        self.groupBoxRasterTypeFilter.setCheckable(True)
        self.groupBoxRasterTypeFilter.setChecked(False)
        self.groupBoxRasterTypeFilter.setObjectName(_fromUtf8("groupBoxRasterTypeFilter"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxRasterTypeFilter)
        self.gridLayout_2.setContentsMargins(5, 9, -1, 9)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.chkGray = QtGui.QCheckBox(self.groupBoxRasterTypeFilter)
        self.chkGray.setObjectName(_fromUtf8("chkGray"))
        self.gridLayout_2.addWidget(self.chkGray, 0, 1, 1, 1)
        self.chkPalette = QtGui.QCheckBox(self.groupBoxRasterTypeFilter)
        self.chkPalette.setObjectName(_fromUtf8("chkPalette"))
        self.gridLayout_2.addWidget(self.chkPalette, 0, 2, 1, 1)
        self.chkMultiband = QtGui.QCheckBox(self.groupBoxRasterTypeFilter)
        self.chkMultiband.setObjectName(_fromUtf8("chkMultiband"))
        self.gridLayout_2.addWidget(self.chkMultiband, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBoxRasterTypeFilter)
        self.tabWidget.addTab(self.tabRaster, _fromUtf8(""))
        self.tabConfiguration = QtGui.QWidget()
        self.tabConfiguration.setObjectName(_fromUtf8("tabConfiguration"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabConfiguration)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setMargin(9)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem2)
        self.chkGroups = QtGui.QCheckBox(self.tabConfiguration)
        self.chkGroups.setMaximumSize(QtCore.QSize(315, 16777215))
        self.chkGroups.setChecked(True)
        self.chkGroups.setObjectName(_fromUtf8("chkGroups"))
        self.verticalLayout_2.addWidget(self.chkGroups)
        self.chkLayersOff = QtGui.QCheckBox(self.tabConfiguration)
        self.chkLayersOff.setMaximumSize(QtCore.QSize(315, 16777215))
        self.chkLayersOff.setChecked(True)
        self.chkLayersOff.setObjectName(_fromUtf8("chkLayersOff"))
        self.verticalLayout_2.addWidget(self.chkLayersOff)
        self.chkDoNotEmpty = QtGui.QCheckBox(self.tabConfiguration)
        self.chkDoNotEmpty.setChecked(True)
        self.chkDoNotEmpty.setObjectName(_fromUtf8("chkDoNotEmpty"))
        self.verticalLayout_2.addWidget(self.chkDoNotEmpty)
        self.chkIsDoneDialog = QtGui.QCheckBox(self.tabConfiguration)
        self.chkIsDoneDialog.setMaximumSize(QtCore.QSize(315, 16777215))
        self.chkIsDoneDialog.setChecked(True)
        self.chkIsDoneDialog.setObjectName(_fromUtf8("chkIsDoneDialog"))
        self.verticalLayout_2.addWidget(self.chkIsDoneDialog)
        self.groupBox = QtGui.QGroupBox(self.tabConfiguration)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 60))
        self.groupBox.setMaximumSize(QtCore.QSize(315, 80))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.txtNumLayersToConfirm = QtGui.QLineEdit(self.groupBox)
        self.txtNumLayersToConfirm.setMaximumSize(QtCore.QSize(50, 25))
        self.txtNumLayersToConfirm.setObjectName(_fromUtf8("txtNumLayersToConfirm"))
        self.horizontalLayout_2.addWidget(self.txtNumLayersToConfirm)
        self.label_6 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.chkCaseInsensitive = QtGui.QCheckBox(self.tabConfiguration)
        self.chkCaseInsensitive.setChecked(True)
        self.chkCaseInsensitive.setObjectName(_fromUtf8("chkCaseInsensitive"))
        self.verticalLayout_2.addWidget(self.chkCaseInsensitive)
        self.chkAccentInsensitive = QtGui.QCheckBox(self.tabConfiguration)
        self.chkAccentInsensitive.setChecked(False)
        self.chkAccentInsensitive.setObjectName(_fromUtf8("chkAccentInsensitive"))
        self.verticalLayout_2.addWidget(self.chkAccentInsensitive)
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.setStretch(1, 1)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabConfiguration, _fromUtf8(""))
        self.tabAbout = QtGui.QWidget()
        self.tabAbout.setObjectName(_fromUtf8("tabAbout"))
        self.formLayout = QtGui.QFormLayout(self.tabAbout)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtGui.QFormLayout.LabelRole, spacerItem4)
        self.label_4 = QtGui.QLabel(self.tabAbout)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.label_4)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtGui.QFormLayout.LabelRole, spacerItem5)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 0, 0, 1, 1)
        self.btnHelp = QtGui.QPushButton(self.tabAbout)
        self.btnHelp.setObjectName(_fromUtf8("btnHelp"))
        self.gridLayout_5.addWidget(self.btnHelp, 0, 1, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem7, 0, 2, 1, 1)
        self.formLayout.setLayout(3, QtGui.QFormLayout.SpanningRole, self.gridLayout_5)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(4, QtGui.QFormLayout.LabelRole, spacerItem8)
        self.label_5 = QtGui.QLabel(self.tabAbout)
        self.label_5.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(_fromUtf8("font:10pt \"Sans Serif\";"))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.label_5)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(6, QtGui.QFormLayout.LabelRole, spacerItem9)
        self.label_2 = QtGui.QLabel(self.tabAbout)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loadthemall/logo_80x94.png")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, -1, -1, -1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem10)
        self.label = QtGui.QLabel(self.tabAbout)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("font: 8pt \"Sans Serif\";"))
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.label_3 = QtGui.QLabel(self.tabAbout)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("font: 8pt \"Sans Serif\";"))
        self.label_3.setWordWrap(True)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        spacerItem11 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout_3.addItem(spacerItem11)
        self.label_7 = QtGui.QLabel(self.tabAbout)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(_fromUtf8("font: 8pt \"Sans Serif\";"))
        self.label_7.setWordWrap(True)
        self.label_7.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_3.addWidget(self.label_7)
        spacerItem12 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem12)
        self.formLayout.setLayout(7, QtGui.QFormLayout.FieldRole, self.verticalLayout_3)
        self.tabWidget.addTab(self.tabAbout, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBar = QtGui.QProgressBar(LoadThemAll)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(LoadThemAll)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LoadThemAll)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LoadThemAll.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LoadThemAll.reject)
        QtCore.QMetaObject.connectSlotsByName(LoadThemAll)

    def retranslateUi(self, LoadThemAll):
        LoadThemAll.setWindowTitle(QtGui.QApplication.translate("LoadThemAll", "Load Them All - v.2.3", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxGeometryTypeFilter.setTitle(QtGui.QApplication.translate("LoadThemAll", "Geometry type filter", None, QtGui.QApplication.UnicodeUTF8))
        self.chkPolygon.setText(QtGui.QApplication.translate("LoadThemAll", "Polygon", None, QtGui.QApplication.UnicodeUTF8))
        self.chkPoint.setText(QtGui.QApplication.translate("LoadThemAll", "Point", None, QtGui.QApplication.UnicodeUTF8))
        self.chkLine.setText(QtGui.QApplication.translate("LoadThemAll", "Line", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVector), QtGui.QApplication.translate("LoadThemAll", "Vector", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxRasterTypeFilter.setTitle(QtGui.QApplication.translate("LoadThemAll", "Raster type filter", None, QtGui.QApplication.UnicodeUTF8))
        self.chkGray.setText(QtGui.QApplication.translate("LoadThemAll", "Gray or Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.chkPalette.setText(QtGui.QApplication.translate("LoadThemAll", "Palette", None, QtGui.QApplication.UnicodeUTF8))
        self.chkMultiband.setText(QtGui.QApplication.translate("LoadThemAll", "Multiband", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRaster), QtGui.QApplication.translate("LoadThemAll", "Raster", None, QtGui.QApplication.UnicodeUTF8))
        self.chkGroups.setText(QtGui.QApplication.translate("LoadThemAll", "Create groups based on directories\' names", None, QtGui.QApplication.UnicodeUTF8))
        self.chkLayersOff.setText(QtGui.QApplication.translate("LoadThemAll", "Turn off the loaded layers", None, QtGui.QApplication.UnicodeUTF8))
        self.chkDoNotEmpty.setText(QtGui.QApplication.translate("LoadThemAll", "Do not load empty vector layers ", None, QtGui.QApplication.UnicodeUTF8))
        self.chkIsDoneDialog.setText(QtGui.QApplication.translate("LoadThemAll", "Show a dialog when the process is done", None, QtGui.QApplication.UnicodeUTF8))
        self.txtNumLayersToConfirm.setText(QtGui.QApplication.translate("LoadThemAll", "50", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("LoadThemAll", "Number of layers to show you a confirmation dialog before the loading", None, QtGui.QApplication.UnicodeUTF8))
        self.chkCaseInsensitive.setText(QtGui.QApplication.translate("LoadThemAll", "Ignore case in the alphanumeric filter", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAccentInsensitive.setToolTip(QtGui.QApplication.translate("LoadThemAll", "This option requires the Python lib \'unidecode\'", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAccentInsensitive.setText(QtGui.QApplication.translate("LoadThemAll", "Ignore accents in the alphanumeric filter", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConfiguration), QtGui.QApplication.translate("LoadThemAll", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("LoadThemAll", "The <i>Load Them All</i> plugin allows you to load at the same time a number of layers stored in a directory structure, based on a variety of filters you may customize.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnHelp.setText(QtGui.QApplication.translate("LoadThemAll", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("LoadThemAll", "Feel free to report bugs, suggest improvements or say hello at geotux_tuxman@linuxmail.org ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoadThemAll", "Copyright (C) 2010-2015 Germán Carrillo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("LoadThemAll", "<i>Licensed under the terms of GNU GPL 2</i>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("LoadThemAll", "<html><head/><body><p><span style=\" font-style:italic;\">Code contributors:</span><br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;David Bakeman (v.2.1)<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Soeren Gebbert (v.2.3)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAbout), QtGui.QApplication.translate("LoadThemAll", "About", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc