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


class LoadConfiguration:
    """ Load Them All configuration object """
    def __init__(self):
        # Vector/Raster/PointCloud tabs
        self.base_dir = ''
        self.extension = []

        # Configuration tab
        self.b_groups = False
        self.b_search_in_compressed_files = False
        self.b_layers_off = False
        self.b_not_empty = True
        self.b_sort = True
        self.b_reverse_sort = False
        self.b_case_insensitive = True
        self.b_accent_insensitive = False
        self.b_styles = False
        self.b_search_parent_layer = False
        self.b_add_parent_layer_name = True
        self.num_layers_to_confirm = 50
