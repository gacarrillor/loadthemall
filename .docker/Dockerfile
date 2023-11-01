ARG QGIS_TEST_VERSION
FROM  qgis/qgis:${QGIS_TEST_VERSION}
MAINTAINER Matthias Kuhn <matthias@opengis.ch>

RUN apt-get update && \
    apt-get -y install \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY ./ /usr/src/

RUN chmod a+x /usr/src/run-docker-tests.sh

WORKDIR /
