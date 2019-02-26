# -*- coding: utf-8 -*-
"""docstring for import_.py"""

from __future__ import print_function
from builtins import str
from builtins import object
from copy import deepcopy
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsPalLayerSettings
from qgis.utils import Qgis
from .utils import (_ms, _qgis, Util)
from .expression_import import Expression

class LabelSettings(object):

    TRUE = "1" # "true"?
    TRUE2 = "true"
    FALSE = "0" # "false"?
    FALSE2 = "false"

    """docstring for LabelSettings"""
    def __init__(self, qgslayer, geom_type, labelitem, labelminscaledenom, labelmaxscaledenom, \
        fontset, msclass, mslabel, props, sizeunits, is_rule=False, is_old=False):
        super(LabelSettings, self).__init__()
        self.qgslayer = qgslayer
        self.geom_type = geom_type
        self.labelitem = labelitem
        self.labelminscaledenom = labelminscaledenom
        self.labelmaxscaledenom = labelmaxscaledenom
        self.fontset = fontset
        self.msclass = msclass
        self.mslabel = mslabel
        self.props = props
        self.sizeunits = sizeunits
        self.is_rule = is_rule
        self.is_old = is_old

        self.background = False
        self.backshadow = False
        self.angle = False
        self.position = False

        self.qgLabel = False

        if not is_old:
            self.qgLabel = QgsPalLayerSettings()

    def getLabel(self):
        #TEXT
        self.__getMsTextLabel()
        self.__getMsFontLabel()
        self.__getMsSizeLabel()
        self.__getMsColorLabel()

        #FORMAT
        self.__getMsWrapLabel()
        self.__getMsAlignLabel()

        #BUFFER
        qbuffer = self.__getMsOutlinecolorLabel()
        if qbuffer:
            self.__getMsOutlinewithLabel()

        (self.background, self.backshadow, backpadding) = self.__getMsGeomTransformLabel()
        #BACKGROUND o SHAPE
        if self.background:
            #self.__getMsBufferLabel()
            self.__getBufferBackground(backpadding)
            self.__getMsShapeOffsetLabel()
            self.__getMsShapeColorLabel()
            self.__getMsShapeOutlinecolorLabel()
            self.__getMsShapeWithLabel()
            self.__getMsShapeLinejoinLabel()

        #SHADOW
        if self.backshadow:
            self.__getMsBackShadowColorLabel()
            self.__getMsBackShadowOffsetLabel()
        else:
            shadow = self.__getMsShadowColorLabel()
            if shadow:
                self.__getMsShadowSizeLabel()

        #PLACEMENT
        self.angle = self.__getMsAngleLabel()
        if self.geom_type == Qgis.Line:
            #paralelo=auto, curvo=follow, horizontal=0
            #si es follow
            if self.angle == 'follow':
                self.__getMsMaxOverlapAngleLabel()
            self.__getMsRepeatDistanceLabel()
        if self.geom_type == Qgis.Point or self.geom_type == Qgis.Polygon:
            #desplazamiento desde el punto
            self.__getMsPositionLabel()
        self.__getMsOffsetLabel()
        self.__getMsPriorityLabel()

        #RENDERER
        self.__getMsMinScaleDenomLabel()
        self.__getMsMaxScaleDenomLabel()
        self.__getMsMinSizeLabel()
        self.__getMsMaxSizeLabel()
        if self.geom_type == Qgis.Line or self.geom_type == Qgis.Polygon:
            self.__getMsMinFeatureSizeLabel()
        self.__getMsForceLabel()

        self.__getMsPartialsLabel()

        if not self.is_rule:
            self.__setCustomsProperties()

        #print(self.props)
        return self.qgLabel

        #https://qgis.org/api/2.18/qgspallabeling_8h_source.html
        #https://qgis.org/api/2.2/qgspallabeling_8cpp_source.html
        #669

    #TEXT
    def __getMsTextLabel(self):
        # "labeling/fieldName", "labeling/isExpression"
        # buscar por LABEL TEXT despues por CLASS TEXT, despues LAYER LABELITEM
        isExpression = True
        text = self.mslabel.get('text', '')
        if not text:
            text = self.msclass.get('text', '')
            if not text:
                isExpression = False
                text = self.labelitem

        if isExpression:
            Expr = Expression(text, self.labelitem, True)
            (exp_type, text) = Expr.type()

        if self.is_rule:
            isExpression = self.TRUE if isExpression else self.FALSE
        else:
            isExpression = self.TRUE2 if isExpression else self.FALSE2

        self.__setSetting("fieldName", text, _qgis.TEXT_STYLE)
        self.__setSetting("isExpression", isExpression, _qgis.TEXT_STYLE)

    def __getMsFontLabel(self):
        # "labeling/fontFamily", "labeling/namedStyle"=Normal o "labeling/dataDefined/Family"
        family = _qgis.FONT_DEFAULT
        font = self.mslabel.get('font')
        if font:
            match_attr = _qgis.REGEX_ATTR.search(font)
            if match_attr:
                self.__setdataDefined("Family", field=match_attr.group(1))
            else:
                if self.fontset and font:
                    family = Util.getFont(self.fontset.get(font))
                else:
                    family = Util.getFont(font)

        self.__setSetting("fontFamily", family, _qgis.TEXT_STYLE)

    def __getMsSizeLabel(self):
        # "labeling/fontSize" en pixel, "labeling/fontSizeInMapUnits"=false o "labeling/dataDefined/Size"
        #mapserver solo integer
        #fontSizeInMapUnits; //true if font size is in map units (otherwise in points)
        """
        https://qgis.org/api/2.18/qgspallabeling_8h_source.html#217
        enum SizeUnit{Points = 0, MM, MapUnits, Percent}
        """
        size = 9
        size_ = self.mslabel.get('size', 9)
        print(size_)
        if isinstance(size_, int):
            #ptsTomm = ( unit == Points ? 0.352778 : 1 )
            size = size_ * _ms.PIXEL_MM * _ms.MM_PTS
        else:
            match_attr = _qgis.REGEX_ATTR.search(size_)
            if match_attr:
                self.__setdataDefined("Size", field=match_attr.group(1))
            else:
                #TODO para Bitmap Fonts
                #tiny|small|medium|large|giant
                pass

        self.__setSetting("fontSize", size, _qgis.TEXT_STYLE)

    def __getMsColorLabel(self):
        # "labeling/textColorA", "labeling/textColorB", "labeling/textColorG", "labeling/textColorR", "labeling/textTransp" o "labeling/dataDefined/Color"
        self.__getColor(self.mslabel, 'color', 'textColor', _qgis.TEXT_STYLE, 'Color', \
            alpha=False, transp='textTransp')

    #FORMAT
    def __getMsWrapLabel(self):
        # "labeling/wrapChar"
        wrap = self.mslabel.get('wrap', '')
        self.__setSetting("wrapChar", wrap, _qgis.TEXT_FORMAT, escape=True)

    def __getMsAlignLabel(self):
        # "labeling/multilineAlign" (0,1,2)
        align = self.mslabel.get('align', 'center').lower()
        if align in _ms.ALIGN:
            self.__setSetting("multilineAlign", _ms.ALIGN[align], _qgis.TEXT_FORMAT)

    #BUFFER
    def __getMsOutlinecolorLabel(self):
        # "labeling/bufferDraw", "labeling/bufferColorA", "labeling/bufferColorB", "labeling/bufferColorG", "labeling/bufferColorR", "labeling/bufferTransp" o "labeling/dataDefined/BufferColor"
        outlinecolor = self.__getColor(self.mslabel, 'outlinecolor', 'bufferColor', \
            _qgis.TEXT_BUFFER, 'BufferColor', alpha=False, transp='bufferTransp')
        if outlinecolor:
            #TODO verificar si 1 funciona igual que true para simple label
            self.__setSetting("bufferDraw", self.TRUE, _qgis.TEXT_BUFFER)
        return outlinecolor

    def __getMsOutlinewithLabel(self):
        # "labeling/bufferSize", "labeling/bufferSizeInMapUnits"=false
        # LABEL OUTLINEWITH no soporta [attribute]
        outlinewidth = int(self.mslabel.get('outlinewidth', 1)) #only int?
        self.__setSetting("bufferSize", _ms.getSize(outlinewidth, self.sizeunits), _qgis.TEXT_BUFFER)

    #BACKGROUND
    def __getMsGeomTransformLabel(self):
        # "labeling/shapeDraw"=true-false, "labeling/shapeType"=0
        background = False
        backshadow = False
        backpadding = 1 #Mapserver usa 1 pixel
        msstyles = self.mslabel.get('styles', [])
        back = []
        for msstyle in msstyles:
            geomtransform = msstyle.get('geomtransform', '').lower()
            if geomtransform == 'labelpoly':
                back.append(msstyle)

        n = len(back)
        if n == 1:
            self.__setSetting("shapeDraw", self.TRUE, _qgis.BACKGROUND)
            background = back[0]
        elif n > 1:
            self.__setSetting("shapeDraw", self.TRUE, _qgis.BACKGROUND)

            #Puede que este 1 para el borde, WIDTH y OUTLINECOLOR (primero)
            #otro para el relleno, COLOR con posibilidad de padding con WIDTH y OUTLINECOLOR del mismo color que COLOR
            # y otro para la sombra, con OFFSET y COLOR (ultimo)
            background = back[n-1]
            background2 = back[n-2]

            #determinar si algun style puede servir de padding del background
            #solo se va a verificar en los dos ultimos styles
            pad = self.__getBackPadding(background)
            if pad:
                backpadding = pad #background
                background = background2
            else:
                pad = self.__getBackPadding(background2)
                if pad:
                    backpadding = pad #background2

            if backpadding > 1:
                if n > 2:
                    backshadow = back[n-3] # o back[0]?
            else:
                backshadow = background2

            if backshadow:
                self.__setSetting("shadowDraw", self.TRUE, _qgis.SHADOW)

        return (background, backshadow, backpadding)

    def __getBackPadding(self, msback):
        #determinar si tiene WIDTH y OUTLINECOLOR igual a COLOR
        width = msback.get("width", 1)
        outlinecolor = msback.get("outlinecolor")
        color = msback.get("color")

        if width > 1 and outlinecolor and color and outlinecolor == color:
            return width
        return None

    #TODO
    def __getMsBufferLabel(self):
        # "labeling/shapeSizeX", "labeling/shapeSizeY", "labeling/shapeSizeUnits"=1 MM
        #msbuffer = int(self.mslabel.get('buffer', 0))
        #msbuffer = _ms.getSize(msbuffer, _ms.UNIT_PIXEL)
        #self.__setSetting("shapeSizeX", msbuffer, _qgis.BACKGROUND)
        #self.__setSetting("shapeSizeY", msbuffer, _qgis.BACKGROUND)
        pass

    def __getBufferBackground(self, padding):
        # "labeling/shapeSizeX", "labeling/shapeSizeY", "labeling/shapeSizeUnits"=1 MM
        pad_mm = _ms.getSize(padding, _ms.UNIT_PIXEL)
        self.__setSetting("shapeSizeX", pad_mm, _qgis.BACKGROUND)
        self.__setSetting("shapeSizeY", pad_mm, _qgis.BACKGROUND)

    def __getMsShapeOffsetLabel(self):
        # "labeling/shapeOffsetX", "labeling/shapeOffsetY", "labeling/shapeOffsetUnits"=1
        offset = self.background.get('offset')
        if offset:
            self.__setSetting("shapeOffsetX", _ms.getSize(offset[0], _ms.UNIT_PIXEL), _qgis.BACKGROUND)
            self.__setSetting("shapeOffsetY", _ms.getSize(offset[1], _ms.UNIT_PIXEL), _qgis.BACKGROUND)

    def __getMsShapeColorLabel(self):
        # "labeling/shapeFillColorA", "labeling/shapeFillColorB", "labeling/shapeFillColorG", "labeling/shapeFillColorR" o "labeling/dataDefined/ShapeFillColor"
        self.__getColor(self.background, 'color', 'shapeFillColor', _qgis.BACKGROUND, 'ShapeFillColor')

    def __getMsShapeOutlinecolorLabel(self):
        # "labeling/shapeBorderColorA", "labeling/shapeBorderColorB", "labeling/shapeBorderColorG", "labeling/shapeBorderColorR" o "labeling/dataDefined/ShapeBorderColor"
        self.__getColor(self.background, 'outlinecolor', 'shapeBorderColor', _qgis.BACKGROUND, 'ShapeBorderColor')

    def __getMsShapeWithLabel(self):
        # "labeling/shapeBorderWidth", "labeling/shapeBorderWidthUnits"=1 o "labeling/dataDefined/ShapeBorderWidth"
        borderwidth = self.background.get('with', 1)
        if isinstance(borderwidth, (int, float)):
            self.__setSetting("shapeBorderWidth", _ms.getSize(borderwidth, _ms.UNIT_PIXEL), _qgis.BACKGROUND)
        else:
            match_attr = _qgis.REGEX_ATTR.search(borderwidth)
            if match_attr:
                self.__setdataDefined("ShapeBorderWidth", field=match_attr.group(1))

    def __getMsShapeLinejoinLabel(self):
        # labeling/shapeJoinStyle"
        linejoin = self.background.get('linejoin', 'round').lower()
        self.__setSetting("shapeJoinStyle", _ms.LINE_JOIN_STYLE[linejoin], _qgis.BACKGROUND)

    #SHADOW
    def __getMsBackShadowColorLabel(self):
        # "labeling/shadowColorB", "labeling/shadowColorG", "labeling/shadowColorR", "labeling/shadowTransparency" o "labeling/dataDefined/ShadowColor"
        self.__getColor(self.backshadow, 'color', 'shadowColor', _qgis.SHADOW, 'ShadowColor', \
            alpha=False, transp='shadowTransparency')

    def __getMsBackShadowOffsetLabel(self):
        # "labeling/shadowOffsetAngle", "labeling/shadowOffsetDist", "labeling/shadowOffsetUnits"=1
        offset = self.backshadow.get('offset')
        if offset:
            (dist, angle) = Util.polar(offset[0], offset[1])
            self.__setSetting("shadowOffsetDist", _ms.getSize(dist, _ms.UNIT_PIXEL), _qgis.SHADOW)
            self.__setSetting("shadowOffsetAngle", angle, _qgis.SHADOW)

    def __getMsShadowColorLabel(self):
        # "labeling/shadowDraw", "labeling/shadowColorB", "labeling/shadowColorG", "labeling/shadowColorR", "labeling/shadowTransparency" o "labeling/dataDefined/ShadowColor"
        color = self.__getColor(self.mslabel, 'shadowcolor', 'shadowColor', _qgis.SHADOW, \
            'ShadowColor', alpha=False, transp='shadowTransparency')
        if color:
            self.__setSetting("shadowDraw", self.TRUE, _qgis.SHADOW)
        return color

    def __getMsShadowSizeLabel(self):
        # "labeling/shadowOffsetAngle", "labeling/shadowOffsetDist", "labeling/shadowOffsetUnits"=1
        shadowsize = self.mslabel.get('shadowsize')
        if shadowsize:
            if isinstance(shadowsize[0], (int, float)) and isinstance(shadowsize[1], (int, float)):
                (dist, angle) = Util.polar(shadowsize[0], shadowsize[1])
                self.__setSetting("shadowOffsetDist", _ms.getSize(dist, _ms.UNIT_PIXEL), _qgis.SHADOW)
                self.__setSetting("shadowOffsetAngle", angle, _qgis.SHADOW)

    #PLACEMENT
    def __getMsAngleLabel(self):
        # "labeling/placement", "labeling/angleOffset" o "labeling/dataDefined/Rotation"
        angle = self.mslabel.get('angle', 0)
        if isinstance(angle, (int, float)):
            self.__setSetting("angleOffset", angle, _qgis.PLACEMENT)
        else:
            match_attr = _qgis.REGEX_ATTR.search(angle)
            if match_attr:
                self.__setdataDefined("Rotation", field=match_attr.group(1))
            else:
                #auto|auto2|follow
                angle = angle.lower()
                if self.geom_type == Qgis.Line and angle in _ms.LABEL_ANGLE:
                    self.position = _ms.LABEL_ANGLE[angle]
                    self.__setSetting("placement", self.position, _qgis.PLACEMENT)

                    if angle == 'auto2':
                        #the text may be rendered upside down
                        #_ms.LINE_PLACEMENT_FLAGS
                        pass
        return angle

    def __getMsMaxOverlapAngleLabel(self):
        # "labeling/maxCurvedCharAngleIn", "labeling/maxCurvedCharAngleOut"=-
        maxoverlapangle = float(self.mslabel.get('maxoverlapangle', 22.5))
        self.__setSetting("maxCurvedCharAngleIn", maxoverlapangle, _qgis.PLACEMENT)
        self.__setSetting("maxCurvedCharAngleOut", maxoverlapangle*(-1), _qgis.PLACEMENT)

    def __getMsRepeatDistanceLabel(self):
        # "labeling/repeatDistance", "labeling/repeatDistanceUnit"=1 MM
        repeatdistance = int(self.mslabel.get('repeatdistance', 0))
        if repeatdistance:
            self.__setSetting("repeatDistance", _ms.getSize(repeatdistance, _ms.UNIT_PIXEL), _qgis.PLACEMENT)

    def __getMsPositionLabel(self):
        # "labeling/placement"
        position = str(self.mslabel.get('position', '')).lower()
        if position == 'auto':
            self.position = QgsPalLayerSettings.AroundPoint
        else:
            if position in _ms.LABEL_POSITION:
                self.__setSetting("quadOffset", _ms.LABEL_POSITION[position], _qgis.PLACEMENT)
            self.position = QgsPalLayerSettings.OverPoint

        self.__setSetting("placement", self.position, _qgis.PLACEMENT)

    def __getMsOffsetLabel(self):
        # "labeling/dist", "labeling/xOffset", "labeling/yOffset", "labeling/offsetType=0", "labeling/labelOffsetInMapUnits"=false
        offset = self.mslabel.get('offset')
        if offset:
            xoffset = offset[0]
            yoffset = offset[1]
            if self.position == QgsPalLayerSettings.OverPoint:
                self.__setSetting("xOffset", _ms.getSize(xoffset, _ms.UNIT_PIXEL), _qgis.PLACEMENT)
                self.__setSetting("yOffset", _ms.getSize(yoffset, _ms.UNIT_PIXEL), _qgis.PLACEMENT)
                self.__setSetting("labelOffsetInMapUnits", self.FALSE, _qgis.PLACEMENT)
            else:
                if self.position == QgsPalLayerSettings.Curved:
                    if yoffset == 99 or yoffset == -99:
                        yoffset = xoffset #atencion al signo de xoffset, negativo abajo?
                self.__setSetting("dist", _ms.getSize(yoffset, _ms.UNIT_PIXEL), _qgis.PLACEMENT)
                self.__setSetting("distInMapUnits", self.FALSE, _qgis.PLACEMENT)

    def __getMsPriorityLabel(self):
        # "labeling/priority" o "labeling/dataDefined/Priority"
        priority = self.mslabel.get('priority', 5)
        if isinstance(priority, int):
            self.__setSetting("priority", priority, _qgis.PLACEMENT)
        else:
            match_attr = _qgis.REGEX_ATTR.search(priority)
            if match_attr:
                self.__setdataDefined("Priority", field=match_attr.group(1))

    #RENDERER
    def __getMsMinScaleDenomLabel(self):
        # "labeling/scaleVisibility", "labeling/scaleMin"
        minscaledenom = self.mslabel.get('minscaledenom')
        if minscaledenom:
            self.__setSetting("scaleVisibility", self.TRUE, _qgis.RENDERING)
            self.__setSetting("scaleMin", minscaledenom, _qgis.RENDERING)
        else:
            if self.labelmaxscaledenom > 0:
                self.__setSetting("scaleVisibility", self.TRUE, _qgis.RENDERING)
                self.__setSetting("scaleMin", self.labelmaxscaledenom, _qgis.RENDERING)
        #TODO self.labelmaxscaledenom ? self.labelminscaledenom ?

    def __getMsMaxScaleDenomLabel(self):
        # "labeling/scaleVisibility", "labeling/scaleMax"
        maxscaledenom = self.mslabel.get('maxscaledenom')
        if maxscaledenom:
            self.__setSetting("scaleVisibility", self.TRUE, _qgis.RENDERING)
            self.__setSetting("scaleMax", maxscaledenom, _qgis.RENDERING)
        else:
            if self.labelminscaledenom > 0:
                self.__setSetting("scaleVisibility", self.TRUE, _qgis.RENDERING)
                self.__setSetting("scaleMax", self.labelminscaledenom, _qgis.RENDERING)
        #TODO self.labelmaxscaledenom ? self.labelminscaledenom ?

    def __getMsMinSizeLabel(self):
        # "labeling/fontLimitPixelSize", "labeling/fontMinPixelSize"
        minsize = int(self.mslabel.get('minsize', 4))
        self.__setSetting("fontLimitPixelSize", self.TRUE, _qgis.RENDERING)
        self.__setSetting("fontMinPixelSize", minsize, _qgis.RENDERING)

    def __getMsMaxSizeLabel(self):
        # "labeling/fontLimitPixelSize", "labeling/fontMaxPixelSize"
        maxsize = int(self.mslabel.get('maxsize', 256))
        self.__setSetting("fontMaxPixelSize", maxsize, _qgis.RENDERING)

    def __getMsMinFeatureSizeLabel(self):
        # "labeling/minFeatureSize", "labeling/fitInPolygonOnly"
        minfeaturesize = self.mslabel.get('minfeaturesize', 'auto')
        if isinstance(minfeaturesize, int):
            self.__setSetting("minFeatureSize", _ms.getSize(minfeaturesize, _ms.UNIT_PIXEL), _qgis.RENDERING)
        else:
            #auto
            if self.geom_type == Qgis.Polygon:
                self.__setSetting("fitInPolygonOnly", self.TRUE, _qgis.PLACEMENT)

    def __getMsForceLabel(self):
        # "labeling/displayAll"
        force = float(self.mslabel.get('force', False))
        if force:
            self.__setSetting("displayAll", self.TRUE, _qgis.RENDERING)

    #TODO
    def __getMsPartialsLabel(self):
        # QgsPalLabeling::isShowingPartialsLabels() loadEngineSettings() setShowingPartialsLabels() saveEngineSettings()
        #q3 QgsLabelingEngineSettings() setFlag(Flag f, bool enabled=true),  writeSettingsToProject (QgsProject *project), Flag::UsePartialCandidates=2
        # mslabel
        pass

    #-----------------------------------------------------------------------------
    def __getColor(self, msobject, strcolor, prop, group, dataDefined, alpha=True, transp=''):
        color = msobject.get(strcolor)
        if color:
            color_ = _qgis.color(color)
            if color_[1]:
                self.__setdataDefined(dataDefined, field=color_[0])
            else:
                if self.is_rule:
                    self.__setSetting(prop, color_[0], group)
                else:
                    channels = ['R', 'G', 'B']
                    if alpha:
                        channels.append('A')
                    else:
                        #Convertir alpha a transparency (255=0%)
                        if transp:
                            self.__setSetting(transp, _qgis.transp(color_[5]), group)

                    i = 2
                    for c in channels:
                        self.__setSetting(prop + c, color_[i], group)
                        i += 1
        return color

    def __setSetting(self, key, value, group=False, escape=False):
        if escape:
            value = Util.escape_xml(str(value))
        if self.is_rule:
            if group:
                self.props["rule"]["settings"][group][key] = value
        else:
            self.props.append(("labeling/" + key, value))

    def __setdataDefined(self, data, active=True, useExpr=False, expr='', field=''):
        #valLabel.setDataDefinedProperty(QgsPalLayerSettings.Size,True,True,'%f' %(textSize),'')
        if not self.is_rule:
            values = []
            newPropertyName = "labeling/dataDefined/" + data
            values.append(self.TRUE if active else self.FALSE)
            values.append(self.TRUE if useExpr else self.FALSE)
            values.append(Util.escape_xml(expr))
            values.append(field)
            propertyValue = QVariant("~~".join(values))
            self.props.append((newPropertyName, propertyValue))
        else:
            self.props["rule"]["data-defined"][data] = {
                'expr': Util.escape_xml(expr),
                'field': field,
                'active': self.TRUE2 if active else self.FALSE2,
                'useExpr': self.TRUE2 if useExpr else self.FALSE2
            }

    def __setCustomsProperties(self):
        for prop in self.props:
            self.qgslayer.setCustomProperty(prop[0], str(prop[1]))
