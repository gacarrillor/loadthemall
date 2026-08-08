ARG QGIS_TEST_VERSION
FROM  qgis/qgis:${QGIS_TEST_VERSION}

RUN apt-get update && \
    apt-get -y install \
    python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

ENV VENV=/usr/.venv
RUN python3 -m venv --system-site-packages $VENV
ENV PATH="$VENV/bin:$PATH"

COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY ./ /usr/src/

# For QGIS 3.44 Docker image:
ENV PYTHONPATH=/usr/share/qgis/python/plugins:$PYTHONPATH

RUN chmod a+x /usr/src/run-docker-tests.sh

ENTRYPOINT ["/usr/src/run-docker-tests.sh"]
