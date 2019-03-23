from qgis.core import QgsPalLayerSettings

layer = iface.activeLayer()

prop=QgsProperty.fromField("COUNTRY")
#prop.setField("COUNTRY")
print(prop.isActive())
print(prop.propertyType() == QgsProperty.FieldBasedProperty)

pc=QgsPropertyCollection('Collection')
pc.setProperty(QgsPalLayerSettings.Color, prop)
pc.setProperty(QgsPalLayerSettings.Family, prop)

pal_layer=QgsPalLayerSettings()
pal_layer.setDataDefinedProperties(pc)
pal_layer.fieldName="COUNTRY"
pal_layer.wrapChar = ' '
pal_layer.multilineAlign = 1
pal_layer.enabled=True

labeler=QgsVectorLayerSimpleLabeling(pal_layer)

layer.setLabeling(labeler)
layer.setLabelsEnabled(True)
layer.triggerRepaint()