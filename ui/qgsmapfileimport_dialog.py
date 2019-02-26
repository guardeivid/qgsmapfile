# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsMapfileImportDialog
                                 A QGIS plugin
 Este plugin permite importar y exportar archivos mapfile (map, lay), especialmente para la definiciion de una capa
                             -------------------
        begin                : 2018-08-04
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

        self.tableWidget.setCurrentCell(0, 0)
        #self.groupShapePath.setStyleSheet("QGroupBox#groupShapePath { border: transparent;}")

        self.tabWidget.currentChanged.connect(self.setCurrentCell)

        self.btnMapfilePath.clicked.connect(self.selectMapFile)
        self.btnMainMapfilePath.clicked.connect(self.selectMainMapFile)
        #self.btnShapePath.clicked.connect(self.selectShapeFolder)
        #self.btnSymbolsetPath.clicked.connect(self.selectSymbolsetFile)
        #self.btnFontsetPath.clicked.connect(self.selectFontsetFile)
        #self.btnIconsetPath.clicked.connect(self.selectIconsetFolder)

        self.cb_layers.currentIndexChanged.connect(self.changeLayers)

    def setCurrentCell(self, idx):
        self.tableWidget.setCurrentCell(idx, 0)

    def selectPath(self, title, isdir=False, ext=''):
        settings = QSettings()
        lastdir = settings.value("/qgsmapfile/lastdir", "", type=str)

        if isdir:
            path = QFileDialog.getExistingDirectory(self, self.tr(title), lastdir, QFileDialog.ShowDirsOnly)
        else:
            path, __ = QFileDialog.getOpenFileName(self, self.tr(title), lastdir, ext)

        if path == "":
            return False

        settings.setValue("/qgsmapfile/lastdir", os.path.split(path)[0])
        return path

    def selectMapFile(self):
        mapfile = self.selectPath("Abrir archivo MAPFILE", ext="Mapfile (*.map *.lay)")
        if mapfile:
            self.cleanAll()
            self.txtMapfilePath.setText(mapfile)
            self.mf = MapfileImport(self.iface, mapfile, True)
            self.showMapFile()

    def selectMainMapFile(self):
        mapfilepath = self.selectPath("Abrir archivo MAPFILE principal", ext="Mapfile (*.map)")
        if mapfilepath and self.mf:
            self.txtMainMapfilePath.setText(mapfilepath)
            if self.mf.readMainMapFile(mapfilepath):
                self.setPaths()

    def setPaths(self):
        self.label_paths.setText(self.mf.from_paths)
        self.label_shapepath.setText(self.mf.relshapepath if self.mf.relshapepath else '...')
        self.label_symbolset.setText(self.mf.relsymbolsetpath if self.mf.relsymbolsetpath else '...')
        self.label_fontset.setText(self.mf.relfontsetpath if self.mf.relfontsetpath else '...')

    def selectShapeFolder(self):
        #shapepath = self.selectPath("Seleccionar directorio SHAPEPATH", isdir=True)
        #if shapepath:
        #    self.txtShapePath.setText(shapepath)
        #    shapenormpath = self.mf.getNormPath(shapepath)
        #    if shapenormpath:
        #       self.mf.shapepath = shapenormpath
        #       self.mf.setRelShapePath()
        pass

    def selectSymbolsetFile(self):
        #symbolsetpath = self.selectPath("Abrir archivo SYMBOLSET", ext="SymbolSet (*.map *.sym *.txt")
        #if symbolsetpath:
        #    self.txtSymbolsetPath.setText(symbolsetpath)
        #    symbolsetnormpath = self.mf.getNormPath(symbolsetpath):
        #    if symbolsetnormpath:
        #       self.mf.symbolsetpath = symbolsetnormpath
        #       self.mf.setRelSymbolsetPath()
        #       self.showSymbolFile()
        pass

    def selectFontsetFile(self):
        #fontsetpath = self.selectPath("Abrir archivo FONTSET", ext="Fontset (*.list *.txt)")
        #if fontsetpath:
        #    self.txtFontsetPath.setText(fontsetpath)
        #    fontsetnormpath = self.mf.getNormPath(fontsetpath)
        #    if fontsetnormpath:
        #       self.mf.fontsetpath = fontsetpath
        #       self.mf.setRelFontsetPath()
        pass

    def selectIconsetFolder(self):
        #iconsetpath = self.selectPath("Seleccionar directorio ICONSET", isdir=True)
        #if iconsetpath:
        #    self.txtIconsetPath.setText(iconsetpath)
        #    iconsetnormpath = self.mf.getNormPath(iconsetpath)
        #    if iconsetnormpath:
        #       self.mf.iconsetpath = iconsetnormpath
        #       self.mf.setRelIconsetPath()
        pass

    def showMapFile(self):
        if self.mf:
            if len(self.mf.layers):
                for layer in self.mf.layers:
                    self.cb_layers.addItem(layer["name"], layer)

            #map_ = deepcopy(self.mf.mapfile)
            #vaciar memoria del mapfile?
            self.mf.mapfile = {}

            #if map_.get("config", '') != '':
            #    del map_["config"]
            #if map_.get("layers", '') != '':
            #    for l in map_["layers"]:
            #        del l["config"]
            #self.txt_mapfile_general.setPlainText(mappyfile.dumps(map_))
            if self.mf.map_type != 'map':
                self.groupMainMap.setEnabled(True)
            #else:
            self.setPaths()
            #if not self.mf.shapepath:
            #    self.groupShapePath.setEnabled(True)
            #if self.mf.symbolset:
            #    self.showSymbolFile()
            #    self.groupSymbolsetPath.setEnabled(False)
            #else:
            #    self.groupSymbolsetPath.setEnabled(True)
            #if not self.mf.fontsetpath:
            #    self.groupFontsetPath.setEnabled(True)
            #if not self.mf.iconsetpath:
            #    self.groupIconsetPath.setEnabled(True)

    def showSymbolFile(self):
        #self.txt_mapfile_symbols.setPlainText(mappyfile.dumps(self.mf.symbolset))
        pass

    def changeLayers(self, idx):
        layer = self.cb_layers.itemData(idx)
        if layer:
            self.title_.setText(layer["config"]["title"])
            self.img_layer.setPixmap(QPixmap(layer["config"]["icon"]))
            clayer = deepcopy(layer)
            del clayer["config"]
            self.txt_mapfile_layer.setPlainText(mappyfile.dumps(clayer))
        else:
            self.img_layer.setPixmap(QPixmap())

    def accept(self):
        if self.mf:
            if len(self.mf.layers):
                for layer in self.mf.layers:
                    self.mf.addLayer(layer)
                self.close()

    def cleanAll(self):
        #Pagina 1
        self.txtMapfilePath.setText("")

        self.groupMainMap.setEnabled(False)

        #self.txtShapePath.setText("")
        #self.groupShapePath.setEnabled(False)

        #self.txtSymbolsetPath.setText("")
        #self.groupSymbolsetPath.setEnabled(False)

        #self.txtFontsetPath.setText("")
        #self.groupFontsetPath.setEnabled(False)

        #self.txtIconsetPath.setText("")
        #self.groupIconsetPath.setEnabled(False)
        #Pagina 2
        self.cb_layers.clear()
        self.img_layer.setPixmap(QPixmap())
        self.title_.setText("")
        self.txt_mapfile_layer.clear()

        #self.visible_.setChecked(True)
        #self.category_.setText("")
        #self.querylable_.setChecked(True)
        #self.tolerance_unit.setCurrentIndex(-1)
        #self.tolerance_.setValue(0.001)
