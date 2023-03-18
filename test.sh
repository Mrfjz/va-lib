#!/bin/bash
set -e
# Run unit tests and code coverage test
coverage run -m pytest python_template
coverage report -m --fail-under 100
