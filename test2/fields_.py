from PyQt4.QtCore import QVariant

layer = iface.activeLayer()

#dataProvider
dp = layer.dataProvider()


print(dp.fieldNameMap())

nombre = 'nomencla'
idx = dp.fieldNameMap()[nombre]

#qgis._core.QgsFields
fields = dp.fields()

#qgis._core.QgsField
field = fields[idx]
#o
field = fields.field(idx)
#o por nombre
field = fields.field(nombre)


print("name", field.name())
print("typeName", field.typeName())

#tipo Qt
ty = fields.at( idx ).type()
print(ty)

print("comment", field.comment())
#qgis 2.18 alias
#print("alias", field.alias())



#print(layer.metadata())


print(QVariant.Bool, QVariant.Int, QVariant.UInt, QVariant.LongLong, QVariant.ULongLong, QVariant.Double)
print(QVariant.Char, QVariant.String)
print(QVariant.Date, QVariant.Time, QVariant.DateTime)