import os, re
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsRectangle

class Filter():
  """ Class to encapsulate filters behavior """
  def __init__( self ):
    pass

  def apply( self, layerPath ):
    """ To be overridden """
    pass


class NoFilter( Filter ):
  """ Dummy filter """
  def __init__( self ):
    pass

  def apply( self, layerPath ):
    """ There is no condition to be applied """
    return True


class AlphanumericFilter( Filter ):
  """ Filter based on text using a regular expression """
  def __init__( self, matchType, filterText, caseInsensitive, accentInsensitive ):
    self.matchType = matchType
    self.filterText = filterText
    self.caseInsensitive = caseInsensitive
    self.accentInsensitive = accentInsensitive
    self.regExpPattern = None # Stores compiled RE pattern to reuse it afterwards

  def apply( self, layerPath ):
    """ Apply an alphanumeric filter """
    if not self.regExpPattern: # We build a RE pattern only once and then reuse it
      self.regExpPattern = self.getRegExpPattern()

    baseName = os.path.basename( layerPath )
    layerBaseName = os.path.splitext( baseName )[ 0 ]
    if '|layername=' in baseName and not baseName.endswith( '|layername=' ):
      layerBaseName = u"".join( [layerBaseName, " ", os.path.basename( layerPath ).split( '|layername=' )[1]] )

    layerBaseName = layerBaseName.lower() if self.caseInsensitive else layerBaseName
    if self.accentInsensitive:
      try:
        from unidecode import unidecode
        layerBaseName = unidecode( layerBaseName )
      except ImportError, NameError:
        pass # This error is handled in LoadThemAllDialog

    return True if self.regExpPattern.search( layerBaseName ) else False

  def getRegExpPattern( self ):
    regExpString = ''
    self.filterText = self.normalizeText( self.filterText.decode('utf-8') )

    andList = self.filterText.split("&&")
    newAndList = []
    for andTerm in andList:
      andTerm = self.normalizeText( andTerm )
      orList = andTerm.split("||")
      newOrList = []

      for orTerm in orList:
        orTerm = self.normalizeText( orTerm )
        if self.matchType == 'StartsWith':
          newOrList.append( ''.join( [ '^', orTerm ] ) )
        elif self.matchType == 'EndsWith':
          newOrList.append( ''.join( [ orTerm, '$' ] ) )
        else: # "anyPosition"
          newOrList.append( orTerm )

      tmp = '|' if len( orList ) > 1 else '' # If there's 1+ 'or' (||) operator...
      newAndList.append( tmp.join( newOrList ) )

    if len( andList ) > 1: # Is there at least an 'and' (&&) operator?
      newAndList = [''.join( ['(', andElem, ')'] ) for andElem in newAndList]
      # .*?, not .*: https://docs.python.org/2/howto/regex.html#greedy-versus-non-greedy
      regExpString = '.*?'.join( newAndList ) # .*? is our and RE operator
    else:
      regExpString = ''.join( newAndList )

    regExpString = regExpString.lower() if self.caseInsensitive else regExpString
    if self.accentInsensitive:
      try:
        from unidecode import unidecode
        regExpString = unidecode( regExpString )
      except ImportError:
        pass # This error is handled in LoadThemAllDialog

    return re.compile( regExpString )

  def normalizeText( self, text ):
    text = text.strip()
    if text.endswith("&&") or text.endswith("||"): text = text[:-2]
    if text.startswith("&&") or text.startswith("||"): text = text[2:]
    return text


class BoundingBoxFilter( Filter ):
  """ Filter based a bounding box """
  def __init__( self, layerType, boundingBox, method ):
    """Constructor

      :param layerType: "raster" or "vector"
      :type string:
      :param boundingBox: The bounding box for selection
      :type QgsRectangle:
      :param method: The topological relation that should be used for selection, "contains" or "intersects"
    """
    self.layerType = layerType
    self.boundingBox = boundingBox
    self.method = method

  def apply( self, layerPath ):
    """ Apply the bounding box filter """

    if self.layerType == "vector":
        #provider = 'gpx' if os.path.splitext( os.path.basename( layerPath ) )[1][:4] == ".gpx" else 'ogr'
        bbox = QgsVectorLayer( layerPath, '', 'ogr' ).extent()
    else:
        bbox = QgsRasterLayer( layerPath, '' ).extent()

    if self.method == "contains":
        return self.boundingBox.contains( bbox )
    else:
        return self.boundingBox.intersects( bbox )


class TypeFilter( Filter ):
  """ Abstract class to define a filter based on an object's type """
  def __init__( self, itemTypes ):
    self.lstFilterItems = [] # Types to be considered as True

  def getItemType( self, layerPath ):
    """ To be overidden """
    pass

  def apply( self, layerPath ):
    """ Apply a type filter """
    itemType = self.getItemType( layerPath )
    return True if itemType in self.lstFilterItems else False


class GeometryTypeFilter( TypeFilter ):
  """ Filter based on the layer's geometry type """
  def __init__( self, itemTypes ):
    TypeFilter.__init__( self, itemTypes )
    if 'Point' in itemTypes: self.lstFilterItems.append( 0 )
    if 'Line' in itemTypes: self.lstFilterItems.append( 1 )
    if 'Polygon' in itemTypes: self.lstFilterItems.append( 2 )

  def getItemType( self, layerPath ):
    """ Get the layer's geometry type """
    #provider = 'gpx' if os.path.splitext( os.path.basename( layerPath ) )[1][:4] == ".gpx" else 'ogr'
    return QgsVectorLayer( layerPath, '', 'ogr').geometryType()

class RasterTypeFilter( TypeFilter ):
  """ Filter based on the layer's raster type """
  def __init__( self, itemTypes ):
    TypeFilter.__init__( self, itemTypes )
    if 'GrayOrUndefined' in itemTypes: self.lstFilterItems.append( 0 )
    if 'Palette' in itemTypes: self.lstFilterItems.append( 1 )
    if 'Multiband' in itemTypes: self.lstFilterItems.append( 2 )
    if 'ColorLayer' in itemTypes: self.lstFilterItems.append( 3 )

  def getItemType( self, layerPath ):
    """ Get the layer's raster type """
    return QgsRasterLayer( layerPath, '').rasterType()


class FilterList( Filter ):
  """Manage a list of filters"""
  def reset( self ):
    self.filterList = []

  def __init__( self ):
    self.reset()

  def addFilter( self, filter ):
    self.filterList.append( filter )

  def apply( self,  layerPath ):
    if not self.filterList:
      return NoFilter().apply( layerPath ) # No filter was specified

    for filter in self.filterList:
      check = filter.apply( layerPath )
      if check is False:
        return check
    return True

