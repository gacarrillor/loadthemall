
all: Ui_DockWidget.py Ui_Base_LoadThemAll.py resources_rc.py

clean:
	rm -f Ui_DockWidget.py Ui_Base_LoadThemAll.py
	rm -f resources_rc.py
	rm -f *.pyc *~

resources_rc.py: resources.qrc
	pyrcc5 -o resources_rc.py resources.qrc

Ui_DockWidget.py: Ui_DockWidget.ui
	pyuic5 -o Ui_DockWidget.py Ui_DockWidget.ui

Ui_Base_LoadThemAll.py: Ui_Base_LoadThemAll.ui
	pyuic5 -o Ui_Base_LoadThemAll.py Ui_Base_LoadThemAll.ui
