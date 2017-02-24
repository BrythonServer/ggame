# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from abc import ABCMeta, abstractmethod

from math import sin, cos

class _MathDynamic(metaclass=ABCMeta):
    
    def __init__(self):
        MathApp._add(self)

    def destroy(self):
        MathApp._remove(self)

    @abstractmethod
    def step():
        pass
    
    def Eval(self, val):
        if callable(val):
            return val
        else:
            return lambda : val  
            

class _MathVisual(Sprite, _MathDynamic, metaclass=ABCMeta):
    
    def __init__(self, asset, pos):
        Sprite.__init__(self, asset, pos)
        _MathDynamic.__init__(self)
    
    def destroy(self):
        super().destroy()
        #MathApp._remove(self)
    
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
    
    def step():
        pass

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
    _stepDynamicList = []
    
    def __init__(self, scale=(_xscale, _yscale)):
        super().__init__()
        MathApp._xscale = scale[0]   # pixels per unit
        MathApp._yscale = scale[1]
        # touch all visual object assets to use scaling
        for obj in self._mathVisualList:
            obj._touchAsset()
            
        self.g = 0
        self.lines = [LineSegment(
            lambda xx=x:(3*sin(self.g), 3*cos(self.g-xx)), 
            lambda xx=x:(-3*sin(self.g+xx), -3*cos(self.g))) for x in range(5)]

    def step(self):
        for spr in self._mathDynamicList:
            spr.step()
        
        self.g = self.g + 0.01
        if self.g > 3.14:
            self.g = 0
        
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
    def _add(cls, obj):
        if isinstance(obj, _MathVisual):
            cls._mathVisualList.append(obj)
            
    @classmethod
    def _remove(cls, obj):
        if isinstance(obj, _MathVisual):
            cls._mathVisualList.remove(obj)


# test code here

p1 = Point((0,0))
p2 = Point((2,0))
p3 = Point((3,0))
p4 = Point((3,3))
for i in range(100):
    Point((i/20, -1))

LineSegment(p1,p4)

ap = MathApp((100,100))
ap.run()