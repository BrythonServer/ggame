export PYTHONPATH=./
pdoc ggame.py --html --html-dir out --overwrite
mv out/ggame.m.html out/index.html
