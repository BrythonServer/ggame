import unittest
from ggame import ImageAsset, Frame, Color, LineStyle, RectangleAsset
from ggame import CircleAsset, EllipseAsset, PolygonAsset, LineAsset, TextAsset
from ggame import App, Sprite

class TestSpriteMethods(unittest.TestCase):

  def __init__(self, arg):
    super().__init__(arg)
    self.image = ImageAsset("bunny.png")
    self.rocket = ImageAsset("ggimages/rocket.png")
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
    self.assertEqual(s.x, 51)
    self.assertEqual(s.y, 52)
    self.assertEqual(s.width, 71)
    self.assertEqual(s.height, 100)
    self.assertEqual(s.position, (51,52))
    self.assertEqual(s.fxcenter, 0.0)
    s.x = 41
    self.assertEqual(s.x, 41)
    self.assertEqual(s.width, 71)
    s.destroy()

  def test_spritecollision(self):
    s1 = Sprite(self.image, (51,52))
    s2 = Sprite(self.image, (51, 52))
    cl = s2.collidingWithSprites()
    self.assertEqual(len(cl), 1)
    self.assertEqual(s2.collidingWith(cl[0]), True)
    s2.x = 125
    self.assertEqual(s2.collidingWith(cl[0]), False)
    s1.destroy()
    s2.destroy()    


  def test_spritevariety(self):
    s1 = Sprite(self.multiimage)
    s2 = Sprite(self.rect)
    s3 = Sprite(self.circ)
    s4 = Sprite(self.ellipse)
    s5 = Sprite(self.line)
    s6 = Sprite(self.poly)
    s7 = Sprite(self.text)
    s1.destroy()
    s2.destroy()
    s3.destroy()
    s4.destroy()
    s5.destroy()
    s6.destroy()
    s7.destroy()

  def test_advancedspritecollision(self):
    class SpriteChild(Sprite):
      pass

    s1 = Sprite(self.image, (51,52))
    s2 = Sprite(self.image, (61,52))
    s3 = SpriteChild(self.image, (71,52))
    cl = s1.collidingWithSprites(SpriteChild)
    self.assertEqual(len(cl), 1)
    self.assertIs(cl[0], s3)
    cl = s1.collidingWithSprites()
    self.assertEqual(len(cl), 2)
    s1.destroy()
    s2.destroy()
    s3.destroy()

  def test_enfoldingcollision(self):
    
    def step():
      s1.x += 1
      s2.x -= 1
      c = s1.collidingWith(s2)
      self.assertTrue(c, msg="big sprite colliding with embedded sprite")
      c = s2.collidingWith(s1)
      self.assertTrue(c, msg="small sprite colliding with enfolding sprite")
      
    s1 = Sprite(self.rocket, (10,10))
    s2 = Sprite(self.image, (15,15))

    a = App()
    a.run(step)
    
    for i in range(10):
      a._animate(1)


    s1.destroy()
    s2.destroy()

if __name__ == '__main__':
    unittest.main()
