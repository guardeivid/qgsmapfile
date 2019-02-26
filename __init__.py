# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsMapfile
                                 A QGIS plugin
 Este plugin permite importar y exportar archivos mapfile (map, lay), especialmente para la definiciion de una capa
                             -------------------
        begin                : 2018-08-04
        copyright            : (C) 2018 by David Orellano
        email                : guardeivid@yahoo.com.ar
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QgsMapfile class from file QgsMapfile.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .qgsmapfile import QgsMapfile
    return QgsMapfile(iface)
