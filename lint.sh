#!/bin/bash
set -e
PACKAGE_NAME=va_lib
# Check style error and static type
# PEP8 checker
pylint $PACKAGE_NAME
# Static type checker
mypy --strict $PACKAGE_NAME
# Import library checker
isort --check-only $PACKAGE_NAME
