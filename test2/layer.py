lyr = iface.activeLayer()

if lyr.labeling():
    lbl = lyr.labeling() #qgis._core.QgsVectorLayerSimpleLabeling || QgsRuleBasedLabeling
    #print(lbl)
    #print(lbl.type()) #simple, rule-based
    
    pal = lbl.settings() #qgis._core.QgsPalLayerSettings
    print(pal) 
    
    '''
    QgsExpression (const QString &expr)
    print(pal.getLabelExpression().dump())
    print(pal.getLabelExpression().expression())
    print(pal.getLabelExpression().isField())
    '''
    pal.wrapChar = 'b'
    print(pal.wrapChar)
    
    
    print(pal.dataDefinedProperties()) #qgis._core.QgsPropertyCollection
    print(pal.dataDefinedProperties().count()) #int
    print(pal.dataDefinedProperties().propertyKeys())
    
    txt = pal.format() #qgis._core.QgsTextFormat
    #print(txt)
    
    buf = txt.buffer() #qgis._core.QgsTextBufferSettings
    #print(buf)
    
    back = txt.background() #qgis._core.QgsTextBackgroundSettings
    #print(back)
    
    shw = txt.shadow() #qgis._core.QgsTextShadowSettings
    #print(shw)
    
    props = pal.dataDefinedProperties() #qgis._core.QgsPropertyCollection
    #print(props)
    propskeys = props.propertyKeys() #lista
    if propskeys:
        #print(propskeys)
        pro = props.property(propskeys[0]) #qgis._core.QgsProperty
        #print(pro.value()) 


lyr.setLabelsEnabled(True)
#print(lyr.labelsEnabled())




'''
for layer in QgsProject.instance().mapLayers().values():
    layer_settings  = QgsPalLayerSettings()
    text_format = QgsTextFormat()

    text_format.setFont(QFont("Arial", 12))
    text_format.setSize(12)

    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(0.10)
    buffer_settings.setColor(QColor("black"))

    text_format.setBuffer(buffer_settings)
    layer_settings.setFormat(text_format)

    layer_settings.fieldName = "Id"
    layer_settings.placement = 4

    layer_settings.enabled = True

    layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
    layer.setLabelsEnabled(True)
    layer.setLabeling(layer_settings)
    layer.triggerRepaint()
'''