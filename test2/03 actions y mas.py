#accions permite reaccionar a eventos, estan en las propiedades de la capa y se guardan en el proyecto

#ejemplo invertir la direccion de las lineas

#1- obtener la feature
'''
layer = iface.activeLayer()
layer.name()
layer_id = layer.id()
#u'line20180720174205275'

feature = layer.selectedFeatures()[0]
feature_id = feature.id()
'''
layer_id = u'line20180720174205275'
feature_id = 2L

#v2
layer=None
for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
    if lyr.id() == layer_id:
        layer = lyr
        break

#v3
#layer = QgsProject.instance().mapLayers(layer_id)

#crear un feature request con el id de la feature
r = QgsFeatureRequest(feature_id)
feature = next(layer.getFeatures(r))

#2- obtener la geometria e invertir la linea
#si es una multilinea (lista de lista de puntos)
geometry = feature.geometry()
lines = geometry.asMultiPolyline()

#revertir
for line in lines:
    line.reverse()
    
#recrear la geometria v3 fromMultiPolylineXY
geom = QgsGeometry.fromMultiPolyline(lines)
    
#si no es multi
line = geometry.asPolyline()
line.reverse()
geom = QgsGeometry.fromPolyline(line)

#3- reemplazar la geometria
layer.startEditing()
if layer.changeGeometry(feature_id, geom):
    layer.triggerRepaint()
else:
    print("no se pudo editar la geometria, enciende el modo de edicion")
    
#Confirmar los cambios
layer.commitChanges()

# o revertir cambios
layer.rollBack()


'''
En propiedades de la capa => acciones => agregar nueva
Canvas, Feature Scope

Pegamos el codigo y se reemplaza el feature_id por [% id %]
'''