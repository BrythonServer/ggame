from ggame.inputpoint import InputImageButton
from ggame.mathapp import MathApp
from ggame.asset import Frame


def pressbutton(btn):
    print("Button Pressed!")


button = InputImageButton(
    "ggimages/button-round.png", pressbutton, (0, 0), frame=Frame(0, 0, 100, 100), qty=2
)
button.scale = 0.5

MathApp().run()
