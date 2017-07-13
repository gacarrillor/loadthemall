# -*- coding:utf-8 -*-
"""
/***************************************************************************
LoadThemAll
A QGIS plugin
Loads files stored in a directory structure recursively, based on several filters
                             -------------------
begin                : 2010-10-03
copyright            : (C) 2010 by Germán Carrillo (GeoTux)
email                : geotux_tuxman@linuxmail.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name():
  return "Load Them All"

def description():
  return "Loads files stored in a directory structure recursively, based on several filters"

def version():
  return "Version 2.7"

def qgisMinimumVersion():
  return "2.0"

def icon():
    return "icon.png"

def authorName():
  return "Germán Carrillo"

def classFactory(iface):
  # load LoadThemAll class from file LoadThemAll
  from LoadThemAll import LoadThemAll
  return LoadThemAll(iface)


