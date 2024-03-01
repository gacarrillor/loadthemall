import nose2

from qgis.core import (QgsApplication,
                       QgsProject)
from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from LoadThemAll.LoadThemAll import LoadThemAll
from LoadThemAll.core.Enums import EnumLoadThemAllResult
from LoadThemAll.core.LoadFiles import LoadPointClouds
from LoadThemAll.core.LoadConfiguration import LoadConfiguration

start_app()


class TestLoadPointClouds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nINFO: Set up test_load_point_clouds')
        cls.plugin = LoadThemAll(get_iface(), with_gui=False)
        cls.project = QgsProject.instance()

    def test_load_point_clouds_single_ept(self):
        configuration = LoadConfiguration()
        configuration.base_dir = "/QGIS/tests/testdata/point_clouds/ept/rgb/"
        configuration.extension = ["ept.json"]
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
        configuration.b_add_parent_layer_name = True
        configuration.num_layers_to_confirm = 50

        # Load 1 layer
        loader = LoadPointClouds(self.plugin.iface, configuration)
        self.assertEqual(self.project.count(), 0)
        res = loader.loadLayers()
        self.assertEqual(res.result, EnumLoadThemAllResult.SUCCESS)
        self.assertEqual(res.layers_found, 1)
        self.assertEqual(res.layers_loaded, 1)
        self.assertTrue(self.project.count() > 0)

        # Check loaded layer
        layers = self.project.mapLayersByName("ept")
        self.assertTrue(bool(layers))
        self.assertTrue(layers[0].isValid())

    def test_load_point_clouds_ept_not_found(self):
        configuration = LoadConfiguration()
        configuration.base_dir = "/QGIS/tests/testdata/point_clouds/ept/rgb/ept-sources/"
        configuration.extension = ["ept.json"]
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
        configuration.b_add_parent_layer_name = True
        configuration.num_layers_to_confirm = 50

        # Load 1 layer
        loader = LoadPointClouds(self.plugin.iface, configuration)
        self.assertEqual(self.project.count(), 0)
        res = loader.loadLayers()

        self.assertEqual(res.result, EnumLoadThemAllResult.SUCCESS)
        self.assertEqual(res.layers_found, 0)
        self.assertEqual(res.layers_loaded, 0)
        self.assertEqual(self.project.count(), 0)

    def tearDown(self):
        print('INFO: Removing all layers after load test...')
        self.project.removeAllMapLayers()

    @classmethod
    def tearDownClass(cls):
        print('INFO: Tear down test_load_point_clouds')
        cls.plugin.unload()


if __name__ == '__main__':
    nose2.main()
