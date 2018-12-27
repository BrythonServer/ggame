from ggame.inputpoint import GlassButton
from ggame.mathapp import MathApp
from ggame.asset import Frame


def pressbutton(btn):
    print("Button Pressed!")


button = GlassButton(pressbutton, (0, 0))

MathApp().run()
