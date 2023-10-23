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

from qgis.core import (QgsApplication,
                       QgsRasterLayer,
                       QgsVectorLayer,
                       QgsCoordinateReferenceSystem,
                       QgsProviderRegistry,
                       Qgis,
                       QgsMapLayerType)

if Qgis.versionInt() >= 31800:
    from qgis.core import QgsPointCloudLayer


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


def get_point_cloud_layer(layer_path, layer_name, layer_dict, rename=False, default_crs: QgsCoordinateReferenceSystem = None):
    if Qgis.versionInt() < 31800:
        return None

    res = layer_dict[layer_path]
    if res is None:
        provider = QgsProviderRegistry.instance().preferredProvidersForUri(layer_path)
        if not provider:
            QgsApplication.messageLog().logMessage(
                "No provider found for layer '{}'!".format(layer_path), "Load Them All", Qgis.Warning)
            return None
        res = QgsPointCloudLayer(layer_path, layer_name, provider[0].metadata().key())
    elif rename:
        res.setName(layer_name)

    if default_crs:
        res.setCrs(default_crs)

    return res


def get_zip_files_to_load(path, extensions):
    """
    Recursive function to get all the files inside a ZIP file that match the expected extensions.

    :param layer_path: Root ZIP file
    :param extensions: List of chosen extensions
    :return: List of files found inside the ZIP file
    """
    import zipfile
    zip = zipfile.ZipFile(path)
    files_to_load = []

    for file_ in zip.namelist():
        try:  # TODO: do we need this in Python 3?
            # Nasty file names like those created by malware should be caught and ignored
            extension = str.lower(str(os.path.splitext(file_)[1]))
        except UnicodeEncodeError as e:
            extension = None

        if extension in extensions:
            files_to_load.append('/vsizip/' + path + '/' + file_)
        elif extension == '.zip':
            files_to_load += get_zip_files_to_load(file_, extensions)

    return files_to_load


def get_parent_folder(layer_path):
    """
    For ZIP files:
    path = '/vsizip//docs/Regional/ZIP_data.zip/AA_PreQuat_NAD27z12.TAB'
    QgsProviderRegistry.instance().decodeUri('ogr', path) -->
        {'layerId': None,
         'layerName': NULL,
         'path': '/docs/Regional/ZIP_data.zip',
         'vsiPrefix': '/vsizip/',
         'vsiSuffix': '/AA_PreQuat_NAD27z12.TAB'}

    For regular files:
    path = '/docs/Regional/AA_PreQuat_NAD27z12.TAB'
    {'layerId': None,
     'layerName': NULL,
     'path': '/docs/geodata/Map_Database_ZIP/Geology/Regional/AA_PreQuat_NAD27z12.TAB'}

    :param layer_path: Full layer path
    :return: Folder in which we can find the layer
    """
    parts = QgsProviderRegistry.instance().decodeUri('ogr', layer_path)
    return os.path.dirname(parts['path'])


def has_point_cloud_provider() -> bool:
    if Qgis.versionInt() < 33000:
        point_cloud_providers = QgsProviderRegistry.instance().providersForLayerType(QgsMapLayerType.PointCloudLayer)
    else:
        point_cloud_providers = QgsProviderRegistry.instance().providersForLayerType(Qgis.LayerType.PointCloud)

    return bool(point_cloud_providers)
