"""
/***************************************************************************
LoadThemAll
A QGIS plugin
Loads files stored in a directory structure recursively, based on several filters
                             -------------------
begin                : 2010-10-03
copyright            : (C) 2010 by Germán Carrillo (GeoTux)
email                : gcarrillo@linuxmail.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (Qt,
                              QSettings)
from qgis.PyQt.QtWidgets import (QApplication,
                                 QDialog,
                                 QFileDialog)

from ..core.FileFormatConfiguration import VECTOR_FORMATS, RASTER_FORMATS
from ..ui.Ui_Base_LoadThemAll import Ui_Base_LoadThemAll


class BaseLoadThemAllDialog(QDialog, Ui_Base_LoadThemAll):
    """ A generic class to be reused in vector and raster dialogs """

    def __init__(self, isVector, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.isVector = isVector  # To know if it should be started with vector parameters
        self.loadFormats(self.isVector)
        self.loadDateComparisons()
        self.btnBaseDir.clicked.connect(self.selectDir)
        self.btnLoadExtent.clicked.connect(self.updateExtentFromCanvas)
        self.cboDateComparison.currentIndexChanged.connect(self.updateDateFormat)
        self.iface = iface

    def selectDir(self):
        """ Open a dialog for the user to choose a starting directory """
        settings = QSettings()
        path = QFileDialog.getExistingDirectory(self, self.tr("Select a base directory"),
                                                settings.value("/Load_Them_All/vector/path", "",
                                                               type=str) if self.isVector else settings.value(
                                                    "/Load_Them_All/raster/path", "", type=str),
                                                QFileDialog.ShowDirsOnly)

        if path: self.txtBaseDir.setText(path)

    def updateExtentFromCanvas(self):
        canvas = self.iface.mapCanvas()
        boundBox = canvas.extent()
        self.txtXMin.setText(str(boundBox.xMinimum()))
        self.txtYMin.setText(str(boundBox.yMinimum()))
        self.txtXMax.setText(str(boundBox.xMaximum()))
        self.txtYMax.setText(str(boundBox.yMaximum()))

    def loadFormats(self, isVector):
        """ Fill the comboBox with file formats """
        allFormats = VECTOR_FORMATS if isVector else  RASTER_FORMATS
        allExtensions = [extension for format in allFormats for extension in format[1]]
        self.cboFormats.addItem("All listed formats (*.*)", allExtensions)
        for format in allFormats:
            self.cboFormats.addItem(*format)

    def loadDateComparisons(self):
        self.cboDateComparison.addItem(QApplication.translate("Base_LoadThemAllDialog", "Before"), "before")
        self.cboDateComparison.addItem(QApplication.translate("Base_LoadThemAllDialog", "Exact date"), "day")
        self.cboDateComparison.addItem(QApplication.translate("Base_LoadThemAllDialog", "After"), "after")

    def updateDateFormat(self, index):
        comparison = self.cboDateComparison.itemData(index)
        if comparison == 'day':
            self.dtDateTime.setDisplayFormat("ddd dd MMM yyyy")
        else:  # 'before' or 'after'
            self.dtDateTime.setDisplayFormat("ddd dd MMM yyyy hh:mm AP")

    def keyPressEvent(self, e):
        """ Handle the ESC key to avoid only the base dialog being closed """
        if e.key() == Qt.Key_Escape:
            e.ignore()
