import unittest
from ggame import ImageAsset, Frame, Color, LineStyle, RectangleAsset
from ggame import CircleAsset, EllipseAsset, PolygonAsset, LineAsset, TextAsset

class TestImageAssetMethods(unittest.TestCase):

  def test_singleimageasset(self):
    a = ImageAsset("bunny.png")
    self.assertEqual(a.gfx.basewidth, 71)
    self.assertEqual(a.gfx.baseheight, 100)
    a.destroy()

  def test_multiimageasset(self):
    a = ImageAsset("bunny.png", Frame(2,2,10,14), 3, 'horizontal', 2)
    self.assertEqual(a.gfxlist[0].basewidth, 71)
    self.assertEqual(a.gfxlist[0].framerect.x, 2)
    self.assertEqual(a.gfxlist[0].framerect.height, 14)
    self.assertEqual(len(a.gfxlist), 3)
    self.assertEqual(a.gfxlist[1].framerect.x, 14)
    self.assertEqual(a.gfxlist[2].framerect.x, 26)
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
    self.assertEqual(r.gfx.visible, False)
    self.assertEqual(r.width, 10)
    self.assertEqual(r.height, 20)
    self.assertEqual(r.gfx.x, 0)

  def test_circleasset(self):
    c = CircleAsset(30, LineStyle(3, Color(0x112233, 0.5)), Color(0x223344, 0.6))
    self.assertEqual(c.gfx.visible, False)
    self.assertEqual(c.radius, 30)
    self.assertEqual(c.gfx.x, 0)

  def test_ellipseasset(self):
    e = EllipseAsset(40, 50, LineStyle(4, Color(0x113355, 0.6)), Color(0x224466, 0.7))
    self.assertEqual(e.gfx.visible, False)
    self.assertEqual(e.gfx.ehw, 40)
    self.assertEqual(e.gfx.ehh, 50)
    self.assertEqual(e.gfx.x, 0)

  def test_lineasset(self):
    l = LineAsset(60, 70, LineStyle(5, Color(0x224466, 0.7)))
    self.assertEqual(l.gfx.visible, False)
    self.assertEqual(l.gfx.xto, 60)
    self.assertEqual(l.gfx.yto, 70)
    self.assertEqual(l.gfx.x, 0)

  def test_polygonasset(self):
    p = PolygonAsset([(10,10), (20,10), (15,15), (10,10)], LineStyle(6, Color(0x665544, 0.9)), Color(0x664422, 1.0))
    self.assertEqual(len(p.gfx.jpath), 8)
    self.assertEqual(p.gfx.jpath[4], 15)
    self.assertEqual(p.gfx.visible, False)

  def test_textasset(self):
    t = TextAsset("sample text", style="20px Arial", width=200, fill=Color(0x123456, 1.0), align='center')
    self.assertEqual(t.gfx.text, "sample text")
    self.assertEqual(t.gfx.styledict['font'], "20px Arial")
    self.assertEqual(t.gfx.styledict['fill'], 0x123456)
    self.assertEqual(t.gfx.alpha, 1.0)


if __name__ == '__main__':
    unittest.main()
