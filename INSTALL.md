# Install

## Windows

1. Ejecutar la Shell de OSGEO4W **`OSGeo4W.bat`**

En una instalacion de Qgis Standalone, el acceso se encuentra en el directorio `C:\Program Files\QGIS 3.xx`

En una instalación avanzada, el acceso directo se encuentra en el directorio de instalación seleccionado, generalmente `C:\OSGeo4W`

2. Cargar variables de entorno
```sh
py3_env
```

3. Si no esta instalado `pip`, primero hay que instalarlo.

    - Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a folder on your computer.
    - Open a command prompt and navigate to the folder containing get-pip.py.
    - Run the following command:
    ```sh
    python3 get-pip.py
    ```
    - Verify that Pip was installed correctly by opening a command prompt and entering the following command:
    ```sh
    pip -V
    ```

4. Actualizar `pip` (opcional)
```sh
python3 -m pip install --upgrade pip
```

5. Instalación de un paquete:
```sh
python3 -m pip install mappyfile
# o
pip install mappyfile
```

6. Actualizar `mappyfile` paquete (opcional)
```sh
python3 -m pip install --upgrade mappyfile
```

---

Actualizar qgis 2 a 3
```sh
pip install qgis2to3
```

Ejecutar
```sh
cd C:\OSGeo4W\apps\Python36\Scripts
python3 qgis2to3 C:\Users\da2\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\QgsMapfile > C:\Users\da2\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\QgsMapfile\CHANGE
```

Si sale el error `No such file or directory: `**`tmp/missing`** crearlo en C:\

#### Cambiar resources.qrc de version 4 a 5
- Iniciar OSGEO4W.bat
- Cargar entorno qt5 tecleando `qt5_env`
- Cargar entorno o4w tecleando `o4w_env`
- Cargar entorno python 3 tecleando `py3_env`

```sh
cd C:\Users\da2\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
C:\OSGeo4W\apps\Python36\Scripts\pyrcc5.bat -o resources.py resources.qrc
```

```batch
@echo off
call "C:\OSGeo4W\bin\o4w_env.bat"
call "C:\OSGeo4W\bin\qt5_env.bat"
call "C:\OSGeo4W\bin\py3_env.bat"

@echo on
pyrcc5 -o resources.py resources.qrc
```