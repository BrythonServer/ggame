from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor

w = window.open("", "")


# depends on pixi.js 
PIXI = JSObject(window.PIXI)
PIXI_loader = JSObject(PIXI.loader)
PIXI_loader.reset()


PIXI_Texture = JSConstructor(PIXI.Texture)
PIXI_Rectangle = JSConstructor(PIXI.Rectangle)


class Frame(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.PIXI = PIXI_Rectangle(x,y,w,h)
    
    @property
    def center(self):
        return (self.x + self.w//2, self.y + self.h//2)
    
    @center.setter
    def center(self, value):
        c = self.center
        self.x += value[0] - c[0]
        self.y += value[1] - c[1]
        
class ImageAsset(object):
    def __init__(self, url):
        self.url = url
        self.PIXI = PIXI.Texture.fromImage(url, False)

class Sprite(object):
    
    PIXI_Sprite = JSConstructor(PIXI.Sprite)
    
    def __init__(self, asset, position = (0,0), frame = False):
        if (frame):
            self.PIXI = Sprite.PIXI_Sprite(PIXI_Texture(asset.PIXI, frame.PIXI))
        else:
            self.PIXI = Sprite.PIXI_Sprite(asset.PIXI)
        self.position = position
        
    @property
    def position(self):
        return (self.PIXI.position.x, self.PIXI.position.y)
        
    @position.setter
    def position(self, value):
        self.PIXI.position.x = value[0]
        self.PIXI.position.y = value[1]

class App(object):
    
    def __init__(self, size, 

if __name__ == '__main__':
    def animate(fake):
      w.requestAnimationFrame(animate)
      RENDERER.render(STAGE)
    
    bunnyurl = "bunny.png"
    print("ggame test.")
    bunny = ImageAsset(bunnyurl)
    Stage = JSConstructor(PIXI.Container)
    STAGE = Stage()
    RENDERER = PIXI.autoDetectRenderer(1000,650, {'transparent':True})

    #s1 = PIXI_Sprite(PIXI_Texture(bunny.texture, frame))

    frame = Frame(0,0,30,30)
    s = Sprite(bunny, (0,0), frame)
    
    for x in range(50,500,10):
        for y in range(50,500,10):
            STAGE.addChild(Sprite(bunny, (x,y)).PIXI)
    
    
    w.document.body.appendChild(RENDERER.view)
    w.requestAnimationFrame(animate)

