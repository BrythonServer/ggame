from ggame.mathapp import MathApp
from ggame.indicator import ImageIndicator
from ggame.inputpoint import InputImageButton
from ggame.asset import Frame

button = InputImageButton(
    "ggimages/button-round.png",
    None,
    (40, 105),
    positioning="physical",
    frame=Frame(0, 0, 100, 100),
    qty=2,
)
button.scale = 0.5

light = ImageIndicator(
    "ggimages/red-led-off-on.png",
    (100, 100),
    button,
    positioning="physical",
    frame=Frame(0, 0, 600, 600),
    qty=2,
)
light.scale = 0.1

MathApp().run()
