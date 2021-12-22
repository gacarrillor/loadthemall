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

    def addGroup(self, path):
        """ Add a group based on a layer's directory.
        If parent groups don't exist, it creates all of them until base dir.
    """
        if path != self.baseDir:
            previousPath = os.path.dirname(path)
            previousGroup = self.addGroup(previousPath)

            lastDir = os.path.split(path)[1]  # Get the last dir in the path
            group = previousGroup.findGroup(lastDir)
            if not group:
                group = previousGroup.addGroup(lastDir)
            return group

        else:
            return self.root

    def addLayerToGroup(self, layer, group):
        """ Add a layer to its corresponding group """
        addedLayer = QgsProject.instance().addMapLayer(layer, False)  # TODO check this!
        group.addLayer(addedLayer)

    def addLayer(self, layer, notVisible):
        """ Add a layer to the root of the layer tree """
        addedLayer = QgsProject.instance().addMapLayer(layer, False)  # TODO check this!
        addedLayerToRoot = self.root.insertLayer(0, addedLayer)
        if notVisible:
            addedLayerToRoot.setItemVisibilityChecked(0)

    def setParentInvisible(self):
        self.root.setItemVisibilityChecked(0)

    def removeEmptyGroups(self):
        """ Remove created groups if layers weren't added to them, e.g., if the
        layer is not valid. """
        self.root.removeChildrenGroupWithoutLayers()
        if len(self.root.children()) == 0:
            QgsProject.instance().layerTreeRoot().removeChildNode(self.root)
