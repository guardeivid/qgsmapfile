"""a=104
b=253
c=a+b
d=c/2
print(d)

opacity = 99
a = int(round(opacity*2.55))

print(a)
b = 100 - int(round(float(a)/2.55))
print(b)





path = 'http://asd.com.as/wms?map=c:\\asd/asd/asd.map&request='
path = 'http://my.host.com/cgi-bin/mapserv?a=vv&map=wms.map&REQUEST=GetMap&SERVICE=WMS&VERSION=1.3.0&LAYERS=0&STYLES=&FORMAT=image/png&BGCOLOR=0xFFFFFF&TRANSPARENT=TRUE&CRS=EPSG:4326&BBOX=17.9995'
#print(urllib.url2pathname(path))
"""
url3 = 'http://my.host.com/cgi-bin/mapserv?a=vv&map=wms.map&REQUEST=GetMap&SERVICE=WMS&VERSION=1.3.0&LAYERS=0&STYLES=&FORMAT=image/png&BGCOLOR=0xFFFFFF&TRANSPARENT=TRUE&CRS=EPSG:4326&BBOX=17.9995'
url2 = 'http://my.host.com/cgi-bin/mapserv?'
url4 = 'http://adjhjdhsakjd.com'
import re

def url(uri):
    match = re.match(r"^https?://", uri)
    if not match:
        return False

    uri = uri.split("?")

    map_ = ''
    if len(uri) > 1:
        for m in uri[1].split("&"):
            if m.lower().startswith("map="):
                map_ = m + '&'
                break
    return "{}?{}".format(uri[0], map_)
print(url(url2))
#

"""
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    return a * 1.0 / b

print suma(45, 144)
print resta(1, 10)
print multiplicacion(4, 10)
print division(15, 2.65)
"""


#print("DAVID".lower().upper())


class ClassName(object):
    BACK = "background"
    """docstring for ClassName"""
    def __init__(self):
        super(ClassName, self).__init__()
        self.back = "arg"

    def get(self):
        print(self.BACK)
        print(self.back)

c = ClassName()
print(c.BACK)
print(c.get())