# -*- coding:utf-8 -*-
import os
import locale

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsMapLayer,
    QgsProject
)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QApplication, QMessageBox

from .Filter import FilterList

class LoadFiles():
  """ Abstract Class to inherit two common methods to Vector and Raster Load classes """
  def __init__( self, baseDir, extension, iface, progressBar, bGroups, bLayersOff,
      bDoNotEmpty, bSort, bReverseSort, bSearchParentLayer, bAddParentLayerName,
      bStyles, numLayersToConfirm, dataType ):
    self.extension = extension
    self.baseDir = baseDir
    self.progressBar = progressBar
    self.filterList = FilterList()
    self.iface = iface
    self.lstFilesToLoad = []
    self.dataType = dataType

    # Configuration parameters
    self.bGroups = bGroups
    self.tree = Tree( baseDir, self.bGroups )
    self.bLayersOff = bLayersOff
    self.bDoNotEmpty = bDoNotEmpty
    self.bSort = bSort
    self.bReverseSort = bReverseSort
    self.bSearchParentLayer = bSearchParentLayer
    self.bAddParentLayerName = bAddParentLayerName
    self.bStyles = bStyles
    self.numLayersToConfirm = numLayersToConfirm

  def applyFilter( self, layerBaseName ):
    """ Method to encapsulate the filter's application  """
    return self.filterList.apply( layerBaseName )

  # def decodeName( self, name ):
  #   """
  #       Function to deal with encoding problems in filenames when using os.walk.
  #       Source: http://stackoverflow.com/a/23841227/1073148
  #       I was experiencing errors when os.walk found files like "╬2╔ìuε╖.╫M"
  #       or "�yG@�Hw@8", generated by whatever malware.
  #       According to the referenced thread, Python 3 shouldn't need this function.
  #   """
  #   if type(name) == str: # leave unicode ones alone
  #     try:
  #       name = name.decode( 'utf8' )
  #     except:
  #       name = name.decode( 'windows-1252' )
  #   return name

  def getFilesToLoad( self ):
    """ Go through directories to fill a list with layers ready to be loaded """
    self.progressBar.setMaximum( 0 ) # ProgressBar in busy mode
    layerPaths = []

    for root, dirs, files in os.walk( self.baseDir ):
        #files = [self.decodeName(f) for f in files]
       	for file_ in files:
          QApplication.processEvents() # TODO: Perhaps better by chunks?
          if not self.progressBar.parent().parent().processStatus:
              #The process was canceled
              return False

          try: # TODO: do we need this in Python 3?
            # Nasty file names like those created by malware should be catched and ignored
            extension = str.lower( str( os.path.splitext( file_ )[ 1 ] ) )
          except UnicodeEncodeError as  e:
            extension = None

          if extension in self.extension:
            # layerPath = os.path.join( self.decodeName( root ), file_ )
            layerPath = os.path.join( root, file_ )

            if self.dataType == 'vector':
              layer = QgsVectorLayer( layerPath, "", "ogr" )
              if layer.isValid():
                # Do we have sublayers?
                if len( layer.dataProvider().subLayers() ) > 1:
                  # Sample: ['0!!::!!line_intersection_collection!!::!!12!!::!!LineString!!::!!geometryProperty']
                  subLayers = dict()
                  for subLayer in layer.dataProvider().subLayers():
                    parts = subLayer.split("!!::!!")  # 1: name, 3: geometry type
                    # Sublayers might share layer name, we need to get geometry types just in case
                    if parts[1] in subLayers:
                      subLayers[parts[1]].append(parts[3])
                    else:
                      subLayers[parts[1]] = [parts[3]]

                  for subLayerName,subLayerGeometries in subLayers.items():
                    if len(subLayerGeometries) > 1:
                      for subLayerGeometry in subLayerGeometries:
                        layerPaths.append( "{}|layername={}|geometrytype={}".format( layerPath, subLayerName, subLayerGeometry) )
                    else:
                      layerPaths.append( "{}|layername={}".format( layerPath, subLayerName) )
                else:
                  layerPaths.append( layerPath )
            else: #'raster'
              layerPaths.append( layerPath )

    for path in layerPaths:
      QApplication.processEvents()
      if not self.progressBar.parent().parent().processStatus:
        # The process was canceled
        return False

      if self.applyFilter( path ): # The layer passes the filter?
        if self.bDoNotEmpty: # Do not load empty layers
          if not self.isEmptyLayer( path ): self.lstFilesToLoad.append( path )
        else:
          self.lstFilesToLoad.append( path )

    self.progressBar.setMaximum( len( self.lstFilesToLoad ) )
    return True

  def loadLayers( self ):
    """ Load the layer to the map """
    if not self.progressBar.parent().parent().processStatus:
        # The process was canceled
        return False

    numLayers = len( self.lstFilesToLoad )

    if numLayers > 0:
      result = QMessageBox.Ok # Convenient variable to pass an upcoming condition

      if numLayers >= self.numLayersToConfirm:
        result = QMessageBox.question( self.iface.mainWindow(),
            QCoreApplication.translate( "Load Them All", "Load Them All" ),
            QCoreApplication.translate( "Load Them All",
                "There are {} layers to load.\n Do you want to continue?" ).format( numLayers ),
            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok )

      if result == QMessageBox.Ok:
        self.iface.mapCanvas().setRenderFlag( False ) # Start the loading process
        step = 0
        layersLoaded = 0

        if self.bSort:
          if self.bGroups:
            self.lstFilesToLoad = sorted( self.lstFilesToLoad, key=locale.strxfrm, reverse=self.bReverseSort )
          else:
            # Get basenames and order them, otherwise folders will distort order
            tmpDict = { path: os.path.splitext( os.path.basename( path ) )[0] for path in self.lstFilesToLoad }
            # We revert the order to load single layers from the back, so any
            #  new layer will be added to the top of the layer tree
            self.lstFilesToLoad = [k for k,v in sorted(tmpDict.items(), key=lambda item:locale.strxfrm(str(item[1])), reverse=not self.bReverseSort)]

        for layerPath in self.lstFilesToLoad:
          QApplication.processEvents()
          if not self.progressBar.parent().parent().processStatus:
            # The process was canceled
            self.iface.mapCanvas().setRenderFlag( True )
            return False

          # Finally add the layer and apply the options the user chose
          if self.bGroups:
            group = self.tree.addGroup( os.path.dirname( layerPath ) )

          baseName = os.path.basename( layerPath )
          layerName = os.path.splitext( baseName )[ 0 ]

          # Let's clear the layer name for sublayers
          if '|layername=' in baseName and not baseName.endswith( '|layername=' ):
            subLayerName = baseName.split('|layername=')[1].split('|geometrytype=')[0]
            if self.bAddParentLayerName:
              layerName = "".join( [layerName, " ", subLayerName] )
            else:
              layerName = subLayerName

          ml = self.createLayer( layerPath, layerName )
          if ml.isValid():
            layersLoaded += 1
            if self.bGroups:
              self.tree.addLayerToGroup( ml, group )
            else:
              self.tree.addLayer( ml, self.bLayersOff )

            # Look if there is a style to apply
            bStyleFound = False
            if self.bStyles:
              if self.bGroups:
                # Has the group a style to apply?
                aGroup = os.path.dirname(layerPath)
                aBaseGroup = os.path.basename(aGroup)
                styleFile = os.path.join(aGroup, aBaseGroup + ".qml")

                if os.path.exists(styleFile):
                  ml.loadNamedStyle(styleFile)
                  bStyleFound = True
                  QgsApplication.messageLog().logMessage("QML for group '{}' applied to layer '{}'".format(
                    aBaseGroup, ml.name()), "Load Them All", Qgis.Info)

              if bStyleFound:
                self.iface.layerTreeView().refreshLayerSymbology( ml.id() )
              else:
                QgsApplication.messageLog().logMessage(
                  "No style found for layer group '{}' or 'create groups' option is disabled!".format(aBaseGroup), "Load Them All", Qgis.Warning)
              # End Styles

          else:
            QgsApplication.messageLog().logMessage(
                "Layer '{}' couldn't be created properly and wasn't loaded into QGIS. Is the layer data valid?".format(layerPath),
                "Load Them All", Qgis.Warning)

          step += 1
          self.progressBar.setValue( step )

        if self.bGroups and self.bLayersOff: # Parent group must be invisible
          self.tree.setParentInvisible()

        self.iface.mapCanvas().setRenderFlag( True ) # Finish the loading process

        postMsg = ''
        if layersLoaded < numLayers:
          postMsg = QCoreApplication.translate( "Load Them All", " You can see a list of not loaded layers in the QGIS log (tab 'Load Them All')." )

        if layersLoaded > 1 and numLayers > 1:
          doneMsg = QCoreApplication.translate( "Load Them All", "layers were loaded succesfully." )
        elif layersLoaded < 1:
          doneMsg = QCoreApplication.translate( "Load Them All", "layers loaded succesfully." )
        elif layersLoaded == 1 and numLayers > 1:
          doneMsg = QCoreApplication.translate( "Load Them All", "layers was loaded succesfully." )
        else:
          doneMsg = QCoreApplication.translate( "Load Them All", "layer was loaded succesfully." )

        self.iface.messageBar().pushMessage( "Load Them All",
          "{} {} {} {}{}".format(layersLoaded,
            QCoreApplication.translate( "Load Them All", " out of " ),
            numLayers,
            doneMsg,
            postMsg),
          duration=20)

    if self.bGroups:
      self.tree.removeEmptyGroups()

    if numLayers == 0:
      self.progressBar.reset()
      self.progressBar.setMaximum( 100 )
      self.progressBar.setValue( 0 )

      if len(self.extension) == 1:
        msgExtensions = str(self.extension[0])[1:]
      else:
        msgExtensions = ", ".join(str(x)[1:] for x in self.extension[:-1]) + \
          QCoreApplication.translate( "Load Them All", " or " ) + \
          str(self.extension[len(self.extension)-1])[1:]
      QMessageBox.information( self.iface.mainWindow(), "Load Them All",
        QCoreApplication.translate( "Load Them All", "There are no <i>" ) + msgExtensions +
        QCoreApplication.translate( "Load Them All", "</i> files to load from the base directory with this filter.\n") +
        QCoreApplication.translate( "Load Them All", "Change those parameters and try again." ),
        QMessageBox.Ok )
    return True

  def createLayer( self, layerPath, layerBaseName ):
    """ To be overriden by subclasses """
    pass

  def isEmptyLayer( self, layerPath ):
    """ To be overriden by subclasses """
    pass

class LoadVectors( LoadFiles ):
  """ Subclass to load vector layers """
  def __init__( self, baseDir, extension, iface, progressBar, bGroups, bLayersOff,
      bDoNotEmpty, bSort, bReverseSort, bSearchParentLayer, bAddParentLayerName,
      bStyles, numLayersToConfirm, filterList ):
    LoadFiles.__init__( self, baseDir, extension, iface, progressBar, bGroups,
      bLayersOff, bDoNotEmpty, bSort, bReverseSort, bSearchParentLayer,
      bAddParentLayerName, bStyles, numLayersToConfirm, 'vector' )

    self.filterList = filterList
    if self.getFilesToLoad():
      self.loadLayers()

  def createLayer( self, layerPath, layerBaseName ):
    """ Create a vector layer """
    return QgsVectorLayer( layerPath, layerBaseName, 'ogr' )

  def isEmptyLayer( self, layerPath ):
    """ Check whether a vector layer has no features """
    layer = QgsVectorLayer( layerPath, 'layerName', 'ogr' )
    if layer.type() == QgsMapLayer.VectorLayer:
      if layer.featureCount() == 0:
        return True
    return False


class LoadRasters( LoadFiles ):
  """ Subclass to load raster layers """
  def __init__( self, baseDir, extension, iface, progressBar, bGroups, bLayersOff,
      bDoNotEmpty, bSort, bReverseSort, bSearchParentLayer, bAddParentLayerName,
      bStyles, numLayersToConfirm, filterList ):
    LoadFiles.__init__( self, baseDir, extension, iface, progressBar, bGroups,
      bLayersOff, bDoNotEmpty, bSort, bReverseSort, bSearchParentLayer,
      bAddParentLayerName, bStyles, numLayersToConfirm, 'raster' )

    self.filterList = filterList
    if self.getFilesToLoad():
      self.loadLayers()

  def createLayer( self, layerPath, layerBaseName ):
    """ Create a raster layer """
    return QgsRasterLayer( layerPath, layerBaseName )

  def isEmptyLayer( self, layerPath ):
    """ Do not check this on raster layers """
    return False


class Tree():
  """ Class to manage QGIS layer tree calls """
  def __init__( self, baseDir, createParentGroup=True ):
    self.baseDir = baseDir

    self.root = QgsProject.instance().layerTreeRoot()
    self.createParentGroup = createParentGroup
    if createParentGroup:
      # Initialize root to match the base dir and build root group in ToC
      baseGroupName = os.path.split( baseDir )[ 1 ]
      group = self.root.findGroup( baseGroupName )
      if not group:
        group = self.root.insertGroup( 0, baseGroupName )
      self.root = group

  def addGroup( self, path ):
    """ Add a group based on a layer's directory.
        If parent groups don't exist, it creates all of them until base dir.
    """
    if path != self.baseDir:
      previousPath = os.path.dirname( path )
      previousGroup = self.addGroup( previousPath )

      lastDir = os.path.split( path )[ 1 ] # Get the last dir in the path
      group = previousGroup.findGroup( lastDir )
      if not group:
        group = previousGroup.addGroup( lastDir )
      return group

    else:
      return self.root

  def addLayerToGroup( self, layer, group ):
    """ Add a layer to its corresponding group """
    addedLayer = QgsProject.instance().addMapLayer( layer, False ) # TODO check this!
    group.addLayer( addedLayer )

  def addLayer( self, layer, notVisible ):
    """ Add a layer to the root of the layer tree """
    addedLayer = QgsProject.instance().addMapLayer( layer, False )  # TODO check this!
    addedLayerToRoot = self.root.insertLayer( 0, addedLayer )
    if notVisible:
      addedLayerToRoot.setItemVisibilityChecked( 0 )

  def setParentInvisible( self ):
    self.root.setItemVisibilityChecked( 0 )

  def removeEmptyGroups( self ):
    """ Remove created groups if layers weren't added to them, e.g., if the
        layer is not valid. """
    self.root.removeChildrenGroupWithoutLayers()
    if len( self.root.children() ) == 0:
      QgsProject.instance().layerTreeRoot().removeChildNode( self.root )
