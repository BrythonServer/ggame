from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor

w = window.open("", "")


# depends on pixi.js 
PIXI = JSObject(window.PIXI)
PIXI_loader = JSObject(PIXI.loader)
PIXI_loader.reset()

Sprite = JSConstructor(PIXI.Sprite)


class ImageAsset(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.texture = PIXI.Texture.fromImage(url, False)



if __name__ == '__main__':
    def animate(fake):
      w.requestAnimationFrame(animate)
      RENDERER.render(STAGE)
    
    bunnyurl = "bunny.png"
    print("ggame test.")
    bunny = ImageAsset('bunny', bunnyurl)
    print(dir(bunny.texture))
    print(bunny.texture.baseTexture)
    Stage = JSConstructor(PIXI.Container)
    STAGE = Stage()
    RENDERER = PIXI.autoDetectRenderer(1000,650, {'transparent':True})
    s = Sprite(bunny.texture)
    s1 = Sprite(bunny.texture)
    STAGE.addChild(s1)
    w.document.body.appendChild(RENDERER.view)
    w.requestAnimationFrame(animate)
