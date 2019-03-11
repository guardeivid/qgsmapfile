# -*- coding: utf-8 -*-
"""docstring for file_management.py"""

#import sys
#sys.setrecursionlimit(9999)
from tempfile import gettempdir
from xml.dom.minidom import parseString
#from PyQt4.QtCore.QDir import temp

LABELING_RULES = {
    "version":"2.14.12-Essen",
    "labeling":{
        "type":"rule-based",
        "rules": [
        ]
    }
}

LABELING_RULE = {
    "rule": {
        "description": "",
        "scalemaxdenom": None,
        "filter": "",
        "scalemindenom":None,
        "settings": {
            "text-style": {
                'fontItalic': '0',
                'fontFamily': 'MS Shell Dlg 2',
                'fontLetterSpacing': '0',
                'fontUnderline': '0',
                'fontWeight': '50',
                'fontStrikeout': '0',
                'textTransp': '0',
                'previewBkgrdColor': '#ffffff',
                'fontCapitals': '0',
                'textColor': '0,0,0,255',
                'fontSizeInMapUnits': '0',
                'isExpression': '0',
                'blendMode': '0',
                'fontSizeMapUnitScale': '0,0,0,0,0,0',
                'fontSize': '8.25',
                'fieldName': '',
                'namedStyle': 'Normal',
                'fontWordSpacing': '0',
                'useSubstitutions': '0'
            },
            "text-format": {
                'placeDirectionSymbol': '0',
                'multilineAlign': '0',
                'rightDirectionSymbol': '&gt;',
                'multilineHeight': '1',
                'plussign': '0',
                'addDirectionSymbol': '0',
                'leftDirectionSymbol': '&lt;',
                'formatNumbers': '0',
                'decimals': '3',
                'wrapChar': '',
                'reverseDirectionSymbol': '0'
            },
            "text-buffer": {
                'bufferSize': '1',
                'bufferSizeMapUnitScale': '0,0,0,0,0,0',
                'bufferColor': '255,255,255,255',
                'bufferDraw': '0',
                'bufferBlendMode': '0',
                'bufferTransp': '0',
                'bufferSizeInMapUnits': '0',
                'bufferNoFill': '0',
                'bufferJoinStyle': '64'
            },
            "background": {
                'shapeSizeUnits': '1',  #MM
                'shapeType': '0',   # rectangulo
                'shapeSVGFile': '',
                'shapeOffsetX': '0',
                'shapeOffsetY': '0',
                'shapeBlendMode': '0',
                'shapeFillColor': '255,255,255,255',
                'shapeTransparency': '0',
                'shapeSizeMapUnitScale': '0,0,0,0,0,0',
                'shapeSizeType': '0', # margen
                'shapeJoinStyle': '64',
                'shapeDraw': '0',   # dibujar o no rectangulo
                'shapeBorderWidthUnits': '1',
                'shapeSizeX': '0',
                'shapeSizeY': '0',
                'shapeOffsetMapUnitScale': '0,0,0,0,0,0',
                'shapeRadiiX': '0',
                'shapeRadiiY': '0',
                'shapeOffsetUnits': '1',
                'shapeRotation': '0',   # angulo de rotacion
                'shapeBorderWidth': '0',
                'shapeBorderColor': '128,128,128,255',
                'shapeRotationType': '0',   # sincronizar con etiqueta
                'shapeBorderWidthMapUnitScale': '0,0,0,0,0,0',
                'shapeRadiiMapUnitScale': '0,0,0,0,0,0',
                'shapeRadiiUnits': '1'
            },
            "shadow": {
                'shadowOffsetMapUnitScale': '0,0,0,0,0,0',
                'shadowOffsetGlobal': '1',
                'shadowRadiusUnits': '1',
                'shadowTransparency': '30',
                'shadowColor': '0,0,0,255',
                'shadowUnder': '0',
                'shadowScale': '100',
                'shadowOffsetDist': '1',
                'shadowDraw': '0',
                'shadowOffsetAngle': '135',
                'shadowRadius': '1.5',
                'shadowRadiusMapUnitScale': '0,0,0,0,0,0',
                'shadowBlendMode': '6',
                'shadowRadiusAlphaOnly': '0',
                'shadowOffsetUnits': '1'
            },
            "placement": {
                'placement': '1',
                'angleOffset': '0',
                'placementFlags': '10',
                'dist': '0',
                'distInMapUnits': '0',
                'distMapUnitScale': '0,0,0,0,0,0',
                'repeatDistance': '0',
                'repeatDistanceUnit': '1',
                'repeatDistanceMapUnitScale': '0,0,0,0,0,0',
                'xOffset': '0',
                'yOffset': '0',
                'offsetType': '0',
                'labelOffsetInMapUnits': '0',
                'labelOffsetMapUnitScale': '0,0,0,0,0,0',
                'predefinedPositionOrder': 'TR,TL,BR,BL,R,L,TSR,BSR',
                'preserveRotation': '1',
                'centroidInside': '0',
                'centroidWhole': '0',
                'maxCurvedCharAngleIn': '20',
                'maxCurvedCharAngleOut': '-20',
                'fitInPolygonOnly': '0',
                'quadOffset': '5',
                'priority': '5'
            },
            "rendering": {
                'scaleVisibility': "0",
                'scaleMin': "1",
                'scaleMax': "10000000",
                'fontLimitPixelSize': "0",
                'fontMinPixelSize': "3",
                'fontMaxPixelSize': "10000",
                'zIndex': "0",
                'displayAll': "0",
                'upsidedownLabels': "0",
                'labelPerPart': "0",
                'mergeLines': "0",  #line
                'limitNumLabels': "0",
                'maxNumLabels': "2000",
                'minFeatureSize': "0",
                'obstacle': "1",
                'obstacleFactor': "1",
                'obstacleType': "0"
            },
            "data-defined": {
                "Size": {},
                "Color": {},
                "Family": {},
                "BufferColor": {},
                "ShapeFillColor": {},
                "ShapeBorderColor": {},
                "ShapeBorderWidth": {},
                "Rotation": {}
            }
        }
    }
}


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
                children.append(dict2xml(value, key))
            elif isinstance(value, list):
                children.append(dict2xml(value, key))
            else:
                if value:
                    xml = xml + ' ' + key + '="' + str(value) + '"'
    else:
        for value in d:
            children.append(dict2xml(value, root_singular))

    end_tag = '>' if children else '/>'

    if wrap or isinstance(d, dict):
        xml = '<' + root + xml + end_tag

    if children:
        for child in children:
            xml = xml + child

        if wrap or isinstance(d, dict):
            xml = xml + '</' + root + '>'

    return xml

class FileManagement(object):

    """docstring for FileManagement"""
    def __init__(self, arg):
        super(FileManagement, self).__init__()
        self.arg = arg

    @staticmethod
    def createXml(d, tmp=False, fileName='', ext='xml', pretty=False):
        xml = dict2xml(d, 'qgis')

        if tmp:
            return xml
        else:
            if pretty:
                dom = parseString(xml)
                xml = dom.toprettyxml()
            fileName = '{}\\{}.{}'.format(gettempdir(), fileName, ext)
            print(fileName)
            with open(fileName, "w") as f:
                f.write(xml)

            return fileName


root = dict(LABELING_RULES)
root_rule = root["labeling"]["rules"]
rule = dict(LABELING_RULE)
root_rule.append(rule)

filename = FileManagement.createXml(root, tmp=False, fileName='prueba', ext='qml', pretty=False)
print(filename)


#print(temp())