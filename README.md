![automatic build status with Travis](https://travis-ci.org/BrythonServer/ggame.svg?branch=master)

# ggame
The simple cross-platform sprite and game platform for Brython Server (Pygame, Tkinter to follow?).

Ggame stands for a couple of things: "good game" (of course!) and also "git game" or "github game" 
because it is designed to operate with [Brython Server](http://runpython.com) in concert with
Github as a backend file store.

Ggame is **not** intended to be a full-featured gaming API, with every bell and whistle. Ggame is
designed primarily as a tool for teaching computer programming, recognizing that the ability
to create engaging and interactive games is a powerful motivator for many progamming students.
Accordingly, any functional or performance enhancements that *can* be reasonably implemented 
by the user are left as an exercise. 

Please visit the [detailed documentation page for ggame](http://brythonserver.github.io/ggame/). 
This is generated automatically from the ggame sources. 

## Functionality Goals

The ggame library is intended to be trivially easy to use. For example:

```python
from ggame import App, ImageAsset, Sprite

# Create a displayed object at 100,100 using an image asset
Sprite(ImageAsset("ggame/bunny.png"), (100,100))
# Create the app, with a 500x500 pixel stage
app = App(500,500)  
# Run the app
app.run()
```

## Another Example 

The following example illustrates the more common use case in which the basic ggame
classes, Sprite and App, are subclassed as Bunny and DemoApp and given event handlers
and step (i.e. poll) functions.

```python
from ggame import App, ImageAsset, Sprite, MouseEvent
from random import random, randint

class Bunny(Sprite):
    
    asset = ImageAsset("ggame/bunny.png")
    
    def __init__(self, position):
        super().__init__(Bunny.asset, position)
        # register mouse events
        self.app.listenMouseEvent(MouseEvent.mousedown, self.mousedown)
        self.app.listenMouseEvent(MouseEvent.mouseup, self.mouseup)
        self.app.listenMouseEvent(MouseEvent.mousemove, self.mousemove)
        self.dragging = False

    
    def step(self):
        """
        Every now and then a bunny hops...
        """
        if random() < 0.001:
            self.x += randint(-50,50)
            self.y += randint(-50,50)
        
    def mousedown(self, event):
        # capture any mouse down within 50 pixels
        self.deltax = event.x - (self.x + self.width//2) 
        self.deltay = event.y - (self.y + self.height//2)
        if abs(self.deltax) < 50 and abs(self.deltay) < 50:
            self.dragging = True
            # only drag one bunny at a time - consume the event
            event.consumed = True
            
    def mousemove(self, event):
        if self.dragging:
            self.x = event.x - self.deltax - self.width//2
            self.y = event.y - self.deltay - self.height//2
            event.consumed = True
            
    def mouseup(self, event):
        if self.dragging:
            self.dragging = False
            event.consumed = True
            
        
class DemoApp(App):
    
    def __init__(self):
        super().__init__(500, 500)
        for i in range(10):
            Bunny((randint(50,450),randint(50,450)))
        
    def step(self):
        """
        Override step to perform action on each frame update
        """
        for bunny in self.spritelist:
            bunny.step()


# Create the app
app = DemoApp()  
# Run the app
app.run()
```

## Installing ggame

Before using ggame with your Python source repository on Github, you may add the ggame source
tree to your repository. If you are executing your code in http://runpython.com, then the current 
ggame repository is already added to your import search path and no installation is required.
