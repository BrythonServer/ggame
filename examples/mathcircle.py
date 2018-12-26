from ggame.point import Point
from ggame.circle import Circle
from ggame.mathapp import MathApp

# p1 is the center of the circle
p1 = Point((0.5, 1))
# p2 is on the perimeter
p2 = Point((1.3, 1))
# define a circle from center and perimeter points
c = Circle(p1, p2)
# allow the user to drag the perimeter point to resize the circle
p2.movable = True

MathApp().run()
