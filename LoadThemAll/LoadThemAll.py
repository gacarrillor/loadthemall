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
import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import (QgsApplication,
                       Qgis)
from qgis.PyQt.QtCore import (QCoreApplication,
                              QFileInfo,
                              QSettings,
                              Qt,
                              QTranslator)

from .resources.resources_rc import *
from .gui.LoadThemAllDialog import LoadThemAllDialog


class LoadThemAll:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        self.__default_action_location = True  # Default location: Plugin menu and plugin toolbar
        self.installTranslator()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/loadthemall/icon.png"), "Load them all...", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
    
        # Add toolbar button and menu item
        dsm = self.iface.dataSourceManagerToolBar()
        if len(dsm.actions()) > 1:
            before_action = dsm.actions()[1]  # Get the action after "Data source manager", which should be the 1st one
            dsm.insertAction(before_action, self.action)  # Add to toolbar
            self.iface.addLayerMenu().addAction(self.action)  # Add to menu (difficult to find)
            self.iface.addPluginToMenu("&Load them all", self.action)  # Add to plugins menu (easy to find)

            self.__default_action_location = False
        else:  # Fallback if somehow the data source manager toolbar is not able to get LTA's main action
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu("&Load them all", self.action)

        self.dockWidget = LoadThemAllDialog(self.iface.mainWindow(), self.iface)

    def unload(self):
        # Remove the plugin menu item and icon
        if not self.__default_action_location:
            self.iface.dataSourceManagerToolBar().removeAction(self.action)
            self.iface.addLayerMenu().removeAction(self.action)
            self.iface.removePluginMenu("&Load them all", self.action)
        else:
            self.iface.removePluginMenu("&Load them all", self.action)
            self.iface.removeToolBarIcon(self.action)

        self.dockWidget.close()
        self.iface.removeDockWidget(self.dockWidget)

    # run method that performs all the real work
    def run(self):
        if Qgis.QGIS_VERSION_INT >= 31300:  # Use native addTabifiedDockWidget
            self.iface.addTabifiedDockWidget(Qt.RightDockWidgetArea, self.dockWidget, raiseTab=True)
        else:
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)

    def installTranslator(self):
        userPluginPath = os.path.join(os.path.dirname(str(QgsApplication.qgisUserDatabaseFilePath())), "python/plugins/loadthemall/i18n")
        systemPluginPath = os.path.join(str(QgsApplication.prefixPath()), "python/plugins/loadthemall/i18n")
        translationPath = ''
    
        try:
            # Errors here could happen if the value cannot be converted to string or
            # if it is not subscriptable (see https://github.com/gacarrillor/loadthemall/issues/11)
            locale = QSettings().value("locale/userLocale", type=str)
            myLocale = str(locale[0:2])
        except TypeError as e:
            myLocale = 'en'
            
        if os.path.exists(userPluginPath):
            translationPath = os.path.join(userPluginPath, "loadthemall_" + myLocale + ".qm")
        else:
            translationPath = os.path.join(systemPluginPath, "loadthemall_" + myLocale + ".qm")
    
        if QFileInfo(translationPath).exists():
            self.translator = QTranslator()
            self.translator.load(translationPath)
            QCoreApplication.installTranslator(self.translator)
