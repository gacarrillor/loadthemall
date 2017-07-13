# Load Them All
QGIS plugin that recursively loads vector and raster layers stored in a directory structure, based on several filters.

![Load Them All][1]

Available filters are:

* **Alphanumeric**:

  Enter a filter text and choose among the modes 'Start with', 'Any position', or 'Ends with' to find files by name.
  You can use the logical operators || (or) and && (and), and even combine them. && has more priority, so the expression "a || b && c" becomes "(a || b) && c".
  Additionally, you can invert the Alphanumeric filter, i.e., prepend a logic NOT to it, allowing you to invert the original filter result.
* **Bounding box**:

  Enter coordinates by hand or get the current map extent. Choose the spatial filter: 'Contains' or 'Intersects'.
* **Date modified**:

  Filter files by their latest modification date, using comparisons like 'before', 'after' and 'exact date'.
* **Geometry type**:

  Choose which geometry type you want to load: 'Point', 'Line', or 'Polygon'.
* **Raster type**:

  Choose which raster type you want to load: 'Gray or undefined', 'Palette', 'Multiband', or 'Color Layer'.



There are several options for you to configure how layers should be loaded to QGIS:

* **Groups**: Whether or not to create groups based on directories' names. When groups are created, they reflect the directory structure, i.e., groups are nested if necessary.
* **Turn off layers**: Make loaded layers invisible (it improves performance).
* **Do not load empty layers**.
* **Sort (or reverse sort) loaded layers**.
* **Ignore case in the alphanumeric filter**.
* **Ignore accents in the alphanumeric filter**.

The plugin supports the following file extensions:
* Vectors
  * ESRI Shapefile (*.shp)", [".shp"]
  * Mapinfo File (*.mif, *.tab)", [".mif", ".tab"]
  * Microstation DGN (*.dgn)", [".dgn"]
  * VRT - Virtual Datasource (*.vrt)
  * Comma Separated Value (*.csv)
  * Geography Markup Language (*.gml)
  * GPX (*.gpx)
  * KML - Keyhole Markup Language (*.kml)
  * GeoJSON (*.geojson)
  * GMT (*.gmt)
  * SQLite (*.sqlite)
  * Arc/Info ASCII Coverage (*.e00)
  * AutoCAD DXF (*.dxf)


* Rasters
  * Virtual Raster (*.vrt)
  * GeoTIFF (*.tif, *.tiff)
  * Erdas Imagine Images (*.img)
  * Arc/Info ASCII Grid (*.asc)
  * Portable Network Graphics (*.png)
  * JPEG JFIF (*.jpg, *.jpeg)
  * Graphics Interchange Format (*.gif)
  * X11 PixMap Format (*.xpm)
  * MS Windows Device Independent Bitmap (*.bmp)
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


LICENSE: GPL v2.0

Code contributors:
* David Bakeman (v2.1 and v2.4)
* Sören Gebbert (v2.3)


More info about LoadThemAll at http://geotux.tuxfamily.org/index.php/en/geo-blogs/item/264-plugin-load-them-all-para-quantum-gis

See the changelog at https://github.com/gacarrillor/loadthemall/blob/master/changelog.txt


[1]: http://downloads.tuxfamily.org/tuxgis/geoblogs/plugin_LoadThemAll/imgs/LoadThemAll_v2_4.png
