"""
Example of using MathApp LEDIndicator class.
"""
from ggame.mathapp import MathApp
from ggame.indicator import LEDIndicator
from ggame.inputpoint import MetalToggle

TOGGLE = MetalToggle(0, (-1, 0))

SWITCH = LEDIndicator((-1, 0.5), TOGGLE)

MathApp().run()
