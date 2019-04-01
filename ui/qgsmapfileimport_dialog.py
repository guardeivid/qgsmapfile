# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsMapfileImportDialog
                                 A QGIS plugin
  This plugin helps import a Mapserver Mapfile in a Qgis Project
                             -------------------
        begin                : 2019-02-26
        git sha              : $Format:%H$
        copyright            : (C) 2018 by David Orellano
        email                : guardeivid@yahoo.com.ar
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
import mappyfile
from copy import deepcopy
from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt import uic
from ..src.mapfile_import import MapfileImport


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'qgsmapfileimport_dialog_base.ui'), resource_suffix='')


class QgsMapfileImportDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(QgsMapfileImportDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.mf = {}

        self.btnMapfilePath.clicked.connect(self.selectMapFile)
        self.btnMainMapfilePath.clicked.connect(self.selectMainMapFile)

    def selectPath(self, title, isdir=False, ext=''):
        settings = QSettings()
        lastdir = settings.value("/qgsmapfile/lastdir", "", type=str)

        if isdir:
            path = QFileDialog.getExistingDirectory(self, title, lastdir, QFileDialog.ShowDirsOnly)
        else:
            path, __ = QFileDialog.getOpenFileName(self, title, lastdir, ext)

        if path == "":
            return False

        settings.setValue("/qgsmapfile/lastdir", os.path.split(path)[0])
        return path

    def selectMapFile(self):
        mapfile = self.selectPath(self.tr("Open Mapfile"), ext="Mapfile (*.map *.lay)")
        if mapfile:
            self.txtMapfilePath.setText(mapfile)
            self.groupMainMap.setEnabled(False)
            self.mf = MapfileImport(self.iface, mapfile, True)
            if self.mf.map_type != 'map':
                self.groupMainMap.setEnabled(True)
            self.setPaths()

    def selectMainMapFile(self):
        mapfilepath = self.selectPath(self.tr("Open main Mapfile"), ext="Mapfile (*.map)")
        if mapfilepath and self.mf:
            self.txtMainMapfilePath.setText(mapfilepath)
            if self.mf.readMainMapFile(mapfilepath):
                self.setPaths()

    def setPaths(self):
        self.label_paths.setText(self.mf.from_paths)
        self.label_shapepath.setText(self.mf.relshapepath if self.mf.relshapepath else '...')
        self.label_symbolset.setText(self.mf.relsymbolsetpath if self.mf.relsymbolsetpath else '...')
        self.label_fontset.setText(self.mf.relfontsetpath if self.mf.relfontsetpath else '...')

    def accept(self):
        if self.mf:
            if len(self.mf.layers):
                for layer in self.mf.layers:
                    self.mf.addLayer(layer)
                self.close()
            else:
                self.iface.messageBar().pushWarning(self.tr('Warning'), self.tr("There are no supported layers to load"))
