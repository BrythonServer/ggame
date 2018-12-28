"""
Example of using MathApp InputButton class.
"""
from ggame.input import InputButton
from ggame.mathapp import MathApp


def pressbutton(_button):
    """
    Callback function executed when button is pressed.
    """
    print("InputButton pressed!")


InputButton(
    pressbutton,  # reference to handler
    (20, 80),  # physical location on screen
    "Press Me",  # text to display
    size=15,  # text size (pixels)
    positioning="physical",
)  # use physical coordinates

MathApp().run()
