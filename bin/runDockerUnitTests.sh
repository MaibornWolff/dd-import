#!/bin/sh

if docker build -f docker/Dockerfile -t dd-import:latest .; then
    docker run --rm dd-import:latest ./bin/runUnitTests.sh
else
    exit 1
fi
