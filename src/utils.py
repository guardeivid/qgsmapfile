# -*- coding: utf-8 -*-

from builtins import str
from builtins import range
from builtins import object

import sys
import os
import re
import math
import matplotlib.font_manager

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsPalLayerSettings #Qgis

class _ms(object):
    REGEX_UID = re.compile(r" using unique (\w*)", re.I)
    REGEX_SRID = re.compile(r" using srid=([-]?\d*)", re.I)
    REGEX_FROMSOURCE = re.compile(r" from ", re.I)
    REGEX_SPACE = re.compile(r" ") #\s+
    REGEX_TABLE = re.compile(r"(?P<schema>.*)\.(?P<table>.*)|(?P<table_>.*)")
    REGEX_SUBSELECT = re.compile(r"(\(.*\)) as", re.I | re.S | re.M | re.U)
    REGEX_SOURCE_POSTGIS = re.compile(r"(\(.*\) as \w*|\"?\w*\"?\.\"?\w*\"?|\"?\w*\"?)", re.I | re.S | re.M | re.U)
    REGEX_NATIVE = re.compile(r"^NATIVE_FILTER=(.*)$")
    REGEX_SUBSTITUTION = re.compile(r"(%+\w*%+)+")
    REGEX_PATTERN = re.compile(r"^\\((.*?)\\)$")
    REGEX_STRING = re.compile(r"^(\w*)$")
    REGEX_REGEX = re.compile(r"^/(.*)/$") #r"^/(.*?)/$"
    REGEX_PROJECTION = re.compile(r"(epsg:\d*)$", re.I)

    TYPE_POINT = 'point'
    TYPE_LINE = 'line'
    TYPE_POLYGON = 'polygon'
    TYPE_RASTER = 'raster'

    CONNTYPE_LOCAL = 'local'
    CONNTYPE_OGR = 'ogr'
    CONNTYPE_POSTGIS = 'postgis'
    CONNTYPE_WFS = 'wfs'
    CONNTYPE_WMS = 'wms'

    SIZE_UNITS = {
        "feet": 0.0833333333333333, #12,
        "inches": 1,
        "kilometers": 0.00002539998628400741, #39370.1,
        "meters": 0.0253999862840074, #39.3701,
        "miles": 63360.0,
        "dd": 4374754,
        "nauticalmiles": 72913.3858,
        "pixels": 1
    }

    UNIT_PIXEL = 'Pixel'
    UNIT_MM = 'MM'

    PIXEL_MM = 0.26458333331386 #qgis usa 0.28
    MM_PIXEL = 3.77952755933333 #qgis usa 1/0.28 = 3.5714285714285714285714285714286
    MM_PTS = 2.834643
    PTS_MM = 0.352778

    MS_SYMBOL_VECTOR = 'vector'
    MS_SYMBOL_ELLIPSE = 'ellipse'
    MS_SYMBOL_PIXMAP = 'pixmap'
    MS_SYMBOL_SIMPLE = 'simple'
    MS_SYMBOL_TRUETYPE = 'truetype'
    MS_SYMBOL_HATCH = 'hatch'
    MS_SYMBOL_SVG = 'svg'
    MS_SYMBOL_ARROW = 'arrow'

    EXTENSIONS = ('.shp', '.gml', '.tif', '.tiff', '.jpeg', '.jpg', '.png')

    ALIGN = {
        "left": QgsPalLayerSettings.MultiLeft,
        "center": QgsPalLayerSettings.MultiCenter,
        "right": QgsPalLayerSettings.MultiRight
    }

    LINE_JOIN_STYLE = {
        'miter': Qt.MiterJoin,  #0
        'bevel': Qt.BevelJoin,  #64
        'round': Qt.RoundJoin,  #128 default mapserver
        'none': Qt.BevelJoin    #default qgis
    }

    LABEL_ANGLE = {
        "auto": QgsPalLayerSettings.Line,
        "auto2": QgsPalLayerSettings.Line,
        "follow": QgsPalLayerSettings.Curved
    }

    LABEL_POSITION = {
        'ul': QgsPalLayerSettings.QuadrantAboveLeft,
        'uc': QgsPalLayerSettings.QuadrantAbove,
        'ur': QgsPalLayerSettings.QuadrantAboveRight,
        'cl': QgsPalLayerSettings.QuadrantLeft,
        'cc': QgsPalLayerSettings.QuadrantOver,
        'cr': QgsPalLayerSettings.QuadrantRight,
        'll': QgsPalLayerSettings.QuadrantBelowLeft,
        'lc': QgsPalLayerSettings.QuadrantBelow,
        'lr':QgsPalLayerSettings.QuadrantBelowRight
    }

    LINE_PLACEMENT_FLAGS = {
        'OnLine'    : 1,
        'AboveLine' : 2,
        'BelowLine' : 4,
        'MapOrientation' : 8
    }

    @staticmethod
    def color(qgcolor):
        a = qgcolor.alpha()

        if a < 255:
            rrggbb = qgcolor.name().upper()
            aa = format(a, '02X')  #rellenar con 0, 2 digitos de ancho, en formato hex
            return rrggbb + aa

        return [qgcolor.red(), qgcolor.green(), qgcolor.blue()]

    @classmethod
    def getSize(cls, size, unit):
        if unit == cls.UNIT_PIXEL:
            return size * cls.PIXEL_MM
        return size


class _qgis(object):
    REGEX_ATTR = re.compile(r'^\[(.*)\]$') #^\[(\w*)\]$'
    REGEX_URL = re.compile(r'^http', re.I)
    REGEX_FILE = re.compile(r"^(?!http://).*\.([a-z]{3,4})$", re.I)
    REGEX_CHAR = re.compile(r"&#(.*);")

    TYPE_POINT = 'Point'
    TYPE_LINE = 'MultiLineString'
    TYPE_POLYGON = 'MultiPolygon'
    TYPE_RASTER = 'raster'

    #Tipos vectores
    CONNTYPE_OGR = 'ogr'
    CONNTYPE_POSTGIS = 'postgres'
    CONNTYPE_GPX = 'gpx'
    CONNTYPE_CSV = 'delimitedtext'
    CONNTYPE_SLITE = 'spatialite'
    CONNTYPE_WFS = 'WFS'
    CONNTYPE_VIRTUAL = 'virtual'
    CONNTYPE_MEMORY = 'memory'

    #Tipos raster
    CONNTYPE_GDAL = 'gdal'  #por defecto
    CONNTYPE_WMS = 'wms'
    CONNTYPE_WCS = 'wcs'

    ICON_POSTGIS = ':/plugins/QgsMapfile/img/mActionAddPostgisLayer.svg'
    ICON_OGR = ':/plugins/QgsMapfile/img/mActionAddOgrLayer.svg'
    ICON_WFS = ':/plugins/QgsMapfile/img/mActionAddWfsLayer.svg'
    ICON_GRID = ':/plugins/QgsMapfile/img/mActionAddRasterLayer.svg'
    ICON_WMS = ':/plugins/QgsMapfile/img/mActionAddWmsLayer.svg'

    MARKERS_WELL_KNOWN = ["square", "rectangle", "diamond", "pentagon", "hexagon", "triangle", \
    "equilateral_triangle", "star", "arrow", "filled_arrowhead", "circle", "cross", "cross_fill", \
    "x", "line", "arrowhead", "cross2", "semi_circle", "third_circle", "quarter_circle", \
    "quarter_square", "half_square", "diagonal_half_square", "right_half_triangle", \
    "left_half_triangle"] #2.18

    MARKERS_ARROW = {
        "": ("", "")
    }

    #estan en MM y ms en PIXEL
    #usar una relacion que permita elegir los patrones predeterminados de qgis
    #1mm=2.5pixel
    #"4;2" => "10;5"
    #"1;2" => "2.5;5"
    #"4;2;1;2" => "10;5;2.5;5"
    #"4;2;1;2;1;2" => "10;5;2.5;5;2.5;5"
    PATTERN_LINE = {
        "10;5": 'dash',
        "2.5;5": 'dot',
        "10;5;2.5;5": 'dash dot',
        "10;5;2.5;5;2.5;5": 'dash dot dot'
    }

    PATTERN_POLYGON = {}


    UNIT = ['MM', 'Pixel', 'MapUnit']

    ANCHORPOINT = {
        "0": '0',
        "0.5": '1',
        "1": '2'
    }

    GEOMTRANSFORM_LINE = {
        "vertices": 'vertex',
        "start": 'firstvertex',
        "end": 'lastvertex'
    }

    #----------------------------------
    #Propiedades QgsMarkerSymbolLayerV2
    SIMPLE_MARKER_SYMBOL_LAYER = [u'outline_width', u'outline_color', \
    u'angle', u'name', u'scale_method', u'color', u'outline_style', u'size_unit', \
    u'joinstyle', u'horizontal_anchor_point', u'size_map_unit_scale', \
    u'outline_width_unit', u'offset', u'offset_map_unit_scale', \
    u'outline_width_map_unit_scale', u'size', u'vertical_anchor_point', u'offset_unit']
    ELLIPSE_SYMBOL_LAYER = [u'symbol_height_map_unit_scale', u'color', u'outline_style', \
    u'joinstyle', u'outline_width_unit', u'symbol_width_unit', u'size', u'angle', \
    u'offset_unit', u'size_unit', u'size_map_unit_scale', u'offset_map_unit_scale', \
    u'outline_width', u'symbol_width', u'offset', u'symbol_width_map_unit_scale', \
    u'outline_color', u'vertical_anchor_point', u'symbol_name', u'symbol_height_unit', \
    u'horizontal_anchor_point', u'outline_width_map_unit_scale', u'symbol_height']
    FONT_MARKER_SYMBOL_LAYER = [u'outline_width', u'outline_color', u'angle', u'offset_unit', \
    u'color', u'outline_width_unit', u'joinstyle', u'size_unit', u'horizontal_anchor_point', \
    u'size_map_unit_scale', u'chr', u'offset', u'offset_map_unit_scale', \
    u'outline_width_map_unit_scale', u'font', u'vertical_anchor_point', u'size']
    SVG_MARKER_SYMBOL_LAYER = [u'outline_width', u'outline_color', u'angle', u'name', \
    u'scale_method', u'color', u'size_unit', u'horizontal_anchor_point', \
    u'size_map_unit_scale', u'outline_width_unit', u'offset', u'offset_map_unit_scale', \
    u'outline_width_map_unit_scale', u'size', u'vertical_anchor_point', u'offset_unit']
    #QgsFilledMarkerSymbolLayer 2.16
    FILLED_MARKER_SYMBOL_LAYER = [u'angle', u'name', u'scale_method', u'color', u'size_unit', \
    u'horizontal_anchor_point', u'size_map_unit_scale', u'offset', u'offset_map_unit_scale', \
    'size', u'vertical_anchor_point', u'offset_unit']
    #---------------------------------
    #Propiedades QgsLineSymbolLayerV2
    SIMPLE_LINE_SYMBOL_LAYER = [u'line_color', u'line_width', u'use_custom_dash', \
    u'offset_unit', u'draw_inside_polygon', u'capstyle', u'customdash_unit', u'joinstyle', \
    u'customdash_map_unit_scale', u'offset', u'customdash', u'offset_map_unit_scale', \
    u'line_style', u'line_width_unit', u'width_map_unit_scale']
    ARROW_SYMBOL_LAYER = [u'head_thickness_unit_scale', u'arrow_width', \
    u'head_length_unit', u'arrow_width_unit', u'offset_unit_scale', u'offset_unit', \
    u'head_length', u'head_length_unit_scale', u'head_thickness_unit', \
    u'arrow_start_width', u'head_type', u'is_repeated', u'arrow_start_width_unit', \
    u'arrow_start_width_unit_scale', u'offset', u'is_curved', u'head_thickness', \
    u'arrow_type', u'arrow_width_unit_scale']
    MARKER_LINE_SYMBOL_LAYER = [u'interval_unit', u'offset_along_line_unit', \
    u'placement', u'offset_unit', u'interval', u'offset', u'offset_along_line', \
    u'rotate', u'offset_along_line_map_unit_scale', u'offset_map_unit_scale', \
    u'interval_map_unit_scale']
    #-----------------------------------
    #Propiedades de QgsFillSymbolLayerV2
    SIMPLE_FILL_SYMBOL_LAYER = [u'outline_width', u'outline_color', u'offset_unit', \
    u'color', u'outline_style', u'style', u'joinstyle', u'outline_width_unit', \
    u'border_width_map_unit_scale', u'offset', u'offset_map_unit_scale']
    #Linea exterior: linea sencilla = SIMPLE_LINE_SYMBOL_LAYER
    #Linea exterior: flecha = ARROW_SYMBOL_LAYER
    #Linea exterior: linea de marcador = MARKER_LINE_SYMBOL_LAYER
    CENTROID_FILL_SYMBOL_LAYER = [u'point_on_surface', u'point_on_all_parts']
    GRADIENT_FILL_SYMBOL_LAYER = [u'coordinate_mode', u'angle', u'offset_unit', u'color', \
    'color_type', u'gradient_color2', u'color1', u'discrete', u'color2', u'offset', \
    u'offset_map_unit_scale', u'reference_point2', u'reference_point1_iscentroid', \
    u'type', u'reference_point1', u'reference_point2_iscentroid', u'spread']
    LINE_PATTERN_FILL_SYMBOL_LAYER = [u'distance', u'line_width_map_unit_scale', \
    u'angle', u'offset_unit', u'line_width', u'color', u'distance_unit', \
    u'outline_width_unit', u'distance_map_unit_scale', u'offset', u'offset_map_unit_scale', \
    u'outline_width_map_unit_scale', u'line_width_unit']
    POINT_PATTERN_FILL_SYMBOL_LAYER = [u'displacement_y_unit', u'displacement_x', \
    u'displacement_y', u'displacement_y_map_unit_scale', u'displacement_x_unit', \
    u'outline_width_unit', u'distance_x_unit', u'distance_x_map_unit_scale', \
    u'distance_x', u'distance_y_map_unit_scale', u'distance_y_unit', \
    u'outline_width_map_unit_scale', u'displacement_x_map_unit_scale', u'distance_y']
    RASTER_FILL_SYMBOL_LAYER = [u'coordinate_mode', u'angle', u'offset_unit', u'offset', \
    u'imageFile', u'width', u'width_unit', u'offset_map_unit_scale', u'alpha', \
    u'width_map_unit_scale']
    SVG_FILL_SYMBOL_LAYER = [u'outline_width', u'outline_color', u'angle', u'color', \
    u'svgFile', u'width', u'outline_width_unit', u'svg_outline_width_map_unit_scale', \
    u'pattern_width_unit', u'outline_width_map_unit_scale', u'svg_outline_width_unit', \
    u'pattern_width_map_unit_scale']

    #---------------------------------

    FONT_DEFAULT = 'MS Shell Dlg 2'#'MS Serif'

    LABEL_POSITION_MAP = {
        QgsPalLayerSettings.QuadrantAboveLeft:  'ul',
        QgsPalLayerSettings.QuadrantAbove:      'uc',
        QgsPalLayerSettings.QuadrantAboveRight: 'ur',
        QgsPalLayerSettings.QuadrantLeft:       'cl',
        QgsPalLayerSettings.QuadrantOver:       'cc',
        QgsPalLayerSettings.QuadrantRight:      'cr',
        QgsPalLayerSettings.QuadrantBelowLeft:  'll',
        QgsPalLayerSettings.QuadrantBelow:      'lc',
        QgsPalLayerSettings.QuadrantBelowRight: 'lr'
    }

    #-----------------------------------------
    TEMPLATE_SVG = {
        "version": "1.1",
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "baseProfile": "full",
        "width": "100%",
        "height": "100%",
        "xml:space": "preserve"
    }

    SVG_PROPS_STROKE = {
        "stroke": "param(outline) #000",
        "stroke-opacity": "param(outline-opacity)",
        "stroke-width": "param(outline-width) 1"
    }

    SVG_PROPS_FILL = {
        "fill": "param(fill) #AAA",
        "fill-opacity": "param(fill-opacity)"
    }

    SVG_PROPS_NO_FILL = {
        "fill": "none"
    }

    @staticmethod
    def transp(alpha):
        return 100 - int(round(float(alpha)/2.55))

    @classmethod
    def color(cls, mscolor, opacity=100):
        n = len(mscolor)
        a = int(round(opacity*2.55))
        color_ = QColor("red") #color de error
        if isinstance(mscolor, list):
            if n == 3:
                color_ = QColor(mscolor[0], mscolor[1], mscolor[2], a)
        elif isinstance(mscolor, str):
            match = cls.REGEX_ATTR.search(mscolor)
            if mscolor[:1] == "#":
                r = int(mscolor[1:3], 16)
                g = int(mscolor[3:5], 16)
                b = int(mscolor[5:7], 16)
                if n == 7:
                    color_ = QColor(r, g, b, a)
                elif n == 9:
                    a2 = int(mscolor[7:9], 16)
                    #unificar "a" con opacity y alpha del string
                    a = int(round((a+a2)/2))
                    color_ = QColor(r, g, b, a)
            elif match:
                #Color es definido por atributo
                return (True, match.group(1))
            else:
                if mscolor in QColor.colorNames():
                    color_ = QColor(mscolor)
                    color_.setAlpha(a)
        r = color_.red()
        g = color_.green()
        b = color_.blue()
        a = color_.alpha()
        o = a/255
        qcolor_ = "{},{},{},{}".format(r, g, b, a)
        return (False, qcolor_, color_, o)

    def getSize(self, size, unit):
        pass

class Util(object):
    """docstring for Util"""
    @staticmethod
    def relpath(cwd, path):
        """Create a relative path for path from cwd, if possible"""
        #https://stackoverflow.com/questions/7287996/python-get-relative-path-from-comparing-two-absolute-paths#answer-43982145
        if sys.platform == "win32":
            cwd = cwd.lower()
            path = path.lower()

        if os.path.isfile(cwd):
            _cwd = os.path.dirname(cwd)
        else:
            _cwd = cwd
        _cwd = os.path.abspath(_cwd).split(os.path.sep)
        _path = os.path.abspath(path).split(os.path.sep)
        equal_until_pos = None
        for i in range(min(len(_cwd), len(_path))):
            if _cwd[i] != _path[i]:
                break
            else:
                equal_until_pos = i
        if equal_until_pos is None:
            return path
        newpath = [".." for i in range(len(_cwd[equal_until_pos + 1:]))]
        newpath.extend(_path[equal_until_pos + 1:])
        if newpath:
            return os.path.join(*newpath)
        return "."

    @staticmethod
    def abspath(mapfilepath, dirpath, filepath):
        """docstring for _abspath
        'mapfilepath': ruta absoluta al archivo mapfile
        'dirpath': ruta rel/abs a un directorio contenedor del archivo 'filepath', ej shapepath
        'filepath': ruta rel/abs a un archivo, ej shapefile

        return: ruta absoluta del archivo 'filepath'
        """
        #Obtener ruta absoluta al archivo
        if os.path.isabs(filepath):
            dirpath = filepath
        elif os.path.isabs(dirpath):
            dirpath = os.path.join(dirpath, filepath)
        else:
            dirpath = os.path.join(os.path.split(mapfilepath)[0], dirpath, filepath)

        return os.path.normpath(dirpath)

    @staticmethod
    def bool(value):
        """Convertir un texto a boolean"""
        return str(value).lower() not in ("no", "n", "false", "f", "0", "0.0", "", "none", "[]", "{}")

    @staticmethod
    def dict2xml(d, root_node=None):
        """ Simple xml serializer. @author Reimund Trost 2013
            https://gist.github.com/reimund/5435343
        """
        wrap = False if root_node is None or isinstance(d, list) else True
        root = 'objects' if root_node is None else root_node
        root_singular = root[:-1] if root[-1] == 's' and root_node is None else root
        xml = ''
        children = []

        if isinstance(d, dict):
            for key, value in dict.items(d):
                if isinstance(value, dict):
                    children.append(Util.dict2xml(value, key))
                elif isinstance(value, list):
                    children.append(Util.dict2xml(value, key))
                else:
                    if value:
                        xml = xml + ' ' + key + '="' + str(value) + '"'
        else:
            for value in d:
                children.append(Util.dict2xml(value, root_singular))

        end_tag = '>' if children else '/>'

        if wrap or isinstance(d, dict):
            xml = '<' + root + xml + end_tag

        if children:
            for child in children:
                xml = xml + child

            if wrap or isinstance(d, dict):
                xml = xml + '</' + root + '>'

        return xml

    @staticmethod
    def escape_xml(s):
        """https://github.com/quandyfactory/dicttoxml"""
        if isinstance(s, str):
            s = Util.unicode_me(s)
            s = s.replace('&', '&amp;')
            s = s.replace('"', '&quot;')
            #s = s.replace('\'', '&apos;')
            s = s.replace('<', '&lt;')
            s = s.replace('>', '&gt;')
        return s

    @staticmethod
    def unicode_me(something):
        """Converts strings with non-ASCII characters to unicode for LOG.
        Python 3 doesn't have a `unicode()` function, so `unicode()` is an alias
        for `str()`, but `str()` doesn't take a second argument, hence this kludge.
        https://github.com/quandyfactory/dicttoxml
        """
        try:
            return str(something, 'utf-8')
        except:
            return str(something)

    @staticmethod
    def rec(r, theta):
        """returns x, x"""
        x = float("{0:.8f}".format(r * math.cos(math.radians(((theta) % 360) + 270)))) + 0
        y = float("{0:.8f}".format(r * math.sin(math.radians(((theta) % 360) + 270)))) * (-1) + 0
        return (x, y)

    @staticmethod
    def polar(x, y):
        """returns r, theta(degrees)"""
        r = (x ** 2 + y ** 2) ** .5
        theta = (int(math.degrees(math.atan2((-1)*y, x))) + 450) % 360
        return (r, theta)

    @staticmethod
    def getFont(msfont):
        """docstring for __getFont"""
        font = _qgis.FONT_DEFAULT

        if msfont != '':
            msfont = os.path.basename(msfont)
            for f in matplotlib.font_manager.fontManager.ttflist:
                if os.path.basename(f.fname) == msfont:
                    #print "<Font '%s' (%s) %s %s %s %s>" % (f.name, os.path.basename(f.fname), \
                    #f.style, f.variant, #f.weight, f.stretch)
                    font = f.name
                    break
        return font

    @staticmethod
    def url(uri):
        match = re.match(r"^https?://", uri)
        if not match:
            return False

        uri = uri.split("?")

        map_ = ''
        if len(uri) > 1:
            for m in uri[1].split("&"):
                if m.lower().startswith("map="):
                    map_ = m + '&'
                    break
        return "{}?{}".format(uri[0], map_)

'''
print(_mapserver.TYPE_POLYGON)

qc = QColor("#ee4507")
qc.setAlpha(10)

qc = QColor(145, 25, 85, 41)

ms = _mapserver()
print(ms.color(qc))


print(_qgis.TYPE_POLYGON)
qg = _qgis()
mscolor = [154, 245, 78]
mscolor = '#12451212'
mscolor = 'blue'
print qg.color(mscolor, 50).name()
print qg.color(mscolor, 50).alpha()
'''
