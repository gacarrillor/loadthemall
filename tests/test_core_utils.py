import nose2

from qgis.testing import unittest, start_app

start_app()

from LoadThemAll.core.Utils import get_file_extension


class TestPluginUtils(unittest.TestCase):

    def test_get_file_exceptions(self):
        print('INFO: Validating get file extensions...')
        self.assertEqual(get_file_extension("abc.zip"), ".zip")
        self.assertEqual(get_file_extension("abc.shp"), ".shp")
        self.assertEqual(get_file_extension("abc.shp.zip"), ".shp.zip")
        self.assertEqual(get_file_extension("a.b.c.shp.zip"), ".shp.zip")
        self.assertEqual(get_file_extension("abc.gz"), ".gz")
        self.assertEqual(get_file_extension("a.b.c.gz"), ".gz")
        self.assertEqual(get_file_extension("abc.geojson.gz"), ".gz")
        self.assertEqual(get_file_extension("a.b.c.geojson"), ".geojson")
        self.assertEqual(get_file_extension("abc.tar.gz"), ".tar.gz")
        self.assertEqual(get_file_extension("a.b.c.tar.gz"), ".tar.gz")
        self.assertEqual(get_file_extension("abc.copc.laz"), ".copc.laz")
        self.assertEqual(get_file_extension("a.b.c.copc.laz"), ".copc.laz")
        self.assertEqual(get_file_extension("abc.laz"), ".laz")
        self.assertEqual(get_file_extension("a.b.c.laz"), ".laz")
        self.assertEqual(get_file_extension("abc.ept.json"), ".ept.json")
        self.assertEqual(get_file_extension("a.b.c.ept.json"), ".ept.json")
        self.assertEqual(get_file_extension("a.b.c.json"), ".json")


if __name__ == '__main__':
    nose2.main()
