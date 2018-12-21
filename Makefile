QGISDIR=.local/share/QGIS/QGIS3/profiles/jhemmi
PLUGINNAME=loadthemall

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

	
deploy: derase all transcompile
	@echo
	@echo "------------------------------------------"
	@echo "Deploying plugin to your production directory."
	@echo "------------------------------------------"
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $(HOME)/$(QGISDIR)/python/plugins
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf *.py $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf *.pro $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf *.ui $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf *.qm $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf *.png $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	@cp -vf metadata.txt $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	# Fin de la copie du plugin loadthemall

# The dclean target removes compiled python files from plugin directory
# also deletes any .git entry
derase:
	@echo
	@echo "-------------------------"
	@echo "Removing deployed plugin."
	@echo "-------------------------"
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)


zip: deploy clean
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	# The zip target deploys the plugin and creates a zip file with the deployed
	# content. You can then upload the zip file on http://plugins.qgis.org
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/$(QGISDIR)/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME)_$(NOW).zip $(PLUGINNAME)

transup:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	@chmod +x scripts/update-strings.sh
	@scripts/update-strings.sh 

transcompile:
	@echo
	@echo "----------------------------------------"
	@echo "Compiled translation files to .qm files."
	@echo "----------------------------------------"
	@chmod +x scripts/compile-strings.sh
	#echo "Trancompile == $(LOCALES) =="
	@scripts/compile-strings.sh 

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	rm -f *.qm
