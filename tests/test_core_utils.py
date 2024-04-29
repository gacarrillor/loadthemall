import nose2
import os.path

from qgis.testing import unittest, start_app

start_app()

from LoadThemAll.core.Utils import (get_parent_folder,
                                    get_file_extension,
                                    get_gzip_file_to_load,
                                    get_tar_files_to_load,
                                    get_zip_files_to_load)


class TestPluginUtils(unittest.TestCase):

    def test_get_parent_folder(self):
        print('INFO: Validating get parent folder...')
        file_path = "/vsizip//docs/Regional/ZIP_data.zip/AA_PreQuat_NAD27z12.TAB"
        folder_path = "/docs/Regional/"
        self.assertEqual(os.path.normpath(get_parent_folder(file_path)), os.path.normpath(folder_path))

        file_path = "/docs/geodata/Map_Database_ZIP/Geology/Regional/AA_PreQuat_NAD27z12.TAB"
        folder_path = "/docs/geodata/Map_Database_ZIP/Geology/Regional"
        self.assertEqual(os.path.normpath(get_parent_folder(file_path)), os.path.normpath(folder_path))

        # Windows paths
        file_path = "/vsizip/C:/Users/33769/Documents/germain/data/ZIP_data.zip/AA_PreQuat_NAD27z12.TAB"
        folder_path = "C:/Users/33769/Documents/germain/data"
        self.assertEqual(os.path.normpath(get_parent_folder(file_path)), os.path.normpath(folder_path))

        # TODO:
        #   test paths with layername=abc suffixes

    def test_get_file_extensions(self):
        print('INFO: Validating get file extensions...')
        self.assertEqual(get_file_extension("abc.zip"), ".zip")
        self.assertEqual(get_file_extension("ABC.ZIP"), ".zip")
        self.assertEqual(get_file_extension("abc.shp"), ".shp")
        self.assertEqual(get_file_extension("ABC.SHP"), ".shp")
        self.assertEqual(get_file_extension("abc.shp.zip"), ".shp.zip")
        self.assertEqual(get_file_extension("ABC.SHP.ZIP"), ".shp.zip")
        self.assertEqual(get_file_extension("a.b.c.shp.zip"), ".shp.zip")
        self.assertEqual(get_file_extension("A.B.C.SHP.ZIP"), ".shp.zip")
        self.assertEqual(get_file_extension("abc.gz"), ".gz")
        self.assertEqual(get_file_extension("ABC.GZ"), ".gz")
        self.assertEqual(get_file_extension("a.b.c.gz"), ".gz")
        self.assertEqual(get_file_extension("A.B.C.GZ"), ".gz")
        self.assertEqual(get_file_extension("abc.geojson.gz"), ".gz")
        self.assertEqual(get_file_extension("ABC.GEOJSON.GZ"), ".gz")
        self.assertEqual(get_file_extension("a.b.c.geojson"), ".geojson")
        self.assertEqual(get_file_extension("A.B.C.GEOJSON"), ".geojson")
        self.assertEqual(get_file_extension("abc.tar.gz"), ".tar.gz")
        self.assertEqual(get_file_extension("ABC.TAR.GZ"), ".tar.gz")
        self.assertEqual(get_file_extension("a.b.c.tar.gz"), ".tar.gz")
        self.assertEqual(get_file_extension("A.B.C.TAR.GZ"), ".tar.gz")
        self.assertEqual(get_file_extension("abc.copc.laz"), ".copc.laz")
        self.assertEqual(get_file_extension("ABC.COPC.LAZ"), ".copc.laz")
        self.assertEqual(get_file_extension("a.b.c.copc.laz"), ".copc.laz")
        self.assertEqual(get_file_extension("A.B.C.COPC.LAZ"), ".copc.laz")
        self.assertEqual(get_file_extension("abc.laz"), ".laz")
        self.assertEqual(get_file_extension("ABC.LAZ"), ".laz")
        self.assertEqual(get_file_extension("a.b.c.laz"), ".laz")
        self.assertEqual(get_file_extension("A.B.C.LAZ"), ".laz")
        self.assertEqual(get_file_extension("ept.json"), "ept.json")
        self.assertEqual(get_file_extension("EPT.JSON"), "ept.json")
        self.assertEqual(get_file_extension("/tmp/ept.json"), "ept.json")
        self.assertEqual(get_file_extension("/TMP/EPT.JSON"), "ept.json")
        self.assertEqual(get_file_extension("ept-build.json"), ".json")
        self.assertEqual(get_file_extension("EPT-BUILD.JSON"), ".json")
        self.assertEqual(get_file_extension("a.b.c.json"), ".json")
        self.assertEqual(get_file_extension("A.B.C.JSON"), ".json")

    def test_get_zip_files_to_load(self):
        self.assertEqual(get_zip_files_to_load("/QGIS/tests/testdata/zip/landsat_b1.zip", [".tif"]),
                         ["/vsizip//QGIS/tests/testdata/zip/landsat_b1.zip/landsat_b1.tif"])
        self.assertEqual(get_zip_files_to_load("/QGIS/tests/testdata/zip/points2.zip", [".shp"]),
                         ["/vsizip//QGIS/tests/testdata/zip/points2.zip/points.shp"])
        self.assertEqual(get_zip_files_to_load("/QGIS/tests/testdata/zip/points2.zip", [".dbf"]),
                         ["/vsizip//QGIS/tests/testdata/zip/points2.zip/points.dbf"])
        self.assertEqual(get_zip_files_to_load("/QGIS/tests/testdata/zip/testzip.zip", [".geojson"]),
                         ["/vsizip//QGIS/tests/testdata/zip/testzip.zip/folder/points.geojson"])
        self.assertEqual(get_zip_files_to_load("/QGIS/tests/testdata/zip/testzip.zip", [".tif"]),
                         ["/vsizip//QGIS/tests/testdata/zip/testzip.zip/folder/folder2/landsat_b2.tif",
                          "/vsizip//QGIS/tests/testdata/zip/testzip.zip/landsat_b1.tif"])
        self.assertEqual(get_zip_files_to_load("/QGIS/tests/testdata/zip/testzip.zip", [".shp"]),
                         ["/vsizip//QGIS/tests/testdata/zip/testzip.zip/points.shp"])
        self.assertEqual(get_zip_files_to_load("/QGIS/tests/testdata/zip/landsat_b1.zip", [".png"]),
                         [])

    def test_get_tar_files_to_load(self):
        self.assertEqual(get_tar_files_to_load("/QGIS/tests/testdata/zip/landsat_b1.tar", [".tif"]),
                         ["/vsitar//QGIS/tests/testdata/zip/landsat_b1.tar/landsat_b1.tif"])
        self.assertEqual(get_tar_files_to_load("/QGIS/tests/testdata/zip/points2.tar", [".shp"]),
                         ["/vsitar//QGIS/tests/testdata/zip/points2.tar/points.shp"])
        self.assertEqual(get_tar_files_to_load("/QGIS/tests/testdata/zip/testtar.tgz", [".tif"]),
                         ["/vsitar//QGIS/tests/testdata/zip/testtar.tgz/folder/folder2/landsat_b2.tif",
                          "/vsitar//QGIS/tests/testdata/zip/testtar.tgz/landsat_b1.tif"])
        self.assertEqual(get_tar_files_to_load("/QGIS/tests/testdata/zip/testtar.tgz", [".geojson"]),
                         ["/vsitar//QGIS/tests/testdata/zip/testtar.tgz/folder/points.geojson"])
        self.assertEqual(get_tar_files_to_load("/QGIS/tests/testdata/zip/testtar.tgz", [".shp"]),
                         ["/vsitar//QGIS/tests/testdata/zip/testtar.tgz/points.shp"])
        self.assertEqual(get_tar_files_to_load("/QGIS/tests/testdata/zip/testtar.tgz", [".gpkg"]),
                         [])

    def test_get_gzip_file_to_load(self):
        self.assertEqual(get_gzip_file_to_load("/QGIS/tests/testdata/zip/points3.geojson.gz", [".geojson"]),
                         ["/vsigzip//QGIS/tests/testdata/zip/points3.geojson.gz"])
        self.assertEqual(get_gzip_file_to_load("/QGIS/tests/testdata/zip/landsat_b1.tif.gz", [".tif"]),
                         ["/vsigzip//QGIS/tests/testdata/zip/landsat_b1.tif.gz"])
        self.assertEqual(get_gzip_file_to_load("/QGIS/tests/testdata/zip/landsat_b1.tif.gz", [".png"]),
                         [])


if __name__ == '__main__':
    nose2.main()
