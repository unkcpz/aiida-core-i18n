#!/bin/bash

## !!!! MAKE SURE TO RUN THIS SCRIPT IN A VENV
## since it will install or update a lots of new packages
## You don't want it breaks your current python environments

# Run this file in your local machine to; 
# - update the source of docs
# - check the diff and patch update the conf.py
# - pull latest translated docs (.pot files) from transfix
# - Install the necessary dependence for sphnix build
# - build the translated docs in local.

# === update the source

# always and only get the latest develop branch
# if exist remove and clone
git clone --single-branch --branch develop --depth 1 https://github.com/aiidateam/aiida-core.git

# delete git of inner repository to make in isolated
# otherwise the outer repository cannot be upload
rm -rf aiida_core/.git

# === pull latest translated docs from tx and put them in docs build path
tx pull --all

# link locales into aiida_core for build
ln -s ./locales ./aiida_core/docs/source/locales

# === install the dependecies for sphnix build
# the command is copied from actual build process in readthedocs.org
conda env update -n ${CONDA_VENV_NAME} --file environment.yml

