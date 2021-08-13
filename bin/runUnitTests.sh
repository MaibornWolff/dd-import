#!/bin/sh

if coverage run -m unittest discover -v; then
    coverage report -m
else
    exit 1
fi
