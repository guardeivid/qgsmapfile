# -*- coding: utf-8 -*-
#import os

#f = 'C:/Users/da2/.qgis2/python/plugins\\QgsMapfile\\src\\settings.db'
#print(f)
"""
f = os.path.abspath(f)
if not os.path.exists(f):
    f = open(f, 'w')
else:
    f = open(f, 'rb+')
    print(f.read())
f.close()
"""
import os
import pickle
import mappyfile

PROPS = {
    "symbolsetpath": u'',
    "symbols": [],
    "fontsetpath": u'',
    "fonts": {}
}
"""
file = 'C:/Users/da2/.qgis2/python/plugins\\QgsMapfile\\src\\settings.db'
with open(file, 'wb') as f:
    pickle.dump(props, f, 2)
exit()
"""

class SymbolSet(object):
    """docstring for SymbolSet"""
    def __init__(self, symbolsetpath):
        super(SymbolSet, self).__init__()
        self.props_new = {
            "symbolsetpath": symbolsetpath,
            "symbols": []
        }
        self.symbolsetpath = symbolsetpath
        #self.file = os.path.join(os.path.dirname(__file__),'settings.db')
        self.file = 'C:/Users/da2/.qgis2/python/plugins\\QgsMapfile\\src\\settings.db'
        #self.props_old = dict(self.props_new)
        self.props_old = self.open()
        print(type(self.props_old), self.props_old)
        #Si no hay datos en el archivo
        #self.props_old = self.props_old if self.props_old else {}
        #print(self.props_old)
        self.symbolsetpath_old = self.props_old.get("symbolsetpath")

    def get(self):
        if self.symbolsetpath == self.symbolsetpath_old:
            print("igual symbolsetpath")
            return self.props_old.get("symbols", [])
        print("distinto symbolsetpath")
        self.props_new["symbols"] = self.getSymbolSet()
        self.props_old.update(self.props_new)
        #print(self.props_old)
        self.save(self.props_old)
        return self.props_new["symbols"]

    def open(self):
        if not os.path.exists(self.file) or os.path.getsize(self.file) == 0:
            self.save(PROPS)
            return {}

        with open(self.file, 'rb') as f:
            #p = pickle.load(f)
            #print(p)
            return pickle.load(f)
            #return p

    def save(self, props):
        print("guardar")
        with open(self.file, 'wb+') as f:
            #print("props:", props)
            pickle.dump(props, f, 2)

    def getSymbolSet(self):
        """docstring for getSymbolSet"""
        symbols = []
        try:
            if self.symbolsetpath != "":
                symbolset = mappyfile.open(self.symbolsetpath)
                print(symbolset)
                #_type = symbolset.get("__type__")
                #if _type == 'map':
                symbols = symbolset.get("symbols", [])
                    #mapy = mappyfile.loads("MAP END")
                    #if symbols:
                    #    mapy["symbols"] = symbols
                    #self.symbolset = mapy
                #elif _type == 'symbolset':
                #    symbols = symbolset.get("symbols", [])
                #self.symbolset = symbolset
        except Exception as e:
            #self.symbolset = {}
            print(str(e))

        return symbols

s = SymbolSet(u'C:\\Users\\da2\\.qgis2\\python\\plugins\\QgsMapfile\\test\\symbols.sym')
print(s.get())
#open(f, 'rb+')