# 🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
# and Cellular Characterization of Screen-Detected Lesions.
#
# Base
# ----

FROM python:3.8.5-alpine3.12


# Metadata
# --------

LABEL "org.label-schema.name"="🏥 MCL Infirmary"
LABEL "org.label-schema.description"="🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions"
LABEL "org.label-schema.version"="1.1.0"
LABEL "org.label-schema.schema-version"="1.0"
LABEL "org.label-schema.docker.cmd"="docker container run --rm --detach --publish 6543:8080 mcl-infirmary"


# Application
# -----------

WORKDIR /usr/src/infirmary
COPY setup.cfg setup.py ./
COPY src/ ./src

RUN : &&\
    apk update --quiet --no-progress &&\
    apk add --quiet --no-progress --virtual /build gcc musl-dev postgresql-dev openldap-dev &&\
    apk add --quiet --no-progress libldap libpq &&\
    python3 setup.py install &&\
    apk del --quiet /build &&\
    rm -rf src setup.cfg setup.py build dist &&\
    rm -rf /var/cache/apk/* &&\
    : /

ENTRYPOINT ["/usr/local/bin/infirmary"]
