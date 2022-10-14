FROM python:3.11.0rc2-alpine@sha256:0ac8cec8bfd1d862a47c1a99507cb9a2023a24d4b281e386cb9d9562e485b681

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
