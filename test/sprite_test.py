import unittest
from ggame import ImageAsset, Frame, Color, LineStyle, RectangleAsset
from ggame import CircleAsset, EllipseAsset, PolygonAsset, LineAsset, TextAsset
from ggame import Sprite

class TestSpriteMethods(unittest.TestCase):

  def __init__(self, arg):
    super().__init__(arg)
    self.image = ImageAsset("bunny.png")
    self.multiimage = ImageAsset("bunny.png", Frame(2,2,10,14), 3, 'horizontal', 2)
    color = 0x001122
    alpha = 0.5
    self.c  = Color(color, alpha)
    pixels = 9
    self.l = LineStyle(pixels, color)
    self.rect = RectangleAsset(10, 20, LineStyle(3, Color(0x112233, 0.5)), Color(0x223344, 0.6))
    self.circ = CircleAsset(30, LineStyle(3, Color(0x112233, 0.5)), Color(0x223344, 0.6))
    self.ellipse = EllipseAsset(40, 50, LineStyle(4, Color(0x113355, 0.6)), Color(0x224466, 0.7))
    self.line = LineAsset(60, 70, LineStyle(5, Color(0x224466, 0.7)))
    self.poly = PolygonAsset([(10,10), (20,10), (15,15), (10,10)], LineStyle(6, Color(0x665544, 0.9)), Color(0x664422, 1.0))
    self.text = TextAsset("sample text", style="20px Arial", width=200, fill=Color(0x123456, 1.0), align='center')

  def test_sprite(self):
    s = Sprite(self.image, (51,52))

if __name__ == '__main__':
    unittest.main()
