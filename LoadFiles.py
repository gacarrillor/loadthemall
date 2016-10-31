import os
import locale

from PyQt4.QtCore import SIGNAL, QCoreApplication
from PyQt4.QtGui import QApplication, QMessageBox

from qgis.core import QgsVectorLayer, QgsMapLayer

from Filter import *

class LoadFiles():
  """ Abstract Class to inherit two common methods to Vector and Raster Load classes """
  def __init__( self, baseDir, extension, iface, progressBar, bGroups, bLayersOff,
      bDoNotEmpty, bSort, bReverseSort, bIsDoneDialog, numLayersToConfirm ):
    self.extension = extension
    self.baseDir = baseDir
    self.progressBar = progressBar
    self.filterList = FilterList()
    self.iface = iface
    self.lstFilesToLoad = []

    # Configuration parameters
    self.bGroups = bGroups
    if self.bGroups: self.groups = Group( baseDir, self.iface )
    self.bLayersOff = bLayersOff
    self.bDoNotEmpty = bDoNotEmpty
    self.bSort = bSort
    self.bReverseSort = bReverseSort
    self.bIsDoneDialog = bIsDoneDialog
    self.numLayersToConfirm = numLayersToConfirm

  def applyFilter( self, layerBaseName ):
    """ Method to encapsulate the filter's application  """
    return self.filterList.apply( layerBaseName )

  def getFilesToLoad( self ):
    """ Go through directories to fill a list with layers ready to be loaded """
    self.progressBar.setMaximum( 0 ) # ProgressBar in busy mode
    layerPaths = []

    for root, dirs, files in os.walk( self.baseDir.decode("utf-8") ):
     	for file in files:
          QApplication.processEvents() # ProgressBar in busy mode
          if self.progressBar.parent().processStatus == False: return #The process was canceled

          extension = str.lower( str( os.path.splitext( file )[ 1 ] ) )
          if extension in self.extension:
            layerPath = os.path.join( root, file )

            if extension == ".gpx":
              layerPaths.extend([layerPath + "?type=" + t for t in ["track","route","waypoint"]])
            else:
              layerPaths.append( layerPath )

    for path in layerPaths:
      if self.applyFilter( path ): # The layer passes the filter?
        if self.bDoNotEmpty: # Do not load empty layers
          if not self.isEmptyLayer( path ): self.lstFilesToLoad.append( path )
        else:
          self.lstFilesToLoad.append( path )

    self.progressBar.setMaximum( len( self.lstFilesToLoad ) )

  def loadLayers( self ):
    """ Load the layer to the map """
    if self.progressBar.parent().processStatus == False: return #The process was canceled
    numLayers = len( self.lstFilesToLoad )

    if numLayers > 0:
      result = QMessageBox.Ok # Convenient variable to pass an upcoming condition

      if numLayers >= self.numLayersToConfirm:
        result = QMessageBox.question( self.iface.mainWindow(),
            QCoreApplication.translate( "Load Them All", "Load Them All" ),
            QCoreApplication.translate( "Load Them All", "There are " ) + str( numLayers ) +
            QCoreApplication.translate( "Load Them All", " layers to load.\n Do you want to continue?" ),
            QMessageBox.Ok | QMessageBox.Cancel , QMessageBox.Ok )

      if result == QMessageBox.Ok:
        self.iface.mapCanvas().setRenderFlag( False ) # Start the loading process
        step = 0
        layersLoaded = 0

        if self.bSort:
          # In Python 3 we should use key=locale.strxfrm instead of cmp=locale.strcoll for performance
          self.lstFilesToLoad = sorted( self.lstFilesToLoad, cmp=locale.strcoll, reverse=not self.bReverseSort )

        for layerPath in self.lstFilesToLoad:
          if self.progressBar.parent().processStatus == False: return #The process was canceled

          # Finally add the layer and apply the options the user chose
          if self.bGroups: self.groups.addGroup( os.path.dirname( layerPath ) )
          ml = self.addLayer( layerPath, os.path.splitext( os.path.basename( layerPath ) )[ 0 ] )
          if ml:
              layersLoaded += 1
              if self.bLayersOff: self.iface.legendInterface().setLayerVisible( ml, False )
              if self.bGroups: self.groups.orderLayer( ml, layerPath )

          step += 1
          self.progressBar.setValue( step )
        self.iface.mapCanvas().setRenderFlag( True ) # Finish the loading process

        if self.bIsDoneDialog:
            if layersLoaded > 1 and numLayers > 1:
                doneMsg = QCoreApplication.translate( "Load Them All", " layers were loaded succesfully." )
            elif layersLoaded < 1:
                doneMsg = QCoreApplication.translate( "Load Them All", " layers loaded succesfully." )
            elif layersLoaded == 1 and numLayers > 1:
                doneMsg = QCoreApplication.translate( "Load Them All", " layers was loaded succesfully." )
            else:
                doneMsg = QCoreApplication.translate( "Load Them All", " layer was loaded succesfully." )

            QMessageBox.information( self.iface.mainWindow(), "Load Them All",
              str( layersLoaded ) +
              QCoreApplication.translate( "Load Them All", " out of " ) + str( numLayers ) +
              doneMsg, QMessageBox.Ok )
        return

    self.progressBar.reset()
    self.progressBar.setMaximum( 100 )
    self.progressBar.setValue( 0 )

    if numLayers == 0:
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

  def addLayer( self, layerPath, layerBaseName ):
    """ To be overriden by subclasses """
    pass

  def isEmptyLayer( self, layerPath ):
    """ To be overriden by subclasses """
    pass

class LoadVectors( LoadFiles ):
  """ Subclass to load vector layers """
  def __init__( self, baseDir, extension, iface, progressBar, bGroups, bLayersOff,
      bDoNotEmpty, bSort, bReverseSort, bIsDoneDialog, numLayersToConfirm,
      filterList ):
    LoadFiles.__init__( self, baseDir, extension, iface, progressBar, bGroups,
      bLayersOff, bDoNotEmpty, bSort, bReverseSort, bIsDoneDialog,
      numLayersToConfirm )

    self.filterList = filterList
    self.getFilesToLoad()
    self.loadLayers()

  def addLayer( self, layerPath, layerBaseName ):
    """ Add a vector layer """
    provider = 'gpx' if os.path.splitext( os.path.basename( layerPath ) )[1][:4] == ".gpx" else 'ogr'
    return self.iface.addVectorLayer( layerPath, layerBaseName, provider )

  def isEmptyLayer( self, layerPath ):
    """ Check whether a vector layer has not features """
    provider = 'gpx' if os.path.splitext( os.path.basename( layerPath ) )[1][:4] == ".gpx" else 'ogr'
    layer = QgsVectorLayer( layerPath, 'layerName', provider )
    if layer.type() == QgsMapLayer.VectorLayer:
      if layer.featureCount() == 0:
        return True
    return False


class LoadRasters( LoadFiles ):
  """ Subclass to load raster layers """
  def __init__( self, baseDir, extension, iface, progressBar, bGroups, bLayersOff,
      bDoNotEmpty, bSort, bReverseSort, bIsDoneDialog, numLayersToConfirm,
      filterList ):
    LoadFiles.__init__( self, baseDir, extension, iface, progressBar, bGroups,
      bLayersOff, bDoNotEmpty, bSort, bReverseSort, bIsDoneDialog,
      numLayersToConfirm )

    self.filterList = filterList
    self.getFilesToLoad()
    self.loadLayers()

  def addLayer( self, layerPath, layerBaseName ):
    """ Add a raster layer """
    return self.iface.addRasterLayer( layerPath, layerBaseName )

  def isEmptyLayer( self, layerPath ):
    """ Do not check this on raster layers """
    return False

class Group():
  """ Class to deal with layer groups """
  def __init__( self, bDir, iface ):
    self.dicGroups = {} # layerDir : index
    self.toc = iface.legendInterface()
    self.baseDir = bDir
    #iface.connect( self.toc, SIGNAL( "groupIndexChanged(int old, int new)" ), self.updateIndexes )

  #def updateIndexes( self, old, new ):
    #indexOfOld = self.dicGroups.values().index( old )
    #keyOfNew = self.dicGroups.keys()[ indexOfOld ]
    #self.dicGroups[ keyOfNew ] = new

  def addGroup( self, path ):
    """ Add a group based on a layer's directory """
    if path not in self.dicGroups:
      if path != self.baseDir:
        dpath = os.path.dirname(path)
        self.addGroup(dpath)
        name = os.path.split( path )[ 1 ] # Get the last dir in the path
        index = self.toc.addGroup( name, True, self.dicGroups[ dpath ] )
        self.dicGroups[ path ] = index
      else:
        name = os.path.split( path )[ 1 ] # Get the last dir in the path
        index = self.toc.addGroup( name )
        self.dicGroups[ path ] = index

  def orderLayer( self, mapLayer, layerPath ):
    """ Put a layer in its group """
    layerDir = os.path.dirname( layerPath )
    self.toc.moveLayer( mapLayer,  self.getGroupIndex( layerDir ) )

  def getGroupIndex( self, layerDir ):
    """ Convenient method to get a group index based on the built dictionary """
    return self.dicGroups[ layerDir ]


class Group2():
  """ Class to deal with layer groups """
  def __init__( self, bDir, iface ):
    self.dicGroups = {} # layerDir : index
    self.toc = iface.legendInterface()
    self.baseDir = bDir
    #iface.connect( self.toc, SIGNAL( "groupIndexChanged(int old, int new)" ), self.updateIndexes )

  #def updateIndexes( self, old, new ):
    #indexOfOld = self.dicGroups.values().index( old )
    #keyOfNew = self.dicGroups.keys()[ indexOfOld ]
    #self.dicGroups[ keyOfNew ] = new

  def addGroup( self, path ):
    """ Add a group based on a layer's directory """
    if path not in self.dicGroups:
      if path != self.baseDir:
        dpath = os.path.dirname(path)
        self.addGroup(dpath)
        name = os.path.split( path )[ 1 ] # Get the last dir in the path

        index = self.toc.addGroup( name, True, self.dicGroups[ dpath ] )
        self.dicGroups[ path ] = index
      else:
        name = os.path.split( path )[ 1 ] # Get the last dir in the path
        index = self.toc.addGroup( name )
        self.dicGroups[ path ] = index

  def orderLayer( self, mapLayer, layerPath ):
    """ Put a layer in its group """
    layerDir = os.path.dirname( layerPath )
    self.toc.moveLayer( mapLayer,  self.getGroupIndex( layerDir ) )

  def getGroupIndex( self, layerDir ):
    """ Convenient method to get a group index based on the built dictionary """
    return self.dicGroups[ layerDir ]


