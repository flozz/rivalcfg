#!/bin/bash

VENV_DIR=./build/macbuild.venv
MACBUILD_DIR=./scripts/macbuild
BUILD_DIR=./build/rivalcfg.macbuild

# Exit on error
set -e

# Create / activate venv
if [ ! -d $VENV_DIR ] ; then
    mkdir -p $(dirname $VENV_DIR)
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

# Print Python version
python --version

# Install dependencies
pip install -r $MACBUILD_DIR/requirements.txt
pip install -e .

# Build
python -m nuitka \
    --mode=standalone \
    --follow-imports \
    --python-flag=-O,isolated \
    --no-deployment-flag=self-execution \
    --assume-yes-for-downloads \
    --output-dir=$BUILD_DIR \
    --output-filename=rivalcfg \
    $MACBUILD_DIR/rivalcfg-cli.py
