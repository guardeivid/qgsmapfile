for layer in QgsProject.instance().mapLayers().values():
    layer_settings  = QgsPalLayerSettings()
    text_format = QgsTextFormat()
    background_color = QgsTextBackgroundSettings()

    background_color.setFillColor(QColor('white'))
    background_color.setEnabled(True)

    text_format.setFont(QFont("Arial", 12))
    text_format.setSize(12)
    text_format.setBackground(background_color )

    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(0.10)
    buffer_settings.setColor(QColor("black"))

    text_format.setBuffer(buffer_settings)
    layer_settings.setFormat(text_format)

    layer_settings.fieldName = "Label"
    layer_settings.placement = 4

    layer_settings.enabled = True

    layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
    layer.setLabelsEnabled(True)
    layer.setLabeling(layer_settings)
    layer.triggerRepaint()