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

AIIDA_DIR="aiida-core"

# ==== check tx is installed

# === update the source
# always and only get the latest develop branch
# if directory already exist remove and clone

if [ -d "$AIIDA_DIR" ]; then
  # Take action if $DIR exists. #
  echo "${AIIDA_DIR} exist delete it in order to redownload"
  rm -rf ${AIIDA_DIR}
fi

REMOTE="https://github.com/aiidateam/aiida-core.git"
echo "Getting list of tags from: $REMOTE"

tag=$(git ls-remote --tags --exit-code --refs "$REMOTE" | sed -E 's/^[[:xdigit:]]+[[:space:]]+refs\/tags\/(.+)/\1/g' | tail -n1)

echo "Selected tag: $tag"

git clone --single-branch --branch "$tag" --depth 1 $REMOTE

# delete git of inner repository to make in isolated
# otherwise the outer repository cannot be upload
rm -rf ${AIIDA_DIR}/.git

# === pull latest translated docs from tx and put them in docs build path
tx pull --all

# link locales into aiida_core for build use -r for relative path
ln -s -r ./locales ${AIIDA_DIR}/docs/source/locales

# ==== testing the build locally: ask for run

# install packages for docs build and run build locally
# PENV_DIR="/tmp/docs/checkouts/readthedocs.org/user_builds/aiida-core-zh-cn/envs/develop"
# /bin/python -mvirtualenv --system-site-packages ${PENV_DIR}
# ${PENV_DIR}/bin/python -m pip install --upgrade --no-cache-dir pip setuptools
# ${PENV_DIR}/bin/python -m pip install --upgrade --no-cache-dir -I \
#     "mock==1.0.1" "pillow==5.4.1" "alabaster>=0.7,<0.8,!=0.7.5" \
#     "commonmark==0.8.1" "recommonmark==0.5.0" "sphinx<2" "sphinx-rtd-theme<0.5" \
#     "readthedocs-sphinx-ext<2.2"
# ${PENV_DIR}/bin/python -m pip install --upgrade --upgrade-strategy eager --no-cache-dir "./aiida-core[docs,tests]"
# ${PENV_DIR}/bin/python -m sphinx -T -E -b html -d _build/doctrees -D language=zh_CN ${AIIDA_DIR}/docs/source _build/html

# # ==== git commit with date automatically and push: ask to run

# git add .
# git commit -m "date"
# git push
