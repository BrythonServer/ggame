from browser import window, document
from random import randint
from javascript import JSObject, JSConstructor


# depends on pixi.js 
PIXI = JSObject(window.PIXI)


class Frame(object):

    PIXI_Rectangle = JSConstructor(PIXI.Rectangle)

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.PIXI = Frame.PIXI_Rectangle(x,y,w,h)
    
    @property
    def center(self):
        return (self.x + self.w//2, self.y + self.h//2)
    
    @center.setter
    def center(self, value):
        c = self.center
        self.x += value[0] - c[0]
        self.y += value[1] - c[1]

        
class ImageAsset(object):

    PIXI_Texture = JSObject(PIXI.Texture)
    PIXI_Texture_fromImage = JSConstructor(PIXI_Texture.fromImage)
    
    def __init__(self, url):
        self.url = url
        self.PIXI = ImageAsset.PIXI_Texture_fromImage(url, False)

class Sprite(object):
    
    PIXI_Sprite = JSConstructor(PIXI.Sprite)
    
    def __init__(self, app, asset, position = (0,0), frame = False):
        if (frame):
            self.PIXI = Sprite.PIXI_Sprite(
                ImageAsset.PIXI_Texture(asset.PIXI, frame.PIXI))
        else:
            self.PIXI = Sprite.PIXI_Sprite(asset.PIXI)
        self.position = position
        self.app = app
        self.app._add(self)
        
    @property
    def x(self):
        return self.PIXI.position.x
        
    @x.setter
    def x(self, value):
        self.PIXI.position.x = value
        
    @property
    def y(self):
        return self.PIXI.position.y
        
    @y.setter
    def y(self, value):
        self.PIXI.position.y = value
        
    @property
    def position(self):
        return (self.PIXI.position.x, self.PIXI.position.y)
        
    @position.setter
    def position(self, value):
        self.PIXI.position.x = value[0]
        self.PIXI.position.y = value[1]

    def destroy(self):
        self.app._remove(self)

class Event(object):
    
    keys = {8: 'backspace',
        9: 'tab',
        13: 'enter',
        16: 'shift',
        17: 'ctrl',
        18: 'alt',
        19: 'pause/break',
        20: 'caps lock',
        27: 'escape',
        33: 'page up',
        34: 'page down',
        35: 'end',
        36: 'home',
        37: 'left arrow',
        38: 'up arrow',
        39: 'right arrow',
        40: 'down arrow',
        45: 'insert',
        46: 'delete',
        48: '0',
        49: '1',
        50: '2',
        51: '3',
        52: '4',
        53: '5',
        54: '6',
        55: '7',
        56: '8',
        57: '9',
        a	65
b	66
c	67
d	68
 	
Key	Code
e	69
f	70
g	71
h	72
i	73
j	74
k	75
l	76
m	77
n	78
o	79
p	80
q	81
r	82
s	83
t	84
u	85
v	86
w	87
x	88
y	89
z	90
left window key	91
right window key	92
select key	93
numpad 0	96
numpad 1	97
numpad 2	98
numpad 3	99
numpad 4	100
numpad 5	101
numpad 6	102
numpad 7	103
 	
Key	Code
numpad 8	104
numpad 9	105
multiply	106
add	107
subtract	109
decimal point	110
divide	111
f1	112
f2	113
f3	114
f4	115
f5	116
f6	117
f7	118
f8	119
f9	120
f10	121
f11	122
f12	123
num lock	144
scroll lock	145
semi-colon	186
equal sign	187
comma	188
dash	189
period	190
forward slash	191
grave accent	192
open bracket	219
back slash	220
close braket	221
single quote	222
    
    def __init__(self, hwevent):
        self.hwevent = hwevent


class App(object):
    
    def __init__(self, width, height):
        self.w = window.open("", "")
        self.stage = JSConstructor(PIXI.Container)()
        self.renderer = PIXI.autoDetectRenderer(width, height, 
            {'transparent':True})
        self.w.document.body.appendChild(self.renderer.view)
        self.w.document.body.bind('keydown', self._keyDown)
        self.w.document.body.bind('mousedown', self._mouseDown)
        self.spritelist = []
        
    def _keyDown(self, hwevent):
        print("keyDown: ", hwevent.keyCode, hwevent.keyIdentifier, hwevent.keyLocation, dir(hwevent))
        
    def _mouseDown(self, hwevent):
        print("mouseDown: ", hwevent.x, hwevent.y)
        
    def _add(self, obj):
        self.stage.addChild(obj.PIXI)
        self.spritelist.append(obj)
        
    def _remove(self, obj):
        self.stage.removeChild(obj.PIXI)
        self.spritelist.remove(obj)
        
    def _animate(self, dummy):
        if self.userfunc:
            self.userfunc()
        else:
            self.step()
        self.renderer.render(self.stage)
        self.w.requestAnimationFrame(self._animate)
        
    def step(self):
        pass
    
    def run(self, userfunc = None):
        self.userfunc = userfunc
        self.w.requestAnimationFrame(self._animate)

if __name__ == '__main__':

    class myApp(App):
        def __init__(self, width, height):
            super().__init__(width, height)
            grassurl = "grass_texture239.jpg"
            grass = ImageAsset(grassurl)
            Sprite(self, grass, (0,0))
            
            self.bunnies = []
            bunnyurl = "bunny.png"
            bunny = ImageAsset(bunnyurl)
            for x in range(50,1000,150):
                for y in range(50,1000,150):
                    self.bunnies.append(Sprite(self, bunny, (x,y)))
            self.direction = 5
        
        def step(self):
            for s in self.bunnies:
                s.x += self.direction
            self.direction *= -1

    app = myApp(1000, 700)
    
    
    app.run()

