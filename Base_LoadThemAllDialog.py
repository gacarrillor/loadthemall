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
            self.cboFormats.addItem("All listed formats (*.*)",
                                    [".gpkg", ".shp", ".mif", ".tab", ".dgn", ".vrt", ".csv", ".gml", ".gpx", ".kml",
                                     ".geojson", ".gmt", ".sqlite", ".e00", ".dxf", ".json"])
            self.cboFormats.addItem("GeoPackage (*.gpkg)", [".gpkg"])
            self.cboFormats.addItem("ESRI Shapefile (*.shp)", [".shp"])
            self.cboFormats.addItem("Mapinfo File (*.mif, *.tab)", [".mif", ".tab"])
            self.cboFormats.addItem("Microstation DGN (*.dgn)", [".dgn"])
            self.cboFormats.addItem("VRT - Virtual Datasource (*.vrt)", [".vrt"])
            self.cboFormats.addItem("Comma Separated Value (*.csv)", [".csv"])
            self.cboFormats.addItem("Geography Markup Language (*.gml)", [".gml"])
            self.cboFormats.addItem("GPX (*.gpx)", [".gpx"])
            self.cboFormats.addItem("KML - Keyhole Markup Language (*.kml)", [".kml"])
            self.cboFormats.addItem("GeoJSON (*.geojson)", [".geojson"])
            self.cboFormats.addItem("GMT (*.gmt)", [".gmt"])
            self.cboFormats.addItem("SQLite (*.sqlite)", [".sqlite"])
            self.cboFormats.addItem("Arc/Info ASCII Coverage (*.e00)", [".e00"])
            self.cboFormats.addItem("AutoCAD DXF (*.dxf)", [".dxf"])
            self.cboFormats.addItem("JSON (*.json)", [".json"])
        else:
            self.cboFormats.addItem("All listed formats (*.*)",
                                    [".vrt", ".tif", ".tiff", ".ecw", ".img", ".dt2", ".dt3", ".asc", ".png", ".jpg",
                                     ".jpeg", ".gif", ".xpm", ".bmp", ".pix", ".map", ".mpr", ".mpl", ".hgt", ".nc",
                                     ".grb", ".rst", ".grd", ".rda", ".hdr", ".dem", ".blx", ".sqlite", ".sdat"])
            self.cboFormats.addItem("Virtual Raster (*.vrt)", [".vrt"])
            self.cboFormats.addItem("GeoTIFF (*.tif, *.tiff)", [".tif", ".tiff"])
            self.cboFormats.addItem("Erdas Imagine Images (*.img)", [".img"])
            self.cboFormats.addItem("Erdas Compressed Wavelets (*.ecw)", [".ecw"])
            self.cboFormats.addItem("DTED Elevation Raster (*.dt)", [".dt2", ".dt3"])
            self.cboFormats.addItem("Arc/Info ASCII Grid (*.asc)", [".asc"])
            self.cboFormats.addItem("Portable Network Graphics (*.png)", [".png"])
            self.cboFormats.addItem("JPEG JFIF (*.jpg, *.jpeg)", [".jpg", ".jpeg"])
            self.cboFormats.addItem("Graphics Interchange Format (*.gif)", [".gif"])
            self.cboFormats.addItem("X11 PixMap Format (*.xpm)", [".xpm"])
            self.cboFormats.addItem("Bitmap image file (*.bmp)", [".bmp"])
            self.cboFormats.addItem("PCIDSK Database File (*.pix)", [".pix"])
            self.cboFormats.addItem("PCRaster Raster File (*.map)", [".map"])
            self.cboFormats.addItem("ILWIS Raster Map (*.mpr, *.mpl)", [".mpr", ".mpl"])
            self.cboFormats.addItem("SRTMHGT File Format (*.hgt)", [".hgt"])
            self.cboFormats.addItem("GMT NetCDF Grid Format (*.nc)", [".nc"])
            self.cboFormats.addItem("GRIdded Binary (*.grb)", [".grb"])
            self.cboFormats.addItem("Idrisi Raster A.1 (*.rst)", [".rst"])
            self.cboFormats.addItem("Golden Software ASCII Grid (*.grd)", [".grd"])
            self.cboFormats.addItem("R Object Data Store (*.rda)", [".rda"])
            self.cboFormats.addItem("Vexcel MFF Raster (*.hdr)", [".hdr"])
            self.cboFormats.addItem("USGS Optional ASCII DEM (*.dem)", [".dem"])
            self.cboFormats.addItem("Magellan topo (*.blx)", [".blx"])
            self.cboFormats.addItem("Rasterlite (*.sqlite)", [".sqlite"])
            self.cboFormats.addItem("SAGA GIS Binary Grid (*.sdat)", [".sdat"])

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
        if (e.key() == Qt.Key_Escape):
            e.ignore()
