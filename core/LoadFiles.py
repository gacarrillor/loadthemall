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
import os
import locale
from abc import (ABC,
                 abstractmethod)

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import (QApplication,
                                 QMessageBox)
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsVectorLayer,
                       QgsMapLayer)

from .Filter import FilterList
from .QGISLayerTree import QGISLayerTree
from .Utils import (get_vector_layer,
                    get_raster_layer,
                    get_zip_files_to_load,
                    get_parent_folder)


class LoadFiles(ABC):
    """ Abstract Class to inherit two common methods to Vector and Raster Load classes """

    def __init__(self, iface, progressBar, configuration):
        self.progressBar = progressBar
        self.filterList = FilterList()
        self.iface = iface
        self.files_to_load = dict()  # {'layer_path_1': layer_obj_1, ...}
        self.dataType = ''

        # Configuration parameters
        self.configuration = configuration
        self.tree = QGISLayerTree(configuration.base_dir, configuration.b_groups)

    def loadLayers(self):
        if self._getFilesToLoad():
            self._loadLayers()

    def _applyFilter(self, layer_path, layer_dict):
        """ Method to encapsulate the filter's application  """
        return self.filterList.apply(layer_path, layer_dict)

    def _getFilesToLoad(self):
        """ Go through directories to fill a list with layers ready to be loaded """
        self.progressBar.setMaximum(0)  # ProgressBar in busy mode
        layer_dict = dict()  # {'layer_path_1': layer_obj_1, ...}

        for root, dirs, files in os.walk(self.configuration.base_dir):
            # files = [self.decodeName(f) for f in files]
            for file_ in files:
                QApplication.processEvents()  # TODO: Perhaps better by chunks?
                if self._process_cancelled():
                    return False

                try:  # TODO: do we need this in Python 3?
                    # Nasty file names like those created by malware should be caught and ignored
                    extension = str.lower(str(os.path.splitext(file_)[1]))
                except UnicodeEncodeError as e:
                    extension = None

                if extension in self.configuration.extension or extension == '.zip':
                    # current_layer_path = os.path.join( self.decodeName( root ), file_ )
                    current_layer_path = os.path.join(root, file_)

                    if extension == '.zip':
                        layer_paths = get_zip_files_to_load(current_layer_path, self.configuration.extension)
                    else:
                        layer_paths = [current_layer_path]

                    for layer_path in layer_paths:
                        if self.dataType == 'vector':
                            layer = QgsVectorLayer(layer_path, "", "ogr")
                            if layer.isValid():
                                # Do we have sublayers?
                                if len(layer.dataProvider().subLayers()) > 1:
                                    # Sample: ['0!!::!!line_intersection_collection!!::!!12!!::!!LineString!!::!!geometryProperty']
                                    subLayers = dict()
                                    for subLayer in layer.dataProvider().subLayers():
                                        parts = subLayer.split("!!::!!")  # 1: name, 3: geometry type
                                        # Sublayers might share layer name, we need to get geometry types just in case
                                        if parts[1] in subLayers:
                                            subLayers[parts[1]].append(parts[3])
                                        else:
                                            subLayers[parts[1]] = [parts[3]]

                                    for subLayerName, subLayerGeometries in subLayers.items():
                                        if len(subLayerGeometries) > 1:
                                            for subLayerGeometry in subLayerGeometries:
                                                layer_dict["{}|layername={}|geometrytype={}".format(layer_path,
                                                                                                    subLayerName,
                                                                                                    subLayerGeometry)] = None
                                        else:
                                            layer_dict["{}|layername={}".format(layer_path, subLayerName)] = None
                                else:
                                    layer_dict[layer_path] = layer
                        else:  # 'raster'
                            layer_dict[layer_path] = None

        for path in layer_dict:
            QApplication.processEvents()
            if self._process_cancelled():
                return False

            if self._applyFilter(path, layer_dict):  # The layer passes the filter?
                if self.configuration.b_not_empty:  # Do not load empty layers
                    if not self._isEmptyLayer(path, layer_dict):
                        self.files_to_load[path] = layer_dict.get(path, None)
                else:
                    self.files_to_load[path] = layer_dict.get(path, None)

        self.progressBar.setMaximum(len(self.files_to_load))
        return True

    def _loadLayers(self):
        """ Load the layer to the map """
        if self._process_cancelled():
            return False

        numLayers = len(self.files_to_load)

        if numLayers > 0:
            result = QMessageBox.Ok  # Convenient variable to pass an upcoming condition

            if numLayers >= self.configuration.num_layers_to_confirm:
                result = QMessageBox.question(self.iface.mainWindow(),
                                              QCoreApplication.translate("Load Them All", "Load Them All"),
                                              QCoreApplication.translate("Load Them All",
                                                                         "There are {} layers to load.\n Do you want to continue?").format(
                                                  numLayers),
                                              QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

            if result == QMessageBox.Ok:
                self.iface.mapCanvas().setRenderFlag(False)  # Start the loading process
                step = 0
                layersLoaded = 0

                if self.configuration.b_sort:
                    self.files_to_load = self._sort_layers_to_load()

                for layer_path, layer in self.files_to_load.items():
                    QApplication.processEvents()
                    if self._process_cancelled():
                        self.iface.mapCanvas().setRenderFlag(True)
                        return False

                    # Finally add the layer and apply the options the user chose
                    if self.configuration.b_groups:
                        group = self.tree.add_group(get_parent_folder(layer_path))

                    baseName = os.path.basename(layer_path)
                    layerName = os.path.splitext(baseName)[0]

                    # Let's clear the layer name for sublayers
                    if '|layername=' in baseName and not baseName.endswith('|layername='):
                        subLayerName = baseName.split('|layername=')[1].split('|geometrytype=')[0]
                        if self.configuration.b_add_parent_layer_name:
                            layerName = "".join([layerName, " ", subLayerName])
                        else:
                            layerName = subLayerName

                    ml = self._createLayer(layer_path, layerName, self.files_to_load)
                    if ml.isValid():
                        layersLoaded += 1
                        if self.configuration.b_groups:
                            self.tree.add_layer_to_group(ml, group)
                        else:
                            self.tree.add_layer(ml, self.configuration.b_layers_off)

                        # Look if there is a style to apply
                        bStyleFound = False
                        if self.configuration.b_styles:
                            if self.configuration.b_groups:
                                # Has the group a style to apply?
                                aGroup = os.path.dirname(layer_path)
                                aBaseGroup = os.path.basename(aGroup)
                                styleFile = os.path.join(aGroup, aBaseGroup + ".qml")

                                if os.path.exists(styleFile):
                                    ml.loadNamedStyle(styleFile)
                                    bStyleFound = True
                                    QgsApplication.messageLog().logMessage(
                                        "QML for group '{}' applied to layer '{}'".format(
                                            aBaseGroup, ml.name()), "Load Them All", Qgis.Info)

                            if bStyleFound:
                                self.iface.layerTreeView().refreshLayerSymbology(ml.id())
                            else:
                                QgsApplication.messageLog().logMessage(
                                    "No style found for layer group '{}' or 'create groups' option is disabled!".format(
                                        aBaseGroup), "Load Them All", Qgis.Warning)
                            # End Styles

                    else:
                        QgsApplication.messageLog().logMessage(
                            "Layer '{}' couldn't be created properly and wasn't loaded into QGIS. Is the layer data valid?".format(
                                layer_path),
                            "Load Them All", Qgis.Warning)

                    step += 1
                    self.progressBar.setValue(step)

                if self.configuration.b_groups and self.configuration.b_layers_off:  # Parent group must be invisible
                    self.tree.set_parent_invisible()

                self.iface.mapCanvas().setRenderFlag(True)  # Finish the loading process

                postMsg = ''
                if layersLoaded < numLayers:
                    postMsg = QCoreApplication.translate("Load Them All",
                                                         " You can see a list of not loaded layers in the QGIS log (tab 'Load Them All').")

                if layersLoaded > 1 and numLayers > 1:
                    doneMsg = QCoreApplication.translate("Load Them All", "layers were loaded succesfully.")
                elif layersLoaded < 1:
                    doneMsg = QCoreApplication.translate("Load Them All", "layers loaded succesfully.")
                elif layersLoaded == 1 and numLayers > 1:
                    doneMsg = QCoreApplication.translate("Load Them All", "layers was loaded succesfully.")
                else:
                    doneMsg = QCoreApplication.translate("Load Them All", "layer was loaded succesfully.")

                self.iface.messageBar().pushMessage("Load Them All",
                                                    "{} {} {} {}{}".format(layersLoaded,
                                                                           QCoreApplication.translate("Load Them All",
                                                                                                      " out of "),
                                                                           numLayers,
                                                                           doneMsg,
                                                                           postMsg),
                                                    duration=20)

        if self.configuration.b_groups:
            self.tree.remove_empty_groups()

        if numLayers == 0:
            self.progressBar.reset()
            self.progressBar.setMaximum(100)
            self.progressBar.setValue(0)

            if len(self.configuration.extension) == 1:
                msgExtensions = str(self.configuration.extension[0])[1:]
            else:
                msgExtensions = ", ".join(str(x)[1:] for x in self.configuration.extension[:-1]) + \
                                QCoreApplication.translate("Load Them All", " or ") + \
                                str(self.configuration.extension[len(self.configuration.extension) - 1])[1:]
            QMessageBox.information(self.iface.mainWindow(), "Load Them All",
                                    QCoreApplication.translate("Load Them All", "There are no <i>") + msgExtensions +
                                    QCoreApplication.translate("Load Them All",
                                                               "</i> files to load from the base directory with this filter.\n") +
                                    QCoreApplication.translate("Load Them All",
                                                               "Change those parameters and try again."),
                                    QMessageBox.Ok)
        return True

    def _process_cancelled(self):
        return not self.progressBar.parent().parent().processStatus

    def _sort_layers_to_load(self):
        """
        :return: Dict of layers to load sorted {'layer_path_1': layer_obj_1, ...}
        """
        files_to_load = self.files_to_load.copy()
        layer_paths = list(files_to_load.keys())
        self.files_to_load = None

        # Sort layer list
        if self.configuration.b_groups:
            layer_paths = sorted(layer_paths, key=locale.strxfrm, reverse=self.configuration.b_reverse_sort)
        else:
            # Get basenames and order them, otherwise folders will distort order
            tmp_dict = {path: os.path.splitext(os.path.basename(path))[0] for path in layer_paths}
            # We revert the order to load single layers from the back, so any
            #  new layer will be added to the top of the layer tree
            layer_paths = [k for k, v in sorted(tmp_dict.items(), key=lambda item: locale.strxfrm(str(item[1])),
                                                reverse=not self.configuration.b_reverse_sort)]

        # Now use the sorted list to return a sorted dict
        sorted_files_to_load = dict()
        for layer_path in layer_paths:
            sorted_files_to_load[layer_path] = files_to_load.get(layer_path, None)

        return sorted_files_to_load

    @abstractmethod
    def _createLayer(self, layer_path, layer_base_name, files_to_load):
        """ To be overwritten by subclasses """
        pass

    @abstractmethod
    def _isEmptyLayer(self, layer_path, layer_dict):
        """ To be overwritten by subclasses """
        pass


class LoadVectors(LoadFiles):
    """ Subclass to load vector layers """

    def __init__(self, iface, progressBar, configuration):
        LoadFiles.__init__(self, iface, progressBar, configuration)

        self.dataType = 'vector'

    def _createLayer(self, layer_path, layer_base_name, files_to_load):
        """ Create a vector layer """
        files_to_load[layer_path] = get_vector_layer(layer_path, layer_base_name, files_to_load, True)

        return files_to_load[layer_path]

    def _isEmptyLayer(self, layer_path, layer_dict):
        """ Check whether a vector layer has no features """
        if layer_dict[layer_path] is None:
            layer_dict[layer_path] = get_vector_layer(layer_path, '', layer_dict)

        if layer_dict[layer_path].type() == QgsMapLayer.VectorLayer:
            if layer_dict[layer_path].featureCount() == 0:
                return True
        return False


class LoadRasters(LoadFiles):
    """ Subclass to load raster layers """

    def __init__(self, iface, progressBar, configuration):
        LoadFiles.__init__(self, iface, progressBar, configuration)

        self.dataType = 'raster'

    def _createLayer(self, layer_path, layer_base_name, files_to_load):
        """ Create a raster layer """
        files_to_load[layer_path] = get_raster_layer(layer_path, layer_base_name, files_to_load, True)

        return files_to_load[layer_path]

    def _isEmptyLayer(self, layer_path, layer_dict):
        """ Do not check this on raster layers """
        return False
