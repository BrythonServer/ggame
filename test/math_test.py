import unittest
from ggame.point import Point
from ggame.circle import Circle
from ggame.mathapp import MathApp
from ggame.slider import Slider
from ggame.inputpoint import InputImageButton
from ggame.label import Label
from ggame.input import InputButton, InputNumeric
from ggame.point import ImagePoint
from ggame.line import LineSegment
from ggame.indicator import ImageIndicator
from ggame import Color, LineStyle, ImageAsset, Frame
from ggame.inputpoint import GlassButton, MetalToggle
from ggame.indicator import LEDIndicator 
from ggame.timer import Timer
import time

class TestMathMethods(unittest.TestCase):

    def buttonstatus(self):
        return "True" if self.imgbutton() else "False"
    
    def labelcoords(self):
        return (100 + self.vslider1(), 175)
        
    def buttoncoords(self):
        return (300 + self.vslider1(), 175)
        
    def labelcolor(self):
        colorval =   self.vslider1()
        return Color(colorval*256,1)
    
    def pressbutton(self, caller):
        print("button pressed: ", caller)
    
    def __init__(self, arg):
        super().__init__(arg)
        
    def test_controls(self):
        self.imgbutton = InputImageButton("ggimages/button-round.png", self.pressbutton, (0,0), frame=Frame(0,0,100,100), qty=2)
        self.imgbutton.scale = 0.5
        self.vslider1 = Slider((100, 150), 0, 250, 125, positioning='physical', steps=10)
        self.label = Label(self.labelcoords, self.buttonstatus, size=15, positioning="physical", color=self.labelcolor)
        self.button = InputButton(self.pressbutton, self.buttoncoords, "Press Me", size=15, positioning="physical")
        self.numinput = InputNumeric((300, 275), 3.14, positioning="physical")
        
        ma = MathApp()
        ma.run()
        
        self.vslider1.destroy()
        self.label.destroy()
        self.button.destroy()
        self.numinput.destroy()
        self.imgbutton.destroy()
        
    def test_geometry(self):
        self.ip = ImagePoint( 'bunny.png', (0,0))
        self.ip.movable = True
        self.p1 = Point((0,0), color=Color(0x008000, 1))
        self.p1.movable = True
        self.p2 = Point((0,-1))
        self.p3 = Point((1.2,0))
        self.l1 = LineSegment(self.p2,self.p3, style=LineStyle(3, Color(0,1)))
        self.l2 = LineSegment(self.p2,self.p1, style=LineStyle(3, Color(0,1)))
        self.c2 = Circle((-1,-1), self.p1)

        ma = MathApp()
        ma.run()
        
        self.ip.destroy()
        self.p1.destroy()
        self.p2.destroy()
        self.p3.destroy()
        self.c2.destroy()
        self.l1.destroy()
        self.l2.destroy()
        
    def test_fancycontrols(self):
        self.imgbutton = InputImageButton("ggimages/button-round.png", self.pressbutton, (0,0), frame=Frame(0,0,100,100), qty=2)
        self.imgbutton.scale = 0.5
        self.ii = ImageIndicator("ggimages/red-led-off-on.png", (300,500), self.imgbutton, positioning="physical", frame=Frame(0,0,600,600), qty=2)
        self.ii.scale = 0.1
        self.glassbutton = GlassButton(None, (0,-0.5))
        self.toggle = MetalToggle(0, (0, -1))
        self.Li = LEDIndicator((300,450), self.glassbutton, positioning="physical")
        self.Lit = LEDIndicator((300,480), self.toggle, positioning="physical")

        ma = MathApp()
        ma.run()

        self.imgbutton.destroy()
        self.ii.destroy()
        self.glassbutton.destroy()
        self.toggle.destroy()
        self.Li.destroy()
        self.Lit.destroy()
        
    def timercallback(self, timer):
        self.assertEqual(timer, self.timer)
        self.callbackcomplete = True
        
    def test_timer(self):
        self.callbackcomplete = False
        self.timer = Timer()
        self.timer.callAfter(0.1, self.timercallback)
        ma = MathApp()
        ma.run()
        
        for i in range(10):
            time.sleep(1/60)
            ma._animate(1)

        self.assertEquals(self.callbackcomplete, True)
        
        self.timer.destroy()
        


if __name__ == '__main__':
    unittest.main()
