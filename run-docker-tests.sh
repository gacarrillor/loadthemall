#!/usr/bin/env bash
set -e

pushd /usr/src/
xvfb-run python3 -m nose2
popd
