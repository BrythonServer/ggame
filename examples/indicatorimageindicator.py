"""
Example of using ImageIndicator class.
"""

from ggame.mathapp import MathApp
from ggame.indicator import ImageIndicator
from ggame.inputpoint import InputImageButton
from ggame.asset import Frame

BUTTON = InputImageButton(
    "ggimages/button-round.png",
    None,
    (40, 105),
    positioning="physical",
    frame=Frame(0, 0, 100, 100),
    qty=2,
)
BUTTON.scale = 0.5

LIGHT = ImageIndicator(
    "ggimages/red-led-off-on.png",
    (100, 100),
    BUTTON,  # button object supplies the indicator state.
    positioning="physical",
    frame=Frame(0, 0, 600, 600),
    qty=2,
)
LIGHT.scale = 0.1

MathApp().run()
