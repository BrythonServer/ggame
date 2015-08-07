from ggame.sysdeps import *

class Frame(object):


    def __init__(self, x, y, w, h):
        self.GFX = GFX_Rectangle(x,y,w,h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    @property
    def x(self):
        return self.GFX.x
    
    @x.setter
    def x(self, value):
        self.GFX.x = value
        
    @property
    def y(self):
        return self.GFX.y
    
    @y.setter
    def y(self, value):
        self.GFX.y = value
    
    @property
    def w(self):
        return self.GFX.width
    
    @w.setter
    def w(self, value):
        self.GFX.width = value
        
    @property
    def h(self):
        return self.GFX.height
        
    @h.setter
    def h(self, value):
        self.GFX.height = value
    
    @property
    def center(self):
        return (self.x + self.w//2, self.y + self.h//2)
    
    @center.setter
    def center(self, value):
        c = self.center
        self.x += value[0] - c[0]
        self.y += value[1] - c[1]

class Asset(object):

    def __init__(self):
        self.index = 0
        self.GFXlist = [None,]

    @property
    def GFX(self):
        return self.GFXlist[0]
        
    @GFX.setter
    def GFX(self, value):
        self.GFXlist[0] = value
        
    def __len__(self):
        return len(self.GFXlist)
        
    def __getitem__(self, key):
        return self.GFXlist[key]
        
    def __setitem__(self, key, value):
        self.GFXlist[key] = value
        
    def __iter__(self):
        class Iter():
            def __init__(self, image):
                self.obj = image
                self.n = len(image.GFXlist)
                self.i = 0
                
            def __iter__(self):
                return self
                
            def __next__(self):
                if self.i ==self.n:
                    raise StopIteration
                self.i += 1
                return self.obj.GFXlist[self.i]
        return Iter(self)

    def destroy(self):
        if hasattr(self, 'GFX'):
            try:
                for gfx in self.GFXlist:
                    try:
                        gfx.destroy(True)
                    except:
                        pass
            except:
                pass
        
        
class ImageAsset(Asset):

    def __init__(self, url, frame=None, qty=1, direction='horizontal', margin=0):
        """
        Create a texture asset from an image file name (or URL)
        url : the name of the file
        frame : a frame that defines a region inside the image (if desired)
        qty : a string of qty frames may be defined for animation purposes
        direction : 'horizontal' or 'vertical' orientation of animation frames
        margin : the number of pixels between frames, if any
        """
        super().__init__()
        self.url = url
        del self.GFXlist[0]
        self.append(url, frame, qty, direction, margin)

    def _subframe(self, texture, frame):
        return GFX_Texture(texture, frame.GFX)
        
    def append(self, url, frame=None, qty=1, direction='horizontal', margin=0):
        """
        Append a texture asset from an image file name (or URL)
        url : the name of the file
        frame : a frame that defines a region inside the image (if desired)
        qty : a string of qty frames may be defined for animation purposes
        direction : 'horizontal' or 'vertical' orientation of animation frames
        margin : the number of pixels between frames, if any
        """
        GFX = GFX_Texture_fromImage(url, False)
        dx = 0
        dy = 0
        for i in range(qty):
            if not frame is None:
                if direction == 'horizontal':
                    dx = frame.w + margin
                elif direction == 'vertical':
                    dy = frame.h + margin
                f = Frame(frame.x + dx * i, frame.y + dy * i, frame.w, frame.h)
                GFX = self._subframe(GFX, f)
            self.GFXlist.append(GFX)


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
        """
        self.width = width
        self.color = color

class GraphicsAsset(Asset):
    
    def __init__(self):
        super().__init__()
        GFX_Graphics.clear()
        

class CurveAsset(GraphicsAsset):

    def __init__(self, line):
        super().__init__()
        GFX_Graphics.lineStyle(line.width, line.color.color, line.color.alpha)

class ShapeAsset(CurveAsset):

    def __init__(self, line, fill):
        super().__init__(line)
        GFX_Graphics.beginFill(fill.color, fill.alpha)
    

class RectangleAsset(ShapeAsset):

    def __init__(self, width, height, line, fill):
        super().__init__(line, fill)
        self.width = width
        self.height = height
        self.GFX = GFX_Graphics.drawRect(0, 0, self.width, self.height).clone()
        self.GFX.visible = False
        

class CircleAsset(ShapeAsset):

    def __init__(self, radius, line, fill):
        super().__init__(line, fill)
        self.radius = radius
        self.GFX = GFX_Graphics.drawCircle(0, 0, self.radius).clone()
        self.GFX.visible = False
        
class EllipseAsset(ShapeAsset):

    def __init__(self, halfw, halfh, line, fill):
        super().__init__(line, fill)
        self.halfw = halfw
        self.halfh = halfh
        self.GFX = GFX_Graphics.drawEllipse(0, 0, self.halfw, self.halfh).clone()
        self.GFX.visible = False
        
class PolygonAsset(ShapeAsset):

    def __init__(self, path, line, fill):
        super().__init__(line, fill)
        self.path = path
        jpath = []
        for point in self.path:
            jpath.extend(point)
        self.GFX = GFX_Graphics.drawPolygon(jpath).clone()
        self.GFX.visible = False
    

class LineAsset(CurveAsset):
    
    def __init__(self, x, y, line):
        super().__init__(line)
        self.deltaX = x
        self.deltaY = y
        GFX_Graphics.moveTo(0, 0)
        self.GFX = GFX_Graphics.lineTo(self.deltaX, self.deltaY).clone()
        self.GFX.visible = False

class TextAsset(GraphicsAsset):
    
    def __init__(self, text, **kwargs):
        """
        app : the App reference
        text : text to display
        style = : default "20px Arial", e.g. "italic 20pt Helvetica"
        width = : width of text area (pixels), default 100
        fill = : color of text, default black
        align = : align style, default "left". "left", "center", "right"

        """
        super().__init__()
        self.text = text
        self.style = kwargs.get('style', '20px Arial')
        self.width = kwargs.get('width', 100)
        self.fill = kwargs.get('fill', Color(0, 1))
        self.align = kwargs.get('align', 'left')
        self.GFX = GFX_Text(self.text, 
            {'font': self.style,
                'fill' : self.fill.color,
                'align' : self.align,
                'wordWrap' : True,
                'wordWrapWidth' : self.width,
                })
        self.GFX.alpha = self.fill.alpha
        self.GFX.visible = False
        
    def clone(self):
        return type(self)(self.text,
            style = self.style,
            width = self.width,
            fill = self.fill,
            align = self.align)


class Sprite(object):
    
    _rectCollision = "rect"
    _circCollision = "circ"
    
    def __init__(self, asset, pos=(0,0)):
        """
        asset: an image or graphics asset instance
        pos: keyward parameter, a tuple with x,y coordinates
        e.g. Sprite(asset, pos=(100,100))
        """
        self.index = 0
        if type(asset) == ImageAsset:
            self.asset = asset
            try:
                #self.GFX = GFX_Sprite()
                self.GFX = GFX_Sprite(asset.GFX) # GFX is PIXI Sprite
            except:
                self.GFX = None
        elif type(asset) in [RectangleAsset, 
            CircleAsset, 
            EllipseAsset, 
            PolygonAsset,
            LineAsset,
            ]:
            self.asset = asset
            self.GFX = asset.GFX.clone() # GFX is PIXI Graphics (from Sprite)
            self.GFX.visible = True
        elif type(asset) in [TextAsset]:
            self.asset = asset.clone()
            self.GFX = self.asset.GFX # GFX is PIXI Text (from Sprite)
            self.GFX.visible = True
        self.position = pos
        self._setExtents()
        self.rectangularCollisionModel()
        App._add(self)
        
    def _setExtents(self):
        """
        update min/max x and y based on position, center, width, height
        """
        self.xmin = int(self.x - self.fxcenter * self.width)
        self.xmax = int(self.x + (1 - self.fxcenter) * self.width)
        self.ymin = int(self.y - self.fycenter * self.height)
        self.ymax = int(self.y + (1 - self.fycenter) * self.height)
        self.radius = int((self.width + self.height)/4)
        #self.xcenter = int(self.x + (1 - self.fxcenter) * self.width / 2)
        #self.ycenter = int(self.y + (1 - self.fycenter) * self.height / 2)

    def firstImage(self):
        self.GFX.texture = self.asset[0]
    
    def lastImage(self):
        self.GFX.texture = self.asset[-1]
    
    def nextImage(self, wrap = False):
        self.index += 1
        if self.index >= len(self.asset):
            if wrap:
                self.index = 0
            else:
                self.index = len(self.asset)-1
        self.GFX.texture = self.asset[self.index]
    
    def prevImage(self, wreap = False):
        self.index -= 1
        if self.index < 0:
            if wrap:
                self.index = len(self.asset)-1
            else:
                self.index = 0
        self.GFX.texture = self.asset[self.index]
    
    def setImage(self, index=0):
        self.index = index
        self.GFX.texture = self.asset[self.index]

    def rectangularCollisionModel(self):
        self._collisionStyle = type(self)._rectCollision

    def circularCollisionModel(self):
        self._collisionStyle = type(self)._circCollision
        

    @property
    def width(self):
        return self.GFX.width
        
    @width.setter
    def width(self, value):
        self.GFX.width = value
        self._setExtents()
    
    @property
    def height(self):
        return self.GFX.height
    
    @height.setter
    def height(self, value):
        self.GFX.height = value
        self._setExtents()
        
    @property
    def x(self):
        return self.GFX.position.x
        
    @x.setter
    def x(self, value):
        self.GFX.position.x = value
        self._setExtents()
        
    @property
    def y(self):
        return self.GFX.position.y
        
    @y.setter
    def y(self, value):
        self.GFX.position.y = value
        self._setExtents()
    
    @property
    def position(self):
        return (self.GFX.position.x, self.GFX.position.y)
        
    @position.setter
    def position(self, value):
        self.GFX.position.x = value[0]
        self.GFX.position.y = value[1]
        self._setExtents()
        
    @property
    def fxcenter(self):
        """
        Float: 0-1
        """
        try:
            return self.GFX.anchor.x
            self._setExtents()
        except:
            return 0.0
        
    @fxcenter.setter
    def fxcenter(self, value):
        """
        Float: 0-1
        """
        try:
            self.GFX.anchor.x = value
            self._setExtents()
        except:
            pass
        
    @property
    def fycenter(self):
        """
        Float: 0-1
        """
        try:
            return self.GFX.anchor.y
        except:
            return 0.0
        
    @fycenter.setter
    def fycenter(self, value):
        """
        Float: 0-1
        """
        try:
            self.GFX.anchor.y = value
            self._setExtents()
        except:
            pass
    
    @property
    def center(self):
        try:
            return (self.GFX.anchor.x, self.GFX.anchor.y)
        except:
            return (0.0, 0.0)
        
    @center.setter
    def center(self, value):
        try:
            self.GFX.anchor.x = value[0]
            self.GFX.anchor.y = value[1]
            self._setExtents()
        except:
            pass
    
    @property
    def visible(self):
        return self.GFX.visible
    
    @visible.setter
    def visible(self, value):
        self.GFX.visible = value

    @property
    def scale(self):
        return self.GFX.scale.x
        
    @scale.setter
    def scale(self, value):
        self.GFX.scale.x = value
        self.GFX.scale.y = value
        self._setExtents()

    @property
    def rotation(self):
        return self.GFX.rotation
        
    @rotation.setter
    def rotation(self, value):
        self.GFX.rotation = value

    def collidingWith(self, obj):
        """
        Very simple: does not work well with rotated sprites!
        """
        if self is obj:
            return False
        elif self._collisionStyle == obj._collisionStyle == type(self)._circCollision:
            dist2 = (self.x - obj.x)**2 + (self.y - obj.y)**2
            return dist2 < (self.radius + obj.radius)**2
        else:
            return (not (self.xmin > obj.xmax
                or self.xmax < obj.xmin
                or self.ymin > obj.ymax
                or self.ymax < obj.ymin))

    def collidingWithSprites(self, sclass = None):
        if sclass is None:
            slist = App.spritelist
        else:
            slist = App.getSpritesbyClass(sclass)
        return list(filter(self.collidingWith, slist))

    def destroy(self):
        App._remove(self)
        self.GFX.destroy()


class SoundAsset(object):
    
    def __init__(self, url):
        self.url = url

        
class Sound(object):

    def __init__(self, asset):
        self.asset = asset
        self.SND = SND_Sound(self.asset.url)
        self.SND.load()
        
    def play(self):
        self.stop()
        self.SND.play()

    def loop(self):
        self.stop()
        self.SND.loop()
        self.SND.play()
        
    def stop(self):
        self.SND.stop()
        
    @property
    def volume(self):
        return self.SND.getVolume()
        
    @volume.setter
    def volume(self, value):
        self.SND.setVolume(value)
    

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

    spritelist = []
    eventdict = {}
    spritesdict = {}
    spritesadded = False
    win = None

    def __init__(self, *args):

        if App.win == None and len(args) == 2:
            App.win = GFX_Window(args[0], args[1], self.destroy)
            self.width = App.win.width
            self.height = App.win.height
            # Add existing sprites to the window
            if not App.spritesadded and len(App.spritelist) > 0:
                App.spritesadded = True
                for sprite in App.spritelist:
                    App.win.add(sprite.GFX)
            App.win.bind(KeyEvent.keydown, self._keyEvent)
            App.win.bind(KeyEvent.keyup, self._keyEvent)
            App.win.bind(KeyEvent.keypress, self._keyEvent)
            App.win.bind(MouseEvent.mousewheel, self._mouseEvent)
            App.win.bind(MouseEvent.mousemove, self._mouseEvent)
            App.win.bind(MouseEvent.mousedown, self._mouseEvent)
            App.win.bind(MouseEvent.mouseup, self._mouseEvent)
            App.win.bind(MouseEvent.click, self._mouseEvent)
            App.win.bind(MouseEvent.dblclick, self._mouseEvent)

        
    def _routeEvent(self, event, evtlist):
        for callback in reversed(evtlist):
            if not event.consumed:
                callback(event)
        
    def _keyEvent(self, hwevent):
        evtlist = App.eventdict.get(
            (hwevent.type, KeyEvent.keys.get(hwevent.keyCode,0)), [])
        evtlist.extend(App.eventdict.get((hwevent.type, '*'), []))
        if len(evtlist) > 0:
            evt = KeyEvent(hwevent)
            self._routeEvent(evt, evtlist)

    def _mouseEvent(self, hwevent):
        evtlist = App.eventdict.get(hwevent.type, [])
        if len(evtlist) > 0:
            evt = MouseEvent(hwevent)
            self._routeEvent(evt, evtlist)

    @classmethod
    def _add(cls, obj):
        if App.win != None:
            App.win.add(obj.GFX)
        App.spritelist.append(obj)
        if type(obj) not in App.spritesdict:
            App.spritesdict[type(obj)] = []
        App.spritesdict[type(obj)].append(obj)

    @classmethod
    def _remove(cls, obj):
        if App.win != None:
            App.win.remove(obj.GFX)
        App.spritelist.remove(obj)
        App.spritesdict[type(obj)].remove(obj)
        
    def _animate(self, dummy):
        if self.userfunc:
            self.userfunc()
        else:
            self.step()
        App.win.animate(self._animate)

    @classmethod
    def destroy(cls, dummy):
        App.win.destroy()
        App.win = None
        for s in list(App.spritelist):
            s.destroy()
        App.spritelist = []
        App.spritesdict = {}
        App.eventdict = {}

    @classmethod
    def listenKeyEvent(cls, eventtype, key, callback):
        """
        eventtype : "keydown", "keyup", "keypress"
        key : e.g. "space", "a" or "*" for ALL!
        callback : function name to receive events
        """
        evtlist = App.eventdict.get((eventtype, key), [])
        evtlist.append(callback)
        App.eventdict[(eventtype, key)] = evtlist

    @classmethod
    def listenMouseEvent(cls, eventtype, callback):
        evtlist = App.eventdict.get(eventtype, [])
        evtlist.append(callback)
        App.eventdict[eventtype] = evtlist

    @classmethod
    def unlistenKeyEvent(cls, eventtype, key, callback):
        App.eventdict[(eventtype,key)].remove(callback)

    @classmethod
    def unlistenMouseEvent(cls, eventtype, callback):
        App.eventdict[eventtype].remove(callback)

    @classmethod
    def getSpritesbyClass(cls, sclass):
        return App.spritesdict.get(sclass, [])
        
    def step(self):
        pass
    
    def run(self, userfunc = None):
        self.userfunc = userfunc
        App.win.animate(self._animate)

