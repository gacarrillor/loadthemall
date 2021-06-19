from qgis.PyQt.QtCore import QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog

from .Ui_Base_LoadThemAll import Ui_Base_LoadThemAll


class Base_LoadThemAllDialog(QDialog, Ui_Base_LoadThemAll):
    """ A generic class to be reused in vector and raster dialogs """

    def __init__(self, isVector, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.isVector = isVector  # To know if it should be started with vector parameters
        self.loadFormats(self.isVector)
        self.loadDateComparisons()
        self.btnBaseDir.clicked.connect(self.selectDir)
        self.btnLoadExtent.clicked.connect(self.updateExtentFromCanvas)
        self.cboDateComparison.currentIndexChanged.connect(self.updateDateFormat)
        self.iface = iface

    def selectDir(self):
        """ Open a dialog for the user to choose a starting directory """
        settings = QSettings()
        path = QFileDialog.getExistingDirectory(self, self.tr("Select a base directory"),
                                                settings.value("/Load_Them_All/vector/path", "",
                                                               type=str) if self.isVector else settings.value(
                                                    "/Load_Them_All/raster/path", "", type=str),
                                                QFileDialog.ShowDirsOnly)

        if path: self.txtBaseDir.setText(path)

    def updateExtentFromCanvas(self):
        canvas = self.iface.mapCanvas()
        boundBox = canvas.extent()
        self.txtXMin.setText(str(boundBox.xMinimum()))
        self.txtYMin.setText(str(boundBox.yMinimum()))
        self.txtXMax.setText(str(boundBox.xMaximum()))
        self.txtYMax.setText(str(boundBox.yMaximum()))

    def loadFormats(self, isVector):
        """ Fill the comboBox with file formats """
        if isVector:
            allFormats = [
                ("GeoPackage (*.gpkg)", [".gpkg"]),
                ("ESRI Shapefile (*.shp)", [".shp"]),
                ("Mapinfo File (*.mif, *.tab)", [".mif", ".tab"]),
                ("Microstation DGN (*.dgn)", [".dgn"]),
                ("VRT - Virtual Datasource (*.vrt)", [".vrt"]),
                ("Comma Separated Value (*.csv)", [".csv"]),
                ("Geography Markup Language (*.gml)", [".gml"]),
                ("GPX (*.gpx)", [".gpx"]),
                ("KML - Keyhole Markup Language (*.kml, *.kmz)", [".kml", ".kmz"]),
                ("GeoJSON (*.geojson)", [".geojson"]),
                ("GMT (*.gmt)", [".gmt"]),
                ("SQLite (*.sqlite)", [".sqlite"]),
                ("Arc/Info ASCII Coverage (*.e00)", [".e00"]),
                ("AutoCAD DXF (*.dxf)", [".dxf"]),
                ("JSON (*.json)", [".json"]),
            ]
        else:
            allFormats = [
                ("Virtual Raster (*.vrt)", [".vrt"]),
                ("GeoTIFF (*.tif, *.tiff)", [".tif", ".tiff"]),
                ("Erdas Imagine Images (*.img)", [".img"]),
                ("Erdas Compressed Wavelets (*.ecw)", [".ecw"]),
                ("DTED Elevation Raster (*.dt)", [".dt2", ".dt3"]),
                ("Arc/Info ASCII Grid (*.asc)", [".asc"]),
                ("Portable Network Graphics (*.png)", [".png"]),
                ("JPEG JFIF (*.jpg, *.jpeg)", [".jpg", ".jpeg"]),
                ("JPEG2000 (*.jp2)", [".jp2"]),
                ("Graphics Interchange Format (*.gif)", [".gif"]),
                ("X11 PixMap Format (*.xpm)", [".xpm"]),
                ("Bitmap image file (*.bmp)", [".bmp"]),
                ("PCIDSK Database File (*.pix)", [".pix"]),
                ("PCRaster Raster File (*.map)", [".map"]),
                ("ILWIS Raster Map (*.mpr, *.mpl)", [".mpr", ".mpl"]),
                ("SRTMHGT File Format (*.hgt)", [".hgt"]),
                ("GMT NetCDF Grid Format (*.nc)", [".nc"]),
                ("GRIdded Binary (*.grb)", [".grb"]),
                ("Idrisi Raster A.1 (*.rst)", [".rst"]),
                ("Golden Software ASCII Grid (*.grd)", [".grd"]),
                ("R Object Data Store (*.rda)", [".rda"]),
                ("Vexcel MFF Raster (*.hdr)", [".hdr"]),
                ("USGS Optional ASCII DEM (*.dem)", [".dem"]),
                ("Magellan topo (*.blx)", [".blx"]),
                ("Rasterlite (*.sqlite)", [".sqlite"]),
                ("SAGA GIS Binary Grid (*.sdat)", [".sdat"]),
            ]
        allExtensions = [extension for format in allFormats for extension in format[1]]
        self.cboFormats.addItem("All listed formats (*.*)", allExtensions)
        for format in allFormats:
            self.cboFormats.addItem(*format)

    def loadDateComparisons(self):
        self.cboDateComparison.addItem(QApplication.translate("Base_LoadThemAllDialog", "Before"), "before")
        self.cboDateComparison.addItem(QApplication.translate("Base_LoadThemAllDialog", "Exact date"), "day")
        self.cboDateComparison.addItem(QApplication.translate("Base_LoadThemAllDialog", "After"), "after")

    def updateDateFormat(self, index):
        comparison = self.cboDateComparison.itemData(index)
        if comparison == 'day':
            self.dtDateTime.setDisplayFormat("ddd dd MMM yyyy")
        else:  # 'before' or 'after'
            self.dtDateTime.setDisplayFormat("ddd dd MMM yyyy hh:mm AP")

    def keyPressEvent(self, e):
        """ Handle the ESC key to avoid only the base dialog being closed """
        if e.key() == Qt.Key_Escape:
            e.ignore()
