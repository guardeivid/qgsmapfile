# -*- coding: utf-8 -*-
"""docstring for import_.py"""

from builtins import chr
from builtins import str
from builtins import object

import os
import mappyfile
import matplotlib.font_manager

from qgis.core import (
    QgsWkbTypes,
    QgsSymbol,
    QgsMarkerSymbol,
    QgsLineSymbol,
    QgsFillSymbol,
    QgsSimpleMarkerSymbolLayer,
    QgsMarkerLineSymbolLayer,
    QgsEllipseSymbolLayer,
    QgsFontMarkerSymbolLayer,
    QgsSimpleLineSymbolLayer,
    QgsSimpleFillSymbolLayer,
    QgsCentroidFillSymbolLayer,
    QgsSVGFillSymbolLayer,
    QgsRasterFillSymbolLayer,
    QgsLinePatternFillSymbolLayer,
    QgsPointPatternFillSymbolLayer,
    QgsSvgMarkerSymbolLayer,
    QgsArrowSymbolLayer
)
from .utils import (_ms, _qgis, Util)
from .file_management import FileManagement

class SymbolImport(object):
    """docstring for SymbolImport"""
    def __init__(self, msclass, qgslayer, geom_type, sizeunits, \
        mssymbols=[], symbolsetpath='', fontset=[]):
        super(SymbolImport, self).__init__()
        self.msclass = msclass
        self.qgslayer = qgslayer
        self.geom_type = geom_type
        self.sizeunits = sizeunits
        self.mssymbols = mssymbols
        self.symbolsetpath = symbolsetpath
        self.fontset = fontset

    #--Obtener simbolo (QgsSymbol)--------------------------------------
    def getSymbol(self):
        """docstring for __getSymbol"""
        symbol = QgsSymbol.defaultSymbol(self.qgslayer.geometryType())
        new_symbol = self.__getQgsSymbol(symbol)
        if new_symbol:
            new_symbol.deleteSymbolLayer(0)
            return new_symbol
        return symbol

    def __getQgsSymbol(self, symbol):
        """docstring for __getMarkerSymbol"""
        new_symbol_layer = False
        for msstyle in self.msclass["styles"][::-1]:
            symbol_layer = None
            if self.geom_type == QgsWkbTypes.PointGeometry:
                symbol_layer = self.__getQgsMarkerSymbolLayer(msstyle)
            elif self.geom_type == QgsWkbTypes.LineGeometry:
                symbol_layer = self.__getQgsLineSymbolLayer(msstyle)
            elif self.geom_type == QgsWkbTypes.PolygonGeometry:
                symbol_layer = self.__getQgsPolygonSymbolLayer(msstyle)
            if symbol_layer:
                new_symbol_layer = True
                symbol.appendSymbolLayer(symbol_layer)
        if new_symbol_layer:
            return symbol
        return False

    #--Obtener capa de simbolo (QgsSymbolLayer)-------------------------
    def __getQgsMarkerSymbolLayer(self, msstyle):
        props = {}
        opacity = self.__getMsOpacity(msstyle)
        self.__getMsColor(msstyle, props, opacity)
        self.__getMsOutlinecolor(msstyle, props, opacity)
        self.__getMsLinejoin(msstyle, props)
        self.__getMsPattern(msstyle, props) #solo predefinido, no personalizado
        self.__getMsWidth(msstyle, props)
        self.__getMsOutline(msstyle, props)
        self.__getMsScale(msstyle, props)
        offset = self.__getMsOffset(msstyle, props)
        self.__setMsOffsetXY(offset, props)
        self.__getMsAngle(msstyle, props)
        size = self.__getMsSize(msstyle, props)
        symbol = msstyle.get('symbol', False)
        if symbol:
            (type_marker, symbolname, msSymbol, props) = self.__getMsSymbol(symbol, props)
            self.__getMsAnchorpoint(msSymbol, props)
            qgsSymbol = self.__getQgsMarkerSubSymbol(type_marker, msSymbol, size, props, False)
        else:
            self.deleteProperties(props, _qgis.SIMPLE_MARKER_SYMBOL_LAYER)
            #si no hay simbolo entonces por defecto creo un circulo
            qgsSymbol = QgsSimpleMarkerSymbolLayer.create(props)
        #print(props)
        return qgsSymbol

    def __getQgsLineSymbolLayer(self, msstyle):
        """docstring for __getLineSymbolLayer"""
        props = {}
        type_marker = ''

        symbol = msstyle.get('symbol', False)
        if symbol:
            (type_marker, symbolname, msSymbol, props) = self.__getMsSymbol(symbol, props)

        opacity = self.__getMsOpacity(msstyle)
        self.__getMsColor(msstyle, props, opacity)
        self.__getMsOutlinecolor(msstyle, props, opacity, isline=True)
        self.__getMsLinecap(msstyle, props)
        self.__getMsLinejoin(msstyle, props)
        self.__getMsPattern(msstyle, props)
        self.__getMsWidth(msstyle, props)
        self.__getMsOutline(msstyle, props)
        self.__getMsScale(msstyle, props)
        offset = self.__getMsOffset(msstyle, props)

        if not type_marker:
            self.deleteProperties(props, _qgis.SIMPLE_LINE_SYMBOL_LAYER)
            qgsSymbol = QgsSimpleLineSymbolLayer.create(props)
        else:
            props_parent = {}
            self.__setMsOffsetXY(offset, props)
            self.__getMsAngle(msstyle, props, props_parent)
            gap = self.__getMsGap(msstyle)

            if type_marker == _ms.MS_SYMBOL_ARROW:
                #El estilo de relleno de la flecha, no soportado por mapserver
                #[solid|horizontal|vertical|cross|b_diagonal|f_diagonal|diagonal_x|dense1|dense2|dense3|dense4|dense5|dense6|dense7|no]
                props['style'] = 'solid'
                props_parent['head_type'] = _qgis.MARKERS_ARROW[symbolname][0]
                props_parent['arrow_type'] = _qgis.MARKERS_ARROW[symbolname][1]
                props_parent['is_repeated'] = '1' if gap else '0'
                self.deleteProperties(props, _qgis.SIMPLE_FILL_SYMBOL_LAYER)
                qgsSubSymbol = self.__getSubSymbol(QgsFillSymbol, QgsSimpleFillSymbolLayer, QgsWkbTypes.LineGeometry, props)
                self.deleteProperties(props_parent, _qgis.ARROW_SYMBOL_LAYER)
                qgsSymbol = QgsArrowSymbolLayer.create(props_parent)
                qgsSymbol.setSubSymbol(qgsSubSymbol)
            else:
                self.__getMarkerDisplacementAndRotate(msstyle, gap, props_parent)
                self.__getMsInitialGap(msstyle, gap, props_parent)
                self.__getMsAnchorpoint(msSymbol, props)
                size = self.__getMsSize(msstyle, props)
                qgsSubSymbol = self.__getQgsMarkerSubSymbol(type_marker, msSymbol, size, props)
                self.deleteProperties(props_parent, _qgis.MARKER_LINE_SYMBOL_LAYER)
                qgsSymbol = QgsMarkerLineSymbolLayer.create(props_parent)
                qgsSymbol.setSubSymbol(qgsSubSymbol)
        #print(props)
        return qgsSymbol

    def __getQgsPolygonSymbolLayer(self, msstyle):
        props = {}
        type_marker = ''

        symbol = msstyle.get('symbol', False)
        if symbol:
            (type_marker, symbolname, msSymbol, props) = self.__getMsSymbol(symbol, props, True)

        opacity = self.__getMsOpacity(msstyle)
        color = self.__getMsColor(msstyle, props, opacity)
        self.__getMsOutlinecolor(msstyle, props, opacity)
        self.__getMsLinecap(msstyle, props)
        self.__getMsLinejoin(msstyle, props)
        self.__getMsPattern(msstyle, props)
        self.__getMsWidth(msstyle, props)
        self.__getMsOutline(msstyle, props)
        self.__getMsScale(msstyle, props)
        offset = self.__getMsOffset(msstyle, props)
        if not type_marker:
            #-linea sencilla exterior-#
            #-relleno simple (sin estilo de relleno preconfigurados)-#
            if not color:
                self.deleteProperties(props, _qgis.SIMPLE_LINE_SYMBOL_LAYER)
                qgsSymbol = QgsSimpleLineSymbolLayer.create(props)
            else:
                self.deleteProperties(props, _qgis.SIMPLE_FILL_SYMBOL_LAYER)
                qgsSymbol = QgsSimpleFillSymbolLayer.create(props)
            #-relleno de gradientes-#
            #el gradiente es para renderer por categorias continuas
            #no aplica, porque aca es para gradiente de un simbolo
        else:
            props_parent = {}
            self.__setMsOffsetXY(offset, props)
            self.__getMsAngle(msstyle, props, props_parent)
            gap = self.__getMsGap(msstyle)
            size = self.__getMsSize(msstyle, props)
            self.__getMarkerDisplacementAndRotate(msstyle, gap, props_parent)

            geomtransform = msstyle.get('geomtransform', '').lower()
            if geomtransform == 'centroid':
                #-relleno de centroides-#
                self.__getMsAnchorpoint(msSymbol, props)
                qgsSubSymbol = self.__getQgsMarkerSubSymbol(type_marker, msSymbol, size, props)
                #self.deleteProperties(props_parent, _qgis.CENTROID_FILL_SYMBOL_LAYER)
                qgsSymbol = QgsCentroidFillSymbolLayer.create({})
                qgsSymbol.setSubSymbol(qgsSubSymbol)
            elif not color:
                #-Linea exterior:linea de marcador-#
                self.__getMsAnchorpoint(msSymbol, props)
                qgsSubSymbol = self.__getQgsMarkerSubSymbol(type_marker, msSymbol, size, props)
                self.deleteProperties(props_parent, _qgis.MARKER_LINE_SYMBOL_LAYER)
                qgsSymbol = QgsMarkerLineSymbolLayer.create(props_parent)
                qgsSymbol.setSubSymbol(qgsSubSymbol)
            elif type_marker == _ms.MS_SYMBOL_HATCH:
                if not props['use_custom_dash']:
                    #-relleno simple (con estilo de relleno)-#
                    self.deleteProperties(props, _qgis.SIMPLE_LINE_SYMBOL_LAYER)
                    qgsSymbol = QgsSimpleLineSymbolLayer.create(props)
                else:
                    #-Patron de relleno de linea-#
                    self.deleteProperties(props, _qgis.SIMPLE_LINE_SYMBOL_LAYER)
                    qgsSubSymbol = self.__getSubSymbol(QgsLineSymbol, QgsSimpleLineSymbolLayer, QgsWkbTypes.LineGeometry, props)
                    self.deleteProperties(props_parent, _qgis.LINE_PATTERN_FILL_SYMBOL_LAYER)
                    qgsSymbol = QgsLinePatternFillSymbolLayer.create(props_parent)
                    qgsSymbol.setSubSymbol(qgsSubSymbol)
            elif type_marker == _ms.MS_SYMBOL_PIXMAP:
                #-relleno de imagen raster-#
                self.deleteProperties(props, _qgis.RASTER_FILL_SYMBOL_LAYER)
                qgsSymbol = QgsRasterFillSymbolLayer.create(props)
            elif type_marker == _ms.MS_SYMBOL_SVG:
                #-relleno SVG-#
                self.deleteProperties(props, _qgis.SIMPLE_LINE_SYMBOL_LAYER)
                qgsSubSymbol = self.__getSubSymbol(QgsLineSymbol, QgsSimpleLineSymbolLayer, QgsWkbTypes.LineGeometry, props)
                self.deleteProperties(props_parent, _qgis.SVG_FILL_SYMBOL_LAYER)
                qgsSymbol = QgsSVGFillSymbolLayer.create(props_parent)
                qgsSymbol.setSubSymbol(qgsSubSymbol)
            else:
                #-patron de relleno de puntos-#
                self.__getMsAnchorpoint(msSymbol, props)
                qgsSubSymbol = self.__getQgsMarkerSubSymbol(type_marker, msSymbol, size, props)
                self.deleteProperties(props_parent, _qgis.POINT_PATTERN_FILL_SYMBOL_LAYER)
                qgsSymbol = QgsPointPatternFillSymbolLayer.create(props_parent)
                qgsSymbol.setSubSymbol(qgsSubSymbol)

        #qgsSymbol.setAlpha((opacity*1.0)/100)
        #print(props)
        return qgsSymbol

    #----------------------------------------------------------------------
    def __getMsSymbol(self, symbolname, props, ispolygon=False):
        """docstring for __getMsSymbol"""
        #SYMBOL [integer|string|filename|url|attribute]
        type_marker = _ms.MS_SYMBOL_SIMPLE
        props['name'] = 'circle'
        msSymbol = None
        #buscar si es un marcador conocido
        if symbolname in _qgis.MARKERS_WELL_KNOWN:
            props['name'] = symbolname
        elif symbolname in _qgis.MARKERS_ARROW:
            type_marker = _ms.MS_SYMBOL_ARROW
            props['name'] = symbolname
        else:
            match_url = _qgis.REGEX_URL.search(symbolname)
            match_file = _qgis.REGEX_FILE.search(symbolname)
            match_attr = _qgis.REGEX_ATTR.search(symbolname)

            if match_url:
                #url
                svgpath = FileManagement.url2svg(symbolname, self.symbolsetpath)
                if svgpath:
                    props['name'] = svgpath
                    type_marker = _ms.MS_SYMBOL_SVG
            elif match_file:
                svgpath = FileManagement.file2svg(symbolname, self.symbolsetpath)
                if svgpath:
                    props['name'] = svgpath
                    type_marker = _ms.MS_SYMBOL_SVG
            elif match_attr:
                #atributo
                props['name_dd_active'] = '1'
                props['name_dd_field'] = match_attr.group(1)
            else:
                #QgsMarkerLineSymbolLayer o QgsArrowSymbolLayer
                if self.mssymbols:
                    if isinstance(symbolname, int):
                        #indice en el symbolset, empieza por 1:
                        msSymbol = self.mssymbols[symbolname - 1]
                        symbolname = msSymbol.get('name')
                    else:
                        #buscar en el symbolset el simbolo por nombre
                        msSymbol = mappyfile.find(self.mssymbols, 'name', symbolname)

                if msSymbol:
                    #print("Tiene simbolo")
                    if symbolname in _qgis.MARKERS_WELL_KNOWN:
                        #print("Tiene simbolo conocido")
                        props['name'] = symbolname
                    elif symbolname in _qgis.MARKERS_ARROW:
                        #print("Tiene simbolo de flecha")
                        type_marker = _ms.MS_SYMBOL_ARROW
                        props['name'] = symbolname
                    else:
                        #print("Busquemos otro tipo de simbolo")
                        symbol_type = msSymbol.get('type').lower()
                        if symbol_type == _ms.MS_SYMBOL_SIMPLE:
                            #type_marker = _ms.MS_SYMBOL_SIMPLE
                            type_marker = ''
                        elif symbol_type == _ms.MS_SYMBOL_VECTOR:
                            #print("Tiene simbolo de tipo vector")
                            #print(self.symbolsetpath)
                            svgpath = FileManagement.vector2svg(msSymbol, self.symbolsetpath)
                            #print(svgpath)
                            if svgpath:
                                props['name'] = svgpath
                                type_marker = _ms.MS_SYMBOL_SVG
                        elif symbol_type == _ms.MS_SYMBOL_ELLIPSE:
                            #print("Tiene simbolo de tipo ellipse")
                            svgpath = FileManagement.ellipse2svg(msSymbol, self.symbolsetpath)
                            if svgpath:
                                props['name'] = svgpath
                                type_marker = _ms.MS_SYMBOL_SVG
                            else:
                                #en este momento no es conocido,
                                #pero aplicar symbol layer de tipo elipse
                                #o usar circulo por defecto?
                                type_marker = _ms.MS_SYMBOL_ELLIPSE
                        elif symbol_type == _ms.MS_SYMBOL_SVG:
                            #print("Tiene simbolo de tipo svg")
                            props['name'] = Util.abspath(self.symbolsetpath, '', msSymbol.get('image'))
                            type_marker = _ms.MS_SYMBOL_SVG
                        elif symbol_type == _ms.MS_SYMBOL_PIXMAP:
                            #print("Tiene simbolo de tipo pixmap")
                            if ispolygon:
                                type_marker = _ms.MS_SYMBOL_PIXMAP
                            else:
                                svgpath = FileManagement.pixmap2svg(msSymbol.get('image'), self.symbolsetpath)
                                if svgpath:
                                    props['name'] = svgpath
                                    type_marker = _ms.MS_SYMBOL_SVG
                        elif symbol_type == _ms.MS_SYMBOL_HATCH:
                            #para poligonos
                            type_marker = _ms.MS_SYMBOL_HATCH if ispolygon else _ms.MS_SYMBOL_SIMPLE
                        elif symbol_type == _ms.MS_SYMBOL_TRUETYPE:
                            #print("Tiene simbolo de tipo truetype")
                            font = msSymbol.get('font', '')
                            if self.fontset and font:
                                props['font'] = Util.getFont(self.fontset.get(font))
                            else:
                                props['font'] = Util.getFont(font)
                            props['chr'] = self.__getChr(msSymbol.get('character', ''))
                            type_marker = _ms.MS_SYMBOL_TRUETYPE
        #print((type_marker, symbolname, msSymbol, props))
        return (type_marker, symbolname, msSymbol, props)

    def __getChr(self, char):
        """docstring for __getChr"""
        mt = _qgis.REGEX_CHAR.search(char)
        if mt:
            return chr(int(mt.group(1)))
        return char

    def __getSizeDefaultVector(self, msSymbol):
        points = None
        default = 0
        if msSymbol:
            points = msSymbol.get('points', [])
        if points:
            for p in points:
                height = p[1]
                if height > default:
                    default = height
        else:
            default = 1
        return str(default)

    #Parametros Mapfile----------------------------------------------------
    def __getMsOpacity(self, msstyle):
        #OPACITY [integer|attribute]
        #qgis usa la inversa del %transparencia del simbolo
        #solo aplica al symbol y no al symbollayer
        #qgis no soporta attribute
        opacity = msstyle.get('opacity', 100)
        if not isinstance(opacity, int):
            opacity = 100
        return opacity

    def __getMsColor(self, msstyle, props, opacity):
        #COLOR [r] [g] [b] | [hexadecimal string] | [attribute]
        color = msstyle.get('color')
        if color:
            color_ = _qgis.color(color, opacity)
            if color_[0]:
                props['color_dd_active'] = props['line_color_dd_active'] = '1'
                props['color_dd_field'] = props['line_color_dd_field'] = color_[1]
            else:
                props['color'] = props['line_color'] = color_[1]
            #para flecha y lineas simples
            props['style'] = props['line_style'] = 'solid'
        else:
            #para flecha y lineas simples
            props['style'] = props['line_style'] = 'no'
        return color

    def __getMsOutlinecolor(self, msstyle, props, opacity, isline=False):
        #OUTLINECOLOR [r] [g] [b] | [hexadecimal string] | [attribute]
        #Color to use for outlining polygons and certain marker symbols (ellipse, vector polygons and truetype).
        #Has no effect for lines
        #Solo aplicable a lineas con marcador y color de borde de flechas
        outlinecolor = msstyle.get('outlinecolor')
        if outlinecolor:
            outlinecolor_ = _qgis.color(outlinecolor, opacity)
            if outlinecolor_[0]:
                props['outline_color_dd_active'] = '1'
                props['outline_color_dd_field'] = outlinecolor_[1]
            else:
                props['outline_color'] = props['line_color'] = outlinecolor_[1]
            props['outline_style'] = props['line_style'] = 'solid'

        else:
            props['outline_style'] = 'no'
            if isline:
                if props['line_style'] != 'solid':
                    props['line_style'] = 'no'

    def __getMsLinecap(self, msstyle, props):
        #LINECAP [butt|round|square]
        props['capstyle'] = msstyle.get('linecap', 'round').lower()

    def __getMsLinejoin(self, msstyle, props):
        #LINEJOIN [round|miter|bevel|none]
        #qgis no soporta none
        linejoin = msstyle.get('linejoin', 'round').lower()
        props['joinstyle'] = linejoin if linejoin != 'none' else 'bevel'

    def __getMsOffset(self, msstyle, props):
        #OFFSET [x][y] en SIZEUNITS, en gral pixels
        #posible sentidos opuestos en q2.18, en q2.14 son iguales
        #TODO si es linea puede tener valor de yoffset -99 y -999
        offset = msstyle.get('offset')
        if offset:
            props['offset'] = str(_ms.getSize(offset[0], self.sizeunits))
        props['offset_unit'] = _ms.UNIT_MM
        return offset

    def __setMsOffsetXY(self, offset, props):
        #TODO si es linea puede tener valor de yoffset -99 y -999
        if offset:
            offset_x = _ms.getSize(offset[0], self.sizeunits)
            offset_y = _ms.getSize(offset[1], self.sizeunits)
            props['offset'] = "{},{}".format(offset_x, offset_y)

    def __getMsGap(self, msstyle):
        #GAP [double], posible colision con angle=AUTO
        """
        Un valor GAP negativo hara que el eje X de los simbolos se alinee con respecto a la tangente de la linea.
        Un valor GAP positivo alinea el eje X de los simbolos con respecto al eje X del dispositivo de salida
        Un GAP de 0 (el valor predeterminado) hara que los simbolos se muestren de punta a punta
        """
        return msstyle.get('gap', 0)

    def __getMsInitialGap(self, msstyle, gap, props_parent):
        #INITIALGAP [double] default GAP/2
        initialgap = msstyle.get('initialgap', (abs(gap)*1.0)/2)
        props_parent['offset_along_line'] = str(_ms.getSize(initialgap, self.sizeunits))
        props_parent['offset_along_line_unit'] = _ms.UNIT_MM

    def __getMsSize(self, msstyle, props):
        #SIZE [double|attribute]
        """Height, in layer SIZEUNITS, of the symbol/pattern to be used.
        Default value depends on the SYMBOL TYPE.
        For pixmap: the height (in pixels) of the pixmap;
        for ellipse and vector: the maximum y value of the SYMBOL POINTS parameter,
        for hatch: 1.0, for truetype: 1.0."""
        size = msstyle.get('size')
        props['size_unit'] = _ms.UNIT_PIXEL
        if size:
            if isinstance(size, (int, float)):
                props['size'] = str(size)
            else:
                match = _qgis.REGEX_ATTR.search(size)
                if match:
                    props['size_dd_active'] = '1'
                    props['size_dd_field'] = match.group(1)
        return size

    #TODO
    def __getMsScale(self, msstyle, props):
        #LINEJOINMAXSIZE [int] max length of the miter LINEJOIN, default=3
        #qgis no lo soporta

        #MAXSCALEDENOM [double]
        #MAXSIZE [double] 500 pixels
        #MAXWIDTH [double] 32 pixels
        #MINSCALEDENOM [double]
        #MINSIZE [double] 0 pixels
        #MINWIDTH [double] 0 pixels

        #'size_map_unit_scale'
        #'width_map_unit_scale', 'outline_width_map_unit_scale', "border_width_map_unit_scale"
        pass

    def __getMsAnchorpoint(self, msSymbol, props):
        #ANCHORPOINT
        #se puede obtener del simbolo y setear en qgis
        #pero no se puede setear y cambiar en el mapfile
        #a menos que se cree un simbolo por cada valor
        ANCHORPOINT_DEFAULT = [0.5, 0.5]
        if msSymbol:
            anchorpoint = msSymbol.get('anchorpoint', [0.5, 0.5])
        else:
            anchorpoint = ANCHORPOINT_DEFAULT
        props['horizontal_anchor_point'] = str(_qgis.ANCHORPOINT[str(anchorpoint[0])])
        props['vertical_anchor_point'] = str(_qgis.ANCHORPOINT[str(anchorpoint[1])])

    def __getMsAngle(self, msstyle, props, props_parent=None):
        #ANGLE [double|attribute|auto] default 0
        angle = msstyle.get('angle', 0)
        if isinstance(angle, int):
            props['angle'] = str(angle)
        elif isinstance(angle, str) and angle.lower() == 'auto':
            if isinstance(props_parent, dict):
                props_parent['rotate'] = '1'
        elif isinstance(angle, str) and angle.lower() != 'auto':
            props['angle_dd_active'] = '1'
            props['angle_dd_field'] = angle

    #TODO
    def __getMsOutline(self, msstyle, props):
        #OUTLINEWIDTH [double|attribute] Default is 0.0 in pixels
        #Ancho de la linea externa
        pass

    def __getMsPattern(self, msstyle, props, ispolygon=False):
        #PATTERN [double on] [double off] [double on] [double off] … END
        #Qgis permite patron personalizado solo en lineas simples
        #Para permitir patrones predeterminados deben tener valores estandarizados
        #Donde 1mm=0.25pixel, o usar unidad pixel por defecto para que sean numeros enteros
        pattern = msstyle.get('pattern')
        props['use_custom_dash'] = '0'
        if pattern:
            lpattern = ["{};{}".format(l[0], l[1]) for l in pattern]
            spattern = ";".join(lpattern)
            props['customdash'] = spattern
            props['customdash_unit'] = _ms.UNIT_PIXEL
            if ispolygon:
                if spattern in _qgis.PATTERN_POLYGON:
                    props['line_style'] = props['outline_style'] = _qgis.PATTERN_POLYGON[spattern]
                else:
                    props['use_custom_dash'] = '1'
            else:
                if spattern in _qgis.PATTERN_LINE:
                    props['line_style'] = props['outline_style'] = _qgis.PATTERN_LINE[spattern]
                else:
                    props['use_custom_dash'] = '1'

    def __getMsWidth(self, msstyle, props):
        #WIDTH [double|attribute]
        width = msstyle.get('width', 1.0)
        props['line_width'] = props['outline_width'] = str(_ms.getSize(width, self.sizeunits))
        props['line_width_unit'] = props['outline_width_unit'] = _ms.UNIT_MM

    #----------------------------------------------------------------------
    def __getMarkerDisplacementAndRotate(self, msstyle, gap, props_parent):
        props_parent['placement'] = 'interval'
        props_parent['interval_unit'] = _ms.UNIT_MM
        if gap > 0:
            props_parent['interval'] = str(_ms.getSize(gap, self.sizeunits))
            props_parent['rotate'] = '0'
        elif gap < 0:
            props_parent['interval'] = str(_ms.getSize(abs(gap), self.sizeunits))
            props_parent['rotate'] = '1'
        else:
            props_parent['rotate'] = '0'
            #GEOMTRANSFORM [bbox|centroid|end|labelpnt|labelpoly|start|vertices|<expression>]
            geomtransform = msstyle.get('geomtransform', '').lower()
            if geomtransform in _qgis.GEOMTRANSFORM_LINE:
                props_parent['placement'] = _qgis.GEOMTRANSFORM_LINE[geomtransform]

    def __getQgsMarkerSubSymbol(self, type_marker, msSymbol, size, props, subsym=True):
        if type_marker == _ms.MS_SYMBOL_SIMPLE:
            if not size:
                props['size'] = self.__getSizeDefaultVector(msSymbol)
            self.deleteProperties(props, _qgis.SIMPLE_MARKER_SYMBOL_LAYER)
            SymbolLayer = QgsSimpleMarkerSymbolLayer
        elif type_marker == _ms.MS_SYMBOL_ELLIPSE:
            if not size:
                props['size'] = self.__getSizeDefaultVector(msSymbol)
            self.deleteProperties(props, _qgis.ELLIPSE_SYMBOL_LAYER)
            SymbolLayer = QgsEllipseSymbolLayer
        elif type_marker == _ms.MS_SYMBOL_TRUETYPE:
            if not size:
                props['size'] = '1.0'
            self.deleteProperties(props, _qgis.FONT_MARKER_SYMBOL_LAYER)
            SymbolLayer = QgsFontMarkerSymbolLayer
        elif type_marker == _ms.MS_SYMBOL_SVG:
            if not size:
                props['size'] = '1.0'
            self.deleteProperties(props, _qgis.SVG_MARKER_SYMBOL_LAYER)
            SymbolLayer = QgsSvgMarkerSymbolLayer

        if subsym:
            return self.__getSubSymbol(QgsMarkerSymbol, SymbolLayer, QgsWkbTypes.PointGeometry, props)
        else:
            return SymbolLayer.create(props)

    def __getSubSymbol(self, Symbol, SymbolLayer, geometry_type, props):
        symbol = Symbol.defaultSymbol(geometry_type)
        symbol.deleteSymbolLayer(0)
        symbol_layer = SymbolLayer.create(props)
        symbol.appendSymbolLayer(symbol_layer)
        return symbol

    def deleteProperties(self, props, properties):
        keys = tuple(props.keys())
        for key in keys:
            if key not in properties:
                del props[key]
