#!/bin/sh
export PYTHONPATH="${PYTHONPATH}:/usr/local/dd-import"
python -m dd_import.dd_reimport_findings
