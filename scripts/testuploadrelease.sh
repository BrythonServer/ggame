#!/bin/bash

python3.11 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
