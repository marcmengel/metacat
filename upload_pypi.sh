#!/bin/bash


rm -rf build dist *.egg-info
#python setup.py sdist bdist
python3 -m build
twine upload --verbose  dist/*
rm -rf build dist *.egg-info

