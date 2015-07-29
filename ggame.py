from browser import window, document
from javascript import JSObject, JSConstructor


# depends on pixi.js, buzz.js



class Frame(object):


    def __init__(self, app, x, y, w, h):
        self.app = app
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.PIXI = app.PIXI_Rectangle(x,y,w,h)
    
    @property
    def center(self):
        return (self.x + self.w//2, self.y + self.h//2)
    
    @center.setter
    def center(self, value):
        c = self.center
        self.x += value[0] - c[0]
        self.y += value[1] - c[1]

        
class ImageAsset(object):

    def __init__(self, app, url):
        self.app = app
        self.url = url
        self.PIXI = self.app.PIXI_Texture_fromImage(url, False)

class Color(object):

    def __init__(self, color, alpha):
        """
        color : integer e.g. 0xffff00
        alpha : float 0-1
        
        """
        self.color = color
        self.alpha = alpha
        

class LineStyle(object):
    
    def __init__(self, width, color):
        """
        width : line width pixels
        color : integer e.g. 0xffff00
        alpha : float 0-1
        
        """
        self.width = width
        self.color = color

class GraphicsAsset(object):
    
    def cleanup(self):
        self.PIXI.destroy()

class CurveAsset(GraphicsAsset):

    def __init__(self, app, line):
        self.app = app
        self.app.PIXI_Graphics.lineStyle(line.width, line.color.color, line.color.alpha)

class ShapeAsset(CurveAsset):

    def __init__(self, app, line, fill):
        super().__init__(app, line)
        self.app.PIXI_Graphics.beginFill(fill.color, fill.alpha)
    

class RectangleAsset(ShapeAsset):

    def __init__(self, app, width, height, line, fill):
        super().__init__(app, line, fill)
        self.width = width
        self.height = height
        self.PIXI = self.app.PIXI_Graphics.drawRect(0, 0, self.width, self.height)
        self.PIXI.visible = False
        

class CircleAsset(ShapeAsset):

    def __init__(self, app, radius, line, fill):
        super().__init__(app, line, fill)
        self.radius = radius
        self.PIXI = self.app.PIXI_Graphics.drawCircle(0, 0, self.radius)
        self.PIXI.visible = False
        
class EllipseAsset(ShapeAsset):

    def __init__(self, app, halfw, halfh, line, fill):
        super().__init__(app, line, fill)
        self.halfw = halfw
        self.halfh = halfh
        self.PIXI = self.app.PIXI_Graphics.drawEllipse(0, 0, self.halfw, self.halfh)
        self.PIXI.visible = False
        
class PolygonAsset(ShapeAsset):

    def __init__(self, app, path, line, fill):
        super().__init__(app, line, fill)
        self.path = path
        jpath = []
        for point in self.path:
            jpath.extend(point)
        self.PIXI = self.app.PIXI_Graphics.drawPolygon(jpath)
        self.PIXI.visible = False
    

class LineAsset(CurveAsset):
    
    def __init__(self, app, x, y, line):
        super().__init__(app, line)
        self.deltaX = x
        self.deltaY = y
        self.app.PIXI_Graphics.moveTo(0, 0)
        self.PIXI = self.app.PIXI_Graphics.lineTo(self.deltaX, self.deltaY)

class TextAsset(GraphicsAsset):
    
    def __init__(self, app, text, **kwargs):
        """
        app : the App reference
        text : text to display
        style = : default "20px Arial", e.g. "italic 20pt Helvetica"
        width = : width of text area (pixels), default 100
        fill = : color of text, default black
        align = : align style, default "left". "left", "center", "right"

        """

        self.app = app
        self.text = text
        self.style = kwargs.get('style', '20px Arial')
        self.width = kwargs.get('width', 100)
        self.fill = kwargs.get('fill', Color(0, 1))
        self.align = kwargs.get('align', 'left')
        self.PIXI = self.app.PIXI_Text(self.text, 
            {'font': self.style,
                'fill' : self.fill.color,
                'align' : self.align,
                'wordWrap' : True,
                'wordWrapWidth' : self.width,
                })
        self.PIXI.alpha = self.fill.alpha
        self.PIXI.visible = False
        
    def clone(self):
        return type(self)(self.app,
            self.text,
            style = self.style,
            width = self.width,
            fill = self.fill,
            align = self.align)


class Sprite(object):
    
    
    def __init__(self, asset, position = (0,0), frame = False):
        self.app = asset.app
        if type(asset) == ImageAsset:
            self.asset = asset
            if (frame):
                self.PIXI = self.app.PIXI_Sprite(
                    self.app.PIXI_Texture(asset.PIXI, frame.PIXI))
            else:
                self.PIXI = self.app.PIXI_Sprite(asset.PIXI)
        elif type(asset) in [RectangleAsset, 
            CircleAsset, 
            EllipseAsset, 
            PolygonAsset,
            LineAsset,
            ]:
            self.asset = asset
            self.PIXI = asset.PIXI.clone()
            self.PIXI.visible = True
        elif type(asset) in [TextAsset]:
            self.asset = asset.clone()
            self.PIXI = self.asset.PIXI
            self.PIXI.visible = True
        self.position = position
        self.app._add(self)
        
    @property
    def width(self):
        return self.PIXI.width
        
    @property
    def height(self):
        return self.PIXI.height
        
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
        
    @property
    def visible(self):
        return self.PIXI.visible
    
    @visible.setter
    def visible(self, value):
        self.PIXI.visible = value

    def cleanup(self):
        self.app._remove(self)
        self.asset.cleanup()


class SoundAsset(object):
    
    def __init__(self, app, url):
        self.app = app
        self.url = url

        
class Sound(object):

    def __init__(self, asset):
        self.asset = asset
        self.app = self.asset.app
        self.BUZZ_Sound = JSConstructor(self.app.BUZZ.sound)
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
        self.PIXI = JSObject(window.PIXI)
        self.PIXI_Rectangle = JSConstructor(self.PIXI.Rectangle)
        self.PIXI_Texture = JSObject(self.PIXI.Texture)
        self.PIXI_Texture_fromImage = JSConstructor(self.PIXI_Texture.fromImage)
        self.PIXI_Sprite = JSConstructor(self.PIXI.Sprite)
        self.PIXI_Graphics = JSConstructor(self.PIXI.Graphics)()
        self.PIXI_Text = JSConstructor(self.PIXI.Text)
        self.BUZZ = JSObject(window.buzz)
        self.w = window.open("", "")
        self.w.onunload = self.cleanup
        self.stage = JSConstructor(self.PIXI.Container)()
        self.renderer = self.PIXI.autoDetectRenderer(width, height, 
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
        evtlist.extend(self.eventdict.get((hwevent.type, '*'), []))
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

    def cleanup(self, dummy):
        self.BUZZ.all().stop()
        self.stage.destroy()

    def listenKeyEvent(self, eventtype, key, callback):
        """
        eventtype : "keydown", "keyup", "keypress"
        key : e.g. "space", "a" or "*" for ALL!
        callback : function name to receive events
        
        """
        evtlist = self.eventdict.get((eventtype, key), [])
        evtlist.append(callback)
        self.eventdict[(eventtype, key)] = evtlist

    def listenMouseEvent(self, eventtype, callback):
        evtlist = self.eventdict.get(eventtype, [])
        evtlist.append(callback)
        self.eventdict[eventtype] = evtlist
        
    def unlistenKeyEvent(self, eventtype, key, callback):
        self.eventdict[(eventtype,key)].remove(callback)

    def unlistenMouseEvent(self, eventtype, callback):
        self.eventdict[eventtype].remove(callback)
        
    def step(self):
        pass
    
    def run(self, userfunc = None):
        self.userfunc = userfunc
        self.w.requestAnimationFrame(self._animate)

if __name__ == '__main__':

    class bunnySprite(Sprite):

        def __init__(self, asset, position = (0,0), frame = False):
            super().__init__(asset, position, frame)
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
            
        def mouse(self, event):
            if event.wheelDelta > 0:
                self.spring1.play()
            elif event.wheelDelta < 0:
                self.spring2.play()
            event.consumed = True
            
        def mouseclick(self, event):
            event.consumed = True
            
        def doubleclick(self, event):
            event.consumed = True
            
        def mousemove(self, event):
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
            grass = ImageAsset(self, grassurl)
            Sprite(grass, (0,0))
            
            self.bunnies = []
            bunnyurl = "bunny.png"
            bunny = ImageAsset(self, bunnyurl)
            
            fcolor = Color(0x5050ff, 0.8)
            lcolor = Color(0, 1)
            line = LineStyle(3, lcolor)
            #rect = RectangleAsset(self, 100, 150, line, fcolor)
            #circ = CircleAsset(self, 50, line, fcolor)
            #ell = EllipseAsset(self, 50, 75, line, fcolor)
            #poly = PolygonAsset(self, [(0,0), (50,50), (50,100), (0,0)], line, fcolor)
            #line = LineAsset(self, -50, 75, line)
            text = TextAsset(self, "what up? big long text string!")
            
            
            for x in range(50,500,150):
                for y in range(50,500,150):
                    self.bunnies.append(bunnySprite(text, (x,y)))
            self.direction = 5
            self.spring = SoundAsset(self, "spring.wav")
            self.springsound =Sound(self.spring)
            self.springsound.loop()
            

        def step(self):
            for s in self.bunnies:
                s.step()

            #for s in self.bunnies:
            #    s.x += self.direction
            #self.direction *= -1

    app = myApp(500, 400)
    
    
    app.run()

