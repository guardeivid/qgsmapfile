layer = iface.activeLayer()
'''
#numero de QgsFeature que tiene la capa  
print(len(layer.fields()))

 #nombre del primer campo de la capa
print(layer.fields()[0].name())

#imprimir todos los nombres de la capa activa
for campo in layer.fields():
    print(campo.name())


#QgsFeatureIterator de QgsFeature que contiene la capa, en v2 no se accede por indice, salvo convirtiendolo en lista
#featureList = list(features)
#featureList[0]
#mejor feature = next(itertools.islice(feature_iteartor, N-1, N))

features = layer.getFeatures()

for f in features:
    #imprimir valores de la columna status
    #print(f['status'])
    #print(f.geometry().exportToWkt())  #v3 asWkt()
    print("Geometria: {}; ID: {}; Status: {}".format( f.geometry().exportToWkt() , f['id'], f['status'] ) )
 '''   
#QgsFeatureIterator al llegar al final se puede rebobinar con features.rewind()

#tomar solo elementos seleccionados
selectedFeatures = layer.selectedFeatures() #listado de QgsFeature
for f in selectedFeatures:
    print("Geometria: {}; ID: {}; Status: {}".format( f.geometry().exportToWkt() , f['id'], f['status'] ) )