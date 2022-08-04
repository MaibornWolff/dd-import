FROM python:3.10.6-alpine@sha256:4543fd9295d8d4f7a61c80d8e490de0f1cb0b37b022dbc1dd92537101a81d149

ARG user=ddimport
ARG group=ddimport

RUN addgroup -g 1000 -S ${group} && \
    adduser -u 1000 -S ${user} -G ${group}

WORKDIR /usr/local/dd-import
RUN mkdir ./dd_import && mkdir ./unittests && mkdir ./bin && \
    mkdir ./coverage_data && chmod ugo+rwx ./coverage_data
COPY --chown=ddimport:ddimport ./ ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PATH="/usr/local/dd-import/bin:$PATH"

USER ${user}
