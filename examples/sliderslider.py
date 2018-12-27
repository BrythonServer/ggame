from ggame.slider import Slider
from ggame.mathapp import MathApp

s = Slider(
    (100, 150),     # screen position
    0,              # minimum value
    250,            # maximum value
    125,            # initial value
    positioning='physical', # use physical coordinates for position
    steps=10)       # 10 steps between 125 and 250

MathApp().run()
