from ggame.mathapp import MathApp
from ggame.indicator import LEDIndicator
from ggame.inputpoint import MetalToggle

toggle = MetalToggle(0, (-1, 0))

switch = LEDIndicator((-1, 0.5), toggle)

MathApp().run()
