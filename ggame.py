from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor

# depends on pixi.js 
PIXI = JSObject(window.PIXI)
PIXI_ImageLoader = JSConstructor(PIXI.ImageLoader)


class ImageAsset(object):
    def __init__(self, url):
        self.url = url
        PIXI_ImageLoader(url, False)


if __name__ == '__main__':
    bunnyurl = "https://github.com/tiggerntatie/brython-\
server-testing/blob/master/bunny.png?raw=true"
    print("ggame test.")
    asset = ImageAsset(bunnyurl)
    
