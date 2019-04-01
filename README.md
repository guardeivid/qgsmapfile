# QgsMapfile

<img src="https://github.com/guardeivid/qgsmapfile/raw/master/icon.png" width="64px" />


Version 0.1.3 - March 2019

This plugin helps import a Mapserver Mapfile in a Qgis Project, for now.

You can import the definition of a layer:
```map
MAP
    ...
    LAYER ...
    END
    ...
END

# or

LAYER ...
END
```

Or the definition of multiple layers:
```map
MAP
    ...
    LAYER ...
    END

    LAYER ...
    END
    ...
END
```

If import one layer (LAYER ... END) (the layers are declared with INCLUDE), then specify the main mapfile to obtain the paths (SHAPEPATH, FONTSET, SYMBOLSET) only once, later they are obtained from the cache.


### Licence

GNU General Public License version 2 or above


### REQUERIMENTS for it to work correctly:
```sh
pip install mappyfile
pip install matplotlib
```

#### Installation

##### Windows

1. Execute shell OSGEO4W **`OSGeo4W.bat`**

In a Qgis Standalone installation, the access is in the directory `C:\Program Files\QGIS 3.xx`

In an advanced installation, the shortcut is in the selected installation directory, usually `C:\OSGeo4W`

2. Load environment variables
```sh
py3_env
```

3. If `pip` is not installed, you must first install it.

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

4. Update `pip` (optional)
```sh
python3 -m pip install --upgrade pip
```

5. Installing packages:
```sh
python3 -m pip install mappyfile
# o
pip install mappyfile
```

6. Update package `mappyfile` (optional)
```sh
python3 -m pip install --upgrade mappyfile
```

7. Install matplotlib
```sh
pip install matplotlib
```

### NOTES:

Qgis and Mapserver are not completely compatible, but even so, we have tried to find the highest degree of common attributes allowing a similarity in the views in the different environments.

Mapfiles are expected to be UTF-8 encoded.

It is compatible with Mapserver Mapfiles versions >= 6.

It allows to add vector layers of different geometric types (Points, Lines and Polygons) and raster layers (not styled).


#### EXPRESSIONS

Filters and expressions are one of the biggest difficulties in converting between Mapserver and Qgis, due to their large number of variants, so not all cases are supported.

Types of expressions supported:
- String comparisons
- Regular expression comparison
- List expressions
- Logical MapServer expressions

	- Logical expressions

	- String expressions that return to logical value

	- Arithmetic expressions that return to logical value

	- String operations that return to string

	- Functions that return to string (tostring, upper, lower, initcap)


#### FORMATS

The types of connection supported (CONNECTIONTYPE) are:
- local (Shapefile shp)
- ogr (GeoJSON)
- postgis
- wfs
- wms (tif, tiff, jpeg, jpg, png)

The mappyfile library does not recognize the use of double quotes in the DATA attribute enclosing the schema and table ("schema"."table") for TYPE POSTGIS


#### STYLES

The styles declared in the map file can be recognized in any of the following Qgis symbologies
- Single symbol
- Categorized
- Graduated
- Rule-based

The translated layer symbols can be any of the following:
For points
- Simple marker
- Ellipse marker
- Font marker
- SVG marker

For lines
- Simple line
- Arrow
- Marker line

For poligons
- Simple fill
- Centroid fill
- Gradient fill
- Line pattern fill
- Point pattern fill
- Raster image fill
- SVG fill
- Line exterior: Simple line
- Line exterior: Marker line


#### SYMBOLS

If the path to the SYMBOLSET file is set, you can try to convert the symbol definition into one of the following formats
- Qgis markers well know (vector)
- Marker arrow (vector)
- SVG (types svg, vector not marker well know, ellipse)
- Font marker (truetype)


#### PATHS


#### LABELS

Support for Qgis Single labels and Labeling rule-based

Qgis translatable settings:
- Text format
- Text buffer
- Text background with rectangle shape (if have CLASS GEOTRANSFORM 'labelpoly')
	- "Shape size" (if have CLASS WITH and COLOR equal OUTLINECOLOR)
- Text shadow (if exists "shape size" and other CLASS OFFSET)
- Placement
- Renderer


#### FONTS

The fonts if they are installed in the system can be recognized, as long as the path to the FONSET file is specified.


### Developement, Help & Support

This plugin is experimental and there are many features that have not yet been implemented. Please contact me with any questions you may have about the plugin or with suggestons for further development.

The GitHub repository can also be used to log issues and suggest enhancements - [https://github.com/guardeivid/qgsmapfile/issues](https://github.com/guardeivid/qgsmapfile/issues)


### Author:

- David Orellano [@guardeivid](https://github.com/guardeivid)


### Acknowledgments

This plugin has been possible thanks to the development of the mappyfile library.
