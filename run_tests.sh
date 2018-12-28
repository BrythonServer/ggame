#!/bin/bash

black examples ggame test
pylint3 -r n examples ggame
python3 -m nose
cd docs && make html
cd ..