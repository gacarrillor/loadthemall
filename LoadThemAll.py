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
"""
import os

from PyQt4.QtCore import ( QTranslator, SIGNAL, QObject, QFileInfo, QCoreApplication, 
    QLocale, QSettings )
from PyQt4.QtGui import QIcon, QAction
from qgis.core import QgsApplication

import resources_rc # Initialize Qt resources from file resources_rc.py

from LoadThemAllDialog import LoadThemAllDialog

class LoadThemAll: 
  def __init__( self, iface ):
    # Save reference to the QGIS interface
    self.iface = iface

    self.installTranslator()

  def initGui( self ):  
    # Create action that will start plugin configuration
    self.action = QAction(QIcon( ":/plugins/loadthemall/icon.png"), \
        "Load them all...", self.iface.mainWindow() )
    # connect the action to the run method
    QObject.connect( self.action, SIGNAL( "triggered()" ), self.run ) 

    # Add toolbar button and menu item
    self.iface.addToolBarIcon( self.action )
    self.iface.addPluginToMenu( "&Load them all", self.action )

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu( "&Load them all", self.action )
    self.iface.removeToolBarIcon( self.action )

  # run method that performs all the real work
  def run(self): 
    dlg = LoadThemAllDialog( self.iface.mainWindow(), self.iface ) 
    dlg.show()

  def installTranslator( self ):
    userPluginPath = os.path.join( os.path.dirname( str( QgsApplication.qgisUserDbFilePath() ) ), "python/plugins/loadthemall" )
    systemPluginPath = os.path.join( str( QgsApplication.prefixPath() ), "python/plugins/loadthemall" )
    translationPath = ''

    locale = QSettings().value("locale/userLocale", type=str)
    myLocale = str( locale[0:2] )

    if os.path.exists( userPluginPath ):
      translationPath = os.path.join( userPluginPath, "loadthemall_" + myLocale + ".qm" )
    else:
      translationPath = os.path.join( systemPluginPath, "loadthemall_" + myLocale + ".qm" )

    if QFileInfo( translationPath ).exists():
      self.translator = QTranslator()
      self.translator.load( translationPath )
      QCoreApplication.installTranslator( self.translator )

