FROM python:3.9.7-alpine@sha256:964a1afa20dd4a3723002560124dd96f2a9e853f7ef5b86f5c2354af336fca37

ARG user=ddimport
ARG group=ddimport

RUN addgroup -g 1000 -S ${group} && \
    adduser -u 1000 -S ${user} -G ${group}

WORKDIR /usr/local/dd-import
RUN mkdir ./dd_import && mkdir ./unittests && mkdir ./bin && \
    mkdir ./coverage_data && chmod ugo+rwx ./coverage_data
COPY --chown=ddimport:ddimport ./ ./
RUN pip install --no-cache-dir -r requirements.txt

USER ${user}
