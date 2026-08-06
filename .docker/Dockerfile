ARG QGIS_TEST_VERSION=4.2.1
FROM qgis/qgis:final-3_28_13 AS qgis-testdata
FROM  qgis/qgis:${QGIS_TEST_VERSION}
LABEL maintainer="Matthias Kuhn <matthias@opengis.ch>"

COPY --from=qgis-testdata /QGIS/tests/testdata/point_clouds/ept/rgb /QGIS/tests/testdata/point_clouds/ept/rgb
COPY --from=qgis-testdata /QGIS/tests/testdata/provider /QGIS/tests/testdata/provider
COPY --from=qgis-testdata /QGIS/tests/testdata/raster /QGIS/tests/testdata/raster
COPY --from=qgis-testdata /QGIS/tests/testdata/zip /QGIS/tests/testdata/zip
COPY LoadThemAll/ /usr/src/LoadThemAll/
COPY tests/ /usr/src/tests/
COPY run-docker-tests.sh /usr/src/run-docker-tests.sh

RUN chmod a+x /usr/src/run-docker-tests.sh && \
    useradd --create-home --uid 10001 loadthemall

USER loadthemall

ENTRYPOINT ["/usr/src/run-docker-tests.sh"]
