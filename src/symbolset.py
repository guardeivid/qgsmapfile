# -*- coding: utf-8 -*-

from builtins import str
from builtins import object
import os
import pickle
import mappyfile

PROPS = {
    "symbolsetpath": u'',
    "symbols": [],
    "fontsetpath": u'',
    "fonts": {}
}

class SymbolSet(object):
    """docstring for SymbolSet"""
    def __init__(self, iface, symbolsetpath):
        super(SymbolSet, self).__init__()
        self.iface = iface
        self.props_new = {
            "symbolsetpath": symbolsetpath,
            "symbols": []
        }
        self.symbolsetpath = symbolsetpath
        self.file = os.path.join(os.path.dirname(__file__),'settings.db')
        self.props_old = self.open()
        self.symbolsetpath_old = self.props_old.get("symbolsetpath")

    def get(self):
        if self.symbolsetpath == self.symbolsetpath_old:
            return self.props_old.get("symbols", [])
        self.props_new["symbols"] = self.getSymbolSet()
        self.props_old.update(self.props_new)
        self.save(self.props_old)
        return self.props_new["symbols"]

    def open(self):
        if not os.path.exists(self.file) or os.path.getsize(self.file) == 0:
            self.save(PROPS)
            return {}

        with open(self.file, 'rb') as f:
            return pickle.load(f)

    def save(self, props):
        with open(self.file, 'wb') as f:
            pickle.dump(props, f, 2)

    def getSymbolSet(self):
        """docstring for getSymbolSet"""
        symbols = []
        try:
            if self.symbolsetpath != "":
                symbolset = mappyfile.open(self.symbolsetpath)
                symbols = symbolset.get("symbols", [])
        except Exception as e:
            self.iface.messageBar().pushWarning(u'Error', str(e))

        return symbols
