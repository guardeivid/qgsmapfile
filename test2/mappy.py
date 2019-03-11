import mappyfile

#m = {"__type__": "map", "name": "Example", "extent": [0, 0, 100, 100]}
# create a list of layers
#m['layers'] = [{"__type__": "layer", 'name': 'weather alerts', 'type': 'Point'}]
#print(mappyfile.dumps(m))


#from mappyfile.ordereddict import CaseInsensitiveOrderedDict

#m = CaseInsensitiveOrderedDict(CaseInsensitiveOrderedDict)
#print(m)
#m = {"__type__": "map", "name": "Example", "extent": [0, 0, 100, 100]}
# create a list of layers
#m['layers'] = [{"__type__": "layer", 'name': 'weather alerts', 'type': 'Point'}]
#print(mappyfile.dumps(m))

"""
a = {
    "__type__": "map",
    "extent": [
        -180,
        -90,
        180,
        90
    ],
    "name": "MyMap",
    "web": {
        "__type__": "web",
        "metadata": {
            "wms_enable_request": "*",
            "wms_feature_info_mime_type": "text/html",
            "__type__": "metadata"
        }
    },
    "projection": [
        "init=epsg:4326"
    ],
    "layers": [
        {
            "__type__": "layer",
            "processing": [
                "BANDS=1",
                "CONTOUR_ITEM=elevation",
                "CONTOUR_INTERVAL=20"
            ],
            "extent": [
                -180,
                -90,
                180,
                90
            ],
            "name": "rgb",
            "type": "RASTER",
            "data": ["../data/raster/bluemarble.tif"],
            "template": "raster.template.html"
        }
    ]
}

#print(mappyfile.dumps(a))

l = '''LAYER
    PROCESSING 'BANDS=1'
        PROCESSING 'CONTOUR_ITEM=elevation'
    PROCESSING 'CONTOUR_INTERVAL=20'
     EXTENT -180 -90 180 90 # set this here as it is not stored in the image
     NAME "rgb"
        TYPE RASTER
     DATA '../data/raster/bluemarble.tif'
     TEMPLATE 'raster.template.html'
    END'''
a = mappyfile.loads(l)
print(mappyfile.dumps(a, indent=2, spacer=" ", newlinechar="\n", end_comment=True))
"""
#from mappyfile.ordereddict import CaseInsensitiveOrderedDict
from collections import OrderedDict

class MapObj(OrderedDict):
    def __init__(self, *args, **kwargs):
        #super(MapObj, self).__init__(*args, **kwargs)
        self.map = {}
        self.map['__type__'] = 'map'
        self.map['name'] = ''
        self.map['extent'] = [-180, -90, 180, 90]
        self.map['web'] = {
            '__type__': 'web',
            'metadata': {
                '__type__': 'metadata'
            }
        }
        self.map['layers'] = []

    def set(self, key, value):
        self.map[key] = value

    def __add(self, key, value):
        if key in ('layers'):
            self.map[key].append(value)

    def addLayer(self, layer):
        self.__add('layers', layer)

    def metadata(self, key, value):
        self.map['web']['metadata'][key] = value

class LayerObj(OrderedDict):
    def __init__(self, *args, **kwargs):
        #super(LayerObj, self).__init__(*args, **kwargs)
        self.layer = {}
        self.layer['__type__'] = 'layer'
        self.layer['name'] = ''
        self.layer['type'] = 'point'
        self.layer['data'] = []
        #self.layer['metadata'] = None
        self.layer['processing'] = []
        self.layer['status'] = 'true'
        self.layer['classes'] = []

    def set(self, key, value):
        self.layer[key] = value

    def __add(self, key, value):
        if key in ('data', 'processing', 'classes'):
            self.layer[key].append(value)

    def addData(self, data):
        self.__add('data', data)

    def addClass(self, clase):
        self.__add('classes', clase)

    def metadata(self, key, value):
        if not hasattr(self.layer, 'metadata'):
            self.layer['metadata'] = {}
        self.layer['metadata'][key] = value

m = MapObj()
m.set('name', 'mymap')

l = LayerObj()
l.set('name', 'layer1')
l.addData('geom FROM table')
l.metadata('wms_enable_request', '*')

m.addLayer(l.layer)
#print(mappyfile.dumps(m.map, indent=4, end_comment=True))

#print(l)

class BaseObj(OrderedDict):
    def __init__(self, base, props=(), hashes=(), *args, **kwargs):
        self[base] = {}
        self[base]['__type__'] = base
        self.base = base
        self.props = props
        self.hashes = hashes

    def set(self, key, value):
        if key in self.props:
            self[self.base][key] = value

    def add(self, key, value):
        if key in self.hashs:
            if not hasattr(self[self.base], key):
                self[self.base][key] = []
            self[self.base][key].append(value)

    def get(self):
        return self[self.base]


class WebObj(BaseObj):

    PROPS = ('browseformat', 'empty', 'error', 'extent', 'footer', 'header', 'imagepath', 'imageurl', 'legendformat', 'log', 'maxscaledenom', 'maxtemplate', 'metadata', 'minscaledenom', 'mintemplate', 'queryformat', 'template', 'temppath')

    def __init__(self, *args, **kwargs):
        BaseObj.__init__(self, 'web', self.PROPS)

class MetadataObj(BaseObj):

    PROPS = ('browseformat', 'empty', 'error', 'extent', 'footer', 'header', 'imagepath', 'imageurl', 'legendformat', 'log', 'maxscaledenom', 'maxtemplate', 'metadata', 'minscaledenom', 'mintemplate', 'queryformat', 'template', 'temppath')

    def __init__(self, *args, **kwargs):
        BaseObj.__init__(self, 'metadata', self.PROPS)


msWeb = WebObj()
#help(webObj)
msWeb['maxscaledenom'] = 2
msWeb.set('minscaledenom', 1)
#print(webObj)

metadataObj = MetadataObj()
metadataObj.set('wms_enable_request', '*')
msWeb.set('metadata', metadataObj.get())
#msWeb.set('aaa', 123)

#msWeb['metadata'] = metadataObj.get()

m.map['web'] = msWeb.get()
#m.map['aaa'] = 123

#print(m.map)
print(mappyfile.dumps(m.map, indent=4, end_comment=True))
