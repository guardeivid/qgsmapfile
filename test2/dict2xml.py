"""
    Simple xml serializer.
    @author Reimund Trost 2013
    Example:

    mydict = {
        'name': 'The Andersson\'s',
        'size': 4,
        'children': {
            'total-age': 62,
            'child': [
                { 'name': 'Tom', 'sex': 'male', },
                {
                    'name': 'Betty',
                    'sex': 'female',
                    'grandchildren': {
                        'grandchild': [
                            { 'name': 'herbert', 'sex': 'male', },
                            { 'name': 'lisa', 'sex': 'female', }
                        ]
                    },
                }
            ]
        },
    }

    print(dict2xml(mydict, 'family'))

    Output:

      <family name="The Andersson's" size="4">
        <children total-age="62">
          <child name="Tom" sex="male"/>
          <child name="Betty" sex="female">
            <grandchildren>
              <grandchild name="herbert" sex="male"/>
              <grandchild name="lisa" sex="female"/>
            </grandchildren>
          </child>
        </children>
      </family>
"""
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
                print(value)
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


mydict = {
    "version":"2.14.12-Essen",
    "labeling":{
        "type":"rule-based",
        "rules": [
            {
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
                            'fieldName': 'nombre',
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
                            'shapeSizeUnits': '1',
                            'shapeType': '0',
                            'shapeSVGFile': '',
                            'shapeOffsetX': '0',
                            'shapeOffsetY': '0',
                            'shapeBlendMode': '0',
                            'shapeFillColor': '255,255,255,255',
                            'shapeTransparency': '0',
                            'shapeSizeMapUnitScale': '0,0,0,0,0,0',
                            'shapeSizeType': '0',
                            'shapeJoinStyle': '64',
                            'shapeDraw': '0',
                            'shapeBorderWidthUnits': '1',
                            'shapeSizeX': '0',
                            'shapeSizeY': '0',
                            'shapeOffsetMapUnitScale': '0,0,0,0,0,0',
                            'shapeRadiiX': '0',
                            'shapeRadiiY': '0',
                            'shapeOffsetUnits': '1',
                            'shapeRotation': '0',
                            'shapeBorderWidth': '0',
                            'shapeBorderColor': '128,128,128,255',
                            'shapeRotationType': '0',
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
                            'repeatDistanceUnit': '1',
                            'placement': '1',
                            'maxCurvedCharAngleIn': '20',
                            'repeatDistance': '0',
                            'distInMapUnits': '0',
                            'labelOffsetInMapUnits': '1',
                            'xOffset': '0',
                            'distMapUnitScale': '0,0,0,0,0,0',
                            'predefinedPositionOrder': 'TR,TL,BR,BL,R,L,TSR,BSR',
                            'preserveRotation': '1',
                            'repeatDistanceMapUnitScale': '0,0,0,0,0,0',
                            'centroidWhole': '0',
                            'priority': '5',
                            'yOffset': '0',
                            'offsetType': '0',
                            'placementFlags': '10',
                            'centroidInside': '0',
                            'dist': '0',
                            'angleOffset': '0',
                            'maxCurvedCharAngleOut': '-20',
                            'fitInPolygonOnly': '0',
                            'quadOffset': '4',
                            'labelOffsetMapUnitScale': '0,0,0,0,0,0'
                        },
                        "data-defined": {
                            "Size": {
                                'expr': '',
                                'field': '',
                                'active': 'false',
                                'useExpr': 'false'
                            },
                            "Color": {
                                'expr': '',
                                'field': '',
                                'active': 'false',
                                'useExpr': 'false'
                            },
                            "Family": {
                                'expr': '',
                                'field': '',
                                'active': 'false',
                                'useExpr': 'false'
                            },
                            "BufferColor": {
                                'expr': '',
                                'field': '',
                                'active': 'false',
                                'useExpr': 'false'
                            },
                            "Rotation": {
                                'expr': '',
                                'field': '',
                                'active': 'false',
                                'useExpr': 'false'
                            }
                        }
                    }
                }
            }
            ]
        }
    }

mydict2 = mydict.copy()
mydict2["version"] = "3.20-Bonn"
xml = dict2xml(mydict2, 'qgis')
from xml.dom.minidom import parseString
#print(xml)
dom = parseString(xml)
prettyxml = dom.toprettyxml()
print(prettyxml)

xml = dict2xml(mydict, 'qgis')
from xml.dom.minidom import parseString
#print(xml)
dom = parseString(xml)
prettyxml = dom.toprettyxml()
print(prettyxml)



#f=open("tmp_labeling.qml","w")
#f.write(prettyxml)
#f.close()


import xml.etree.ElementTree as ET

file = 'C:\\Users\\da2\\.qgis2\\python\\plugins\\QgsMapfile\\test\\label_rules_218.qml'

tree = ET.parse(file)
root = tree.getroot()
labeling = root.find('labeling')
#print(labeling)

ltype = labeling.attrib['type']
#print(ltype)

if ltype == 'rule-based':
    rules = labeling.findall('rules/rule')
    for rule in rules:
        rule_ = rule.attrib
        filter_ = rule_.get('filter', '')
        description = rule.get('description', '')
        scalemaxdenom = rule.get('scalemaxdenom', '')
        scalemindenom = rule.get('scalemindenom', '')
        print(description, " - ", filter_, " - ", scalemaxdenom, " - ", scalemindenom)
        text_style = rule.find('settings/text-style').attrib
        text_format = rule.find('settings/text-format').attrib
        text_buffer = rule.find('settings/text-buffer').attrib
        background = rule.find('settings/background').attrib
        shadow = rule.find('settings/shadow').attrib
        placement = rule.find('settings/placement').attrib
        print(text_style)
        print(text_format)
        print(text_buffer)
        print(background)
        print(shadow)
        print(placement)
        Size = rule.find('settings/data-defined/Size')
        Color = rule.find('settings/data-defined/Color')
        Family = rule.find('settings/data-defined/Family')
        BufferColor = rule.find('settings/data-defined/BufferColor')
        Rotation = rule.find('settings/data-defined/Rotation')
        #print(Size.attrib)
        if Size !=None:
            Size = Size.attrib
        if Color !=None:
            Color = Color.attrib
        if Family !=None:
            Family = Family.attrib
        if BufferColor !=None:
            BufferColor = BufferColor.attrib
        if Rotation !=None:
            Rotation = Rotation.attrib
        print(Size)
        print(Color)
        print(Family)
        print(BufferColor)
        print(Rotation)
"""
#Convertir dict a xml
"""
xmlstring = dict2xml(mydict, 'qgis')
print(xmlstring)
root = ET.fromstring(xmlstring)
labeling = root.find('labeling')
print(labeling)
ltype = labeling.attrib['type']
print(ltype)
if ltype == 'rule-based':
    rules = labeling.findall('rules/rule')
    print(rules)
"""

"""
#Con minidom
from xml.dom.minidom import parse, parseString

tree = parse(file)
#root = tree.getroot()
labeling = tree.getElementsByTagName('labeling')
print(labeling)
ltype = labeling.item(0).getAttribute('type')
print(ltype)


"""
  -   "gid" > 10  -    -
{'fontItalic': '0', 'fontFamily': 'MS Shell Dlg 2', 'fontLetterSpacing': '0', 'fontUnderline': '0', 'fontWeight': '50', 'fontStrikeout': '0', 'textTransp': '0', 'previewBkgrdColor': '#ffffff', 'fontCapitals': '0', 'textColor': '0,0,0,255', 'fontSizeInMapUnits': '0', 'isExpression': '0', 'blendMode': '0', 'fontSizeMapUnitScale': '0,0,0,0,0,0', 'fontSize': '8.25', 'fieldName': 'nombre', 'namedStyle': 'Normal', 'fontWordSpacing': '0', 'useSubstitutions': '0'}
{'placeDirectionSymbol': '0', 'multilineAlign': '0', 'rightDirectionSymbol': '>', 'multilineHeight': '1', 'plussign': '0', 'addDirectionSymbol': '0', 'leftDirectionSymbol': '<', 'formatNumbers': '0', 'decimals': '3', 'wrapChar': '', 'reverseDirectionSymbol': '0'}
{'bufferSize': '1', 'bufferSizeMapUnitScale': '0,0,0,0,0,0', 'bufferColor': '255,255,255,255', 'bufferDraw': '0', 'bufferBlendMode': '0', 'bufferTransp': '0', 'bufferSizeInMapUnits': '0', 'bufferNoFill': '0', 'bufferJoinStyle': '64'}
{'shapeSizeUnits': '1', 'shapeType': '0', 'shapeSVGFile': '', 'shapeOffsetX': '0', 'shapeOffsetY': '0', 'shapeBlendMode': '0', 'shapeFillColor': '255,255,255,255', 'shapeTransparency': '0', 'shapeSizeMapUnitScale': '0,0,0,0,0,0', 'shapeSizeType': '0', 'shapeJoinStyle': '64', 'shapeDraw': '0', 'shapeBorderWidthUnits': '1', 'shapeSizeX': '0', 'shapeSizeY': '0', 'shapeOffsetMapUnitScale': '0,0,0,0,0,0', 'shapeRadiiX': '0', 'shapeRadiiY': '0', 'shapeOffsetUnits': '1', 'shapeRotation': '0', 'shapeBorderWidth': '0', 'shapeBorderColor': '128,128,128,255', 'shapeRotationType': '0', 'shapeBorderWidthMapUnitScale': '0,0,0,0,0,0', 'shapeRadiiMapUnitScale': '0,0,0,0,0,0', 'shapeRadiiUnits': '1'}
{'shadowOffsetMapUnitScale': '0,0,0,0,0,0', 'shadowOffsetGlobal': '1', 'shadowRadiusUnits': '1', 'shadowTransparency': '30', 'shadowColor': '0,0,0,255', 'shadowUnder': '0', 'shadowScale': '100', 'shadowOffsetDist': '1', 'shadowDraw': '0', 'shadowOffsetAngle': '135', 'shadowRadius': '1.5', 'shadowRadiusMapUnitScale': '0,0,0,0,0,0', 'shadowBlendMode': '6', 'shadowRadiusAlphaOnly': '0', 'shadowOffsetUnits': '1'}
{'repeatDistanceUnit': '1', 'placement': '1', 'maxCurvedCharAngleIn': '20', 'repeatDistance': '0', 'distInMapUnits': '0', 'labelOffsetInMapUnits': '1', 'xOffset': '0', 'distMapUnitScale': '0,0,0,0,0,0', 'predefinedPositionOrder': 'TR,TL,BR,BL,R,L,TSR,BSR', 'preserveRotation': '1', 'repeatDistanceMapUnitScale': '0,0,0,0,0,0', 'centroidWhole': '0', 'priority': '5', 'yOffset': '0', 'offsetType': '0', 'placementFlags': '10', 'centroidInside': '0', 'dist': '0', 'angleOffset': '0', 'maxCurvedCharAngleOut': '-20', 'fitInPolygonOnly': '0', 'quadOffset': '4', 'labelOffsetMapUnitScale': '0,0,0,0,0,0'}
{'expr': '', 'field': 'gid', 'active': 'true', 'useExpr': 'false'}
{'expr': '', 'field': 'nombre', 'active': 'true', 'useExpr': 'false'}
{'expr': '', 'field': 'nombre', 'active': 'true', 'useExpr': 'false'}
{'expr': '', 'field': 'nombre', 'active': 'true', 'useExpr': 'false'}
{'expr': '', 'field': 'union', 'active': 'false', 'useExpr': 'false'}
"""