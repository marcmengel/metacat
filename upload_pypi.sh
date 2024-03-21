#!/bin/bash


rm -rf build dist *.egg-info
python setup.py sdist bdist
twine upload dist/*
rm -rf build dist *.egg-info

