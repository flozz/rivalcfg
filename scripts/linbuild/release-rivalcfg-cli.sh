#!/bin/bash

VENV_DIR=./build/linbuild.venv
LINBUILD_DIR=./scripts/linbuild
BUILD_DIR=./build/rivalcfg.linbuild
DIST_DIR=./dist

# Exit on error
set -e

# Define some useful vars
_arch=$(uname -m)
_version=$(python3 -c "import tomllib;print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
_output_dir_name=rivalcfg-cli_v${_version}_linux_${_arch}
_output_tarball_name=rivalcfg-cli_v${_version}_linux_${_arch}.tar.gz

# Copy files
mkdir -p $BUILD_DIR/$_output_dir_name/
cp $BUILD_DIR/rivalcfg-cli.dist/* $BUILD_DIR/$_output_dir_name/
cp LICENSE $BUILD_DIR/$_output_dir_name/
cp $LINBUILD_DIR/README.dist.rst $BUILD_DIR/$_output_dir_name/README.rst

# Make the tarball
cd $BUILD_DIR
tar -cvzf $_output_tarball_name $_output_dir_name
cd -
mkdir -p $DIST_DIR
mv $BUILD_DIR/$_output_tarball_name $DIST_DIR
