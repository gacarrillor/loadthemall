import nose2

from qgis.core import (QgsApplication,
                       QgsProject)
from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from LoadThemAll.LoadThemAll import LoadThemAll
from LoadThemAll.core.Enums import EnumLoadThemAllResult
from LoadThemAll.core.Filter import (FilterList,
                                     AlphanumericFilter)
from LoadThemAll.core.LoadFiles import (LoadVectors,
                                        LoadRasters)
from tests.utils import get_configuration

start_app()


class TestCompressedLayers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nINFO: Set up test_compressed_layers')
        cls.plugin = LoadThemAll(get_iface(), with_gui=False)
        cls.project = QgsProject.instance()

    def test_compressed_shp(self):
        configuration = get_configuration()
        configuration.base_dir = "/QGIS/tests/testdata/zip/"
        configuration.extension = [".shp"]
        configuration.b_search_in_compressed_files = True

        # Set filters for next session
        filter_list = FilterList()
        filter = AlphanumericFilter('EndsWith', 'points', configuration)
        filter_list.addFilter(filter)

        # Load layers
        loader = LoadVectors(self.plugin.iface, configuration)
        self.assertEqual(self.project.count(), 0)
        loader.filterList = filter_list
        res = loader.loadLayers()
        self.assertEqual(res.result, EnumLoadThemAllResult.SUCCESS)
        self.assertEqual(res.layers_found, 4)
        self.assertEqual(res.layers_loaded, 4)
        self.assertTrue(self.project.count() > 0)

        # Check loaded layer
        #print([l.source() for l in self.project.mapLayers().values()])
        layers = self.project.mapLayersByName("points")
        self.assertEqual(len(layers), 4)
        self.assertTrue(layers[0].isValid())

    def test_compressed_gz_geojson(self):
        configuration = get_configuration()
        configuration.base_dir = "/QGIS/tests/testdata/zip/"
        configuration.extension = [".geojson"]
        configuration.b_search_in_compressed_files = True

        # Set filters for next session
        filter_list = FilterList()
        filter = AlphanumericFilter('EndsWith', 'points3', configuration)
        filter_list.addFilter(filter)

        # Load 1 layer
        loader = LoadVectors(self.plugin.iface, configuration)
        self.assertEqual(self.project.count(), 0)
        loader.filterList = filter_list
        res = loader.loadLayers()
        self.assertEqual(res.result, EnumLoadThemAllResult.SUCCESS)
        self.assertEqual(res.layers_found, 1)
        self.assertEqual(res.layers_loaded, 1)
        self.assertTrue(self.project.count() > 0)

        # Check loaded layer
        #print([l.source() for l in self.project.mapLayers().values()])
        layers = self.project.mapLayersByName("points3.geojson")
        self.assertTrue(bool(layers))
        self.assertTrue(layers[0].isValid())

    def test_compressed_tif(self):
        configuration = get_configuration()
        configuration.base_dir = "/QGIS/tests/testdata/zip/"
        configuration.extension = [".tif"]
        configuration.b_search_in_compressed_files = True

        # Set filters for next session
        filter_list = FilterList()
        filter = AlphanumericFilter('StartsWith', 'landsat_b2', configuration)
        filter_list.addFilter(filter)

        # Load 2 layers
        loader = LoadRasters(self.plugin.iface, configuration)
        self.assertEqual(self.project.count(), 0)
        loader.filterList = filter_list
        res = loader.loadLayers()
        self.assertEqual(res.result, EnumLoadThemAllResult.SUCCESS)
        self.assertEqual(res.layers_found, 2)
        self.assertEqual(res.layers_loaded, 2)
        self.assertTrue(self.project.count() > 0)

        # Check loaded layers
        #print(self.project.mapLayers())
        layers = self.project.mapLayersByName("landsat_b2")
        self.assertTrue(bool(layers))
        self.assertTrue(layers[0].isValid())

    def tearDown(self):
        print('INFO: Removing all layers after compressed layers test...')
        self.project.removeAllMapLayers()

    @classmethod
    def tearDownClass(cls):
        print('INFO: Tear down test_compressed_layers')
        cls.plugin.unload()


if __name__ == '__main__':
    nose2.main()
