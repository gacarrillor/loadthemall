import nose2

from qgis.core import (QgsApplication,
                       QgsProject)
from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from LoadThemAll.LoadThemAll import LoadThemAll
from LoadThemAll.core.Enums import EnumLoadThemAllResult
from LoadThemAll.core.Filter import (FilterList,
                                     AlphanumericFilter)
from LoadThemAll.core.LoadFiles import LoadRasters
from LoadThemAll.core.LoadConfiguration import LoadConfiguration

start_app()


class TestLoadRasters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nINFO: Set up test_load_rasters')
        cls.plugin = LoadThemAll(get_iface(), with_gui=False)
        cls.project = QgsProject.instance()

    def test_load_rasters(self):
        configuration = LoadConfiguration()
        configuration.base_dir = "/QGIS/tests/testdata/raster/"
        configuration.extension = [".png"]
        configuration.with_gui = False  # Non-default
        configuration.b_sort = False  # Non-default

        configuration.b_groups = False
        configuration.b_search_in_compressed_files = False
        configuration.b_layers_off = False
        configuration.b_not_empty = True
        configuration.b_reverse_sort = False
        configuration.b_case_insensitive = True
        configuration.b_accent_insensitive = False
        configuration.b_styles = False
        configuration.b_search_parent_layer = False
        configuration.b_add_parent_layer_name = False
        configuration.num_layers_to_confirm = 50

        # Set filters for next session
        filter_list = FilterList()
        filter = AlphanumericFilter('EndsWith', 'rgb', configuration)
        filter_list.addFilter(filter)

        # Load 1 layer
        loader = LoadRasters(self.plugin.iface, configuration)
        self.assertEqual(self.project.count(), 0)
        loader.filterList = filter_list
        res = loader.loadLayers()
        self.assertEqual(res.result, EnumLoadThemAllResult.SUCCESS)
        self.assertEqual(res.layers_found, 1)
        self.assertEqual(res.layers_loaded, 1)
        self.assertTrue(self.project.count() > 0)

        # Check loaded layer
        layers = self.project.mapLayersByName("rotated_rgb")
        self.assertTrue(bool(layers))
        self.assertTrue(layers[0].isValid())

    def tearDown(self):
        print('INFO: Removing all layers after load test...')
        self.project.removeAllMapLayers()

    @classmethod
    def tearDownClass(cls):
        print('INFO: Tear down test_load_rasters')
        cls.plugin.unload()


if __name__ == '__main__':
    nose2.main()
