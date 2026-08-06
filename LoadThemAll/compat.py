import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QT_VERSION_STR, Qt
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox
from qgis.core import Qgis


def _enum_member(container, enum_name, member_name):
    scoped_enum = getattr(container, enum_name, None)
    if scoped_enum is not None and hasattr(scoped_enum, member_name):
        return getattr(scoped_enum, member_name)
    return getattr(container, member_name)


QT_MAJOR_VERSION = int(QT_VERSION_STR.split(".", 1)[0])

KEY_ESCAPE = _enum_member(Qt, "Key", "Key_Escape")
RIGHT_DOCK_WIDGET_AREA = _enum_member(
    Qt, "DockWidgetArea", "RightDockWidgetArea"
)
SHOW_DIRS_ONLY = _enum_member(QFileDialog, "Option", "ShowDirsOnly")

MESSAGE_BOX_OK = _enum_member(QMessageBox, "StandardButton", "Ok")
MESSAGE_BOX_CANCEL = _enum_member(QMessageBox, "StandardButton", "Cancel")

QGIS_VERSION_INT = (
    Qgis.versionInt()
    if hasattr(Qgis, "versionInt")
    else Qgis.QGIS_VERSION_INT
)
QGIS_MESSAGE_INFO = _enum_member(Qgis, "MessageLevel", "Info")
QGIS_MESSAGE_WARNING = _enum_member(Qgis, "MessageLevel", "Warning")


def load_ui_class(filename):
    ui_path = os.path.join(os.path.dirname(__file__), "ui", filename)
    return uic.loadUiType(ui_path)[0]
