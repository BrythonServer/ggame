from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor

w = window.open("", "")


# depends on pixi.js 
PIXI = JSObject(window.PIXI)
PIXI_loader = JSObject(PIXI.loader)
PIXI_loader.reset()

Sprite = JSConstructor(PIXI.Sprite)

def loadComplete(ev):
    print("loaded asset!")

class ImageAsset(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        PIXI_loader.add(name, url)
        PIXI_loader.on('complete', self.loadComplete)
        PIXI_loader.load()

    def loadComplete(self, ev):
        print("loaded asset!")



if __name__ == '__main__':
    bunnyurl = "bunny.png"
    print("ggame test.")
    asset = ImageAsset('bunny', bunnyurl)
    STAGE = Stage()
    RENDERER = PIXI.autoDetectRenderer(1000,650, {'transparent':True})
    stage.addChild(Sprite.fromImage(bunnyurl))
    w.document.body.appendChild(RENDERER.view)
    RENDERER.render(STAGE)    
