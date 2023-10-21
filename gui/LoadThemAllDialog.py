"""
/***************************************************************************
LoadThemAllDialog
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
from qgis.PyQt.QtCore import (QSettings,
                              QDateTime)
from qgis.PyQt.QtWidgets import (QDockWidget,
                                 QMessageBox)
from qgis.core import (QgsRectangle,
                       Qgis)

from .BaseLoadThemAllDialog import BaseLoadThemAllDialog
from ..core.LayerTypes import LayerType
from ..core.LoadConfiguration import LoadConfiguration
from ..core.Filter import (AlphanumericFilter,
                           BoundingBoxFilter,
                           DateModifiedFilter,
                           GeometryTypeFilter,
                           InvertedAlphanumericFilter,
                           RasterTypeFilter)
from ..core.LoadFiles import *
from ..core.Utils import has_point_cloud_provider
from ..ui.Ui_DockWidget import Ui_DockWidget


class LoadThemAllDialog(QDockWidget, Ui_DockWidget):
    def __init__(self, parent, iface):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)

        self.iface = iface
        self.parent = parent
        self.dlgBase = None  # It permits to reuse a base dialog

        # To remember the last tab before a tab switch to save settings
        self.currentTab = 'a'  # a:another, v:vector, r:raster

        self.updateControls()
        self.progressBar.setMinimum(0)
        self.processStatus = True  # To handle a dialog cancel event

        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.chkGroups.stateChanged.connect(self.saveConfigTabSettings)
        self.chkSearchInZIPs.stateChanged.connect(self.saveConfigTabSettings)
        self.chkLayersOff.stateChanged.connect(self.saveConfigTabSettings)
        self.chkDoNotEmpty.stateChanged.connect(self.saveConfigTabSettings)
        self.chkSort.stateChanged.connect(self.saveConfigTabSettings)
        self.chkReverseSort.stateChanged.connect(self.saveConfigTabSettings)
        self.txtNumLayersToConfirm.editingFinished.connect(self.saveConfigTabSettings)
        self.chkCaseInsensitive.stateChanged.connect(self.saveConfigTabSettings)
        self.chkAccentInsensitive.stateChanged.connect(self.saveConfigTabSettings)
        self.chkSearchParentLayer.stateChanged.connect(self.saveConfigTabSettings)
        self.chkAddParentLayerName.stateChanged.connect(self.saveConfigTabSettings)
        self.chkStyles.stateChanged.connect(self.saveConfigTabSettings)
        self.btnHelp.clicked.connect(self.help)
        self.btnLoadLayers.clicked.connect(self.load)
        self.btnCancel.setVisible(False)
        self.btnCancel.clicked.connect(self.cancelLoad)

        if Qgis.versionInt() < 31800 or not has_point_cloud_provider():
            self.tabWidget.widget(2).setEnabled(False)

    def updateControls(self):
        """ Read stored settings and put them into the appropriate tab """
        settings = QSettings()
        if not settings.value("/Load_Them_All/currentTab") is None:
            self.tabWidget.setCurrentIndex(int(settings.value("/Load_Them_All/currentTab")))
        else:
            self.tabWidget.setCurrentIndex(0)

        self.configureTabs(self.tabWidget.currentIndex())

    def tabChanged(self, index):
        """ Save settings from the previous tab and prepare the current one """
        self.progressBar.setValue(0)
        self.saveSettings()  # Save the previous tab settings if it was vector, raster or point cloud
        self.configureTabs(index)

    def configureTabs(self, index):
        if self.tabWidget.tabText(index) == "Vecteur" or \
                self.tabWidget.tabText(index) == "Vector":
            self.currentTab = 'v'
            self.dlgBase = BaseLoadThemAllDialog(LayerType.VECTOR, self.iface)
            self.stackedWidgetVector.addWidget(self.dlgBase)
            self.stackedWidgetVector.setCurrentWidget(self.dlgBase)
        elif self.tabWidget.tabText(index) == "Raster":
            self.currentTab = 'r'
            self.dlgBase = BaseLoadThemAllDialog(LayerType.RASTER, self.iface)
            self.stackedWidgetRaster.addWidget(self.dlgBase)
            self.stackedWidgetRaster.setCurrentWidget(self.dlgBase)
        elif self.tabWidget.tabText(index) == "Point Cloud":
            self.currentTab = 'p'
            self.dlgBase = BaseLoadThemAllDialog(LayerType.POINTCLOUD, self.iface)
            self.stackedWidgetPointCloud.addWidget(self.dlgBase)
            self.stackedWidgetPointCloud.setCurrentWidget(self.dlgBase)
        else:
            self.currentTab = 'a'

        self.restoreControls()

    def apply(self):
        """ Read parameters and create the LoadFiles instance """
        # TODO : Trouver un translation tips pour éviter ce test
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Vector" or \
                self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Vecteur" or \
                self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Raster" or \
                self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Point Cloud":

            # Configuration
            configuration = LoadConfiguration()
            configuration.b_groups = self.chkGroups.isChecked()
            configuration.b_search_in_zip_files = self.chkSearchInZIPs.isChecked()
            configuration.b_layers_off = self.chkLayersOff.isChecked()
            configuration.b_not_empty = self.chkDoNotEmpty.isChecked()
            configuration.b_sort = self.chkSort.isChecked()
            configuration.b_reverse_sort = self.chkReverseSort.isChecked()
            configuration.b_case_insensitive = self.chkCaseInsensitive.isChecked()
            configuration.b_accent_insensitive = self.chkAccentInsensitive.isChecked()
            configuration.b_search_parent_layer = self.chkSearchParentLayer.isChecked()
            configuration.b_add_parent_layer_name = self.chkAddParentLayerName.isChecked()
            configuration.b_styles = self.chkStyles.isChecked()
            n = int(self.txtNumLayersToConfirm.text())
            if n <= 0: n = 50
            configuration.num_layers_to_confirm = n

            baseDir = self.dlgBase.txtBaseDir.text()  # TODO: Adjusted, does it break here?
            # Remove trailing (back)slashes to avoid problemas when comparing paths
            baseDir = baseDir[:-1] if len(baseDir) > 1 and baseDir[-1] == "/" else baseDir
            baseDir = baseDir[:-1] if len(baseDir) > 1 and baseDir[-1] == "\\" else baseDir
            configuration.base_dir = baseDir

            bBoundingBoxFilter = False
            filterList = FilterList()

            if os.path.exists(configuration.base_dir):
                configuration.extension = self.dlgBase.cboFormats.itemData(self.dlgBase.cboFormats.currentIndex())

                # Alphanumeric Filter
                if self.dlgBase.groupBoxAlphanumeric.isChecked() and self.dlgBase.txtFilter.text() != "":
                    filterText = self.dlgBase.txtFilter.text()
                    if self.dlgBase.radStarts.isChecked(): matchType = 'StartsWith'
                    if self.dlgBase.radAny.isChecked(): matchType = 'Any'
                    if self.dlgBase.radEnds.isChecked(): matchType = 'EndsWith'

                    if self.dlgBase.chkInvertAlphanumeric.isChecked():
                        filter = InvertedAlphanumericFilter(matchType, filterText, configuration)
                    else:
                        filter = AlphanumericFilter(matchType, filterText, configuration)
                    filterList.addFilter(filter)

                    if configuration.b_accent_insensitive:
                        try:
                            from unidecode import unidecode
                        except ImportError as e:
                            result = QMessageBox.question(self.iface.mainWindow(),
                                                          self.tr("Accents cannot be ignored!"),
                                                          self.tr("You have chosen to ignore accents in the alphanumeric filter, but first") +
                                                          self.tr(" you need to install the Python library 'unidecode'.\n\n") +
                                                          self.tr("Should we continue loading layers without ignoring accents?"),
                                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
                            if result == QMessageBox.Cancel:
                                return

                # Bounding Box Filter (part 1 out of 2)
                if self.dlgBase.groupBoxBoundingBox.isChecked():
                    if self.dlgBase.txtXMin.text().strip() != "" and self.dlgBase.txtYMin.text().strip() != "" and \
                            self.dlgBase.txtXMax.text().strip() != "" and self.dlgBase.txtYMax.text().strip() != "":
                        try:
                            xMin = float(self.dlgBase.txtXMin.text())
                            yMin = float(self.dlgBase.txtYMin.text())
                            xMax = float(self.dlgBase.txtXMax.text())
                            yMax = float(self.dlgBase.txtYMax.text())
                        except ValueError as e:
                            QMessageBox.warning(self.parent, "Load Them All",
                                                self.tr("The bounding box coordinates are not correct!\n") +
                                                self.tr("Please adjust the bounding box settings."),
                                                QMessageBox.Ok, QMessageBox.Ok)
                            return
                        extent = QgsRectangle(xMin, yMin, xMax, yMax)
                        bBoundingBoxFilter = True
                    else:
                        QMessageBox.warning(self.parent, "Load Them All",
                                            self.tr("Some bounding box coordinates are missing!\n") +
                                            self.tr("Please set all bounding box coordinates."),
                                            QMessageBox.Ok, QMessageBox.Ok)
                        return

                # Date Modified Filter
                if self.dlgBase.groupBoxDateModified.isChecked():
                    datetime = self.dlgBase.dtDateTime.dateTime()
                    comparison = self.dlgBase.cboDateComparison.itemData(self.dlgBase.cboDateComparison.currentIndex())

                    filter = DateModifiedFilter(comparison, datetime)
                    filterList.addFilter(filter)

                # Vector/Raster particular Filters
                loader = None
                if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Vecteur" or \
                        self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Vector":

                    # Vector Type Filter
                    if self.groupBoxGeometryTypeFilter.isChecked() and \
                            not (self.chkPoint.isChecked() and self.chkLine.isChecked() and self.chkPolygon.isChecked()):
                        lstItemTypes = []
                        if self.chkPoint.isChecked(): lstItemTypes.append('Point')
                        if self.chkLine.isChecked(): lstItemTypes.append('Line')
                        if self.chkPolygon.isChecked(): lstItemTypes.append('Polygon')

                        filter = GeometryTypeFilter(lstItemTypes)
                        filterList.addFilter(filter)

                    # Bounding Box Filter (part 2 out of 2)
                    if bBoundingBoxFilter is True:
                        if self.dlgBase.radContains.isChecked():
                            filter = BoundingBoxFilter(LayerType.VECTOR, extent, "contains")
                        else:
                            filter = BoundingBoxFilter(LayerType.VECTOR, extent, "intersects")
                        filterList.addFilter(filter)

                    loader = LoadVectors(self.iface, self.progressBar, configuration)

                elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Raster":

                    # Raster Type Filter
                    if self.groupBoxRasterTypeFilter.isChecked() and \
                            not (self.chkGray.isChecked() and self.chkPalette.isChecked() and self.chkMultiband.isChecked() and self.chkColorLayer.isChecked()):
                        lstItemTypes = []
                        if self.chkGray.isChecked(): lstItemTypes.append('GrayOrUndefined')
                        if self.chkPalette.isChecked(): lstItemTypes.append('Palette')
                        if self.chkMultiband.isChecked(): lstItemTypes.append('Multiband')
                        if self.chkColorLayer.isChecked(): lstItemTypes.append('ColorLayer')

                        if not lstItemTypes:
                            QMessageBox.warning(self.parent, "Load Them All",
                                                self.tr("No layer will match the filter!\n") +
                                                self.tr("Select a raster type or uncheck the Raster type filter."),
                                                QMessageBox.Ok, QMessageBox.Ok)
                            return

                        filter = RasterTypeFilter(lstItemTypes)
                        filterList.addFilter(filter)

                    # Bounding Box Filter (part 2 out of 2)
                    if bBoundingBoxFilter is True:
                        if self.dlgBase.radContains.isChecked():
                            filter = BoundingBoxFilter(LayerType.RASTER, extent, "contains")
                        else:
                            filter = BoundingBoxFilter(LayerType.RASTER, extent, "intersects")
                        filterList.addFilter(filter)

                    loader = LoadRasters(self.iface, self.progressBar, configuration)

                elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Point Cloud":

                    crs = None
                    if self.groupBoxPointCloudsCrs.isChecked():
                        temp_crs = self.pointCloudCrs.crs()
                        if temp_crs.isValid():
                            crs = self.pointCloudCrs.crs()

                    # Bounding Box Filter (part 2 out of 2)
                    if bBoundingBoxFilter is True:
                        if self.dlgBase.radContains.isChecked():
                            filter = BoundingBoxFilter(LayerType.POINTCLOUD, extent, "contains")
                        else:
                            filter = BoundingBoxFilter(LayerType.POINTCLOUD, extent, "intersects")
                        filterList.addFilter(filter)

                    loader = LoadPointClouds(self.iface, self.progressBar, configuration)
                    if crs:
                        loader.set_default_crs(crs)

                if loader:
                    loader.filterList = filterList
                    loader.loadLayers()

            else:
                QMessageBox.warning(self.parent, "Load Them All",
                                    self.tr("The specified directory could not be found!\n") +
                                    self.tr("Please select an existing directory."),
                                    QMessageBox.Ok, QMessageBox.Ok)

    def load(self):
        """ Protect the Load Layers button and apply """
        self.processStatus = True  # To handle a dialog cancel event

        settings = QSettings()
        # Take the "CRS for new layers" config, overwrite it while loading layers and...
        oldProjValue = settings.value("/Projections/defaultBehaviour", "prompt", type=str)
        settings.setValue("/Projections/defaultBehaviour", "useProject")

        self.btnLoadLayers.setVisible(False)
        self.btnCancel.setVisible(True)
        self.apply()
        self.btnCancel.setVisible(False)
        self.btnLoadLayers.setVisible(True)

        # ... then set the "CRS for new layers" back
        settings.setValue("/Projections/defaultBehaviour", oldProjValue)

        self.saveSettings()

    def cancelLoad(self):
        self.processStatus = False  # To handle a dialog cancel event
        self.progressBar.reset()
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.iface.messageBar().pushMessage("Load Them All",
                                            "You have just cancelled the loading process.", duration=15)
        self.btnCancel.setVisible(False)
        self.btnLoadLayers.setVisible(True)

    def help(self):
        """ Open a browser to get help """
        import webbrowser
        webbrowser.open("https://github.com/gacarrillor/loadthemall/blob/master/README.md")

    def closeEvent(self, e):
        """ Do some actions before closing the dialog """
        settings = QSettings()
        settings.setValue("/Load_Them_All/currentTab", self.tabWidget.currentIndex())
        self.saveSettings()

    def saveConfigTabSettings(self):
        """ The configuration tab is special, so it needs to save parameters separately """
        settings = QSettings()
        settings.beginGroup("/Load_Them_All/config")
        settings.setValue("groups", self.chkGroups.isChecked())
        settings.setValue("searchInZIPs", self.chkSearchInZIPs.isChecked())
        settings.setValue("layersOff", self.chkLayersOff.isChecked())
        settings.setValue("doNotEmpty", self.chkDoNotEmpty.isChecked())

        sortChecked = self.chkSort.isChecked()
        settings.setValue("sort", sortChecked)
        self.chkReverseSort.setEnabled(sortChecked)
        settings.setValue("reverseSortEnabled", sortChecked)

        settings.setValue("reverseSort", self.chkReverseSort.isChecked())
        settings.setValue("caseInsensitive", self.chkCaseInsensitive.isChecked())
        settings.setValue("accentInsensitive", self.chkAccentInsensitive.isChecked())
        settings.setValue("searchParentLayer", self.chkSearchParentLayer.isChecked())
        settings.setValue("addParentLayerName", self.chkAddParentLayerName.isChecked())
        settings.setValue("styles", self.chkStyles.isChecked())
        n = int(self.txtNumLayersToConfirm.text())
        if n <= 0: n = 50
        settings.setValue("numLayersToConfirm", n)
        settings.endGroup()

    def saveBaseSettings(self, settings):
        """ Settings of the base dialog """
        settings.setValue("path", self.dlgBase.txtBaseDir.text())
        settings.setValue("extension", self.dlgBase.cboFormats.currentIndex())
        settings.setValue("alphaNumericFilter", self.dlgBase.groupBoxAlphanumeric.isChecked())
        settings.setValue("invertAlphaNumericFilter", self.dlgBase.chkInvertAlphanumeric.isChecked())
        settings.setValue("filterText", self.dlgBase.txtFilter.text())
        settings.setValue("boundingBoxFilter", self.dlgBase.groupBoxBoundingBox.isChecked())
        settings.setValue("dateModifiedFilter", self.dlgBase.groupBoxDateModified.isChecked())
        settings.setValue("dateComparisonType", self.dlgBase.cboDateComparison.currentIndex())
        settings.setValue("comparisonDate", str(self.dlgBase.dtDateTime.dateTime().toString()))
        if self.dlgBase.radStarts.isChecked(): settings.setValue("matchType", 'StartsWith')
        if self.dlgBase.radAny.isChecked(): settings.setValue("matchType", 'Any')
        if self.dlgBase.radEnds.isChecked(): settings.setValue("matchType", 'EndsWith')
        settings.setValue("xMin", self.dlgBase.txtXMin.text())
        settings.setValue("yMin", self.dlgBase.txtYMin.text())
        settings.setValue("xMax", self.dlgBase.txtXMax.text())
        settings.setValue("yMax", self.dlgBase.txtYMax.text())
        if self.dlgBase.radContains.isChecked(): settings.setValue("boundingBoxMethod", 'contains')
        if self.dlgBase.radIntersects.isChecked(): settings.setValue("boundingBoxMethod", 'intersects')

    def saveSettings(self):
        """ Read and save parameters in Qt persistent settings """
        settings = QSettings()

        if self.currentTab == 'v':  # Vector parameters
            settings.beginGroup("/Load_Them_All/vector")
            self.saveBaseSettings(settings)
            settings.setValue("geometryTypeFilter", self.groupBoxGeometryTypeFilter.isChecked())
            settings.setValue("Point", self.chkPoint.isChecked())
            settings.setValue("Line", self.chkLine.isChecked())
            settings.setValue("Polygon", self.chkPolygon.isChecked())
            settings.endGroup()
        elif self.currentTab == 'r':  # Raster parameters
            settings.beginGroup("/Load_Them_All/raster")
            self.saveBaseSettings(settings)
            settings.setValue("rasterTypeFilter", self.groupBoxRasterTypeFilter.isChecked())
            settings.setValue("GrayOrUndefined", self.chkGray.isChecked())
            settings.setValue("Palette", self.chkPalette.isChecked())
            settings.setValue("Multiband", self.chkMultiband.isChecked())
            settings.setValue("ColorLayer", self.chkColorLayer.isChecked())
            settings.endGroup()
        elif self.currentTab == 'p':  # Point Cloud parameters
            settings.beginGroup("/Load_Them_All/pointcloud")
            self.saveBaseSettings(settings)
            settings.endGroup()

    def restoreBaseSettings(self, settings):
        """ Restore settings of the base dialog """
        if not settings.value("path") is None:
            self.dlgBase.txtBaseDir.setText(settings.value("path", type=str))
        else:
            self.dlgBase.txtBaseDir.setText('')
        if not settings.value("extension") is None:
            self.dlgBase.cboFormats.setCurrentIndex(settings.value("extension", type=int))
        else:
            self.dlgBase.cboFormats.setCurrentIndex(0)
        if not settings.value("alphaNumericFilter") is None:
            self.dlgBase.groupBoxAlphanumeric.setChecked(settings.value("alphaNumericFilter", type=bool))
        else:
            self.dlgBase.groupBoxAlphanumeric.setChecked(False)
        if not settings.value("invertAlphaNumericFilter") is None:
            self.dlgBase.chkInvertAlphanumeric.setChecked(settings.value("invertAlphaNumericFilter", type=bool))
        else:
            self.dlgBase.chkInvertAlphanumeric.setChecked(False)
        if not settings.value("filterText") is None:
            self.dlgBase.txtFilter.setText(settings.value("filterText", type=str))
        else:
            self.dlgBase.txtFilter.setText('')
        if not settings.value("matchType") is None:
            if str(settings.value("matchType")) == 'StartsWith': self.dlgBase.radStarts.setChecked(True)
            if str(settings.value("matchType")) == 'Any': self.dlgBase.radAny.setChecked(True)
            if str(settings.value("matchType")) == 'EndsWith': self.dlgBase.radEnds.setChecked(True)

        if not settings.value("boundingBoxFilter") is None:
            self.dlgBase.groupBoxBoundingBox.setChecked(settings.value("boundingBoxFilter", type=bool))
        else:
            self.dlgBase.groupBoxBoundingBox.setChecked(False)
        if not settings.value("xMin") is None:
            self.dlgBase.txtXMin.setText(settings.value("xMin", type=str))
        else:
            self.dlgBase.txtXMin.setText('')
        if not settings.value("xMax") is None:
            self.dlgBase.txtXMax.setText(settings.value("xMax", type=str))
        else:
            self.dlgBase.txtXMax.setText('')
        if not settings.value("yMin") is None:
            self.dlgBase.txtYMin.setText(settings.value("yMin", type=str))
        else:
            self.dlgBase.txtYMin.setText('')
        if not settings.value("yMax") is None:
            self.dlgBase.txtYMax.setText(settings.value("yMax", type=str))
        else:
            self.dlgBase.txtYMax.setText('')
        if not settings.value("boundingBoxMethod") is None:
            if str(settings.value("boundingBoxMethod")) == 'contains': self.dlgBase.radContains.setChecked(True)
            if str(settings.value("boundingBoxMethod")) == 'intersects': self.dlgBase.radIntersects.setChecked(True)

        if not settings.value("dateModifiedFilter") is None:
            self.dlgBase.groupBoxDateModified.setChecked(settings.value("dateModifiedFilter", type=bool))
        else:
            self.dlgBase.groupBoxDateModified.setChecked(False)
        if not settings.value("dateComparisonType") is None:
            self.dlgBase.cboDateComparison.setCurrentIndex(settings.value("dateComparisonType", type=int))
        else:
            self.dlgBase.cboDateComparison.setCurrentIndex(0)
        if not settings.value("comparisonDate") is None:
            self.dlgBase.dtDateTime.setDateTime(QDateTime().fromString(settings.value("comparisonDate", type=str)))
        else:
            self.dlgBase.dtDateTime.setDateTime(QDateTime().currentDateTime())

    def restoreControls(self):
        """ Read Qt settings and restore controls """
        settings = QSettings()

        # Configuration
        settings.beginGroup("/Load_Them_All/config")
        if not settings.value("groups") is None:
            self.chkGroups.setChecked(settings.value("groups", type=bool))
        else:
            self.chkGroups.setChecked(False)
        if not settings.value("searchInZIPs") is None:
            self.chkSearchInZIPs.setChecked(settings.value("searchInZIPs", type=bool))
        else:
            self.chkSearchInZIPs.setChecked(False)
        if not settings.value("layersOff") is None:
            self.chkLayersOff.setChecked(settings.value("layersOff", type=bool))
        else:
            self.chkLayersOff.setChecked(False)
        if not settings.value("doNotEmpty") is None:
            self.chkDoNotEmpty.setChecked(settings.value("doNotEmpty", type=bool))
        else:
            self.chkDoNotEmpty.setChecked(True)
        if not settings.value("sort") is None:
            self.chkSort.setChecked(settings.value("sort", type=bool))
        else:
            self.chkSort.setChecked(True)
        if not settings.value("reverseSort") is None:
            self.chkReverseSort.setChecked(settings.value("reverseSort", type=bool))
        else:
            self.chkReverseSort.setChecked(False)
        if not settings.value("reverseSortEnabled") is None:
            self.chkReverseSort.setEnabled(settings.value("reverseSortEnabled", type=bool))
        else:
            self.chkReverseSort.setEnabled(True)
        if not settings.value("caseInsensitive") is None:
            self.chkCaseInsensitive.setChecked(settings.value("caseInsensitive", type=bool))
        else:
            self.chkCaseInsensitive.setChecked(True)
        if not settings.value("accentInsensitive") is None:
            self.chkAccentInsensitive.setChecked(settings.value("accentInsensitive", type=bool))
        else:
            self.chkAccentInsensitive.setChecked(False)
        if not settings.value("searchParentLayer") is None:
            self.chkSearchParentLayer.setChecked(settings.value("searchParentLayer", type=bool))
        else:
            self.chkSearchParentLayer.setChecked(False)
        if not settings.value("addParentLayerName") is None:
            self.chkAddParentLayerName.setChecked(settings.value("addParentLayerName", type=bool))
        else:
            self.chkAddParentLayerName.setChecked(True)
        if not settings.value("styles") is None:
            self.chkStyles.setChecked(settings.value("styles", type=bool))
        else:
            self.chkStyles.setChecked(False)

        if not settings.value("numLayersToConfirm") is None:
            n = int(settings.value("numLayersToConfirm"))
        else:
            n = 50
        self.txtNumLayersToConfirm.setText(str(n))
        settings.endGroup()

        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Vecteur" or \
                self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Vector":
            settings.beginGroup("/Load_Them_All/vector")
            self.restoreBaseSettings(settings)

            if not settings.value("geometryTypeFilter") is None:
                self.groupBoxGeometryTypeFilter.setChecked(settings.value("geometryTypeFilter", type=bool))
            else:
                self.groupBoxGeometryTypeFilter.setChecked(False)
            if not settings.value("Point") is None:
                self.chkPoint.setChecked(settings.value("Point", type=bool))
            else:
                self.chkPoint.setChecked(False)
            if not settings.value("Line") is None:
                self.chkLine.setChecked(settings.value("Line", type=bool))
            else:
                self.chkLine.setChecked(False)
            if not settings.value("Polygon") is None:
                self.chkPolygon.setChecked(settings.value("Polygon", type=bool))
            else:
                self.chkPolygon.setChecked(False)
            settings.endGroup()
            self.btnLoadLayers.setEnabled(True)

        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Raster":
            settings.beginGroup("/Load_Them_All/raster")
            self.restoreBaseSettings(settings)

            if not settings.value("rasterTypeFilter") is None:
                self.groupBoxRasterTypeFilter.setChecked(settings.value("rasterTypeFilter", type=bool))
            else:
                self.groupBoxRasterTypeFilter.setChecked(False)
            if not settings.value("GrayOrUndefined") is None:
                self.chkGray.setChecked(settings.value("GrayOrUndefined", type=bool))
            else:
                self.chkGray.setChecked(False)
            if not settings.value("Palette") is None:
                self.chkPalette.setChecked(settings.value("Palette", type=bool))
            else:
                self.chkPalette.setChecked(False)
            if not settings.value("Multiband") is None:
                self.chkMultiband.setChecked(settings.value("Multiband", type=bool))
            else:
                self.chkMultiband.setChecked(False)
            if not settings.value("ColorLayer") is None:
                self.chkColorLayer.setChecked(settings.value("ColorLayer", type=bool))
            else:
                self.chkColorLayer.setChecked(False)
            settings.endGroup()
            self.btnLoadLayers.setEnabled(True)

        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Point Cloud":
            settings.beginGroup("/Load_Them_All/pointcloud")
            self.restoreBaseSettings(settings)
            settings.endGroup()
            self.btnLoadLayers.setEnabled(True)

        else:
            self.btnLoadLayers.setEnabled(False)
