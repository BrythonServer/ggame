"""
Example of using GlassButton class.
"""
from ggame.inputpoint import GlassButton
from ggame.mathapp import MathApp


def pressbutton(_button):
    """
    Callback function executed when button is pressed.
    """
    print("Button Pressed!")


BUTTON = GlassButton(pressbutton, (0, 0))

MathApp().run()
