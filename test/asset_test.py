import unittest
from ggame import ImageAsset, Frame, Color, LineStyle, RectangleAsset
from ggame import CircleAsset, EllipseAsset, PolygonAsset, LineAsset, TextAsset

class TestImageAssetMethods(unittest.TestCase):

  def test_singleimageasset(self):
    a = ImageAsset("bunny.png")
    self.assertEqual(a.GFX.basewidth, 71)
    self.assertEqual(a.GFX.baseheight, 100)
    a.destroy()

  def test_multiimageasset(self):
    a = ImageAsset("bunny.png", Frame(2,2,10,14), 3, 'horizontal', 2)
    self.assertEqual(a.GFXlist[0].basewidth, 71)
    self.assertEqual(a.GFXlist[0].framerect.x, 2)
    self.assertEqual(a.GFXlist[0].framerect.height, 14)
    self.assertEqual(len(a.GFXlist), 3)
    self.assertEqual(a.GFXlist[1].framerect.x, 14)
    self.assertEqual(a.GFXlist[2].framerect.x, 26)
    a.destroy()

  def test_color(self):
    color = 0x001122
    alpha = 0.5
    c = Color(color, alpha)
    self.assertEqual(c.color, color)
    self.assertEqual(c.alpha, alpha)

  def test_linestyle(self):
    color = 0x001122
    alpha = 0.5
    c = Color(color, alpha)
    pixels = 9
    l = LineStyle(pixels, c)
    self.assertEqual(l.width, pixels)
    self.assertEqual(l.color.color, color)
    self.assertEqual(l.color.alpha, alpha)

  def test_rectangleasset(self):
    r = RectangleAsset(10, 20, LineStyle(3, Color(0x112233, 0.5)), Color(0x223344, 0.6))
    self.assertEqual(r.GFX.visible, False)
    self.assertEqual(r.width, 10)
    self.assertEqual(r.height, 20)
    self.assertEqual(r.GFX.x, 0)

  def test_circleasset(self):
    c = CircleAsset(30, LineStyle(3, Color(0x112233, 0.5)), Color(0x223344, 0.6))
    self.assertEqual(c.GFX.visible, False)
    self.assertEqual(c.radius, 30)
    self.assertEqual(c.GFX.x, 0)


if __name__ == '__main__':
    unittest.main()
