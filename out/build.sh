#!/bin/bash

# Delete previous build
rm build -r
rm dist -r 
rm pywfs.egg-info -r

# Pack python script
python3 setup.py sdist bdist_wheel
