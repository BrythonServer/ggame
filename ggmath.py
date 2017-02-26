# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from ggame import TextAsset
from abc import ABCMeta, abstractmethod

from math import sin, cos, sqrt
from time import time

class _MathDynamic(metaclass=ABCMeta):
    
    def __init__(self):
        self._dynamic = False  # not switched on, by default!
    
    def destroy(self):
        MathApp._removeDynamic(self)

    @abstractmethod
    def step(self):
        pass
    
    def Eval(self, val):
        if callable(val):
            self._setDynamic() # dynamically defined .. must step
            return val
        else:
            return lambda : val  
            
    def _setDynamic(self):
        MathApp._addDynamic(self)
        self._dynamic = True
            

class _MathVisual(Sprite, _MathDynamic, metaclass=ABCMeta):
    
    def __init__(self, asset, pos):
        MathApp._addVisual(self)
        Sprite.__init__(self, asset, pos)
        _MathDynamic.__init__(self)
        self._movable = False
    
    def destroy(self):
        MathApp._removeVisual(self)
        MathApp._removeMovable(self)
        _MathDynamic.destroy(self)
        Sprite.destroy(self)

    def _updateAsset(self, asset):
        if App._win != None:
            App._win.remove(self.GFX)
        self.asset = asset
        self.GFX = self.asset.GFX
        self.GFX.visible = True        
        if App._win != None:
            App._win.add(self.GFX)
            
    @property
    def movable(self):
        return self._movable
        
    @movable.setter
    def movable(self, val):
        if not self._dynamic:
            self._setMovable(val)

    def _setMovable(self, val):
        self._movable = val
        if val:
            MathApp._addMovable(self)
        else:
            MathApp._removeMovable(self)
            
    # define how your class responds to mouse clicks - returns True/False
    @abstractmethod
    def physicalPointTouching(self, ppos):
        pass
    
    # define how your class responds to being moved (physical units)
    @abstractmethod
    def translate(self, pdisp):
        pass
            
    @abstractmethod
    def _newAsset(self):    
        pass

    @abstractmethod
    def _touchAsset(self):
        pass


class Timer(_MathDynamic):
    
    def __init__(self):
        super().__init__()
        self.reset()
        self.step()
        MathApp._addDynamic(self)  # always dynamically defined
        
    def reset(self):
        self._reset = MathApp.time
        
    def step(self):
        self.time = MathApp.time - self._reset
        

class Label(_MathVisual):
    
    def __init__(self, pos, text, positioning="logical", size=10, width=200, color=Color(0,1)):
        self._text = self.Eval(text) # create a *callable* text value function
        self._ptext = self._text()
        self._pos = self.Eval(pos)
        self._positioning = positioning
        self._size = size
        self._width = width
        self._color = color
        if self._positioning == "physical":
            self._ppos = self._pos()
        else:
            self._ppos = MathApp.logicalToPhysical(self._pos())
            
        super().__init__(TextAsset(self._ptext, 
                style="{0}px Arial".format(self._size), 
                width=self._width,
                color=self._color), 
            self._ppos)

    def _newAsset(self, pos, text, size, width, color):    
        if self._positioning != "physical":
            ppos = MathApp.logicalToPhysical(pos())
        else:
            ppos = pos()
        text = text()
        if ppos != self._ppos or text != self._ptext:
            self._ppos = ppos
            self._ptext = text
            self._updateAsset(TextAsset(text, 
                style="{0}px Arial".format(size),
                width=width,
                color=color))
            self.position = ppos
        

    def _touchAsset(self):
        self._newAsset(self._pos, self._text, self._size, self._width, self._color)

    def step(self):
        self._touchAsset()
    
    def physicalPointTouching(self, ppos):
        return False
        
    def translate(self, pdisp):
        pass

    

class Point(_MathVisual):
    
    def __init__(self, pos, size=5, color=Color(0,1), style=LineStyle(0, Color(0,1))):
        self._pos = self.Eval(pos)  # create a *callable* position function
        self._ppos = MathApp.logicalToPhysical(self._pos()) # physical position
        self._size = size
        self._color = color
        self._style = style
        super().__init__(CircleAsset(size, style, color), self._ppos)
        self.center = (0.5, 0.5)
        
    def __call__(self):
        return self._pos()

    def _newAsset(self, pos, size, color, style):
        ppos = MathApp.logicalToPhysical(pos())
        if ppos != self._ppos:
            self._ppos = ppos
            self._updateAsset(CircleAsset(size, style, color))
            self.position = ppos
            self._setExtents()

    def _touchAsset(self):
        self._newAsset(self._pos, self._size, self._color, self._style)

    def step(self):
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        return MathApp.distance(ppos, self._ppos) < self._size
        
    def translate(self, pdisp):
        ldisp = MathApp.translatePhysicalToLogical(pdisp)
        print(ldisp)
        pos = self._pos()
        self._pos = self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1]))
        self._touchAsset()


class LineSegment(_MathVisual):
    
    def __init__(self, start, end, style=LineStyle(1, Color(0,1))):
        self._start = self.Eval(start)  # save function
        self._end = self.Eval(end)
        self._style = style
        self._pstart = MathApp.logicalToPhysical(self._start())
        self._pend = MathApp.logicalToPhysical(self._end())
        super().__init__(LineAsset(self._pend[0]-self._pstart[0], 
            self._pend[1]-self._pstart[1], style), self._pstart)

    def _newAsset(self, start, end, style):
        pstart = MathApp.logicalToPhysical(start())
        pend = MathApp.logicalToPhysical(end())
        if pstart != self._pstart or pend != self._pend:
            self._pstart = pstart
            self._pend = pend
            self._updateAsset(LineAsset(pend[0]-pstart[0], pend[1]-pstart[1], style))
            self.position = pstart

    def _touchAsset(self):
        self._newAsset(self._start, self._end, self._style)
    
    @property
    def start(self):
        return self._start()

    @start.setter
    def start(self, val):
        newval = self.Eval(val)
        if newval != self._start:
            self._start = newval
            self._touchAsset()

    @property
    def end(self):
        return self._end()

    @end.setter
    def end(self, val):
        newval = self.Eval(val)
        if newval != self._end:
            self._end = newval
            self._touchAsset()
        
    def step(self):
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        return False
        
    def translate(self, pdisp):
        pass


class MathApp(App):
    
    _xscale = 200   # pixels per unit
    _yscale = 200
    _xcenter = 0    # center of screen in units
    _ycenter = 0    
    _mathVisualList = [] #
    _mathDynamicList = []
    _mathMovableList = []
    time = time()
    
    def __init__(self, scale=(_xscale, _yscale)):
        super().__init__()
        MathApp._xscale = scale[0]   # pixels per unit
        MathApp._yscale = scale[1]
        # register event callbacks
        self.listenMouseEvent("click", self.handleMouseClick)
        self.listenMouseEvent("mousedown", self.handleMouseDown)
        self.listenMouseEvent("mouseup", self.handleMouseUp)
        self.listenMouseEvent("mousemove", self.handleMouseMove)
        self.listenMouseEvent("mousewheel", self.handleMouseWheel)
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseX = self.mouseY = None
        # touch all visual object assets to use scaling
        for obj in self._mathVisualList:
            obj._touchAsset()

    def step(self):
        MathApp.time = time()
        for spr in self._mathDynamicList:
            spr.step()
        

    @classmethod
    def logicalToPhysical(cls, lp):
        xxform = lambda xvalue, xscale, xcenter, physwidth: int((xvalue-xcenter)*xscale + physwidth/2)
        yxform = lambda yvalue, yscale, ycenter, physheight: int(physheight/2 - (yvalue-ycenter)*yscale)

        try:
            return (xxform(lp[0], cls._xscale, cls._xcenter, cls._win.width),
                yxform(lp[1], cls._yscale, cls._ycenter, cls._win.height))
        except AttributeError:
            return lp
            
    @classmethod
    def physicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale, xcenter, physwidth: (xvalue - physwidth/2)/xscale + xcenter
        yxform = lambda yvalue, yscale, ycenter, physheight: (physheight/2 - yvalue)/yscale + ycenter

        try:
            return (xxform(pp[0], cls._xscale, cls._xcenter, cls._win.width),
                yxform(pp[1], cls._yscale, cls._ycenter, cls._win.height))
        except AttributeError:
            return pp
            
    @classmethod
    def translatePhysicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale: xvalue/xscale
        yxform = lambda yvalue, yscale: -yvalue/yscale

        try:
            return (xxform(pp[0], cls._xscale), yxform(pp[1], cls._yscale))
        except AttributeError:
            return pp

    def _tweakMouseEvent(self, event):
        rect = self._win._renderer.view.getBoundingClientRect()
        event.x = event.x - rect.left
        event.y = event.y - rect.top
        
    def handleMouseClick(self, event):
        self._tweakMouseEvent(event)
        pass
    
    def handleMouseDown(self, event):
        self._tweakMouseEvent(event)
        self.mouseDown = True
        for obj in self._mathMovableList:
            if obj.physicalPointTouching((event.x, event.y)):
                self.mouseCapturedObject = obj
                break

    def handleMouseUp(self, event):
        self._tweakMouseEvent(event)
        self.mouseUp = False
        self.mouseCapturedObject = None

    def handleMouseMove(self, event):
        self._tweakMouseEvent(event)
        if not self.mouseX:
            self.mouseX = event.x
            self.mouseY = event.y
        dx = event.x - self.mouseX
        dy = event.y - self.mouseY
        self.mouseX = event.x
        self.mouseY = event.y
        if self.mouseDown and self.mouseCapturedObject:
            self.mouseCapturedObject.translate((dx, dy))

    def handleMouseWheel(self, event):
        self._tweakMouseEvent(event)
        pass
     
    @classmethod   
    def distance(cls, pos1, pos2):
        return sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
            
    @classmethod
    def _addVisual(cls, obj):
        if isinstance(obj, _MathVisual):
            cls._mathVisualList.append(obj)
            
    @classmethod
    def _removeVisual(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathVisualList:
            cls._mathVisualList.remove(obj)

    @classmethod
    def _addDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and obj not in cls._mathDynamicList:
            cls._mathDynamicList.append(obj)
            
    @classmethod
    def _removeDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and obj in cls._mathDynamicList:
            cls._mathDynamicList.remove(obj)

    @classmethod
    def _addMovable(cls, obj):
        if isinstance(obj, _MathVisual) and obj not in cls._mathMovableList:
            cls._mathMovableList.append(obj)
            
    @classmethod
    def _removeMovable(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathMovableList:
            cls._mathMovableList.remove(obj)


# test code here

p1 = Point((0,0))
p2 = Point((2,0))
p2.movable = True
p3 = Point((3,0))
t = Timer()
p4 = Point(lambda :(3, (int(t.time*100) % 400)/100))
for i in range(100):
    Point((i/20, -1))

LineSegment(p1,p4)
[LineSegment(
            lambda xx=x:(3*sin(t.time), 3*cos(t.time-xx)), 
            lambda xx=x:(-3*sin(t.time+xx), -3*cos(t.time))) for x in range(5)]

l1 = Label((200,200), lambda: "Elapsed Time: {0:.0}".format(t.time), size=20, width=400, positioning="physical")



ap = MathApp((100,100))
ap.run()