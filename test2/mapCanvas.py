print(qgis.utils.iface.activeLayer())
layer = iface.activeLayer()
#ayer = QgsVectorLayer(path, name, provider)
if not layer.isValid():
    raise(IOError, "Failed to open the layer")

# add layer to the registry
#QgsMapLayerRegistry.instance().addMapLayer(layer)

# set extent to the extent of our layer
canvas = iface.mapCanvas()
canvas.setExtent(layer.extent())
print(layer.extent())


render = canvas.mapRenderer()

# set layer set
#lst = [layer.id()] # add ID of every layer
#render.setLayerSet(lst)

# set layer set
#layers = QgsMapLayerRegistry.instance().mapLayers()
#lst = layers.keys()
#render.setLayerSet(lst)
# Set destination CRS to match the CRS of the first layer
render.setDestinationCrs(layers.values()[0].crs())
# Enable OTF reprojection
#render.setProjectionsEnabled(True)


# activar solamente las capas pasadas, set the map canvas layer set
#canvas.setLayerSet([QgsMapCanvasLayer(layer)])
