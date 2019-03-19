import os
import sys
import mappyfile
from qgis.core import (
    QgsProject,
    QgsWkbTypes,
    QgsLayerTreeLayer,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsDataSourceUri
)
from qgis import utils


class QMapy(object):
    def __init__(self, mapfilepath):
        super(QMapy, self).__init__()
        self.mapfilepath = mapfilepath
        self.mslayer = {}

    def run(self):
        self.mapfile = mappyfile.open(self.mapfilepath)
        _type = self.mapfile.get("__type__")
        if _type == 'map':
            layers = self.mapfile.get("layers")
            self.mslayer = layers[0]
        elif _type == 'layer':
            self.mslayer = self.mapfile

        self.mslayer = self.parse(self.mslayer)

        # Test SHAPEFILE
        l = self.addLayer(
            self.getLocalPath(self.mslayer, True),
            self.mslayer,
            'ogr'
        )
        print(l)

    def abspath(self, mapfilepath, dirpath, filepath):
        if os.path.isabs(filepath):
            dirpath = filepath
        elif os.path.isabs(dirpath):
            dirpath = os.path.join(dirpath, filepath)
        else:
            dirpath = os.path.join(os.path.split(mapfilepath)[0], dirpath, filepath)

        return os.path.normpath(dirpath)

    def getLocalPath(self, mslayer, isshape=False):
        data = mslayer.get("data", '')
        path = mslayer["config"].get("shapepath", '')
        #TODO permitir kml, kmz, gpx, sqlite
        #conn = mslayer.get('connection', '')

        if not data:
            return None

        data = data[0]

        if isshape:
            if not data.endswith('.shp'):
                data += ".shp"

        fullpath = self.abspath('', path, data)
        (filepath, ext) = os.path.splitext(fullpath)

        if ext in ('.shp', '.gml', '.tif', '.tiff', '.jpeg', '.jpg', '.png'):
            return fullpath

        return None

    def getLayerType(self, layer):
        _type = layer.get('type', '').lower()
        if _type == 'point':
            return (QgsWkbTypes.PointGeometry, 'Point')
        if _type == 'line':
            return (QgsWkbTypes.LineGeometry, 'MultiLineString')
        if _type == 'polygon':
            return (QgsWkbTypes.PolygonGeometry, 'MultiPolygon')
        if _type == 'raster':
            return (QgsWkbTypes.NullGeometry, 'raster')

    def getLayerTitle(self, layer):
        title = layer["name"]
        if layer.get("metadata", '') != '':
            metadata = layer["metadata"]
            if metadata.get("title", '') != '':
                title = metadata["title"]
            elif metadata.get("wms_title", '') != '':
                title = metadata["wms_title"]
            elif metadata.get("wfs_title", '') != '':
                title = metadata["wfs_title"]
            elif metadata.get("ows_title", '') != '':
                title = metadata["ows_title"]
            elif metadata.get("description", '') != '':
                title = metadata["description"]
        return title

    def parse(self, layer):
        layer["config"] = {}
        layer["config"]["title"] = self.getLayerTitle(layer)
        layer["config"]["connectiontype"] = "local"
        layer["config"]["geomtype"], layer["config"]["type"] = self.getLayerType(layer)
        return layer

    def addLayer(self, path, mslayer, provider, raster=False):
        if not path:
            return False

        name = mslayer["name"]

        if raster:
            qgslayer = QgsRasterLayer(path, name, provider)
        else:
            qgslayer = QgsVectorLayer(path, name, provider)

        if not qgslayer.isValid():
            iface.messageBar().pushWarning(u'Error', u"El layer {} no es valido".format(name))
            return False

        addedlayer = QgsProject.instance().addMapLayer(qgslayer)

        if not addedlayer:
            iface.messageBar().pushWarning(u'Error', u"El layer {} no se pudo agregar al mapa".format(name))
            return False

        return qgslayer


qm = utils.plugins['QgsMapfile']
mapfile = qm.plugin_dir + "\\tests\\data\\map\\" + "point.map"

qm = QMapy(mapfile)
qm.run()
