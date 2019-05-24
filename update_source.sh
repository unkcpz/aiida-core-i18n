#!/usr/bin/bash

git submodule foreach git pull
cp -r aiida_core/docs/source/* source/
cp conf.py.tmpl source/conf.py


