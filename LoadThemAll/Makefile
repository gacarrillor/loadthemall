
all: ui/Ui_DockWidget.py ui/Ui_Base_LoadThemAll.py resources/resources_rc.py i18n/loadthemall_es.ts i18n/loadthemall_fr.ts i18n/loadthemall_es.qm i18n/loadthemall_fr.qm

clean:
	rm -f ui/Ui_DockWidget.py ui/Ui_Base_LoadThemAll.py
	rm -f resources/resources_rc.py
	rm -f i18n/*.qm
	rm -f *.pyc *~

resources/resources_rc.py: resources/resources.qrc
	pyrcc5 -o resources/resources_rc.py resources/resources.qrc

ui/Ui_DockWidget.py: ui/Ui_DockWidget.ui
	pyuic5 -o ui/Ui_DockWidget.py ui/Ui_DockWidget.ui

ui/Ui_Base_LoadThemAll.py: ui/Ui_Base_LoadThemAll.ui
	pyuic5 -o ui/Ui_Base_LoadThemAll.py ui/Ui_Base_LoadThemAll.ui

i18n/loadthemall_es.ts i18n/loadthemall_fr.ts: i18n/loadthemall.pro
	lupdate i18n/loadthemall.pro

i18n/loadthemall_es.qm i18n/loadthemall_fr.qm: i18n/loadthemall.pro
	lrelease i18n/loadthemall.pro

build:
	cd ..;zip -r /tmp/LoadThemAll.zip LoadThemAll -x LoadThemAll/.git/\* LoadThemAll/.idea/\* \
	LoadThemAll/.gitignore LoadThemAll/README.md LoadThemAll/changelog.txt LoadThemAll/Makefile \
	LoadThemAll/i18n/*.ts LoadThemAll/i18n/*.pro LoadThemAll/resources/resources.qrc \
	LoadThemAll/ui/*.ui
