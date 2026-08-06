from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog, QDockWidget
from qgis.testing import unittest, start_app

start_app()


class TestQtCompatibility(unittest.TestCase):

    def test_ui_forms_and_resources(self):
        from LoadThemAll.gui.BaseLoadThemAllDialog import Ui_Base_LoadThemAll
        from LoadThemAll.gui.LoadThemAllDialog import Ui_DockWidget
        import LoadThemAll.LoadThemAll

        base_dialog = QDialog()
        Ui_Base_LoadThemAll().setupUi(base_dialog)

        dock_widget = QDockWidget()
        Ui_DockWidget().setupUi(dock_widget)

        self.assertFalse(QIcon(":/plugins/loadthemall/icon.png").isNull())


if __name__ == "__main__":
    unittest.main()
