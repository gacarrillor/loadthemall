"""
/***************************************************************************
LoadThemAll
A QGIS plugin
Loads files stored in a directory structure recursively, based on several filters
                             -------------------
begin                : 2024-03-01
copyright            : (C) 2024 by Germán Carrillo (GeoTux)
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
from .Enums import EnumLoadThemAllResult


class LoadThemAllResult:
    def __init__(self, result: EnumLoadThemAllResult, layers_found:int = 0, layers_loaded:int = 0):
        """
        Stores the result of an LTA session.

        :param result: EnumLoadThemAllResult value. indicates the overall result of an LTA session.
        :param layers_found: Number of layers that matched the filters and extensions set.
        :param layers_loaded: Number of loaded layers.
        """
        self.result = result
        self.layers_found = layers_found
        self.layers_loaded = layers_loaded
