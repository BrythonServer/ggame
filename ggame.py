from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor

# depends on pixi.js 
PIXI = JSObject(window.PIXI)
PIXI_loader = JSObject(PIXI.loader)
PIXI_loader.reset()

def loadComplete():
    print("loaded asset!")

class ImageAsset(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        PIXI_loader.add(name, url)
        PIXI_loader.load(self.loadComplete)
    
    def loadComplete(self):
        print("loaded asset!")

if __name__ == '__main__':
    bunnyurl = "bunny.png"
    print("ggame test.")
    asset = ImageAsset('bunny', bunnyurl)
    
