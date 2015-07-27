from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor

w = window.open("", "")


# depends on pixi.js 
PIXI = JSObject(window.PIXI)
PIXI_loader = JSObject(PIXI.loader)
PIXI_loader.reset()

Sprite = JSConstructor(PIXI.Sprite)
PIXI_Texture = JSConstructor(PIXI.Texture)
PIXI_Rectangle = JSConstructor(PIXI.Rectangle)


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
    Stage = JSConstructor(PIXI.Container)
    STAGE = Stage()
    RENDERER = PIXI.autoDetectRenderer(1000,650, {'transparent':True})
    s = Sprite(bunny.texture)
    frame = PIXI_Rectangle(0,0,30,30)


    s1 = Sprite(PIXI_Texture(bunny.texture, frame))
    STAGE.addChild(s1)
    w.document.body.appendChild(RENDERER.view)
    w.requestAnimationFrame(animate)

    print(crop.x, crop.y, crop.width, crop.height)
    print(frame.x, frame.y, frame.width, frame.height)