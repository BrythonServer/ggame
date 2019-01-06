#!/bin/bash

sudo python3 setup.py sdist
sudo python3 -m pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz

