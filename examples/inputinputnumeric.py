from ggame.input import InputNumeric
from ggame.mathapp import MathApp

p = InputNumeric(
    (300, 275),  # screen coordinates of input
    3.14,  # initial value
    positioning="physical",
)  # use physical coordinates

MathApp().run()
