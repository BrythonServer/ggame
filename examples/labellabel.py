from ggame.asset import Color
from ggame.label import Label
from ggame.mathapp import MathApp

Label(
    (20, 80),  # physical location on screen
    "Initial Speed (m/s)",  # text to display
    size=15,  # text size (pixels)
    positioning="physical",  # use physical coordinates
    color=Color(0x202000, 1.0),
)  # text color

MathApp().run()
