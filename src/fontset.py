# -*- coding: utf-8 -*-

from builtins import object
import os
import pickle

PROPS = {
    "symbolsetpath": u'',
    "symbols": [],
    "fontsetpath": u'',
    "fonts": {}
}

class FontSet(object):

    """docstring for FontSet"""
    def __init__(self, fontsetpath):
        super(FontSet, self).__init__()
        self.fontsetpath = fontsetpath
        self.props_new = {
            "fontsetpath": fontsetpath,
            "fonts": {}
        }
        self.fontsetpath = fontsetpath
        self.file = os.path.join(os.path.dirname(__file__),'settings.db')
        self.props_old = self.open()
        self.fontsetpath_old = self.props_old.get("fontsetpath")


    def get(self):
        if self.fontsetpath == self.fontsetpath_old:
            return self.props_old.get("fonts", {})

        self.props_new["fonts"] = self.getFontSet()
        self.props_old.update(self.props_new)
        self.save()
        return self.props_new["fonts"]

    def open(self):
        if not os.path.exists(self.file):
            self.save(PROPS)
            return {}
        with open(self.file, 'rb') as f:
            return pickle.load(f)

    def save(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self.props_old, f, 2)

    def getFontSet(self):
        f = {}
        if os.path.isfile(self.fontsetpath):
            with open(self.fontsetpath, "r") as file:
                for line in file:
                    line = line.strip().split()
                    if len(line) == 2:
                        f[line[0]] = line[1]
        return f
