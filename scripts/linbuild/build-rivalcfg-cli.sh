#!/bin/bash

VENV_DIR=./build/linbuild.venv
LINBUILD_DIR=./scripts/linbuild
BUILD_DIR=./build/rivalcfg.linbuild

# Exit on error
set -e

# Create / activate venv
if [ ! -d $VENV_DIR ] ; then
    mkdir -p $(dirname $VENV_DIR)
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

# Install dependencies
pip install -r $LINBUILD_DIR/requirements.txt
pip install -e .

# Build
python -m nuitka \
    --mode=standalone \
    --python-flag=-O,isolated \
    --follow-imports \
    --output-dir=$BUILD_DIR \
    --output-filename=rivalcfg \
    $LINBUILD_DIR/rivalcfg-cli.py
