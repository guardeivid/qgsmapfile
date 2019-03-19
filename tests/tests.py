import sys
from qgis import utils

QgsMapfile = utils.plugins['QgsMapfile']
dir_ = QgsMapfile.plugin_dir
sys.path.append(dir_)

from src.mapfile_import import MapfileImport


class Test(object):
    def __init__(self, iface, dir_):
        super(Test, self).__init__()
        self.iface = iface
        self.dir_ = dir_
        self.dir_map = dir_ + "\\tests\\data\\map\\"

    def mapfile_import(self, mapfile):
        mf = MapfileImport(self.iface, self.dir_map + mapfile, True)
        for layer in mf.layers:
            mf.addLayer(layer)

    def run(self):
        self.mapfile_import("polygon.map")
        #self.mapfile_import("line.map")
        #self.mapfile_import("point.map")



t = Test(iface, dir_)
t.run()
