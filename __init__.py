# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsMapfile
                                 A QGIS plugin
 This plugin helps import a Mapserver Mapfile in a Qgis Project
                             -------------------
        begin                : 2019-02-26
        copyright            : (C) 2019 by David Orellano
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
# import os
# import site

# site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/extlibs'))

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QgsMapfile class from file QgsMapfile.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .qgsmapfile import QgsMapfile
    return QgsMapfile(iface)
