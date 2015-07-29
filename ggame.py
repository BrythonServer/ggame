from browser import window, document
from javascript import JSObject, JSConstructor


# depends on pixi.js, buzz.js
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


class SoundAsset(object):
    
    def __init__(self, url):
        self.url = url

        
class Sound(object):

    def __init__(self, app, asset):
        self.app = app
        self.BUZZ_Sound = JSConstructor(app.BUZZ.sound)
        self.asset = asset
        self.BUZZ = self.BUZZ_Sound(self.asset.url)
        self.BUZZ.load()
        
    def play(self):
        self.stop()
        self.BUZZ.play()

    def loop(self):
        self.stop()
        self.BUZZ.loop()
        self.BUZZ.play()
        
    def stop(self):
        self.BUZZ.stop()
        
    @property
    def volume(self):
        return self.BUZZ.getVolume()
        
    @volume.setter
    def volume(self, value):
        self.BUZZ.setVolume(value)
    

class Event(object):
    
    def __init__(self, hwevent):
        self.hwevent = hwevent
        self.type = hwevent.type
        self.consumed = False
        
class MouseEvent(Event):
    
    mousemove = "mousemove"
    mousedown = "mousedown"
    mouseup = "mouseup"
    click = "click"
    dblclick = "dblclick"
    mousewheel = "wheel"
    
    def __init__(self, hwevent):
        super().__init__(hwevent)
        if self.type == self.mousewheel:
            self.wheelDelta = hwevent.deltaY
        else:
            self.wheelDelta = 0
        self.x = hwevent.clientX
        self.y = hwevent.clientY


class KeyEvent(Event):

    no_location = 0
    right_location = 2
    left_location = 1
    keydown = "keydown"
    keyup = "keyup"
    keypress = "keypress"
    keys = {8: 'backspace',
        9: 'tab',
        13: 'enter',
        16: 'shift',
        17: 'ctrl',
        18: 'alt',
        19: 'pause/break',
        20: 'caps lock',
        27: 'escape',
        32: 'space',
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
        65: 'a',
        66: 'b',
        67: 'c',
        68: 'd',
        69: 'e',
        70: 'f',
        71: 'g',
        72: 'h',
        73: 'i',
        74: 'j',
        75: 'k',
        76: 'l',
        77: 'm',
        78: 'n',
        79: 'o',
        80: 'p',
        81: 'q',
        82: 'r',
        83: 's',
        84: 't',
        85: 'u',
        86: 'v',
        87: 'w',
        88: 'x',
        89: 'y',
        90: 'z',
        91: 'left window key',
        92: 'right window key',
        93: 'select key',
        96: 'numpad 0',
        97: 'numpad 1',
        98: 'numpad 2',
        99: 'numpad 3',
        100: 'numpad 4',
        101: 'numpad 5',
        102: 'numpad 6',
        103: 'numpad 7',
        104: 'numpad 8',
        105: 'numpad 9',
        106: 'multiply',
        107: 'add',
        109: 'subtract',
        110: 'decimal point',
        111: 'divide',
        112: 'f1',
        113: 'f2',
        114: 'f3',
        115: 'f4',
        116: 'f5',
        117: 'f6',
        118: 'f7',
        119: 'f8',
        120: 'f9',
        121: 'f10',
        122: 'f11',
        123: 'f12',
        144: 'num lock',
        145: 'scroll lock',
        186: 'semicolon',
        187: 'equal sign',
        188: 'comma',
        189: 'dash',
        190: 'period',
        191: 'forward slash',
        192: 'grave accent',
        219: 'open bracket',
        220: 'back slash',
        221: 'close bracket',
        222: 'single quote'}    
    
    def __init__(self, hwevent):
        super().__init__(hwevent)
        self.keynum = hwevent.keyCode
        self.key = self.keys[hwevent.keyCode]



class App(object):
    
    def __init__(self, width, height):
        self.w = window.open("", "")
        body = JSObject(self.w.document.body)
        body.children.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/buzz/1.1.10/buzz.min.js"></script>');
        #self.w.document.body.innerHTML = "<script src="https://cdnjs.cloudflare.com/ajax/libs/buzz/1.1.10/buzz.min.js"></script>"
        #self.w.buzz = window.buzz
        self.BUZZ = JSObject(self.w.buzz)
        self.stage = JSConstructor(PIXI.Container)()
        self.renderer = PIXI.autoDetectRenderer(width, height, 
            {'transparent':True})
        self.w.document.body.appendChild(self.renderer.view)
        self.w.document.body.bind(KeyEvent.keydown, self._keyEvent)
        self.w.document.body.bind(KeyEvent.keyup, self._keyEvent)
        self.w.document.body.bind(KeyEvent.keypress, self._keyEvent)
        self.w.document.body.bind(MouseEvent.mousewheel, self._mouseEvent)
        self.w.document.body.bind(MouseEvent.mousemove, self._mouseEvent)
        self.w.document.body.bind(MouseEvent.mousedown, self._mouseEvent)
        self.w.document.body.bind(MouseEvent.mouseup, self._mouseEvent)
        self.w.document.body.bind(MouseEvent.click, self._mouseEvent)
        self.w.document.body.bind(MouseEvent.dblclick, self._mouseEvent)
        self.spritelist = []
        self.eventdict = {}
        
    def _routeEvent(self, event, evtlist):
        for callback in reversed(evtlist):
            if not event.consumed:
                callback(event)
        
    def _keyEvent(self, hwevent):
        evtlist = self.eventdict.get(
            (hwevent.type, KeyEvent.keys.get(hwevent.keyCode,0)), [])
        if len(evtlist) > 0:
            evt = KeyEvent(hwevent)
            self._routeEvent(evt, evtlist)

    def _mouseEvent(self, hwevent):
        evtlist = self.eventdict.get(hwevent.type, [])
        if len(evtlist) > 0:
            evt = MouseEvent(hwevent)
            self._routeEvent(evt, evtlist)
        
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
        
    def listenKeyEvent(self, eventtype, key, callback):
        evtlist = self.eventdict.get((eventtype, key), [])
        evtlist.append(callback)
        self.eventdict[(eventtype, key)] = evtlist

    def listenMouseEvent(self, eventtype, callback):
        evtlist = self.eventdict.get(eventtype, [])
        evtlist.append(callback)
        self.eventdict[eventtype] = evtlist
        
    def unlistenKeyEvent(self, eventtype, key, callback, location = KeyEvent.no_location):
        self.eventdict[(eventtype,key, location)].remove(callback)

    def unlistenMouseEvent(self, eventtype, callback):
        self.eventdict[eventtype].remove(callback)
        
    def step(self):
        pass
    
    def run(self, userfunc = None):
        self.userfunc = userfunc
        self.w.requestAnimationFrame(self._animate)

if __name__ == '__main__':

    class bunnySprite(Sprite):
        
        spring = SoundAsset("spring.wav")

        def __init__(self, app, asset, position = (0,0), frame = False):
            super().__init__(app, asset, position, frame)
            self.app.listenKeyEvent(KeyEvent.keydown, "space", self.spaceKey)
            self.app.listenKeyEvent(KeyEvent.keydown, "left arrow", self.leftKey)
            self.app.listenKeyEvent(KeyEvent.keydown, "right arrow", self.rightKey)
            self.app.listenKeyEvent(KeyEvent.keydown, "up arrow", self.upKey)
            self.app.listenKeyEvent(KeyEvent.keydown, "down arrow", self.downKey)
            self.app.listenKeyEvent(KeyEvent.keyup, "left arrow", self.horizUp)
            self.app.listenKeyEvent(KeyEvent.keyup, "right arrow", self.horizUp)
            self.app.listenKeyEvent(KeyEvent.keyup, "up arrow", self.vertUp)
            self.app.listenKeyEvent(KeyEvent.keyup, "down arrow", self.vertUp)
            self.app.listenMouseEvent(MouseEvent.mousewheel, self.mouse)
            self.app.listenMouseEvent(MouseEvent.click, self.mouseclick)
            self.app.listenMouseEvent(MouseEvent.dblclick, self.doubleclick)
            self.app.listenMouseEvent(MouseEvent.mousemove, self.mousemove)
            self.vx = 0
            self.vy = 0
            self.spring1 = Sound(self.app, self.__class__.spring)
            self.spring2 = Sound(self.app, self.__class__.spring)
            self.spring1.volume = 10
            #self.spring1.loop()
            self.spring2.volume = 90
            
        def mouse(self, event):
            if event.wheelDelta > 0:
                self.spring1.play()
                print("UP")
            elif event.wheelDelta < 0:
                self.spring2.play()
                print("DOWN")
            event.consumed = True
            
        def mouseclick(self, event):
            print("CLICK")
            event.consumed = True
            
        def doubleclick(self, event):
            print("DOUBLE CLICK")
            event.consumed = True
            
        def mousemove(self, event):
            print("MOVE, ", event.x, event.y)
            event.consumed = True
        
        def leftKey(self, event):
            self.vx = -1
            event.consumed = True

        def rightKey(self, event):
            self.vx = 1
            event.consumed = True
            
        def upKey(self, event):
            self.vy = -1
            event.consumed = True
        
        def downKey(self, event):
            self.vy = 1
            event.consumed = True
            
        def horizUp(self, event):
            self.vx = 0
            event.consumed = True
            
        def vertUp(self, event):
            self.vy = 0
            event.consumed = True
        
        def spaceKey(self, event):
            pass
        
        def step(self):
            self.x += self.vx*2
            self.y += self.vy*2

    class myApp(App):
        def __init__(self, width, height):
            super().__init__(width, height)
            grassurl = "grass_texture239.jpg"
            grass = ImageAsset(grassurl)
            Sprite(self, grass, (0,0))
            
            self.bunnies = []
            bunnyurl = "bunny.png"
            bunny = ImageAsset(bunnyurl)
            for x in range(50,500,150):
                for y in range(50,500,150):
                    self.bunnies.append(bunnySprite(self, bunny, (x,y)))
            self.direction = 5
        
        def step(self):
            for s in self.bunnies:
                s.step()
            #for s in self.bunnies:
            #    s.x += self.direction
            #self.direction *= -1

    app = myApp(500, 400)
    
    
    app.run()

