#!/bin/bash

black examples ggame test || { echo 'black failed' ; exit 1; }
pylint3 -r n examples ggame || { echo 'pylint failed' ; exit 1; }
python3 -m nose || { echo 'automatic test failed' ; exit 1; }
cd docs && make html || { echo 'sphinx build failed' ; exit 1; }
cd ..