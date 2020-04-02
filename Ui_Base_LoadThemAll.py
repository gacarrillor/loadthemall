# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Base_LoadThemAll.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Base_LoadThemAll(object):
    def setupUi(self, Base_LoadThemAll):
        Base_LoadThemAll.setObjectName("Base_LoadThemAll")
        Base_LoadThemAll.resize(375, 488)
        self.gridLayout = QtWidgets.QGridLayout(Base_LoadThemAll)
        self.gridLayout.setObjectName("gridLayout")
        self.btnBaseDir = QtWidgets.QPushButton(Base_LoadThemAll)
        self.btnBaseDir.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/loadthemall/dir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBaseDir.setIcon(icon)
        self.btnBaseDir.setIconSize(QtCore.QSize(22, 22))
        self.btnBaseDir.setObjectName("btnBaseDir")
        self.gridLayout.addWidget(self.btnBaseDir, 0, 0, 1, 1)
        self.txtBaseDir = QtWidgets.QLineEdit(Base_LoadThemAll)
        self.txtBaseDir.setObjectName("txtBaseDir")
        self.gridLayout.addWidget(self.txtBaseDir, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Base_LoadThemAll)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cboFormats = QtWidgets.QComboBox(Base_LoadThemAll)
        self.cboFormats.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.cboFormats.setObjectName("cboFormats")
        self.gridLayout.addWidget(self.cboFormats, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.groupBoxAlphanumeric = QtWidgets.QGroupBox(Base_LoadThemAll)
        self.groupBoxAlphanumeric.setCheckable(True)
        self.groupBoxAlphanumeric.setChecked(False)
        self.groupBoxAlphanumeric.setObjectName("groupBoxAlphanumeric")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBoxAlphanumeric)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.chkInvertAlphanumeric = QtWidgets.QCheckBox(self.groupBoxAlphanumeric)
        self.chkInvertAlphanumeric.setObjectName("chkInvertAlphanumeric")
        self.verticalLayout_2.addWidget(self.chkInvertAlphanumeric)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBoxAlphanumeric)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txtFilter = QtWidgets.QLineEdit(self.groupBoxAlphanumeric)
        self.txtFilter.setObjectName("txtFilter")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtFilter)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.splitter = QtWidgets.QSplitter(self.groupBoxAlphanumeric)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.radStarts = QtWidgets.QRadioButton(self.splitter)
        self.radStarts.setObjectName("radStarts")
        self.radAny = QtWidgets.QRadioButton(self.splitter)
        self.radAny.setChecked(True)
        self.radAny.setObjectName("radAny")
        self.radEnds = QtWidgets.QRadioButton(self.splitter)
        self.radEnds.setObjectName("radEnds")
        self.verticalLayout_2.addWidget(self.splitter)
        self.gridLayout.addWidget(self.groupBoxAlphanumeric, 3, 0, 1, 2)
        self.groupBoxBoundingBox = QtWidgets.QGroupBox(Base_LoadThemAll)
        self.groupBoxBoundingBox.setCheckable(True)
        self.groupBoxBoundingBox.setChecked(False)
        self.groupBoxBoundingBox.setObjectName("groupBoxBoundingBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxBoundingBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.txtYMax = QtWidgets.QLineEdit(self.groupBoxBoundingBox)
        self.txtYMax.setMinimumSize(QtCore.QSize(150, 0))
        self.txtYMax.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.txtYMax.setFont(font)
        self.txtYMax.setObjectName("txtYMax")
        self.horizontalLayout_2.addWidget(self.txtYMax)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtXMin = QtWidgets.QLineEdit(self.groupBoxBoundingBox)
        self.txtXMin.setMinimumSize(QtCore.QSize(150, 0))
        self.txtXMin.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.txtXMin.setFont(font)
        self.txtXMin.setObjectName("txtXMin")
        self.horizontalLayout.addWidget(self.txtXMin)
        self.txtXMax = QtWidgets.QLineEdit(self.groupBoxBoundingBox)
        self.txtXMax.setMinimumSize(QtCore.QSize(150, 0))
        self.txtXMax.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.txtXMax.setFont(font)
        self.txtXMax.setObjectName("txtXMax")
        self.horizontalLayout.addWidget(self.txtXMax)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.txtYMin = QtWidgets.QLineEdit(self.groupBoxBoundingBox)
        self.txtYMin.setMinimumSize(QtCore.QSize(150, 0))
        self.txtYMin.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.txtYMin.setFont(font)
        self.txtYMin.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.txtYMin.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txtYMin.setObjectName("txtYMin")
        self.horizontalLayout_3.addWidget(self.txtYMin)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.splitter_2 = QtWidgets.QSplitter(self.groupBoxBoundingBox)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.radContains = QtWidgets.QRadioButton(self.splitter_2)
        self.radContains.setChecked(True)
        self.radContains.setObjectName("radContains")
        self.radIntersects = QtWidgets.QRadioButton(self.splitter_2)
        self.radIntersects.setObjectName("radIntersects")
        self.btnLoadExtent = QtWidgets.QPushButton(self.splitter_2)
        self.btnLoadExtent.setObjectName("btnLoadExtent")
        self.verticalLayout.addWidget(self.splitter_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxBoundingBox, 4, 0, 1, 2)
        self.groupBoxDateModified = QtWidgets.QGroupBox(Base_LoadThemAll)
        self.groupBoxDateModified.setCheckable(True)
        self.groupBoxDateModified.setChecked(False)
        self.groupBoxDateModified.setObjectName("groupBoxDateModified")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBoxDateModified)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cboDateComparison = QtWidgets.QComboBox(self.groupBoxDateModified)
        self.cboDateComparison.setMaximumSize(QtCore.QSize(100, 16777215))
        self.cboDateComparison.setObjectName("cboDateComparison")
        self.horizontalLayout_4.addWidget(self.cboDateComparison)
        self.dtDateTime = QtWidgets.QDateTimeEdit(self.groupBoxDateModified)
        self.dtDateTime.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dtDateTime.setAccelerated(True)
        self.dtDateTime.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dtDateTime.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.dtDateTime.setCalendarPopup(True)
        self.dtDateTime.setObjectName("dtDateTime")
        self.horizontalLayout_4.addWidget(self.dtDateTime)
        self.gridLayout.addWidget(self.groupBoxDateModified, 5, 0, 1, 2)

        self.retranslateUi(Base_LoadThemAll)
        QtCore.QMetaObject.connectSlotsByName(Base_LoadThemAll)

    def retranslateUi(self, Base_LoadThemAll):
        _translate = QtCore.QCoreApplication.translate
        Base_LoadThemAll.setWindowTitle(_translate("Base_LoadThemAll", "Dialog"))
        self.btnBaseDir.setToolTip(_translate("Base_LoadThemAll", "Select a base directory"))
        self.label_2.setText(_translate("Base_LoadThemAll", "Format "))
        self.groupBoxAlphanumeric.setTitle(_translate("Base_LoadThemAll", "Alphanumeric filter"))
        self.chkInvertAlphanumeric.setText(_translate("Base_LoadThemAll", "Invert filter (i.e., prepend a logic NOT)"))
        self.label_3.setText(_translate("Base_LoadThemAll", "Filter string"))
        self.radStarts.setText(_translate("Base_LoadThemAll", "Starts with"))
        self.radAny.setText(_translate("Base_LoadThemAll", "In any position"))
        self.radEnds.setText(_translate("Base_LoadThemAll", "Ends with"))
        self.groupBoxBoundingBox.setTitle(_translate("Base_LoadThemAll", "Bounding box filter"))
        self.txtYMax.setPlaceholderText(_translate("Base_LoadThemAll", "North"))
        self.txtXMin.setPlaceholderText(_translate("Base_LoadThemAll", "West"))
        self.txtXMax.setPlaceholderText(_translate("Base_LoadThemAll", "East"))
        self.txtYMin.setPlaceholderText(_translate("Base_LoadThemAll", "South"))
        self.radContains.setText(_translate("Base_LoadThemAll", "Contains"))
        self.radIntersects.setText(_translate("Base_LoadThemAll", "Intersects"))
        self.btnLoadExtent.setText(_translate("Base_LoadThemAll", "Map extent"))
        self.groupBoxDateModified.setTitle(_translate("Base_LoadThemAll", "Date modified filter"))
        self.dtDateTime.setDisplayFormat(_translate("Base_LoadThemAll", "ddd dd MMM yyyy hh:mm AP"))

