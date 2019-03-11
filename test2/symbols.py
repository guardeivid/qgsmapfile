
import os
from xml.dom.minidom import parseString
from operator import itemgetter
from tempfile import gettempdir
import mappyfile

s2 ="""
SYMBOL
    NAME "arrow"
    TYPE VECTOR
    POINTS
      0 4
      8 4
      -99 -99
      5 1
      8 4
      5 7
      -99 -99
      4 0
      -99 -99
      4 8
    END
  END
    """

s = '''
  SYMBOL
  NAME "circle"
  TYPE ELLIPSE
  POINTS
    1 1
  END
  FILLED TRUE
END'''

s3 = """SYMBOL
  NAME "rectangle"
  TYPE VECTOR
  POINTS
    0 0
    1 0
    1 0.8
    0 0.8
    5 2
    0 0
  END
  FILLED TRUE
END"""

s4="""
SYMBOL
  NAME "triangle"
  TYPE VECTOR
  POINTS
    0 1
    0.5 0
    1 1
    0 1
  END
  FILLED TRUE
END"""

TEMPLATE_SVG = {
    "version": "1.1",
    "xmlns": "http://www.w3.org/2000/svg",
    "xmlns:xlink": "http://www.w3.org/1999/xlink",
    "baseProfile": "full",
    #"x": "0px",
    #"y": "0px",
    "width": "100%",
    "height": "100%",
    #"viewBox": "0 0 100 100",
    #"enable-background": "new 0 0 100 100",
    #"style": "background:red;",
    "xml:space": "preserve"
}

SVG_PROPS_STROKE = {
    "stroke": "param(outline) #000",
    #"stroke": "#000",
    "stroke-opacity": "param(outline-opacity)",
    "stroke-width": "param(outline-width) 1"
    #"stroke-width": "1"
}

SVG_PROPS_FILL = {
    "fill": "param(fill) #AAA",
    #"fill": "#AAA",
    "fill-opacity": "param(fill-opacity)"
}

SVG_PROPS_NO_FILL = {
    "fill": "none"
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
    def createDir(name):
        directory = os.path.dirname(name)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def createXml(d, root="qgis", tmp=False, fileName='', ext='xml', pretty=False):
        xml = dict2xml(d, root)

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
            #print(fileName)
            with open(fileName, "w") as f:
                f.write(xml)

            return fileName

    @staticmethod
    def getName():
        return "tmp"

    @classmethod
    def ellipse2svg(cls, mssymbol, symbolsetpath):
        points = mssymbol.get("points", [])
        if not points:
            return False
        #print(min(points))
        filled = mssymbol.get("filled", False)
        name = mssymbol.get("name", cls.getName())
        name = os.path.join(os.path.dirname(symbolsetpath), name)
        cls.createDir(name)
        x, y = points[0]
        width = min(x, y) * 1.0 / 10

        svg = {"ellipse": {"cx": x + width / 2, "cy": y + width / 2, "rx": x, "ry": y}}
        svg.update({"viewBox": "0 0 {} {}".format(x * 2 + width, y * 2 + width)})

        if not filled:
            (svg["ellipse"]).update(dict(SVG_PROPS_NO_FILL))
        else:
            (svg["ellipse"]).update(dict(SVG_PROPS_FILL))

        props_stroke = dict(SVG_PROPS_STROKE)
        props_stroke['stroke-width'] = "param(outline-width) {}".format(width)
        (svg["ellipse"]).update(props_stroke)
        svg.update(TEMPLATE_SVG)
        svg["type"] = "ellipse"

        return cls.createXml(svg, root='svg', tmp=False, fileName=name, \
            ext='svg', pretty=True)

    @classmethod
    def vector2svg(cls, mssymbol, symbolsetpath):
        filled = mssymbol.get("filled", False)
        name = mssymbol.get("name", cls.getName())
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

        #max_x = max(points,key=itemgetter(0))[0] + 1
        #max_y = max(points,key=itemgetter(1))[1] + 1
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
            (svg["g"]).update(dict(SVG_PROPS_NO_FILL))
        else:
            svg["g"]["path"][n]["d"] += " Z"
            (svg["g"]).update(dict(SVG_PROPS_FILL))

        props_stroke = dict(SVG_PROPS_STROKE)
        props_stroke['stroke-width'] = "param(outline-width) {}".format(width)
        (svg["g"]).update(props_stroke)
        svg.update(TEMPLATE_SVG)
        svg["type"] = "vector"

        return cls.createXml(svg, root='svg', tmp=False, fileName=name, \
            ext='svg', pretty=True)


def svg(sym, path):
    type_ = sym.get('type', '').lower()

    if type_ == 'vector':
        print(FileManagement.vector2svg(sym, path))
    elif type_ == 'ellipse':
        print(FileManagement.ellipse2svg(sym, path))

a = """
SYMBOL
  NAME "Tent"
  TYPE VECTOR
  POINTS
    0 4
    2 0
    4 4
    3 4
    2 2
    1 4
    0 4
  END
  FILLED TRUE
END"""

b= """
SYMBOL
  NAME "square"
  TYPE VECTOR
  POINTS
    0 0
    0 1
    1 1
    1 0
    0 0
  END
  FILLED TRUE
END
"""

c= """
SYMBOL
  NAME "cross"  #cross-3
  TYPE VECTOR
  POINTS
    0 0.4
    0.4 0.4
    0.4 0
    0.6 0
    0.6 0.4
    1 0.4
    1 0.6
    0.6 0.6
    0.6 1
    0.4 1
    0.4 0.6
    0 0.6
    0 0.4
  END
  FILLED TRUE
END
"""

d= """
 SYMBOL
    NAME "star"
    TYPE VECTOR
    FILLED TRUE
    POINTS
      0 0.375
      0.35 0.375
      0.5 0
      0.65 0.375
      1 0.375
      0.75 0.625
      0.875 1
      0.5 0.75
      0.125 1
      0.25 0.625
      0 0.375
    END
    FILLED TRUE
  END
  """

e= """
SYMBOL
  NAME "HalfCircle"
  TYPE VECTOR
  FILLED TRUE
  POINTS
   0 7
   0 6
   1 4
   2 3
   3 2
   4 1
   7 .5
   9 1
   11 2
   12 3
   13 4
   14 6
   14 7
   0 7
  END
END
"""
f= """
  SYMBOL
    NAME "Grass"
    TYPE VECTOR
    POINTS
      0 2
      1 3
      -99 -99
      1 0
      3 2
      3 3
      -99 -99
      7 0
      5 2
      5 3
      -99 -99
      8 2
      7 3
      -99 -99
      8 10
      9 11
      -99 -99
      9 8
      11 10
      11 11
      -99 -99
      15 8
      13 10
      13 11
      -99 -99
      16 10
      15 11
      -99 -99
      17 13
    END
  END"""

g="""
SYMBOL
    NAME "Tree"
    TYPE VECTOR
    POINTS
      5 0
      4 0
      3 1
      3 2
      0 5
      0 7
      1 8
      8 8
      9 7
      9 5
      6 2
      6 1
      5 0
      -99 -99
      4 7
      4 12
      5 12
      5 7
    END
  END
  """

h= """
   SYMBOL
    NAME "RightDiag-1"
    TYPE VECTOR
    POINTS
      10 0
      0 10
      -99 -99
      0 0
      0.3 0
      -99 -99
      10 10
      9.7 10
    END
  END"""

sym = mappyfile.loads(h)
path = os.path.join(os.path.dirname(__file__), "symbols.sym") #'C:\\Users\\User\\apps\\gis\\config\\templates\\symbols.sym'
svg(sym, path)


'''

<svg width="200" height="200" viewBow="0 0 100 100" style="border: green solid;">
    <path stroke="green" stroke-width=".2" d="M20 0 V200" />
    <path stroke="green" stroke-width=".2" d="M40 0 V200" />
    <path stroke="green" stroke-width=".2" d="M60 0 V200" />
    <path stroke="green" stroke-width=".2" d="M80 0 V200" />
    <path stroke="green" stroke-width=".2" d="M100 0 V200" />
    <path stroke="green" stroke-width=".2" d="M120 0 V200" />
    <path stroke="green" stroke-width=".2" d="M140 0 V200" />
    <path stroke="green" stroke-width=".2" d="M160 0 V200" />
    <path stroke="green" stroke-width=".2" d="M180 0 V200" />

    <path stroke="green" stroke-width=".2" d="M0 20 H200" />
    <path stroke="green" stroke-width=".2" d="M0 40 H200" />
    <path stroke="green" stroke-width=".2" d="M0 60 H200" />
    <path stroke="green" stroke-width=".2" d="M0 80 H200" />
    <path stroke="green" stroke-width=".2" d="M0 100 H200" />
    <path stroke="green" stroke-width=".2" d="M0 120 H200" />
    <path stroke="green" stroke-width=".2" d="M0 140 H200" />
    <path stroke="green" stroke-width=".2" d="M0 160 H200" />
    <path stroke="green" stroke-width=".2" d="M0 180 H200" />

    <ellipse cx="100" cy="140" rx="40" ry="40" style="fill:yellow;stroke:purple;stroke-width:1" />

    <g fill="none">
     <path stroke="red" stroke-width="1" d="M0 80 L160 80" />
     <path stroke="red" stroke-width="1" d="M100 10 L160 80 L 100 140" />
     <path stroke="red" stroke-width="1" d="M40 10 L40 11" />
     <path stroke="red" stroke-width="1" d="M80 0" />
     <circle cx="80" cy="0" r="0.1" style="fill:none;stroke:red;" />
    </g>

</svg>

<svg style="fill:none;stroke:red;"><g><path d="M 0 4 L 8 4"/><path d="M 5 1 L 8 4 L 5 7"/><path d="M 4 0"/><path d="M 4 8"/></g></svg>


l = QgsApplication.svgPaths()
#l.append('C:/Users/User/.qgis2/python/plugins/QgsMapfile/test')
print(l)
#QgsApplication.setDefaultSvgPaths(l)

'''