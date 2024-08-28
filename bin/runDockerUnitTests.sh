#!/bin/sh

if docker build -f docker/Dockerfile -t brightercore.azurecr.io/dd-import:latest .; then
    docker run --rm brightercore.azurecr.io/dd-import:latest ./bin/runUnitTests.sh
else
    exit 1
fi
