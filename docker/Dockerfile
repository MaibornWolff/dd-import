FROM python:3.11.0-alpine@sha256:786ff436e5baef1998d2d67da9081a0d40289e3dff25d71845624b1f4ecb3272

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
