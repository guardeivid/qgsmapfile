# qgsmapfile

This plugin helps import a Mapserver Mapfile in a Qgis Project, for now.

Version 0.1.0 - March 2019

### Licence

GNU General Public License version 2


### REQUERIMENTS for it to work correctly:
```sh
pip install mappyfile
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
- ogr (GML)
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
- SVG (types svg, url, file, vector not marker well know, ellipse, pixmap)
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


### Developement

This plugin is experimental and there are many features that have not yet been implemented.


### Author:

- David Orellano [@guardeivid](https://github.com/guardeivid)


### Acknowledgments

This plugin has been possible thanks to the development of the mappyfile library.
