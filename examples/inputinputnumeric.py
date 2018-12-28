"""
Example of using InputNumeric class.
"""

from ggame.input import InputNumeric
from ggame.mathapp import MathApp

P = InputNumeric(
    (300, 275),  # screen coordinates of input
    3.14,  # initial value
    positioning="physical",
)  # use physical coordinates

MathApp().run()
