#! /bin/bash

black examples ggame test
python3 -m nose
cd docs && make html
cd ..