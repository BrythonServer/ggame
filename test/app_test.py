import unittest
from ggame import App, KeyEvent, MouseEvent



class keyevent(object):
  def __init__(self, ktype, code):
    self.keyCode = code
    self.type = ktype

class mouseevent(object):
  def __init__(self, etype, x, y, value):
    self.type = etype
    self.clientX = x
    self.clientY = y
    self.deltaY = value

class TestAppMethods(unittest.TestCase):

  def __init__(self, arg):
    super().__init__(arg)
    self.keyevtx = 0
    self.mouseevtx = 0

  def test_app(self):
    a3 = App(100,100)
    # event handling
    a3.listenKeyEvent(KeyEvent.keydown, "space", self.spacehandler)
    a3.listenMouseEvent(MouseEvent.mousewheel, self.wheelhandler)
    key = keyevent('keydown', 32)
    a3._keyEvent(key)
    mouse = mouseevent('wheel', 1, 2, 99)
    a3._mouseEvent(mouse)
    # confirm no events after unlisten
    a3.unlistenKeyEvent(KeyEvent.keydown, "space", self.spacehandler)
    a3.unlistenMouseEvent(MouseEvent.mousewheel, self.wheelhandler)
    a3._keyEvent(key)
    a3._mouseEvent(mouse)
    # assert that each handler was executed only once
    self.assertEqual(self.keyevtx, 1)
    self.assertEqual(self.mouseevtx, 1)
    # run the app
    a3.run()
    # and destroy it
    a3.destroy()

  def spacehandler(self, event):
    self.assertEqual(type(event), KeyEvent)
    self.keyevtx += 1

  def wheelhandler(self, event):
    self.assertEqual(type(event), MouseEvent)
    self.assertEqual(event.wheelDelta, 99)
    self.mouseevtx += 1

if __name__ == '__main__':
    unittest.main()
