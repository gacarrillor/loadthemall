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
import os, re
import time
from abc import (ABC,
                 abstractmethod)

from qgis.PyQt.QtCore import QDateTime
from qgis.core import (QgsRectangle,
                       QgsWkbTypes)

from .Utils import (get_raster_layer,
                    get_vector_layer)


class Filter(ABC):
    """ Abstract class to encapsulate filters behavior """
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, layer_path, layer_dict):
        """ To be overwritten """
        pass


class NoFilter(Filter):
    """ Dummy filter """
    def __init__(self):
        Filter.__init__(self)

    def apply(self, layer_path, layer_dict):
        """ There is no condition to be applied """
        return True


class AlphanumericFilter(Filter):
    """ Filter based on text using a regular expression """
    def __init__(self, matchType, filterText, configuration):
        Filter.__init__(self)
        self.matchType = matchType
        self.filterText = filterText
        self.caseInsensitive = configuration.b_case_insensitive
        self.accentInsensitive = configuration.b_accent_insensitive
        self.bSearchParentLayer = configuration.b_search_parent_layer
        self.regExpPattern = None  # Stores compiled RE pattern to reuse it afterwards

    def apply(self, layer_path, layer_dict):
        """ Apply an alphanumeric filter """
        if not self.regExpPattern:  # We build a RE pattern only once and then reuse it
            self.regExpPattern = self._getRegExpPattern()

        baseName = os.path.basename(layer_path)
        layerBaseName = os.path.splitext(baseName)[0]
        if '|layername=' in baseName and not baseName.endswith('|layername='):
            if self.bSearchParentLayer:
                layerBaseName = "".join([layerBaseName, " ", os.path.basename(layer_path).split('|layername=')[1]])
            else:
                layerBaseName = baseName.split('|layername=')[1]

        layerBaseName = layerBaseName.lower() if self.caseInsensitive else layerBaseName
        if self.accentInsensitive:
            try:
                from unidecode import unidecode
                layerBaseName = unidecode(layerBaseName)
            except (ImportError, NameError) as e:
                pass  # This error is handled in LoadThemAllDialog

        return True if self.regExpPattern.search(layerBaseName) else False

    def _getRegExpPattern(self):
        regExpString = ''
        self.filterText = self._normalizeText(self.filterText)

        andList = self.filterText.split("&&")
        newAndList = []
        for andTerm in andList:
            andTerm = self._normalizeText(andTerm)
            orList = andTerm.split("||")
            newOrList = []

            for orTerm in orList:
                orTerm = self._normalizeText(orTerm)
                if self.matchType == 'StartsWith':
                    newOrList.append(''.join(['^', orTerm]))
                elif self.matchType == 'EndsWith':
                    newOrList.append(''.join([orTerm, '$']))
                else:  # "anyPosition"
                    newOrList.append(orTerm)

            tmp = '|' if len(orList) > 1 else ''  # If there's 1+ 'or' (||) operator...
            newAndList.append(tmp.join(newOrList))

        if len(andList) > 1:  # Is there at least an 'and' (&&) operator?
            newAndList = [''.join(['(', andElem, ')']) for andElem in newAndList]
            # .*?, not .*: https://docs.python.org/2/howto/regex.html#greedy-versus-non-greedy
            regExpString = '.*?'.join(newAndList)  # .*? is our and RE operator
        else:
            regExpString = ''.join(newAndList)

        regExpString = regExpString.lower() if self.caseInsensitive else regExpString
        if self.accentInsensitive:
            try:
                from unidecode import unidecode
                regExpString = unidecode(regExpString)
            except ImportError as e:
                pass  # This error is handled in LoadThemAllDialog

        return re.compile(regExpString)

    def _normalizeText(self, text):
        text = text.strip()
        if text.endswith("&&") or text.endswith("||"): text = text[:-2]
        if text.startswith("&&") or text.startswith("||"): text = text[2:]
        return text


class InvertedAlphanumericFilter(Filter):
    """ Prepend a logic NOT to an Alphanumeric filter """
    def __init__(self, matchType, filterText, configuration):
        Filter.__init__(self)
        self._filter = AlphanumericFilter(matchType, filterText, configuration)

    def apply(self, layer_path, layer_dict):
        """ Invert Alphanumeric filter result """
        return not self._filter.apply(layer_path, layer_dict)


class BoundingBoxFilter(Filter):
    """ Filter based on a bounding box """
    def __init__(self, layerType, boundingBox, method):
        """
        :param layerType: "raster" or "vector"
        :type string:
        :param boundingBox: The bounding box for selection
        :type QgsRectangle:
        :param method: The topological relation that should be used for selection, "contains" or "intersects"
        """
        Filter.__init__(self)
        self.layerType = layerType
        self.boundingBox = boundingBox
        self.method = method

    def apply(self, layer_path, layer_dict):
        """ Apply the bounding box filter """

        if self.layerType == "vector":
            if layer_dict[layer_path] is None:
                layer_dict[layer_path] = get_vector_layer(layer_path, '', layer_dict)
        else:
            if layer_dict[layer_path] is None:
                layer_dict[layer_path] = get_raster_layer(layer_path, '', layer_dict)

        bbox = layer_dict[layer_path].extent()

        if self.method == "contains":
            return self.boundingBox.contains(bbox)
        else:
            return self.boundingBox.intersects(bbox)


class DateModifiedFilter(Filter):
    """ Filter based on 'date modified' from file metadata """
    def __init__(self, comparison, datetime):
        Filter.__init__(self)
        self._comparison = comparison
        self._datetime = datetime

    def apply(self, layer_path, layer_dict):
        """ Apply date modifier filter """
        dateModified = QDateTime().fromString(time.ctime(os.path.getmtime(layer_path.split('|layername=')[0])))

        if self._comparison == 'before':
            return dateModified < self._datetime
        elif self._comparison == 'after':
            return dateModified > self._datetime
        else:  # 'day'
            return dateModified.date() == self._datetime.date()


class TypeFilter(Filter):
    """ Abstract class to define a filter based on an object's type """
    def __init__(self, itemTypes):
        Filter.__init__(self)
        self.lstFilterItems = []  # Types to be considered as True

    @abstractmethod
    def getItemType(self, layer_path, layer_dict):
        """ To be overwritten """
        pass

    def apply(self, layer_path, layer_dict):
        """ Apply a type filter """
        itemType = self.getItemType(layer_path, layer_dict)
        return itemType in self.lstFilterItems


class GeometryTypeFilter(TypeFilter):
    """ Filter based on the layer's geometry type """
    def __init__(self, itemTypes):
        TypeFilter.__init__(self, itemTypes)
        if 'Point' in itemTypes: self.lstFilterItems.append(QgsWkbTypes.PointGeometry)
        if 'Line' in itemTypes: self.lstFilterItems.append(QgsWkbTypes.LineGeometry)
        if 'Polygon' in itemTypes: self.lstFilterItems.append(QgsWkbTypes.PolygonGeometry)

        if not self.lstFilterItems:
            # The user created a Geometry Filter but doesn't want points, lines nor polygons.
            # In conclusion, he/she wants geometryless layers.
            self.lstFilterItems.append(QgsWkbTypes.NullGeometry)  # Alphanumeric tables

    def getItemType(self, layer_path, layer_dict):
        """ Get the layer's geometry type """
        if layer_dict[layer_path] is None:
            layer_dict[layer_path] = get_vector_layer(layer_path, '', layer_dict)

        return layer_dict[layer_path].geometryType()


class RasterTypeFilter(TypeFilter):
    """ Filter based on the layer's raster type """
    def __init__(self, itemTypes):
        TypeFilter.__init__(self, itemTypes)
        if 'GrayOrUndefined' in itemTypes: self.lstFilterItems.append(0)
        if 'Palette' in itemTypes: self.lstFilterItems.append(1)
        if 'Multiband' in itemTypes: self.lstFilterItems.append(2)
        if 'ColorLayer' in itemTypes: self.lstFilterItems.append(3)

    def getItemType(self, layer_path, layer_dict):
        """ Get the layer's raster type """
        if layer_dict[layer_path] is None:
            layer_dict[layer_path] = get_raster_layer(layer_path, '', layer_dict)

        return layer_dict[layer_path].rasterType()


class FilterList(Filter):
    """ Manage a list of filters """
    def __init__(self):
        Filter.__init__(self)
        self.reset()

    def reset(self):
        self.filterList = []

    def addFilter(self, filter):
        self.filterList.append(filter)

    def apply(self, layer_path, layer_dict):
        if not self.filterList:
            return NoFilter().apply(layer_path, layer_dict)  # No filter was specified

        for filter in self.filterList:
            check = filter.apply(layer_path, layer_dict)
            if check is False:
                return check
        return True
