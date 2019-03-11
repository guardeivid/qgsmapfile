#iface.legendInterface().addGroup( 'abc')
"""
li = iface.legendInterface()
print(li)
#help(li)
print(li.groups()) #QStringList
print(li.layers()) #list-of-QgsMapLayer

print(li.groupExists(0))  # -> bool

print(li.currentLayer()) #QgsMapLayer   == print(iface.activeLayer())

#li.moveLayer(QgsMapLayer, int)

#li.removeGroup(int)
"""

root = QgsProject.instance().layerTreeRoot()
print(root) # qgis.core.QgsLayerTreeGroup
#help(root)
print(root.name())
#print(root.dump())

#QgsLayerTreeLayer
tl = root.findLayers()[0]
#help(tl) 
#QgsLayerTreeLayer.layer() -> QgsMapLayer
#QgsLayerTreeLayer.layerName() -> QString

group = root.findGroup('abc')
print(group)
print(group.name())
print(group.findLayers())

#QgsLayerTreeGroup.addChildNode(QgsLayerTreeNode)
#QgsLayerTreeGroup.addGroup(QString) -> QgsLayerTreeGroup
#QgsLayerTreeGroup.addLayer(QgsMapLayer) -> QgsLayerTreeLayer
#QgsLayerTreeGroup.clone() -> QgsLayerTreeGroup
#QgsLayerTreeGroup.dump() -> QString
#QgsLayerTreeGroup.findGroup(QString) -> QgsLayerTreeGroup
#QgsLayerTreeGroup.findLayer(QString) -> QgsLayerTreeLayer
#QgsLayerTreeGroup.findLayerIds() -> QStringList
#QgsLayerTreeGroup.findLayers() -> list-of-QgsLayerTreeLayer
#QgsLayerTreeGroup.insertChildNode(int, QgsLayerTreeNode)
#QgsLayerTreeGroup.insertChildNodes(int, list-of-QgsLayerTreeNode)
#QgsLayerTreeGroup.insertGroup(int, QString) -> QgsLayerTreeGroup
#QgsLayerTreeGroup.insertLayer(int, QgsMapLayer) -> QgsLayerTreeLayer
#QgsLayerTreeGroup.name() -> QString
#QgsLayerTreeGroup.removeAllChildren()
#QgsLayerTreeGroup.removeChildNode(QgsLayerTreeNode)
#QgsLayerTreeGroup.removeChildren(int, int)
#QgsLayerTreeGroup.removeChildrenGroupWithoutLayers()
#QgsLayerTreeGroup.removeLayer(QgsMapLayer)
#QgsLayerTreeGroup.setName(QString)

#inherited from QgsLayerTreeNode
#QgsLayerTreeNode.children() -> list-of-QgsLayerTreeNode
#QgsLayerTreeNode.customProperties() -> QStringList
#QgsLayerTreeNode.customProperty(QString, QVariant defaultValue=QVariant()) -> QVariant
#QgsLayerTreeNode.nodeType() -> QgsLayerTreeNode.NodeType
#QgsLayerTreeNode.parent() -> QgsLayerTreeNode
#QgsLayerTreeNode.removeCustomProperty(QString)
#QgsLayerTreeNode.setCustomProperty(QString, QVariant)

#NodeGroup = 0
#NodeLayer = 1

l = iface.activeLayer()
print(l)
if l:
    print(l.name())


