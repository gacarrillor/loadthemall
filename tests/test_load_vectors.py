import nose2

from qgis.core import (QgsApplication,
                       QgsProject)
from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from LoadThemAll.LoadThemAll import LoadThemAll
from LoadThemAll.core.Enums import EnumLoadThemAllResult
from LoadThemAll.core.Filter import (FilterList,
                                     AlphanumericFilter)
from LoadThemAll.core.LoadFiles import LoadVectors
from tests.utils import get_configuration

start_app()


class TestLoadVectors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nINFO: Set up test_load_vectors')
        cls.plugin = LoadThemAll(get_iface(), with_gui=False)
        cls.project = QgsProject.instance()

    def test_load_vectors(self):
        configuration = get_configuration()
        configuration.base_dir = "/QGIS/tests/testdata/provider/"
        configuration.extension = [".gpkg"]

        # Set filters for next session
        filter_list = FilterList()
        filter = AlphanumericFilter('EndsWith', 'geopackage', configuration)
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
        layers = self.project.mapLayersByName("geopackage")
        self.assertTrue(bool(layers))
        self.assertTrue(layers[0].isValid())

    def tearDown(self):
        print('INFO: Removing all layers after load test...')
        self.project.removeAllMapLayers()

    @classmethod
    def tearDownClass(cls):
        print('INFO: Tear down test_load_vectors')
        cls.plugin.unload()


if __name__ == '__main__':
    nose2.main()
