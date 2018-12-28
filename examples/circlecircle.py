"""
Example of using MathApp Circle class.
"""
from ggame.point import Point
from ggame.circle import Circle
from ggame.mathapp import MathApp

# P1 is the center of the circle
P1 = Point((0.5, 1))
# P2 is on the perimeter
P2 = Point((1.3, 1))
# define a circle from center and perimeter points
C = Circle(P1, P2)
# allow the user to drag the perimeter point to resize the circle
P2.movable = True

MathApp().run()
