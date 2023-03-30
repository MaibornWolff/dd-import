FROM python:3.11.2-alpine@sha256:4b4078a3ab81edc2f5725cd42b065beaeeb4f9be3b4b1e3b4cf11dd6ae9720d3

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
