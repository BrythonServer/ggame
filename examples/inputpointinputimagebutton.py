"""
Example of using the InputImageButton class.
"""
from ggame.inputpoint import InputImageButton
from ggame.mathapp import MathApp
from ggame.asset import Frame


def pressbutton(dummy):
    """
    Callback function executed when button is pressed.
    """
    print("Button Pressed!")


BUTTON = InputImageButton(
    "ggimages/button-round.png", pressbutton, (0, 0), frame=Frame(0, 0, 100, 100), qty=2
)
BUTTON.scale = 0.5

MathApp().run()
