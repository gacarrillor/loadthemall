![Unit tests](https://github.com/gacarrillor/loadthemall/actions/workflows/main.yml/badge.svg)
[![Release](https://img.shields.io/github/v/release/gacarrillor/loadthemall.svg)](https://github.com/gacarrillor/loadthemall/releases)


# Load Them All

QGIS plugin that recursively loads **vector**, **raster**, and **point cloud** (🆕✨) layers stored in a directory structure, based on several filters.

**License**: This plugin is distributed under the [GNU GPL v2 license](https://github.com/gacarrillor/loadthemall/blob/master/LICENSE).

📹  [Screencasts](#-screencasts)<br>
🚦  [Available filters](#-available-filters)<br>
⚙️  [Configuration](#%EF%B8%8F-configuration)<br>
🗄️  [Supported file formats](#%EF%B8%8F-supported-flle-formats)<br>
🔎  [Where to find the plugin in QGIS](#-where-to-find-the-plugin-in-qgis)<br>
💻  [For developers](#-for-developers)<br>
🙋‍♂️  [Code contributors](#%EF%B8%8F-code-contributors)<br>
ℹ️  [More info](#%E2%84%B9%EF%B8%8F-more-info)

-----------
### 📹 Screencasts

![Load Them All 3][2]

![Load Them All][1]

![Load Them All][3]



### 🚦 Available filters

Load Them All offers you several filters to properly choose the layers to be loaded. These are:

* **Alphanumeric**:

  Enter a filter text and choose among the modes `Start with`, `Any position`, or `Ends with` to find files by name.
  You can use the logical operators `||` (or) and `&&` (and), and even combine them. `&&` has more priority, so the expression `a || b && c` becomes `(a || b) && c`.
  
  Additionally, you can invert the Alphanumeric filter, i.e., prepend a logic NOT to it, allowing you to invert the original filter result.

* **Bounding box**:

  Enter coordinates by hand or get the current map extent. Choose the spatial filter: `Contains` or `Intersects`.

* **Date modified**:

  Filter files by their latest modification date, using comparisons like `before`, `after` and `exact date`.

* **Geometry type**:

  Choose which geometry type you want to load: `Point`, `Line`, or `Polygon`. Uncheck all geometry types for loading only geometryless layers (i.e., alphanumeric tables).

* **Raster type**:

  Choose which raster type you want to load: `Gray or undefined`, `Palette`, `Multiband`, or `Color Layer`.


### ⚙️ Configuration

There are several options for you to configure how layers should be loaded to QGIS:

* **Groups**: Whether or not to create groups based on directories' names. When groups are created, they reflect the directory structure, i.e., groups are nested if necessary.

* **Also search inside compressed files** 📦: Enable searching layers inside compressed files (ZIP, Gzip, 7zip, TAR, and RAR). 🆕✨

* **Turn off layers**: Make loaded layers invisible (it improves performance).

* **Do not load empty layers**.

* **Sort (or reverse sort) loaded layers by name**.

* **Ignore case in the alphanumeric filter**: Make the alphanumeric filter case insensitive.

* **Ignore accents in the alphanumeric filter**: You need the `unidecode` module for this option to work (you probably need to install it because it doesn't come with the standard Python installation). If enabled, an alphanumeric filter like 'arbol' will also match 'árbol'.

* **Sublayers**:
  The following two options can work independently from each other.
  * **Include parent in search**: Make alphanumeric filters work with the parent name prepended. If enabled,  an alphanumeric filter like 'Starts with: rivers' won't match the sublayer rivers, because the parent layer name is taken into account (e.g., 'parent_layer_name rivers').
  * **Include parent in loaded sublayers**: Prepend the parent layer name in all its sublayers. 

* **Apply group style to layers**: Whether or not to load QML style (group_name.qml) for all layers inside a group. The QML file must have the same name as the parent folder and must be found in the layer folder.


### 🗄️ Supported flle formats

The plugin supports the following file extensions:

* Vectors
  * Arc/Info ASCII Coverage (*.e00)
  * Arc/Info Generate (*.gen) 🆕
  * AutoCAD Driver (*.dwg) 🆕
  * AutoCAD DXF (*.dxf)
  * Bathymetry Attributed Grid (*.bag) 🆕
  * Comma Separated Value (*.csv)
  * Czech Cadastral Exchange Data Format (*.vfk) 🆕
  * ESRI Shapefile (*.shp *.shz 🆕 *.shp.zip 🆕)
  * FlatGeobuf (*.fgb) 🆕
  * Flexible Image Transport System (*.fits) 🆕
  * Geoconcept (*.gxt *.txt) 🆕
  * GeoJSON (*.geojson)
  * GeoJSON Newline Delimited JSON (*.geojsonl *.geojsons *.nlgeojson *.json) 🆕
  * Geography Markup Language [GML] (*.gml)
  * Geomedia .mdb (*.mdb) 🆕
  * GeoPackage (*.gpkg)
  * GeoRSS (*.xml) 🆕
  * Geospatial PDF (*.pdf) 🆕
  * GMT ASCII Vectors (*.gmt)
  * GPS eXchange Format [GPX] (*.gpx)
  * GPSTrackMaker (*.gtm *.gtz) 🆕
  * INTERLIS 2 (*.xtf *.xml *.ili) 🆕
  * JSON (*.json)
  * Keyhole Markup Language [KML] (*.kml *.kmz)
  * Mapbox Vector Tiles (*.mvt *.mvt.gz *.pbf) 🆕
  * Mapinfo File (*.mif *.tab)
  * MBTiles (*.mbtiles) 🆕
  * Microstation DGN (*.dgn)
  * OpenJUMP JML (*.jml) 🆕
  * OpenStreetMap (*.osm *.pbf) 🆕
  * PCI Geomatics Database File (*.pix) 🆕
  * Scalable Vector Graphics (*.svg) 🆕
  * SQLite/SpatiaLite (*.sqlite *.db 🆕 *.sqlite3 🆕 *.db3 🆕 *.s3db 🆕 *.sl3 🆕)
  * TopoJSON (*.json *.topojson) 🆕
  * Virtual Datasource [VRT] (*.vrt *.ovf 🆕)


* Rasters
  * Virtual Raster (*.vrt)
  * GeoTIFF (*.tif, *.tiff)
  * Erdas Imagine Images (*.img)
  * Erdas Compressed Wavelets (*.ecw)
  * ERMapper .ers Labelled (*.ers)
  * DTED Elevation Raster (*.dt)
  * Arc/Info ASCII Grid (*.asc)
  * Portable Network Graphics (*.png)
  * JPEG JFIF (*.jpg, *.jpeg)
  * JPEG2000 (*.jp2)
  * Graphics Interchange Format (*.gif)
  * X11 PixMap Format (*.xpm)
  * Bitmap image file (*.bmp)
  * PCIDSK Database File (*.pix)
  * PCRaster Raster File (*.map)
  * ILWIS Raster Map (*.mpr, *.mpl)
  * SRTMHGT File Format (*.hgt)
  * GMT NetCDF Grid Format (*.nc)
  * GRIdded Binary (*.grb)
  * Idrisi Raster A.1 (*.rst)
  * Golden Software ASCII Grid (*.grd)
  * R Object Data Store (*.rda)
  * Vexcel MFF Raster (*.hdr)
  * USGS Optional ASCII DEM (*.dem)
  * Magellan topo (*.blx)
  * Rasterlite (*.sqlite)
  * SAGA GIS Binary Grid (*.sdat)
  * Multi-resolution Seamless Image Database (*.sid)


* Point Clouds 🆕✨
  * COPC Point Clouds (*.copc.laz)
  * Entwine Point Clouds (*.ept.json)
  * PDAL Point Clouds (*.bpf, *.e57, *.las, *.laz)
  * Virtual Point Clouds (*.vpc)


### 🔎 Where to find the plugin in QGIS

After installation, Load Them All can be found in these places:

 + `Data source manager` toolbar:

    ![image](https://user-images.githubusercontent.com/652785/157999846-5e355b84-d4c7-4005-b347-393f2ac3a338.png)

 + `Layer -> Add layer` menu:

    ![image](https://user-images.githubusercontent.com/652785/157999893-31261a30-2c16-4c66-a7ea-de61ae79d6bd.png)

 + `Plugins` menu:

    ![image](https://user-images.githubusercontent.com/652785/157999941-b25b70ec-aa65-4631-8d87-91ecece7f460.png)


### 💻 For developers

 + To build the plugin run this command on the `loadthemall/LoadThemAll` directory:

   ```$ make clean;make;make build```

### 🙋‍♂️ Code contributors

* David Bakeman (v2.1 and v2.4)
* Sören Gebbert (v2.3)
* Jean Hemmi (v3.1 and French translation)
* Guillaume Lostis (v3.3)
* Jan Caha (v3.5)


### ℹ️ More info

 + More info about LoadThemAll at http://geotux.tuxfamily.org/index.php/en/geo-blogs/item/264-plugin-load-them-all-para-quantum-gis

 + See the changelog at https://github.com/gacarrillor/loadthemall/blob/master/changelog.txt


[1]: http://downloads.tuxfamily.org/tuxgis/geoblogs/plugin_LoadThemAll/imgs/LoadThemAll_v2_4.png
[2]: http://downloads.tuxfamily.org/tuxgis/geoblogs/plugin_LoadThemAll/imgs/load_them_all_v3_0.gif
[3]: http://downloads.tuxfamily.org/tuxgis/geoblogs/plugin_LoadThemAll/imgs/LoadThemAll_ApplyGroupStyles.gif
