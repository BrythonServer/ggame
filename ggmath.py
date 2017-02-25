# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from ggame import TextAsset
from abc import ABCMeta, abstractmethod

from math import sin, cos
from time import time

class _MathDynamic(metaclass=ABCMeta):
    
    def destroy(self):
        MathApp._removeDynamic(self)

    @abstractmethod
    def step():
        pass
    
    def Eval(self, val):
        if callable(val):
            MathApp._addDynamic(self) # dynamically defined .. must step
            return val
        else:
            return lambda : val  
            

class _MathVisual(Sprite, _MathDynamic, metaclass=ABCMeta):
    
    def __init__(self, asset, pos):
        MathApp._addVisual(self)
        Sprite.__init__(self, asset, pos)
        _MathDynamic.__init__(self)
    
    def destroy(self):
        MathApp._removeVisual(self)
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

    def step():
        self._touchAsset()
    
    def _newAsset(self, pos, text, size, width, color):    
        if self._positioning != "physical":
            ppos = MathApp.logicalToPhysical(pos())
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
    

class Point(_MathVisual):
    
    def __init__(self, pos, size=5, color=Color(0,1), style=LineStyle(0, Color(0,1))):
        self._pos = self.Eval(pos)  # create a *callable* position function
        self._ppos = MathApp.logicalToPhysical(self._pos()) # physical position
        self._size = size
        self._color = color
        self._style = style
        super().__init__(CircleAsset(size, style, color), self._ppos)
        
    def __call__(self):
        return self._pos()

    def _newAsset(self, pos, size, color, style):
        ppos = MathApp.logicalToPhysical(pos())
        if ppos != self._ppos:
            self._ppos = ppos
            self._updateAsset(CircleAsset(size, style, color))
            self.position = ppos

    def _touchAsset(self):
        self._newAsset(self._pos, self._size, self._color, self._style)

    def step(self):
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



class MathApp(App):
    
    _xscale = 200   # pixels per unit
    _yscale = 200
    _xcenter = 0    # center of screen in units
    _ycenter = 0    
    _mathVisualList = [] #
    _mathDynamicList = []
    time = time()
    
    def __init__(self, scale=(_xscale, _yscale)):
        super().__init__()
        MathApp._xscale = scale[0]   # pixels per unit
        MathApp._yscale = scale[1]
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


# test code here

p1 = Point((0,0))
p2 = Point((2,0))
p3 = Point((3,0))
t = Timer()
p4 = Point(lambda :(3, (int(t.time*100) % 400)/100))
for i in range(100):
    Point((i/20, -1))

LineSegment(p1,p4)
[LineSegment(
            lambda xx=x:(3*sin(t.time), 3*cos(t.time-xx)), 
            lambda xx=x:(-3*sin(t.time+xx), -3*cos(t.time))) for x in range(5)]

l1 = Label((3,-3), "Hello, world!", size=20)



ap = MathApp((100,100))
ap.run()