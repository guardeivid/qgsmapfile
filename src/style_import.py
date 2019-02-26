# -*- coding: utf-8 -*-
"""docstring for import_.py"""

from builtins import zip
from builtins import object
import os
from copy import deepcopy
from qgis.core import (QgsSingleSymbolRenderer, QgsCategorizedSymbolRenderer, QgsNullSymbolRenderer, \
    QgsGraduatedSymbolRenderer, QgsRuleBasedRenderer, QgsRendererRange, QgsRendererCategory)
from qgis.utils import Qgis
from .utils import (_ms, _qgis, Util)
from .symbol_import import SymbolImport
from .label_import import LabelSettings
from .expression_import import Expression
from .file_management import FileManagement


class StyleImport(object):
    """docstring for StyleImport"""
    def __init__(self, mslayer, qgslayer, symbols=[], symbolsetpath='', fontset={}):
        super(StyleImport, self).__init__()
        self.mslayer = mslayer
        self.qgslayer = qgslayer
        self.mssymbols = symbols
        self.symbolsetpath = symbolsetpath
        self.fontset = fontset

        self.geom_type = self.mslayer["config"]["geomtype"]
        self.sizeunits = self.__getSizeUnits()

        #LABEL
        self.labels = []
        self.has_labelitem = self.__hasLabelItem()
        self.labelminscaledenom = self.__getLabelMinScaledenom()
        self.labelmaxscaledenom = self.__getLabelMaxScaledenom()
        self.num_classes = 0
        self.num_labels = 0
        self.exp_class = True
        self.exp_label = False
        self.max_class = False
        self.max_label = False
        self.min_class = False
        self.min_label = False
        self.text_class = True
        self.text_label = True
        self.__getLabelProps()

        label = self.getLabel()

        #STYLE
        #classes = self.mslayer.get("classes", 0)
        #self.num_classes = len(classes) if classes else classes
        self.are_all_exp_string = False
        self.are_all_exp_logical_between = False
        self.attributes = []
        self.has_classitem = self.__hasClassItem()
        self.has_scaledenom = self.__hasScaledenom()
        self.expressions = self.__getExpressions()
        self.has_expression = self.__hasExpression()

        renderer = self.getRenderer()
        if renderer != False:
            self.qgslayer.setRenderer(renderer)

    def getRenderer(self):
        """docstring for getRenderer"""
        if self.num_classes == 0:
            return QgsNullSymbolRenderer()
        elif (self.num_classes == 1 and not self.has_classitem and not self.has_expression and not self.has_scaledenom):
            return self.__getSingleSymbolRenderer()
        else:
            if not self.has_expression:
                #if self.has_scaledenom:
                return self.__getRuleBasedRenderer()
                # Mal formado el MAPFILE, se dibujara con estilo por defecto de QGIS
                #return False
            else:
                if self.has_classitem and self.are_all_exp_string and not self.has_scaledenom:
                    return self.__getCategorizedSymbolRenderer()
                elif self.are_all_exp_logical_between and not self.has_scaledenom:
                    return self.__getGraduatedSymbolRenderer()
                return self.__getRuleBasedRenderer()

    def getLabel(self):
        """docstring for getLabel"""
        """Para setear no esta disponible hasta qgis3.0 varias funciones esenciales
         Solo se permite a traves de archivos qml para rule-based
        QgsAbstractVectorLayerLabeling QgsVectorLayer::labeling()
        QgsAbstractVectorLayerLabeling::type() (simple, rule-based)

        Obtener tipo de etiqueta:
        (X) (Simple) si
          -Tiene el mismo numero de CLASS que LABEL
            o tiene un LABEL sin CLASS MAXSCALEDENOM ni CLASS MINSCALEDENOM y
          -Tienen el mismo CLASS TEXT y
          -Tienen el mismo LABEL TEXT y
          -Tienen el mismo CLASS EXPRESSION y
          -No tienen LABEL EXPRESSION y
          -No tienen LABEL MAXSCALEDENOM y
          -No tienen LABEL MINSCALEDENOM y
          -No tienen LAYER LABELMAXSCALEDENOM y
          -No tienen LAYER LABELMINSCALEDENOM
        ( ) Sino (Rule-based)
        """
        if self.labels:
            if (self.num_labels == self.num_classes or \
                (self.num_labels == 1 and not self.max_class and not self.min_class)) and \
                self.text_class and self.text_label and self.exp_class and \
                not self.exp_label and not self.max_label and not self.min_label and \
                self.labelmaxscaledenom == -1 and self.labelminscaledenom == -1:
                #simple
                return self.__getSingleLabel()
            else:
                #rule-based
                return self.__getRuleBasedLabel()

    #--Obtener propiedades primarias---------------------------------------
    def __hasClassItem(self):
        """docstring for __hasClassItem"""
        return self.mslayer.get("classitem", False)

    def __getExpressions(self):
        """docstring for __getExpressions"""
        expressions = []
        if len(self.mslayer["classes"]) > 0:
            all_string, all_betwwen = True, True
            for msclass in self.mslayer["classes"]:
                exp = msclass.get('expression', '')
                if exp != '':
                    Expr = Expression(exp, self.has_classitem)
                    exp_type = Expr.type()
                    if exp_type[0] != Expression.TYPE_STRING:
                        all_string = False
                    if exp_type[0] != Expression.TYPE_BETWEEN:
                        all_betwwen = False
                    else:
                        self.attributes.append(exp_type[2])
                    expressions.append(exp_type)
                else:
                    expressions.append((Expression.TYPE_UNKNOWN, exp))
                    all_string = False
                    all_betwwen = False

            self.are_all_exp_string = all_string
            self.are_all_exp_logical_between = all_betwwen
        return expressions

    def __hasExpression(self):
        """docstring for __hasExpression"""
        for exp in self.expressions:
            if exp[0] != Expression.TYPE_UNKNOWN:
                return True
        return False

    def __hasScaledenom(self):
        """docstring for __hasScaledenom"""
        for msclass in self.mslayer["classes"]:
            if msclass.get('minscaledenom', False) != False or msclass.get('maxscaledenom', False) != False:
                return True
            for msstyle in msclass["styles"]:
                if msstyle.get('minscaledenom', False) != False or msstyle.get('maxscaledenom', False) != False:
                    return True
        return False

    def __getScaledenom(self, msclass, typescaledenom, mssubclass):
        """docstring for __getScaledenom
        Obtiene el min o max scalesdenom
        msclass: LAYER CLASS
        typescaledenom: 'minscaledenom'|'maxscaledenom'
        mssubclass: 'styles'|'labels'

        return valor max() de maxscaledenom, o min() de minscaledenom
        """
        scaledenom = []

        scale = int(msclass.get(typescaledenom, 0))
        if scale:
            scaledenom.append(scale)

        for msobject in msclass[mssubclass]:
            scale = int(msobject.get(typescaledenom, 0))
            if scale:
                scaledenom.append(scale)

        if not scaledenom:
            return 0
        if typescaledenom == "minscaledenom":
            return min(scaledenom)
        return max(scaledenom)

    def __getSizeUnits(self):
        #SIZEUNITS [feet|inches|kilometers|meters|miles|nauticalmiles|pixels] pixels
        sizeunit = self.mslayer.get('sizeunits', 'pixel').lower()
        if sizeunit == _ms.UNIT_PIXEL.lower():
            return _ms.UNIT_PIXEL
        return _ms.UNIT_MM
        #self.sizeunits = self.mslayer.get('sizeunits', 'pixel').lower()
        #return _ms.SIZE_UNITS[self.sizeunits]

    #Label----------------
    def __hasLabelItem(self):
        """docstring for __hasLabelItem"""
        return self.mslayer.get("labelitem", False)

    def __getLabelMinScaledenom(self):
        """docstring for __getLabelMinScaledenom"""
        return self.mslayer.get("labelminscaledenom", -1)

    def __getLabelMaxScaledenom(self):
        """docstring for __getLabelMaxScaledenom"""
        return self.mslayer.get("labelmaxscaledenom", -1)

    def __getLabelProps(self):
        """docstring for __getLabelProps """
        for c in self.mslayer.get("classes", []):
            self.num_classes += 1

            if self.num_classes == 1:
                self.text_class = c.get("text", True)
            else:
                if self.text_class != c.get("text", True):
                    self.text_class = False

            if self.num_classes == 1:
                self.exp_class = c.get("expression", True)
            else:
                if self.exp_class != c.get("expression", True):
                    self.exp_class = False

            for l in c.get("labels", []):
                self.labels.append({"class": c, "label": l})

                self.num_labels += 1
                if self.num_labels == 1:
                    self.text_label = l.get("text", True)
                else:
                    if self.text_label != l.get("text", True):
                        self.text_label = False

                if l.get("expression"):
                    self.exp_label = True
                if l.get("maxscaledenom"):
                    self.max_label = True
                if l.get("minscaledenom"):
                    self.min_label = True

            if self.num_labels == 1:
                if c.get("maxscaledenom"):
                    self.max_class = True
                if c.get("minscaledenom"):
                    self.min_class = True

    def __getLabelExpressions(self):
        """docstring for __getLabelExpressions"""
        expressions = []
        if self.labels:
            for msobject in self.labels:
                exp = msobject['label'].get('expression', '')
                if exp != '':
                    Expr = Expression(exp, self.has_labelitem)
                    exp_type = Expr.type()
                    expressions.append(exp_type)
                else:
                    exp = msobject['class'].get('expression', '')
                    if exp != '':
                        Expr = Expression(exp, self.has_labelitem)
                        exp_type = Expr.type()
                        expressions.append(exp_type)
                    else:
                        expressions.append((Expression.TYPE_UNKNOWN, exp))

        return expressions

    #--Obtener tipo de label-----------------------------------------------
    def __getSingleLabel(self):
        """docstring for __getSingleLabel"""
        """
        label = QgsPalLayerSettings();label.readFromLayer(layer)
        #label.isExpression = True;label.enabled = True
        label.drawLabels = True;label.fieldName = 'gid'
        label.writeToLayer(layer);iface.mapCanvas().refresh()
        """
        obj = self.labels[0]
        msclass = obj["class"]
        mslabel = obj["label"]

        #old version
        props = list(_qgis.LABELING_DEFAULT_OLD)
        Label = LabelSettings(self.qgslayer, self.geom_type, self.has_labelitem, \
        self.labelminscaledenom, self.labelmaxscaledenom, self.fontset, \
        msclass, mslabel, props, self.sizeunits, is_rule=False)

        #TODO q3 return, ya que seria QgsPalLayerSettings
        Label.getLabel()

    def __getRuleBasedLabel(self):
        """docstring for __getRuleBasedLabel"""
        expressions = self.__getLabelExpressions()
        root = deepcopy(_qgis.LABELING_RULES)
        root["version"] = Qgis.QGIS_VERSION
        root_rule = root["labeling"]["rules"]
        for exp, msobject in zip(expressions[::-1], self.labels[::-1]):
            rule = deepcopy(_qgis.LABELING_RULE)
            msclass = msobject["class"]
            mslabel = msobject["label"]
            name = msclass.get('name')

            if name:
                rule["description"] = name
            if exp[0] != Expression.TYPE_UNKNOWN:
                rule["filter"] = Util.escape_xml(exp[1])
            if self.labelminscaledenom != -1:
                rule["scalemaxdenom"] = self.labelminscaledenom
            if self.labelmaxscaledenom != -1:
                rule["scalemindenom"] = self.labelmaxscaledenom

            Label = LabelSettings(self.qgslayer, self.geom_type, self.has_labelitem, \
                self.labelminscaledenom, self.labelmaxscaledenom, self.fontset, \
                msclass, mslabel, rule, self.sizeunits, is_rule=True)
            Label.getLabel()
            root_rule.append(rule)

        #solo para q2
        #generar un xml con root_rule y guardar el xml en archivo qml
        qml = FileManagement.createXml(root, fileName=self.mslayer["name"], ext='qml', pretty=True)
        #cargar qml a la capa
        self.qgslayer.loadNamedStyle(qml)
        #eliminar archivo tmp
        os.remove(qml)
        #TODO q3 return, ya que seria QgsPalLayerSettings

    #--Obtener tipo de renderer--------------------------------------------
    def __getSingleSymbolRenderer(self):
        """docstring for __getSingleSymbolRenderer"""
        msclass = self.mslayer["classes"][0]
        Symbol = SymbolImport(msclass, self.qgslayer, self.geom_type, self.sizeunits, \
            self.mssymbols, self.symbolsetpath, self.fontset)
        symbol = Symbol.getSymbol()
        return QgsSingleSymbolRenderer(symbol)

    def __getCategorizedSymbolRenderer(self):
        """docstring for __getCategorizedSymbolRenderer"""
        field = self.has_classitem
        categories = []
        for exp, msclass in zip(self.expressions[::-1], self.mslayer["classes"][::-1]):
            Symbol = SymbolImport(msclass, self.qgslayer, self.geom_type, self.sizeunits, \
                self.mssymbols, self.symbolsetpath, self.fontset)
            symbol = Symbol.getSymbol()
            value = exp[1]
            label = msclass.get("name", value)
            status = False if msclass.get("status", 'on').lower() == 'off' else True
            categories.append(QgsRendererCategory(value, symbol, label, status))
        return QgsCategorizedSymbolRenderer(field, categories)

    def __getGraduatedSymbolRenderer(self):
        """docstring for __getGraduatedSymbolRenderer"""

        #Comprobar que los atributos sean el mismo, sino renderizar por basado en reglas
        if len(set(self.attributes)) != 1:
            return self.__getRuleBasedRenderer()

        rangelist = []
        field = self.has_classitem if self.has_classitem == self.attributes[0] else self.attributes[0]

        for exp, msclass in zip(self.expressions[::-1], self.mslayer["classes"][::-1]):
            Symbol = SymbolImport(msclass, self.qgslayer, self.geom_type, self.sizeunits, \
                self.mssymbols, self.symbolsetpath, self.fontset)
            symbol = Symbol.getSymbol()
            label = msclass.get("name", exp[1])
            render = False if msclass.get("status", 'on').lower() == 'off' else True
            rangelist.append(QgsRendererRange(exp[3], exp[4], symbol, label, render))

        renderer = QgsGraduatedSymbolRenderer(field, rangelist)
        renderer.setMode(QgsGraduatedSymbolRenderer.Custom)
        return renderer

    def __getRuleBasedRenderer(self):
        """docstring for __getRuleBasedRenderer"""
        root_rule = QgsRuleBasedRenderer.Rule(None)

        n = (len(self.expressions) - 1)
        i = 0
        for exp, msclass in zip(self.expressions[::-1], self.mslayer["classes"][::-1]):
            Symbol = SymbolImport(msclass, self.qgslayer, self.geom_type, self.sizeunits, \
                self.mssymbols, self.symbolsetpath, self.fontset)
            symbol = Symbol.getSymbol()
            scalemindenom = self.__getScaledenom(msclass, 'minscaledenom', 'styles')
            scalemaxdenom = self.__getScaledenom(msclass, 'maxscaledenom', 'styles')
            label = msclass.get("name", exp[1])
            state = False if msclass.get("status", 'on').lower() == 'off' else True

            filterexp = ''
            if exp[0] == Expression.TYPE_STRING and self.has_classitem:
                filterexp = "\"{}\" = '{}'".format(self.has_classitem, exp[1])
            elif exp[0] == Expression.TYPE_LIST or exp[0] == Expression.TYPE_BETWEEN or exp[0] == Expression.TYPE_LOGICAL:
                filterexp = exp[1]

            description = ''
            #Si no tiene expresion y si es la ultima regla setear a True, tener en cuenta que se puede declarar al reves
            #elserule = True if exp[0] == 'unknown' and exp[1] == '' and i == n else False
            elserule = False
            rule = QgsRuleBasedRenderer.Rule(symbol, scalemindenom, scalemaxdenom, filterexp, label, description, elserule)
            rule.setActive(state)
            root_rule.appendChild(rule)
            i += 1

        return QgsRuleBasedRenderer(root_rule)
