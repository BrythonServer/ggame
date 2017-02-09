# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, Sprite, App
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
        self.asset = asset
        self.GFX = self.asset.GFX
        self.GFX.visible = True        
        App._add(self)

    @abstractmethod
    def _newAsset():    
        pass

    @abstractmethod
    def _refreshAsset():
        pass


class LineSegment(_MathVisual):
    
    def __init__(self, start, end, style=LineStyle(1, Color(0,1))):
        self._start = self.Eval(start)
        self._end = self.Eval(end)
        self._style = style
        self._oldstart = None
        self._oldend = None
        self._newAsset(self._start(), self._end(), self._style)
        
    def _newAsset(self, start, end, style):
        if start != self.oldstart or end != self.oldend:
            self._updateAsset(LineAsset(end[0]-start[0], end[1]-start[1], style))
            self.position = start

    def _refreshAsset(self, start, end, style):
        App._remove(self)
        self._newAsset(start, end, style)
    
    @property
    def start(self):
        return self._start()

    @start.setter
    def start(self, val):
        newval = self.Eval(val)
        if newval != self._start:
            self._start = newval
            self._refreshAsset(self._start(), self._end(), self._style)

    @property
    def end(self):
        return self._end()

    @end.setter
    def end(self, val):
        newval = self.Eval(val)
        if newval != self._end:
            self._end = newval
            self._refreshAsset(self._start(), self._end(), self._style)
        
    def step(self):
        self.start = (self.start[0]+1, self.start[1])
        


lines = [LineSegment((300*sin(x)+300,300*cos(x)+300), (-300*sin(x)+300,-300*cos(x)+300)) for x in range(50)]
#l = LineSegment((200,200), (500,500))
g = 0
class MathApp(App):
    def step(self):
        global g
        for spr in MathApp.getSpritesbyClass(LineSegment):
            g = g + 1
            #spr.step()
            #spr.start = (300*sin(g)+300,300*cos(g)+300)
            spr.start = (spr.start[0]+1, spr.start[1])
            pass

ap = MathApp()
ap.run()