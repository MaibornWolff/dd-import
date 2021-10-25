FROM python:3.10.0-alpine@sha256:c13a6cf74fb452f9eab9f1a521f3ff6d056d5bc51b1a29bfe4758fcb00135394

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
