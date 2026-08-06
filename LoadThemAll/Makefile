
all: resources/resources_rc.py resources/resources_rc_qt5.py i18n/loadthemall_es.ts i18n/loadthemall_fr.ts i18n/loadthemall_es.qm i18n/loadthemall_fr.qm

clean:
	rm -f resources/resources_rc.py resources/resources_rc_qt5.py
	rm -f i18n/*.qm
	rm -f *.pyc *~

resources/resources_rc.py: resources/resources.qrc
	rcc -g python -o resources/resources_rc.py resources/resources.qrc
	sed -i 's/from PySide6 import/from qgis.PyQt import/' resources/resources_rc.py

resources/resources_rc_qt5.py: resources/resources.qrc
	pyrcc5 -o resources/resources_rc_qt5.py resources/resources.qrc
	sed -i 's/from PyQt5 import/from qgis.PyQt import/' resources/resources_rc_qt5.py

i18n/loadthemall_es.ts i18n/loadthemall_fr.ts: i18n/loadthemall.pro
	lupdate i18n/loadthemall.pro

i18n/loadthemall_es.qm i18n/loadthemall_fr.qm: i18n/loadthemall.pro
	lrelease i18n/loadthemall.pro

build:
	cd ..;zip -r /tmp/LoadThemAll.zip LoadThemAll -x LoadThemAll/.git/\* LoadThemAll/.idea/\* \
	LoadThemAll/.gitignore LoadThemAll/README.md LoadThemAll/changelog.txt LoadThemAll/Makefile \
	LoadThemAll/i18n/*.ts LoadThemAll/i18n/*.pro LoadThemAll/resources/resources.qrc
