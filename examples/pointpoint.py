"""
Example of using MathApp Point class.
"""
from ggame.asset import Color
from ggame.point import Point
from ggame.mathapp import MathApp

P1 = Point((0, 1), color=Color(0xFF8000, 1.0))
P1.movable = True
# An orange point that can be moved

P2 = Point(lambda: (P1()[0], P1()[1] + 1))
# A point position based on P1
P3 = Point((1, 0))
# A third, fixed point

MathApp().run()
