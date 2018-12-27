from ggame.asset import Color
from ggame.point import Point
from ggame.mathapp import MathApp

p1 = Point((0,1), color=Color(0xff8000, 1.0))
p1.movable = True
# An orange point that can be moved

p2 = Point(lambda: (p1()[0], p1()[1]+1))
# A point position based on P1
p3 = Point((1,0))
# A third, fixed point

MathApp().run()