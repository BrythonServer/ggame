from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor

# depends on pixi.js 
PIXI = JSObject(window.PIXI)
PIXI_loader = JSObject(PIXI.loader)


class ImageAsset(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        PIXI_loader.add(name, url)


if __name__ == '__main__':
    bunnyurl = "https://github.com/tiggerntatie/brython-\
server-testing/blob/master/bunny.png?raw=true"
    print("ggame test.")
    asset = ImageAsset('bunny', bunnyurl)
    
