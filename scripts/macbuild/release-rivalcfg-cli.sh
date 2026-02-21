#!/bin/bash

VENV_DIR=./build/macbuild.venv
MACBUILD_DIR=./scripts/macbuild
BUILD_DIR=./build/rivalcfg.macbuild
DIST_DIR=./dist

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

# Define some useful vars
_arch=$(uname -m)
_version=$(python3 -c "import tomllib;print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
_output_dir_name=rivalcfg-cli_v${_version}
_output_dmg_name=rivalcfg-cli_v${_version}_macos_${_arch}.dmg

# Copy files
mkdir -p $BUILD_DIR/$_output_dir_name/
cp $BUILD_DIR/rivalcfg-cli.dist/* $BUILD_DIR/$_output_dir_name/
cp LICENSE $BUILD_DIR/$_output_dir_name/
cp $MACBUILD_DIR/README.dist.rst $BUILD_DIR/$_output_dir_name/README.txt

# Patch the README
sed -i "" "s/<VERSION>/$_version/g" $BUILD_DIR/$_output_dir_name/README.txt

# Make the DMG
mkdir -p $DIST_DIR
dmgbuild \
    -s $MACBUILD_DIR/settings.py \
    "Rivalcfg CLI" \
    $DIST_DIR/$_output_dmg_name
