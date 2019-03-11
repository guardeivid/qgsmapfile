## Traduccion de un plugin QGIS
1- Crear archivo <nombre-plugin>.pro en la carpeta <nombre-plugin>/i18n
```plain
FORMS = ../<nombre-dialog>.ui

SOURCES = ../<nombre-scripts>.py

TRANSLATIONS = <nombre-plugin>_<codigo-idioma>.ts
```

2- Crear los archivos <nombre-plugin>_<codigo-idioma>.ts que estan configurados en el archivo `<nombre-plugin>.pro`
```sh
cd C:\Users\user\.qgis2\python\plugins\QgsMapfile\i18n
pylupdate4 -noobsolete <nombre-plugin>.pro
```

3- Traducir los archivos `.ts` con Qt Linguist (o directamente en el archivo)
```xml
    <message>
        <location filename="../ui/qgsmapfileexport_dialog_base.ui" line="486"/>
        <source>General</source>
        <translation>General</translation>
    </message>
    ...
```
4- Compilar archivo `.ts` a `.qm`
```sh
lrelease <nombre-plugin>_<codigo-idioma>.ts
```

#### Ejemplo
```sh
cd C:\Users\user\.qgis2\python\plugins\QgsMapfile\i18n
pylupdate4 -noobsolete qgsmapfile.pro
lrelease en.ts
```
