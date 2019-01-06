#!/bin/bash

sudo python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
