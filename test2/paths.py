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

m = 'C:\\Users\\User\\apps\\gis\\config\\users\\administrador\\map.map'
d = ''
f = "../../templates/symbols.sym"

print(abspath(m, d , f))