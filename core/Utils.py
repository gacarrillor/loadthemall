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
from qgis.core import (QgsRasterLayer,
                       QgsVectorLayer)


def get_vector_layer(layer_path, layer_name, layer_dict, rename=False):
    res = layer_dict[layer_path]
    if res is None:
        res = QgsVectorLayer(layer_path, layer_name, 'ogr')
    elif rename:
        res.setName(layer_name)

    return res


def get_raster_layer(layer_path, layer_name, layer_dict, rename=False):
    res = layer_dict[layer_path]
    if res is None:
        res = QgsRasterLayer(layer_path, layer_name)
    elif rename:
        res.setName(layer_name)

    return res
