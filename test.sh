#!/bin/bash
set -e
# Run unit tests and code coverage test
coverage run -m pytest tests
coverage report -m --fail-under 100
