import unittest
from ggame import Frame

class TestFrameMethods(unittest.TestCase):

  def test_frame(self):
    f1 = Frame(10, 20, 30, 40)
    self.assertEqual(f1.x, 10)
    self.assertEqual(f1.y, 20)
    self.assertEqual(f1.w, 30)
    self.assertEqual(f1.h, 40)
    self.assertEqual(f1.center, (25, 40))
    f1.center = (15,30)
    self.assertEqual(f1.x, 0)
    self.assertEqual(f1.y, 10)
    self.assertEqual(f1.w, 30)
    self.assertEqual(f1.h, 40)
    self.assertEqual(f1.center, (15, 30))


if __name__ == '__main__':
    unittest.main()
