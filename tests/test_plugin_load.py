import nose2

from qgis.core import QgsApplication
from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

start_app()


class TestPluginLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nINFO: Set up test_plugin_load')
        iface = get_iface()
        from LoadThemAll.LoadThemAll import LoadThemAll
        cls.plugin = LoadThemAll(get_iface(), with_gui=False)
        # cls.plugin.initGui()  # No GUI for tests

    def test_plugin_load(self):
        print('INFO: Validating plugin load...')
        self.assertIsNotNone(self.plugin.iface)

    @classmethod
    def tearDownClass(cls):
        print('INFO: Tear down test_plugin_load')
        cls.plugin.unload()


if __name__ == '__main__':
    nose2.main()
