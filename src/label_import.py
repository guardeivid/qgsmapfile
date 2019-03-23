# -*- coding: utf-8 -*-
"""docstring for import_.py"""

from __future__ import print_function
from builtins import str
from builtins import object

from copy import deepcopy
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QFont
from qgis.core import (
    QgsPalLayerSettings,
    QgsPropertyCollection,
    QgsProperty,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsTextBackgroundSettings,
    QgsTextShadowSettings,
    QgsWkbTypes
)
from .utils import (_ms, _qgis, Util)
from .expression_import import Expression

class LabelSettings(object):

    """docstring for LabelSettings"""
    def __init__(self, qgslayer, geom_type, labelitem, labelminscaledenom, \
        labelmaxscaledenom, fontset, msclass, mslabel, sizeunits):
        super(LabelSettings, self).__init__()
        self.qgslayer = qgslayer
        self.geom_type = geom_type
        self.labelitem = labelitem
        self.labelminscaledenom = labelminscaledenom
        self.labelmaxscaledenom = labelmaxscaledenom
        self.fontset = fontset
        self.msclass = msclass
        self.mslabel = mslabel
        self.sizeunits = sizeunits

        self.msbackground = False
        self.msshadow = False
        self.angle = False
        self.position = False

        self.pal_layer = QgsPalLayerSettings()
        self.prop_col = QgsPropertyCollection('Collection')
        self.text_format = QgsTextFormat()
        self.text_buffer = QgsTextBufferSettings()
        self.text_background = QgsTextBackgroundSettings()
        self.text_shadow = QgsTextShadowSettings()

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

        (self.msbackground, self.msshadow, backpadding) = self.__getMsGeomTransformLabel()
        #BACKGROUND o SHAPE
        if self.msbackground:
            #self.__getMsBufferLabel()
            self.__getBufferBackground(backpadding)
            self.__getMsShapeOffsetLabel()
            self.__getMsShapeColorLabel()
            self.__getMsShapeOutlinecolorLabel()
            self.__getMsShapeWithLabel()
            self.__getMsShapeLinejoinLabel()

        #SHADOW
        if self.msshadow:
            self.__getMsBackShadowColorLabel()
            self.__getMsBackShadowOffsetLabel()
        else:
            shadow = self.__getMsShadowColorLabel()
            if shadow:
                self.__getMsShadowSizeLabel()

        #PLACEMENT
        self.angle = self.__getMsAngleLabel()
        if self.geom_type == QgsWkbTypes.LineGeometry:
            #paralelo=auto, curvo=follow, horizontal=0
            #si es follow
            if self.angle == 'follow':
                self.__getMsMaxOverlapAngleLabel()
            self.__getMsRepeatDistanceLabel()
        if self.geom_type == QgsWkbTypes.PointGeometry or self.geom_type == QgsWkbTypes.PolygonGeometry:
            #desplazamiento desde el punto
            self.__getMsPositionLabel()
        self.__getMsOffsetLabel()
        self.__getMsPriorityLabel()

        #RENDERER
        self.__getMsMinScaleDenomLabel()
        self.__getMsMaxScaleDenomLabel()
        self.__getMsMinSizeLabel()
        self.__getMsMaxSizeLabel()
        if self.geom_type == QgsWkbTypes.LineGeometry or self.geom_type == QgsWkbTypes.PolygonGeometry:
            self.__getMsMinFeatureSizeLabel()
        self.__getMsForceLabel()

        self.__getMsPartialsLabel()

        self.text_format.setBuffer(self.text_buffer)
        self.text_format.setBackground(self.text_background)
        self.text_format.setShadow(self.text_shadow)
        self.pal_layer.setFormat(self.text_format)
        self.pal_layer.setDataDefinedProperties(self.prop_col)
        return self.pal_layer

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

        self.pal_layer.fieldName = text

    def __getMsFontLabel(self):
        # "labeling/fontFamily", "labeling/namedStyle"=Normal o "labeling/dataDefined/Family"
        family = _qgis.FONT_DEFAULT
        font = self.mslabel.get('font')
        if font:
            match_attr = _qgis.REGEX_ATTR.search(font)
            if match_attr:
                self.__setdataDefined(QgsPalLayerSettings.Family, match_attr.group(1))
            else:
                if self.fontset and font:
                    family = Util.getFont(self.fontset.get(font))
                else:
                    family = Util.getFont(font)

        self.text_format.setFont(QFont(family, 9))

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
                self.__setdataDefined(QgsPalLayerSettings.Size, match_attr.group(1))
            else:
                #TODO para Bitmap Fonts
                #tiny|small|medium|large|giant
                pass

        self.text_format.setSize(size)

    def __getMsColorLabel(self):
        self.__getColor(self.mslabel, 'color', self.text_format, QgsPalLayerSettings.Color)

    #FORMAT
    def __getMsWrapLabel(self):
        # "labeling/wrapChar"
        wrap = self.mslabel.get('wrap', '')
        self.pal_layer.wrapChar = wrap

    def __getMsAlignLabel(self):
        # "labeling/multilineAlign" (0,1,2)
        align = self.mslabel.get('align', 'center').lower()
        if align in _ms.ALIGN:
            self.pal_layer.multilineAlign = _ms.ALIGN[align]

    #BUFFER
    def __getMsOutlinecolorLabel(self):
        outlinecolor = self.__getColor(self.mslabel, 'outlinecolor', self.text_buffer, QgsPalLayerSettings.BufferColor)
        if outlinecolor:
            self.text_buffer.setEnabled(True)
        return outlinecolor

    def __getMsOutlinewithLabel(self):
        # "labeling/bufferSize", "labeling/bufferSizeInMapUnits"=false
        # LABEL OUTLINEWITH no soporta [attribute]
        outlinewidth = int(self.mslabel.get('outlinewidth', 1)) #only int?
        self.text_buffer.setSize(_ms.getSize(outlinewidth, self.sizeunits))

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
            self.text_background.setEnabled(True)
            background = back[0]
        elif n > 1:
            self.text_background.setEnabled(True)

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
                self.text_shadow.setEnabled(True)

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
        offset = self.msbackground.get('offset')
        if offset:
            self.__setSetting("shapeOffsetX", _ms.getSize(offset[0], _ms.UNIT_PIXEL), _qgis.BACKGROUND)
            self.__setSetting("shapeOffsetY", _ms.getSize(offset[1], _ms.UNIT_PIXEL), _qgis.BACKGROUND)

    def __getMsShapeColorLabel(self):
        self.__getColor(self.msbackground, 'color', self.text_background, QgsPalLayerSettings.ShapeFillColor)

    def __getMsShapeOutlinecolorLabel(self):
        self.__getColor(self.msbackground, 'outlinecolor', self.text_background, QgsPalLayerSettings.ShapeBorderColor)

    def __getMsShapeWithLabel(self):
        # "labeling/shapeBorderWidth", "labeling/shapeBorderWidthUnits"=1 o "labeling/dataDefined/ShapeBorderWidth"
        borderwidth = self.msbackground.get('with', 1)
        if isinstance(borderwidth, (int, float)):
            self.__setSetting("shapeBorderWidth", _ms.getSize(borderwidth, _ms.UNIT_PIXEL), _qgis.BACKGROUND)
        else:
            match_attr = _qgis.REGEX_ATTR.search(borderwidth)
            if match_attr:
                self.__setdataDefined(QgsPalLayerSettings.ShapeBorderWidth, match_attr.group(1))

    def __getMsShapeLinejoinLabel(self):
        # labeling/shapeJoinStyle"
        linejoin = self.msbackground.get('linejoin', 'round').lower()
        self.__setSetting("shapeJoinStyle", _ms.LINE_JOIN_STYLE[linejoin], _qgis.BACKGROUND)

    #SHADOW
    def __getMsBackShadowColorLabel(self):
        self.__getColor(self.msshadow, 'color', self.text_shadow, QgsPalLayerSettings.ShadowColor)

    def __getMsBackShadowOffsetLabel(self):
        # "labeling/shadowOffsetAngle", "labeling/shadowOffsetDist", "labeling/shadowOffsetUnits"=1
        offset = self.msshadow.get('offset')
        if offset:
            (dist, angle) = Util.polar(offset[0], offset[1])
            self.__setSetting("shadowOffsetDist", _ms.getSize(dist, _ms.UNIT_PIXEL), _qgis.SHADOW)
            self.__setSetting("shadowOffsetAngle", angle, _qgis.SHADOW)

    def __getMsShadowColorLabel(self):
        color = self.__getColor(self.mslabel, 'shadowcolor', self.text_shadow, QgsPalLayerSettings.ShadowColor)
        if color:
            self.text_shadow.setEnabled(True)
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
                self.__setdataDefined(QgsPalLayerSettings.Rotation, match_attr.group(1))
            else:
                #auto|auto2|follow
                angle = angle.lower()
                if self.geom_type == QgsWkbTypes.LineGeometry and angle in _ms.LABEL_ANGLE:
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
                self.__setdataDefined(QgsPalLayerSettings.Priority, match_attr.group(1))

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
            if self.geom_type == QgsWkbTypes.PolygonGeometry:
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
    def __getColor(self, msobject, strcolor, qsetting, qproperty):
        color = msobject.get(strcolor)
        if color:
            color_ = _qgis.color(color)
            if color_[0]:
                self.__setdataDefined(qproperty, color_[1])
            else:
                qsetting.setColor(color_[2])
        return color

    def __setdataDefined(self, qproperty, field):
        self.prop_col.setProperty(qproperty, QgsProperty.fromField(field))
