export PYTHONPATH=./
pdoc ggame.py --html --html-dir out --overwrite
pdoc ggmath.py --html --html-dir out --overwrite
pdoc ggrocket.py --html --html-dir out --overwrite
mv out/ggame.m.html out/index.html
mv out/ggmath.m.html out/ggmath.html
mv out/ggrocket.m.html out/ggrocket.html
