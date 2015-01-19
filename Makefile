
all: Ui_LoadThemAll.py Ui_Base_LoadThemAll.py resources_rc.py

clean: 	
	rm -f Ui_LoadThemAll.py Ui_Base_LoadThemAll.py 
	rm -f resources_rc.py
	rm -f *.pyc *~

resources_rc.py: resources.qrc
	pyrcc4 -o resources_rc.py resources.qrc

Ui_LoadThemAll.py: Ui_LoadThemAll.ui
	pyuic4 -o Ui_LoadThemAll.py Ui_LoadThemAll.ui

Ui_Base_LoadThemAll.py: Ui_Base_LoadThemAll.ui
	pyuic4 -o Ui_Base_LoadThemAll.py Ui_Base_LoadThemAll.ui
