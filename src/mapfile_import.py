# -*- coding: utf-8 -*-
"""docstring for import_.py"""

from future import standard_library
standard_library.install_aliases()

from builtins import str
from builtins import object

import os
import urllib.request, urllib.parse, urllib.error
import mappyfile

from qgis.PyQt.QtCore import QSettings
from qgis.core import (
    QgsProject,
    QgsWkbTypes,
    QgsLayerTreeLayer,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsDataSourceUri
)
from .utils import (_ms, _qgis, Util)
from .symbolset import SymbolSet
from .fontset import FontSet
from .style_import import StyleImport

class MapfileImport(object):
    FROM_PATHS_MAPFILE = u'(en mapfile)'
    FROM_PATHS_MEMORY = u'(en memoria)'

    """docstring for MapfileImport"""
    def __init__(self, iface, mapfilepath="", auto=False):
        super(MapfileImport, self).__init__()
        self.iface = iface
        self.mapfiledir = ''
        self.setMapfilePath(mapfilepath)
        self.param = {}
        self.mapfile = {}
        self.layers = []
        self.map_type = ''

        self.shapepath = ''
        self.relshapepath = ''

        self.symbolsetpath = ''
        self.relsymbolsetpath = ''
        #self.symbolset = {}
        self.symbols = []

        self.fontsetpath = ''
        self.relfontsetpath = ''
        self.fontset = {}

        self.from_paths = ''
        self.root = QgsProject.instance().layerTreeRoot()
        #devuelve q2 QgsLayerTreeGroup q3 QgsLayerTree que hereda todo de QgsLayerTreeGroup

        #self.iconsetpath = ''
        #self.reliconsetpath = ''

        if self.isSetPath() and auto:
            self.run()

    #def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        #return QCoreApplication.translate('QgsMapfile', message)

    def isSetPath(self):
        """docstring for isSetPath"""
        return True if self.mapfilepath != "" else False

    def setMapfilePath(self, mapfilepath):
        """docstring for setMapfilePath"""
        self.mapfilepath = mapfilepath
        if mapfilepath:
            if os.path.isfile(mapfilepath):
                self.mapfiledir = os.path.dirname(mapfilepath)

    def __setMainPaths(self):
        shapepath = self.getNormPath(self.mapfile.get("shapepath", ''))
        if shapepath:
            self.shapepath = Util.abspath(self.mapfiledir, '', shapepath)
            self.setRelShapePath()

        symbolsetpath = self.getNormPath(self.mapfile.get("symbolset", ''))
        if symbolsetpath:
            self.symbolsetpath = Util.abspath(self.mapfiledir, '', symbolsetpath)
            self.setRelSymbolsetPath()
            s = SymbolSet(self.iface, self.symbolsetpath)
            self.symbols = s.get()

        fontsetpath = self.getNormPath(self.mapfile.get("fontset", ''))
        if fontsetpath:
            self.fontsetpath = Util.abspath(self.mapfiledir, '', fontsetpath)
            self.setRelFontsetPath()
            f = FontSet(self.fontsetpath)
            self.fontset = f.get()

    def __savePaths(self):
        s = QSettings()
        s.setValue("/qgsmapfile/mapfiledir", self.mapfiledir)
        s.setValue("/qgsmapfile/shapepath", self.shapepath)
        s.setValue("/qgsmapfile/symbolsetpath", self.symbolsetpath)
        s.setValue("/qgsmapfile/fontsetpath", self.fontsetpath)
        s.setValue("/qgsmapfile/relshapepath", self.relshapepath)
        s.setValue("/qgsmapfile/relsymbolsetpath", self.relsymbolsetpath)
        s.setValue("/qgsmapfile/relfontsetpath", self.relfontsetpath)

    def __getSavedPaths(self):
        s = QSettings()
        self.mapfiledir = s.value("/qgsmapfile/mapfiledir", self.mapfiledir, type=str)
        self.shapepath = s.value("/qgsmapfile/shapepath", self.shapepath, type=str)
        self.symbolsetpath = s.value("/qgsmapfile/symbolsetpath", self.symbolsetpath, type=str)
        self.fontsetpath = s.value("/qgsmapfile/fontsetpath", self.fontsetpath, type=str)
        self.relshapepath = s.value("/qgsmapfile/relshapepath", self.relshapepath, type=str)
        self.relsymbolsetpath = s.value("/qgsmapfile/relsymbolsetpath", self.relsymbolsetpath, type=str)
        self.relfontsetpath = s.value("/qgsmapfile/relfontsetpath", self.relfontsetpath, type=str)

        s = SymbolSet(self.iface, self.symbolsetpath)
        self.symbols = s.get()
        f = FontSet(self.fontsetpath)
        self.fontset = f.get()

    def getNormPath(self, path):
        """docstring for getNormPath"""
        if not path:
            return False

        if not os.path.isabs(path):
            path = os.path.join(self.mapfiledir, path)
        return os.path.normpath(path)

    def setRelShapePath(self):
        """docstring for setRelShapePath"""
        self.relshapepath = Util.relpath(self.mapfiledir, self.shapepath)

    def setRelSymbolsetPath(self):
        """docstring for setRelSymbolsetPath"""
        self.relsymbolsetpath = Util.relpath(self.mapfiledir, self.symbolsetpath)

    def setRelFontsetPath(self):
        """docstring for setRelFontsetPath"""
        self.relfontsetpath = Util.relpath(self.mapfiledir, self.fontsetpath)

    def setRelIconsetPath(self):
        """docstring for setRelIconsetPath"""
        #self.reliconsetpath = _relpath(self.mapfiledir, self.iconsetpath)
        pass

    def run(self):
        """docstring for run"""
        if self.readMapFile():
            self.getLayers()
            self.parse()

    ###########################################################
    def readMapFile(self):
        """docstring for readMapFile"""
        try:
            if self.isSetPath():
                self.mapfile = mappyfile.open(self.mapfilepath)
                return True
            return False
        except Exception as e:
            self.iface.messageBar().pushWarning(u'Error', str(e))
            return False

    def readMainMapFile(self, mapfilepath):
        """docstring for readMapFile"""
        try:
            mapyfile = mappyfile.open(mapfilepath, expand_includes=False)
            _type = mapyfile.get("__type__")
            if _type == 'map':
                self.mapfile = mapyfile
                self.setMapfilePath(mapfilepath)
                self.__setMainPaths()
                self.__savePaths()
                self.from_paths = self.FROM_PATHS_MAPFILE
                return True
            else:
                return False
        except Exception as e:
            self.iface.messageBar().pushWarning(u'Error', str(e))
            return False

    def getLayers(self):
        """docstring for getLayers"""
        _type = self.mapfile.get("__type__")
        self.map_type = _type
        if _type == 'map':
            self.__setMainPaths()
            self.__savePaths()
            self.from_paths = self.FROM_PATHS_MAPFILE
            layers = self.mapfile.get("layers")
            if isinstance(layers, list):
                self.layers = layers
        elif _type == 'layer':
            self.layers = [self.mapfile]
            self.__getSavedPaths()
            self.from_paths = self.FROM_PATHS_MEMORY

    #TODO permitir capas OGR
    def parse(self):
        """docstring for parse"""
        for layer in self.layers:
            layer["config"] = {}
            connectiontype = self.getConnectionType(layer)
            if connectiontype == _ms.CONNTYPE_LOCAL:
                self.getConfig(layer, connectiontype, _qgis.ICON_OGR)
                if layer["config"]["type"] == _qgis.TYPE_RASTER:
                    layer["config"]["icon"] = _qgis.ICON_GRID
            elif connectiontype == _ms.CONNTYPE_POSTGIS:
                layer["config"] = self.parseDataPostgis(layer.get('data', ['']))
                fromsource = layer["config"]["fromsource"]
                if not self.isValidSource(fromsource):
                    self.layers.remove(layer)
                    continue
                layer["config"]["schema"], layer["config"]["table"] = self.findTableFromSource(fromsource)
                layer["config"]["sql"] = self.getLayerFilter(layer)
                self.getConfig(layer, connectiontype, _qgis.ICON_POSTGIS)
            elif connectiontype == _ms.CONNTYPE_WMS:
                (layer["config"], isValid) = self.parseDataWms(layer)
                if not isValid:
                    self.layers.remove(layer)
                    continue
                self.getConfig(layer, connectiontype, _qgis.ICON_WMS)
            elif connectiontype == _ms.CONNTYPE_WFS:
                (layer["config"], isValid) = self.parseDataWfs(layer)
                if not isValid:
                    self.layers.remove(layer)
                    continue
                self.getConfig(layer, connectiontype, _qgis.ICON_WFS)
            else:
                self.layers.remove(layer)

    def getConnectionType(self, layer):
        """docstring for getConncectionType"""
        return layer.get('connectiontype', 'local').lower()

    #POSTGIS###################################################
    def parseDataPostgis(self, data):
        """docstring for parseData"""
        olyr = {}
        uid, pos_uid, pos_srid, pos_scn, srid = (0, 0, 0, 0, -1)
        geom = ''

        data = data[0]
        match_uid = _ms.REGEX_UID.search(data)
        if match_uid:
            pos_uid = match_uid.start(1) - 14
            uid = match_uid.group(1)

        olyr['uid'] = uid

        match_srid = _ms.REGEX_SRID.search(data)
        if match_srid:
            pos_srid = match_srid.start(1) - 12
            srid = match_srid.group(1)

        olyr['srid'] = srid

        match_fromsource = _ms.REGEX_FROMSOURCE.search(data)
        if match_fromsource:
            pos_scn = match_fromsource.end()
            geom = data[:match_fromsource.start()].strip()

        olyr['geom'] = geom

        #If they are both set, return the smaller one.
        if pos_srid and pos_uid:
            pos_opt = pos_uid if (pos_srid > pos_uid) else pos_srid
        #If one or none is set, return the larger one.
        else:
            pos_opt = pos_srid if (pos_srid > pos_uid) else pos_uid

        #No pos_opt? Move it to the end of the string.
        if pos_opt == 0:
            pos_opt = len(data)

        olyr['fromsource'] = data[pos_scn:pos_opt]
        return olyr

    def findTableFromSource(self, fromsource):
        """docstring for findTable"""
        schema = ""
        table = ""
        match_table = _ms.REGEX_SPACE.search(fromsource)
        if match_table is None:
            # target table is one word
            match_table = _ms.REGEX_TABLE.search(fromsource)
            dtable = match_table.groupdict()
            if dtable["table_"] is None:
                schema = dtable["schema"].replace('"', '')
                table = dtable["table"].replace('"', '')
            else:
                schema = "public"
                table = dtable["table_"].replace('"', '')
        else:
            # target table is hiding in sub-select clause
            match_from = _ms.REGEX_SUBSELECT.search(fromsource)
            if match_from:
                table = match_from.group(1)

        return (schema, table)

    def isValidSource(self, fromsource):
        """docstring for isValidSource"""
        return _ms.REGEX_SOURCE_POSTGIS.search(fromsource)

    #WFS#######################################################
    def parseDataWfs(self, layer):
        NO_VALID = (False, False)
        url = layer.get('connection', '')
        metadata = layer.get('metadata', '')
        if not url or not metadata:
            return NO_VALID

        #Verificar si tiene parametro map=...&
        url = Util.url(url)
        if url is False:
            return NO_VALID

        wfs_typename = metadata.get('wfs_typename', '')
        if not wfs_typename:
            wfs_typename = metadata.get('ows_typename', '')
            if not wfs_typename:
                return NO_VALID

        wfs_filter = metadata.get('wfs_filter', '')
        if not wfs_filter:
            wfs_filter = metadata.get('ows_filter')

        wfs_geometryname = metadata.get('wfs_geometryname', '')
        if not wfs_geometryname:
            wfs_geometryname = metadata.get('ows_geometryname', 'geometry')

        wfs_maxfeatures = metadata.get('wfs_maxfeatures')
        if not wfs_maxfeatures:
            wfs_maxfeatures = metadata.get('ows_maxfeatures')

        wfs_version = metadata.get('wfs_version', '1.0.0')

        srs = "EPSG:4326"
        srs_metadata = metadata.get('wfs_srs', '').strip()
        if srs_metadata:
            srs = srs_metadata.split(" ")[0]
        else:
            srs_metadata = metadata.get('ows_srs', '').strip()
            if srs_metadata:
                srs = srs_metadata.split(" ")[0]
            else:
                srs_projection = layer.get('projection', '')
                if srs_projection and isinstance(srs_projection, str):
                    match = _ms.REGEX_PROJECTION.search(srs_projection)
                    if match:
                        srs = match.group(1).upper()

        params = {
            'service': 'WFS',
            'version': wfs_version,
            'request': 'GetFeature',
            'typename': wfs_typename,
            'srsname': srs,
            'maxfeatures': wfs_maxfeatures,
            'filter': wfs_filter
        }
        uri = url + urllib.parse.unquote(urllib.parse.urlencode(params))
        return ({"uri": uri}, True)

    #WMS#######################################################
    def parseDataWms(self, layer):
        NO_VALID = (False, False)
        url = layer.get('connection', '')
        metadata = layer.get('metadata', '')
        if not url or not metadata:
            return NO_VALID

        #Verificar si tiene parametro map=...&
        url = Util.url(url)
        if url is False:
            return NO_VALID

        wms_name = metadata.get('wms_name')
        if not wms_name:
            wms_name = metadata.get('ows_name')
            if not wms_name:
                return NO_VALID

        wms_format = metadata.get('wms_format')
        if not wms_format:
            wms_format = metadata.get('ows_format', 'image/png')

        wms_server_version = metadata.get('wms_server_version')
        if not wms_server_version:
            wms_server_version = metadata.get('ows_server_version', '1.1.0')

        srs = "CRS:84" if wms_server_version == '1.3.0' else "EPSG:4326"
        srs_metadata = metadata.get('wms_srs', '').strip()
        if srs_metadata:
            srs = srs_metadata.split(" ")[0]
        else:
            srs_metadata = metadata.get('ows_srs', '').strip()
            if srs_metadata:
                srs = srs_metadata.split(" ")[0]

        params = {
            'service': 'WMS',
            'version': wms_server_version,
            'request': 'GetMap',
            'layers': wms_name,
            'format': wms_format
        }

        if wms_server_version == '1.3.0':
            params["crs"] = srs
        else:
            params["srs"] = srs

        wms_style = metadata.get('wms_style')
        if wms_style:
            params["style"] = wms_style
        wms_sld_body = metadata.get('wms_sld_body')
        if wms_sld_body:
            params["sld_body"] = wms_sld_body
        wms_sld_url = metadata.get('wms_sld_url')
        if wms_sld_url:
            params["sld_url"] = wms_sld_url

        uri = url + urllib.parse.unquote(urllib.parse.urlencode(params))
        return ({"uri": uri}, True)

    #COMMON####################################################
    def getLayerType(self, layer):
        """docstring for getLayerType"""
        _type = layer.get('type', '').lower()

        if _type == _ms.TYPE_POINT:
            return (QgsWkbTypes.PointGeometry, _qgis.TYPE_POINT)
        if _type == _ms.TYPE_LINE:
            return (QgsWkbTypes.LineGeometry, _qgis.TYPE_LINE)
        if _type == _ms.TYPE_POLYGON:
            return (QgsWkbTypes.PolygonGeometry, _qgis.TYPE_POLYGON)
        if _type == _ms.TYPE_RASTER:
            return (QgsWkbTypes.NullGeometry, _qgis.TYPE_RASTER)

    #TODO ver como se aplica en otras capas, ademas de POSTGIS
    def getLayerFilter(self, layer):
        """docstring for getLayerFilter"""
        def substitution(filt, validation):
            #SUBSTITUTION
            match_subst = _ms.REGEX_SUBSTITUTION.finditer(filt)
            if validation and match_subst:
                for match in enumerate(match_subst):
                    old_value = match.group(1)
                    new_value = validation.get("default_" + old_value.replace('%', ''), '')
                    filt.replace(old_value, new_value)
            return filt

        proccessing = layer.get('proccessing', [])
        validation = layer.get('validation', '')
        #NATIVE FILTER
        if len(proccessing):
            for prc in proccessing:
                match_native = _ms.REGEX_NATIVE.search(prc)
                if match_native:
                    _filter = match_native.group(1)
                    return substitution(_filter, validation)

        _filter_ = ''
        _filter = layer.get('filter', '')
        if _filter:
            match_pattern = _ms.REGEX_PATTERN.search(_filter)   #pattern

            #SUBSTITUTION
            _filter = substitution(_filter, validation)
            _filteritem = layer.get('filteritem', '')
            if _filteritem:
                #Si es string agregar comillas simples
                if isinstance(_filter, str):
                    _filter = "'{}'".format(_filter)

                match_regexp = _ms.REGEX_REGEX.search(_filter)    #regexp
                #Si es expresion regular
                if match_regexp:
                    _filter = match_regexp.group(1)  #_filter.replace('/', '')
                    _filter_ = "\"{}\" ~* {}".format(_filteritem, _filter)
                elif match_pattern:
                    pass
                #Si es una cadena
                else:
                    _filter_ = "\"{}\" = {}".format(_filteritem, _filter)

            else:
                match_string = _ms.REGEX_STRING.search(_filter)   #string

                if match_pattern:
                    pass
                elif match_string:
                    pass
                else:
                    _filter_ = _filter

        return _filter_

    def getLayerTitle(self, layer):
        """docstring for getLayerTitle"""
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

    def getConfig(self, layer, connectiontype, icon):
        layer["config"]["title"] = self.getLayerTitle(layer)
        layer["config"]["connectiontype"] = connectiontype
        layer["config"]["geomtype"], layer["config"]["type"] = self.getLayerType(layer)
        layer["config"]["icon"] = icon

    #PATHS#####################################################
    def __getPostgisPath(self, mslayer):
        """docstring for __getPostgisPath"""
        _uri = "{conn} type={type} srid={srid}".format(
            conn=mslayer["connection"],
            type=mslayer["config"]["type"],
            srid=mslayer["config"]["srid"]
        )

        uri = QgsDataSourceUri(_uri)
        uri.setDataSource(
            mslayer["config"]["schema"],
            mslayer["config"]["table"],
            mslayer["config"]["geom"],
            mslayer["config"]["sql"],
            mslayer["config"]["uid"]
        )
        return uri.uri()

    #TODO obtener PATH para otros formatos kml, kmz, gpx, sqlite
    def __getLocalPath(self, mslayer, isshape=False):
        """docstring for __getLocalPath"""
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

        fullpath = Util.abspath(self.mapfilepath, path, data)
        (filepath, ext) = os.path.splitext(fullpath)

        if ext in _ms.EXTENSIONS:
            return fullpath

        return None

    def __getWfsPath(self, mslayer):
        """docstring for __getWfsPath"""
        return mslayer["config"]["uri"]

    def __getWmsPath(self, mslayer):
        """docstring for __getWmsPath"""
        return mslayer["config"]["uri"]

    ###########################################################
    def __getFilePaths(self, mslayer):
        mslayer["config"]['shapepath'] = self.shapepath
        mslayer["config"]['relshapepath'] = self.relshapepath
        mslayer["config"]['symbolsetpath'] = self.symbolsetpath
        mslayer["config"]['relsymbolsetpath'] = self.relsymbolsetpath
        mslayer["config"]['fontsetpath'] = self.fontsetpath
        mslayer["config"]['relfontsetpath'] = self.relfontsetpath
        #mslayer["config"]['iconsetpath'] = self.iconsetpath
        #mslayer["config"]['reliconsetpath'] = self.reliconsetpath
        return mslayer

    def addLayer(self, mslayer):
        """docstring for addLayer"""
        mslayer = self.__getFilePaths(mslayer)
        connectiontype = mslayer["config"]['connectiontype']
        if mslayer["config"]["type"] == _ms.TYPE_RASTER:
            if connectiontype == _ms.CONNTYPE_LOCAL:
                return self.__addLayer(self.__getLocalPath(mslayer), mslayer, _qgis.CONNTYPE_GDAL, True)
            elif connectiontype == _ms.CONNTYPE_WMS:
                return self.__addLayer(self.__getWmsPath(mslayer), mslayer, _qgis.CONNTYPE_WMS, True)
        else:
            if connectiontype == _ms.CONNTYPE_POSTGIS:
                return self.__addLayer(self.__getPostgisPath(mslayer), mslayer, _qgis.CONNTYPE_POSTGIS)
            elif connectiontype == _ms.CONNTYPE_LOCAL:   #Shapefile por defecto, no tiene extension
                return self.__addLayer(self.__getLocalPath(mslayer, True), mslayer, _qgis.CONNTYPE_OGR)
            elif connectiontype == _ms.CONNTYPE_OGR:
                return self.__addLayer(self.__getLocalPath(mslayer), mslayer, _qgis.CONNTYPE_OGR)
            elif connectiontype == _ms.CONNTYPE_WFS:
                return self.__addLayer(self.__getWfsPath(mslayer), mslayer, _qgis.CONNTYPE_WFS)
        return None

    def __addLayer(self, path, mslayer, provider, raster=False):
        """ Metodo __addLayerPostgis: agrega una capa (mslayer) al map canvas de Qgis,
        con los valores de configuracion analizados del archivo mapfile

        Args:
            mslayer (DefaultOrderedDict): Capa analizada por mappyfile.
        """
        if not path:
            return False

        name = mslayer["name"]

        if raster:
            qgslayer = QgsRasterLayer(path, name, provider)
        else:
            qgslayer = QgsVectorLayer(path, name, provider)

        if not qgslayer.isValid():
            self.iface.messageBar().pushWarning(u'Error', u"El layer {} no es valido".format(name))
            return False

        self.setScaleBasedVisibility(mslayer, qgslayer)
        self.setLayerOpacity(mslayer, qgslayer)

        if not raster:
            StyleImport(mslayer, qgslayer, self.symbols, \
                self.symbolsetpath, self.fontset)

        msgroup = self.__getMsGroup(mslayer)
        if msgroup:
            addedlayer = QgsProject.instance().addMapLayer(qgslayer, addToLegend=False)
            self.__addGroup(msgroup, qgslayer)
        else:
            addedlayer = QgsProject.instance().addMapLayer(qgslayer)

        if not addedlayer:
            self.iface.messageBar().pushWarning(u'Error', u"El layer {} no se pudo agregar al mapa".format(name))
            return False

        self.setStatus(qgslayer, mslayer)

        self.setCustomProperty(qgslayer, mslayer)
        return qgslayer

    def setScaleBasedVisibility(self, mslayer, qgslayer):
        """docstring for setScaleBasedVisibility"""
        hasScaleBasedVisibility = False
        minscale = mslayer.get('minscaledenom', 0)
        maxscale = mslayer.get('maxscaledenom', 0)
        if minscale:
            qgslayer.setMinimumScale(float(minscale))
            hasScaleBasedVisibility = True
        if maxscale:
            qgslayer.setMaximumScale(float(maxscale))
            hasScaleBasedVisibility = True

        qgslayer.setScaleBasedVisibility(hasScaleBasedVisibility)

    def setLayerOpacity(self, mslayer, qgslayer):
        """docstring for __setLayerOpacity"""
        opacity = 1
        if mslayer.get('opacity', -1) != -1:
            opacity = (int(mslayer.get('opacity')) / 100)
        elif mslayer.get('composites', '') != '':
            if mslayer['composites'][0].get('opacity', -1) != -1:
                opacity = (int(mslayer['composites'][0].get('opacity')) / 100)

        qgslayer.setOpacity(opacity)

    def setStatus(self, qgslayer, mslayer):
        status = (mslayer.get('status', 'on')).lower()
        if status == 'off':
            QgsProject.instance().layerTreeRoot().findLayer(qgslayer.id()).setItemVisibilityChecked(False)


    def setCustomProperty(self, qgslayer, mslayer):
        #TODO Guardar propiedades separadas en la capa, ya que al cargar un proyecto no conserva
        qgslayer.setCustomProperty("layer", mslayer)

    def __getMsGroup(self, mslayer):
        return mslayer.get('group')

    def __addGroup(self, msgroup, qgslayer):
        group = self.__getGroup(msgroup)
        if group is None:
            group = self.root.addGroup(msgroup)
        group.addLayer(qgslayer)

    def __getGroup(self, msgroup):
        return self.root.findGroup(msgroup)
