#!/usr/bin/env bash
set -e

pushd /usr/src/
export PYTHONPATH="/usr/share/qgis/python:/usr/share/qgis/python/plugins:${PYTHONPATH:-}"
export QT_QPA_PLATFORM=offscreen
python3 -m unittest discover -s tests -p "test_*.py" -v
popd
