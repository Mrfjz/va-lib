#!/bin/bash
set -e

PYTHON_VERSION=3.11.2
PROJECT_NAME=$(basename "$PWD")
# Add two space to avoid substring matching
if ! pyenv virtualenvs | grep -q " $PROJECT_NAME "; then
    # Setup pyenv
    pyenv install -s $PYTHON_VERSION
    pyenv virtualenv $PYTHON_VERSION $PROJECT_NAME
fi
pyenv local $PROJECT_NAME

pip install -r requirements.txt
# # Install pre-commit hooks
pre-commit install
