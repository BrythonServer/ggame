#!/bin/bash

python3.11 setup.py sdist
python3.11 -m pip wheel --no-index --no-build-isolation --no-deps --wheel-dir dist dist/*.tar.gz

