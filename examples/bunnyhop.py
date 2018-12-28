"""
Example of a simple ggame-based application.
"""
from random import random, randint
from ggame import App, ImageAsset, Sprite, MouseEvent


class Bunny(Sprite):
    """
    Sprite-based class representing an image of a bunny rabbit.

    :param (float,float) position: The screen coordinates of the new rabbit.
    """

    asset = ImageAsset("bunny.png")

    def __init__(self, position):
        super().__init__(Bunny.asset, position)
        # register mouse events
        App.listenMouseEvent(MouseEvent.mousedown, self.mousedown)
        App.listenMouseEvent(MouseEvent.mouseup, self.mouseup)
        App.listenMouseEvent(MouseEvent.mousemove, self.mousemove)
        self.dragging = False
        self.deltax = self.deltay = 0

    def step(self):
        """
        Every now and then a bunny hops...
        """
        if random() < 0.01:
            self.x += randint(-20, 20)
            self.y += randint(-20, 20)

    def mousedown(self, event):
        """
        Capture any mouse down event within 50 pixels of a rabbit.
        """
        self.deltax = event.x - (self.x + self.width // 2)
        self.deltay = event.y - (self.y + self.height // 2)
        if abs(self.deltax) < 50 and abs(self.deltay) < 50:
            self.dragging = True
            # only drag one bunny at a time - consume the event
            event.consumed = True

    def mousemove(self, event):
        """
        Capture any mouse move event following a mouse down event (dragging).
        """
        if self.dragging:
            self.x = event.x - self.deltax - self.width // 2
            self.y = event.y - self.deltay - self.height // 2
            event.consumed = True

    def mouseup(self, event):
        """
        Capture any mouse up event to finish a dragging action.
        """
        if self.dragging:
            self.dragging = False
            event.consumed = True


class DemoApp(App):
    """
    Subclass of App, creates a herd of rabbit sprites and services their step
    function.
    """

    def __init__(self):
        super().__init__()
        for dummy in range(10):
            Bunny((randint(50, self.width), randint(50, self.height)))

    def step(self):
        """
        Override step to perform action on each frame update
        """
        for bunny in self.spritelist:
            bunny.step()


# Create the app
APP = DemoApp()
# Run the app
APP.run()
