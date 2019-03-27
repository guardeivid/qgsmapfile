# -*- coding: utf-8 -*-
"""docstring for import_.py"""

from builtins import str
from builtins import object

from qgis.PyQt.QtCore import QVariant, QPointF, QSizeF
from qgis.PyQt.QtGui import QFont
from qgis.core import (
    QgsPalLayerSettings,
    QgsPropertyCollection,
    QgsProperty,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsTextBackgroundSettings,
    QgsTextShadowSettings,
    QgsWkbTypes,
    QgsUnitTypes
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
                    family = font #Util.getFont(font)

        self.text_format.setFont(QFont(family, 9))

    def __getMsSizeLabel(self):
        # "labeling/fontSize" en pixel, "labeling/fontSizeInMapUnits"=false o "labeling/dataDefined/Size"
        # mapserver only integer
        size = self.mslabel.get('size', 9)
        if isinstance(size, int):
            # there is unit pixel now
            pass
        else:
            match_attr = _qgis.REGEX_ATTR.search(size)
            if match_attr:
                self.__setdataDefined(QgsPalLayerSettings.Size, match_attr.group(1))
            else:
                #TODO for Bitmap Fonts
                #tiny|small|medium|large|giant
                pass

        self.text_format.setSizeUnit(QgsUnitTypes.RenderPixels)
        self.text_format.setSize(size)

    def __getMsColorLabel(self):
        self.__getColor(self.mslabel, 'color', self.text_format, QgsPalLayerSettings.Color, True)

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
        outlinecolor = self.__getColor(self.mslabel, 'outlinecolor', self.text_buffer, QgsPalLayerSettings.BufferColor, True)
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
        self.text_background.setSize(QSizeF(pad_mm, pad_mm))

    def __getMsShapeOffsetLabel(self):
        # "labeling/shapeOffsetX", "labeling/shapeOffsetY", "labeling/shapeOffsetUnits"=1
        offset = self.msbackground.get('offset')
        if offset:
            x = _ms.getSize(offset[0], _ms.UNIT_PIXEL)
            y = _ms.getSize(offset[1], _ms.UNIT_PIXEL)
            self.text_background.setOffset(QPointF(x, y))

    def __getMsShapeColorLabel(self):
        self.__getColor(self.msbackground, 'color', self.text_background, QgsPalLayerSettings.ShapeFillColor)

    def __getMsShapeOutlinecolorLabel(self):
        self.__getColor(self.msbackground, 'outlinecolor', self.text_background, QgsPalLayerSettings.ShapeBorderColor)

    def __getMsShapeWithLabel(self):
        # "labeling/shapeBorderWidth", "labeling/shapeBorderWidthUnits"=1 o "labeling/dataDefined/ShapeBorderWidth"
        borderwidth = self.msbackground.get('with', 1)
        if isinstance(borderwidth, (int, float)):
            self.text_background.setStrokeWidth(_ms.getSize(borderwidth, _ms.UNIT_PIXEL))
        else:
            match_attr = _qgis.REGEX_ATTR.search(borderwidth)
            if match_attr:
                self.__setdataDefined(QgsPalLayerSettings.ShapeBorderWidth, match_attr.group(1))

    def __getMsShapeLinejoinLabel(self):
        # labeling/shapeJoinStyle"
        linejoin = self.msbackground.get('linejoin', 'round').lower()
        self.text_background.setJoinStyle(_ms.LINE_JOIN_STYLE[linejoin])

    #SHADOW
    def __getMsBackShadowColorLabel(self):
        self.__getColor(self.msshadow, 'color', self.text_shadow, QgsPalLayerSettings.ShadowColor, True)

    def __getMsBackShadowOffsetLabel(self):
        # "labeling/shadowOffsetAngle", "labeling/shadowOffsetDist", "labeling/shadowOffsetUnits"=1
        offset = self.msshadow.get('offset')
        if offset:
            (dist, angle) = Util.polar(offset[0], offset[1])
            self.text_shadow.setOffsetDistance(_ms.getSize(dist, _ms.UNIT_PIXEL))
            self.text_shadow.setOffsetAngle(angle)

    def __getMsShadowColorLabel(self):
        color = self.__getColor(self.mslabel, 'shadowcolor', self.text_shadow, QgsPalLayerSettings.ShadowColor, True)
        if color:
            self.text_shadow.setEnabled(True)
        return color

    def __getMsShadowSizeLabel(self):
        # "labeling/shadowOffsetAngle", "labeling/shadowOffsetDist", "labeling/shadowOffsetUnits"=1
        shadowsize = self.mslabel.get('shadowsize')
        if shadowsize:
            if isinstance(shadowsize[0], (int, float)) and isinstance(shadowsize[1], (int, float)):
                (dist, angle) = Util.polar(shadowsize[0], shadowsize[1])
                self.text_shadow.setOffsetDistance(_ms.getSize(dist, _ms.UNIT_PIXEL))
                self.text_shadow.setOffsetAngle(angle)

    #PLACEMENT
    def __getMsAngleLabel(self):
        # "labeling/placement", "labeling/angleOffset" o "labeling/dataDefined/Rotation"
        angle = self.mslabel.get('angle', 0)
        if isinstance(angle, (int, float)):
            self.pal_layer.angleOffset = angle
        else:
            match_attr = _qgis.REGEX_ATTR.search(angle)
            if match_attr:
                self.__setdataDefined(QgsPalLayerSettings.Rotation, match_attr.group(1))
            else:
                #auto|auto2|follow
                angle = angle.lower()
                if self.geom_type == QgsWkbTypes.LineGeometry and angle in _ms.LABEL_ANGLE:
                    self.position = _ms.LABEL_ANGLE[angle]
                    self.pal_layer.placement = self.position

                    if angle == 'auto2':
                        #the text may be rendered upside down
                        #_ms.LINE_PLACEMENT_FLAGS
                        pass
        return angle

    def __getMsMaxOverlapAngleLabel(self):
        # "labeling/maxCurvedCharAngleIn", "labeling/maxCurvedCharAngleOut"=-
        maxoverlapangle = float(self.mslabel.get('maxoverlapangle', 22.5))
        self.pal_layer.maxCurvedCharAngleIn = maxoverlapangle
        self.pal_layer.maxCurvedCharAngleOut = maxoverlapangle*(-1)

    def __getMsRepeatDistanceLabel(self):
        # "labeling/repeatDistance", "labeling/repeatDistanceUnit"=1 MM
        repeatdistance = int(self.mslabel.get('repeatdistance', 0))
        if repeatdistance:
            self.pal_layer.repeatDistance = _ms.getSize(repeatdistance, _ms.UNIT_PIXEL)

    def __getMsPositionLabel(self):
        # "labeling/placement"
        position = str(self.mslabel.get('position', '')).lower()
        if position == 'auto':
            self.position = QgsPalLayerSettings.AroundPoint
        else:
            if position in _ms.LABEL_POSITION:
                self.pal_layer.quadOffset = _ms.LABEL_POSITION[position]
            self.position = QgsPalLayerSettings.OverPoint

        self.pal_layer.placement = self.position

    def __getMsOffsetLabel(self):
        # "labeling/dist", "labeling/xOffset", "labeling/yOffset", "labeling/offsetType=0", "labeling/labelOffsetInMapUnits"=false
        offset = self.mslabel.get('offset')
        if offset:
            xoffset = offset[0]
            yoffset = offset[1]
            if self.position == QgsPalLayerSettings.OverPoint:
                self.pal_layer.xOffset = _ms.getSize(xoffset, _ms.UNIT_PIXEL)
                self.pal_layer.yOffset = _ms.getSize(yoffset, _ms.UNIT_PIXEL)
                self.pal_layer.offsetUnits = QgsUnitTypes.RenderPixels
            else:
                if self.position == QgsPalLayerSettings.Curved:
                    if yoffset == 99 or yoffset == -99:
                        yoffset = xoffset #atencion al signo de xoffset, negativo abajo?
                self.pal_layer.dist = _ms.getSize(yoffset, _ms.UNIT_PIXEL)
                self.pal_layer.distUnits = QgsUnitTypes.RenderPixels

    def __getMsPriorityLabel(self):
        # "labeling/priority" o "labeling/dataDefined/Priority"
        priority = self.mslabel.get('priority', 5)
        if isinstance(priority, int):
            self.pal_layer.priority = priority
        else:
            match_attr = _qgis.REGEX_ATTR.search(priority)
            if match_attr:
                self.__setdataDefined(QgsPalLayerSettings.Priority, match_attr.group(1))

    #RENDERER
    def __getMsMinScaleDenomLabel(self):
        # "labeling/scaleVisibility", "labeling/scaleMin"
        minscaledenom = self.mslabel.get('minscaledenom')
        if minscaledenom:
            self.pal_layer.scaleVisibility = True
            self.pal_layer.minimumScale = minscaledenom
        else:
            if self.labelmaxscaledenom > 0:
                self.pal_layer.scaleVisibility = True
                self.pal_layer.minimumScale = self.labelmaxscaledenom
        #TODO self.labelmaxscaledenom ? self.labelminscaledenom ?

    def __getMsMaxScaleDenomLabel(self):
        # "labeling/scaleVisibility", "labeling/scaleMax"
        maxscaledenom = self.mslabel.get('maxscaledenom')
        if maxscaledenom:
            self.pal_layer.scaleVisibility = True
            self.pal_layer.maximumScale = maxscaledenom
        else:
            if self.labelminscaledenom > 0:
                self.pal_layer.scaleVisibility = True
                self.pal_layer.maximumScale = self.labelminscaledenom
        #TODO self.labelmaxscaledenom ? self.labelminscaledenom ?

    def __getMsMinSizeLabel(self):
        # "labeling/fontLimitPixelSize", "labeling/fontMinPixelSize"
        minsize = int(self.mslabel.get('minsize', 4))
        self.pal_layer.fontLimitPixelSize = True
        self.pal_layer.fontMinPixelSize = minsize

    def __getMsMaxSizeLabel(self):
        # "labeling/fontLimitPixelSize", "labeling/fontMaxPixelSize"
        maxsize = int(self.mslabel.get('maxsize', 256))
        self.pal_layer.fontMaxPixelSize = maxsize

    def __getMsMinFeatureSizeLabel(self):
        # "labeling/minFeatureSize", "labeling/fitInPolygonOnly"
        minfeaturesize = self.mslabel.get('minfeaturesize', 'auto')
        if isinstance(minfeaturesize, int):
            self.pal_layer.minFeatureSize = _ms.getSize(minfeaturesize, _ms.UNIT_PIXEL)
        else:
            #auto
            if self.geom_type == QgsWkbTypes.PolygonGeometry:
                self.pal_layer.fitInPolygonOnly = True

    def __getMsForceLabel(self):
        # "labeling/displayAll"
        force = float(self.mslabel.get('force', False))
        if force:
            self.pal_layer.displayAll = True

    #TODO
    def __getMsPartialsLabel(self):
        # QgsPalLabeling::isShowingPartialsLabels() loadEngineSettings() setShowingPartialsLabels() saveEngineSettings()
        #q3 QgsLabelingEngineSettings() setFlag(Flag f, bool enabled=true),  writeSettingsToProject (QgsProject *project), Flag::UsePartialCandidates=2
        # mslabel
        pass

    #-----------------------------------------------------------------------------
    def __getColor(self, msobject, strcolor, qsetting, qproperty, opacity=False):
        color = msobject.get(strcolor)
        if color:
            color_ = _qgis.color(color)
            if color_[0]:
                self.__setdataDefined(qproperty, color_[1])
            else:
                if opacity:
                    qsetting.setOpacity(color_[3])
                    c = color_[2]
                    c.setAlpha(255)
                    qsetting.setColor(c)
                else:
                    qsetting.setColor(color_[2])

        return color

    def __setdataDefined(self, qproperty, field):
        self.prop_col.setProperty(qproperty, QgsProperty.fromField(field))
