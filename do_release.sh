#!/bin/bash

python setup.py sdist bdist_egg
twine upload --verbose dist/*