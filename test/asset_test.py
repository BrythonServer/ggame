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

  def test_ellipseasset(self):
    e = EllipseAsset(40, 50, LineStyle(4, Color(0x113355, 0.6)), Color(0x224466, 0.7))
    self.assertEqual(e.GFX.visible, False)
    self.assertEqual(e.GFX.ehw, 40)
    self.assertEqual(e.GFX.ehh, 50)
    self.assertEqual(e.GFX.x, 0)

  def test_lineasset(self):
    l = LineAsset(60, 70, LineStyle(5, Color(0x224466, 0.7)))
    self.assertEqual(l.GFX.visible, False)
    self.assertEqual(l.GFX.xto, 60)
    self.assertEqual(l.GFX.yto, 70)
    self.assertEqual(l.GFX.x, 0)

  def test_polygonasset(self):
    p = PolygonAsset([(10,10), (20,10), (15,15), (10,10)], LineStyle(6, Color(0x665544, 0.9)), Color(0x664422, 1.0))
    self.assertEqual(len(p.GFX.jpath), 8)
    self.assertEqual(p.GFX.jpath[4], 15)
    self.assertEqual(p.GFX.visible, False)

  def test_textasset(self):
    t = TextAsset("sample text", style="20px Arial", width=200, fill=Color(0x123456, 1.0), align='center')
    self.assertEqual(t.GFX.text, "sample text")
    self.assertEqual(t.GFX.styledict['font'], "20px Arial")
    self.assertEqual(t.GFX.styledict['fill'], 0x123456)
    self.assertEqual(t.GFX.alpha, 1.0)


if __name__ == '__main__':
    unittest.main()
