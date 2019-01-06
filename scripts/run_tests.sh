#!/bin/bash

black --check examples ggame test || { echo 'black failed (use black first)' ; exit 1; }
python3 -m pylint -r n examples ggame || { echo 'pylint failed' ; exit 1; }
python3 -m nose || { echo 'automatic test failed' ; exit 1; }
cd docs && make html || { echo 'sphinx build failed' ; exit 1; }
cd ..