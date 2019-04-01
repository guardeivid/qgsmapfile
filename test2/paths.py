import os
def abspath(mapfilepath, dirpath, filepath):
    """docstring for _abspath
    'mapfilepath': ruta absoluta al archivo mapfile
    'dirpath': ruta rel/abs a un directorio contenedor del archivo 'filepath', ej shapepath
    'filepath': ruta rel/abs a un archivo, ej shapefile

    return: ruta absoluta del archivo 'filepath'
    """
    #Obtener ruta absoluta al archivo
    if os.path.isabs(filepath):
        dirpath = filepath
    elif os.path.isabs(dirpath):
        dirpath = os.path.join(dirpath, filepath)
    else:
        dirpath = os.path.join(os.path.split(mapfilepath)[0], dirpath, filepath)

    return os.path.normpath(dirpath)

def getFileExtension(path):
    return os.path.splitext(path)[1]
    #return ext[1]

m = 'C:\\Users\\User\\apps\\gis\\config\\users\\administrador\\map.map'
d = ''
f = "../../templates/symbols.sym"

print(abspath(m, d , f))

m = 'C:\\Users\\da2\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\QgsMapfile\\tests\\data\\map\\geojson.map'
d = '..\\shapes\\World_Hydrography.geojson'
#f = 'C:\\Users\\da2\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\QgsMapfile\\tests\\data\\shapes\\World_Hydrography.geojson'
f = 'World_Hydrography.geojson'

print(abspath(m, d , f))
