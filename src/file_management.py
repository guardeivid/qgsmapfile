# -*- coding: utf-8 -*-
"""docstring for file_management.py"""

from builtins import object

import os

from xml.dom.minidom import parseString
from tempfile import gettempdir
from .utils import (_ms, _qgis, Util)

class FileManagement(object):

    @staticmethod
    def createDir(name):
        directory = os.path.dirname(name)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def createXml(d, root="qgis", tmp=False, fileName='', ext='xml', pretty=False):
        xml = Util.dict2xml(d, root)

        if tmp:
            if pretty:
                dom = parseString(xml)
                return dom.toprettyxml()
            else:
                return xml
        else:
            if pretty:
                dom = parseString(xml)
                xml = dom.toprettyxml()
            if os.path.isabs(fileName):
                fileName = '{}.{}'.format(fileName, ext)
            else:
                fileName = '{}\\{}.{}'.format(gettempdir(), fileName, ext)
            with open(fileName, "w") as f:
                f.write(xml)

            return fileName

    @classmethod
    def ellipse2svg(cls, mssymbol, symbolsetpath):
        points = mssymbol.get("points", [])
        if not points:
            return False
        filled = mssymbol.get("filled", False)
        name = mssymbol.get("name", cls.getName())
        #TODO verificar si la carpeta es svg, no crear una dentro de esa
        name = os.path.join(os.path.dirname(symbolsetpath), 'svg', name)
        cls.createDir(name)
        x, y = points[0]
        width = min(x, y) * 1.0 / 10

        svg = {"ellipse": {"cx": x + width / 2, "cy": y + width / 2, "rx": x, "ry": y}}
        svg.update({"viewBox": "0 0 {} {}".format(x * 2 + width, y * 2 + width)})

        if not filled:
            (svg["ellipse"]).update(dict(_qgis.SVG_PROPS_NO_FILL))
        else:
            (svg["ellipse"]).update(dict(_qgis.SVG_PROPS_FILL))

        props_stroke = dict(_qgis.SVG_PROPS_STROKE)
        props_stroke['stroke-width'] = "param(outline-width) {}".format(width)
        (svg["ellipse"]).update(props_stroke)
        svg.update(_qgis.TEMPLATE_SVG)
        svg["type"] = "ellipse"

        return cls.createXml(svg, root='svg', tmp=False, fileName=name, \
            ext='svg', pretty=True)

    @classmethod
    def vector2svg(cls, mssymbol, symbolsetpath):
        filled = mssymbol.get("filled", False)
        name = mssymbol.get("name", cls.getName())
        #TODO verificar si la carpeta es svg, no crear una dentro de esa
        name = os.path.join(os.path.dirname(symbolsetpath), 'svg', name)
        cls.createDir(name)
        points = mssymbol.get("points", [])
        d = ''
        svg = {"g": {"path": []}}
        n = 0
        start = True
        i = 0

        max_x = []
        max_y = []

        min_ = []

        def deletelastpath(i, mx, my):
            if i == 1:
                max_x.pop()
                max_y.pop()

        for p in points:
            x, y = p
            if p == (-99, -99):
                deletelastpath(i, max_x, max_y)
                n += 1
                start = True
                d = ''
                i = 0
            else:
                if start:
                    start = False
                    d += 'M'
                    svg["g"]["path"].append({"d": d})
                else:
                    d += ' L'
                d += " {} {}".format(x, y)
                svg["g"]["path"][n]["d"] = d
                i += 1

                if x != 0:
                    min_.append(x)
                if y != 0:
                    min_.append(y)
                max_x.append(x)
                max_y.append(y)

        deletelastpath(i, max_x, max_y)

        width = min(min_) * 1.0 / 10
        viewBox = "0 0 {} {}".format(max(max_x), max(max_y))
        svg.update({"viewBox": viewBox})

        if not filled or min(points) == (-99, -99):
            (svg["g"]).update(dict(_qgis.SVG_PROPS_NO_FILL))
        else:
            svg["g"]["path"][n]["d"] += " Z"
            (svg["g"]).update(dict(_qgis.SVG_PROPS_FILL))

        props_stroke = dict(_qgis.SVG_PROPS_STROKE)
        props_stroke['stroke-width'] = "param(outline-width) {}".format(width)
        (svg["g"]).update(props_stroke)
        svg.update(_qgis.TEMPLATE_SVG)
        svg["type"] = "vector"

        return cls.createXml(svg, root='svg', tmp=False, fileName=name, \
            ext='svg', pretty=True)

    @classmethod
    def pixmap2svg(cls, pixmap, symbolsetpath):
        """docstring for pixmap2svg"""
        #TODO crear un archivo svg con la imagen embebida
        return False

    @classmethod
    def url2svg(cls, url, symbolsetpath):
        """docstring for href2svg"""
        #TODO descargar de internet, y embeber en un svg si no lo es
        return False

    @classmethod
    def file2svg(cls, file, symbolsetpath):
        #TODO es necesario conocer carpeta donde se sencuentran los archivos
        return False

    @staticmethod
    def getName():
        return 'tmp'

    #https://www.rapidtables.com/web/tools/svg-viewer-editor.html
    #https://www.janvas.com/v6.1/janvas_app_6.1_public/index.html
    #https://github.com/qt/qtsvg/blob/5.11/src/svg/qsvghandler.cpp
    #https://github.com/baoboa/pyqt5/blob/master/examples/painting/basicdrawing/basicdrawing.py
    #http://3adly.blogspot.com/2013/04/qt-save-qpainter-output-in-svg-or-image.html