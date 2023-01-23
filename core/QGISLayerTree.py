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
import os.path

from qgis.core import QgsProject


class QGISLayerTree:
    """ Class to manage QGIS layer tree calls """

    def __init__(self, baseDir, createParentGroup=True):
        self.baseDir = baseDir

        self.root = QgsProject.instance().layerTreeRoot()
        self.createParentGroup = createParentGroup
        if createParentGroup:
            # Initialize root to match the base dir and build root group in ToC
            baseGroupName = os.path.split(baseDir)[1]
            group = self.root.findGroup(baseGroupName)
            if not group:
                group = self.root.insertGroup(0, baseGroupName)
            self.root = group

    def add_group(self, path):
        """
        Add a group based on a layer's directory.
        If parent groups don't exist, it creates all of them until base dir.
        """
        if path != self.baseDir:
            previousPath = os.path.dirname(path)
            previousGroup = self.add_group(previousPath)

            lastDir = os.path.split(path)[1]  # Get the last dir in the path
            group = previousGroup.findGroup(lastDir)
            if not group:
                group = previousGroup.addGroup(lastDir)
            return group

        else:
            return self.root

    def add_layer_to_group(self, layer, group):
        """ Add a layer to its corresponding group """
        addedLayer = QgsProject.instance().addMapLayer(layer, False)
        group.addLayer(addedLayer)

    def add_layer(self, layer, notVisible):
        """ Add a layer to the root of the layer tree """
        addedLayer = QgsProject.instance().addMapLayer(layer, False)
        addedLayerToRoot = self.root.insertLayer(0, addedLayer)
        if notVisible:
            addedLayerToRoot.setItemVisibilityChecked(0)

    def set_parent_invisible(self):
        self.root.setItemVisibilityChecked(0)

    def remove_empty_groups(self):
        """
        Remove created groups if layers weren't added to them, e.g., if the
        layer is not valid.
        """
        self.root.removeChildrenGroupWithoutLayers()
        if len(self.root.children()) == 0:
            QgsProject.instance().layerTreeRoot().removeChildNode(self.root)
