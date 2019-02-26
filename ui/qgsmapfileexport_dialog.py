# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsMapfileExportDialog
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

from builtins import range
import os

from qgis.PyQt import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'qgsmapfileexport_dialog_base.ui'))


class QgsMapfileExportDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(QgsMapfileExportDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

        #add etiquetas solamente, mejor
        self.listWidget.addItems(["a", "b", "c"])

        #add etiquetas solamente
        for x in ["a", "b", "c"]:
            self.listWidget.addItem(x)

        for i in range(10):
            item = QListWidgetItem("Item %i" % i)
            self.listWidget.addItem(item)

        for i in range(10):
            icon = QIcon()
            item = QListWidgetItem(icon, "Item %i" % i)
            self.listWidget.addItem(item)
