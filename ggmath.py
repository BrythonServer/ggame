# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from abc import ABCMeta, abstractmethod

from math import sin, cos

class _MathDynamic(metaclass=ABCMeta):
    
    @abstractmethod
    def step():
        pass
    
    @classmethod
    def Eval(cls, val):
        if callable(val):
            return(val)
        else:
            return lambda : val  
            

class _MathVisual(Sprite, _MathDynamic, metaclass=ABCMeta):
    
    def _updateAsset(self, asset):
        if App._win != None:
            App._win.remove(self.GFX)
        self.asset = asset
        self.GFX = self.asset.GFX
        self.GFX.visible = True        
        if App._win != None:
            App._win.add(self.GFX)
            
    @abstractmethod
    def _newAsset():    
        pass

    @abstractmethod
    def _refreshAsset():
        pass


class Point(_MathVisual):
    
    def __init__(self, pos, size=5, color=Color(0,1), style=LineStyle(0, Color(0,1))):
        self._pos = self.Eval(pos)  # create a *callable* position function
        self._size = size
        super().__init__(CircleAsset(size, style, color), self._pos())

    def _newAsset():
        pass
    
    def _refreshAsset():
        pass

    def step():
        pass

class LineSegment(_MathVisual):
    
    def __init__(self, start, end, style=LineStyle(1, Color(0,1))):
        self._start = self.Eval(start)  # save function
        self._end = self.Eval(end)
        self._style = style
        self._oldstart = start
        self._oldend = end
        super().__init__(LineAsset(self.end[0]-self.start[0], 
            self.end[1]-self.start[1], style), self._start())

    def _newAsset(self, start, end, style):
        # start and end are simple numerics
        if start != self._oldstart or end != self._oldend:
            self._oldstart = start
            self._oldend = end
            self._updateAsset(LineAsset(end[0]-start[0], end[1]-start[1], style))
            self.position = start

    def _refreshAsset(self, start, end, style):
        self._newAsset(start, end, style)

    def _touchAsset(self):
        self._refreshAsset(self._start(), self._end(), self._style)
    
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



#l = LineSegment((200,200), (500,500))

p = Point((300,300))

class MathApp(App):
    
    _xscale = 200
    _yscale = 200
    
    def __init__(self, xscale=MathApp._xscale, yscale=MathApp._yscale):
        super().__init__()
        MathApp._xscale = xscale   # pixels per unit
        MathApp._yscale = yscale
        
        self.g = 0
        self.lines = [LineSegment(
            lambda xx=x:(300*sin(self.g)+300, 300*cos(self.g-xx)+300), 
            lambda xx=x:(-300*sin(self.g+xx)+300, -300*cos(self.g)+300)) for x in range(5)]

    def step(self):
        for spr in self.lines:
            spr.step()
        
        self.g = self.g + 0.01
        if self.g > 3.14:
            self.g = 0
        

ap = MathApp()
ap.run()