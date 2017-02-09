# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, Sprite, App
from math import sin, cos

class LineSegment(Sprite):
    
    la = LineAsset(0,0, LineStyle(1, Color(0x000000, 1)))
    
    def __init__(self, start, end, style=LineStyle(1, Color(0,1))):
        self._start = start
        self._end = end
        self._style = style
        super().__init__(LineSegment.la, start)
        self._newSegment(self._start, self._end, self._style)
        
    def _newSegment(self, start, end, style):
        App._remove(self)
        self.asset = LineAsset(end[0]-start[0], end[1]-start[1], style)
        self.GFX = self.asset.GFX
        self.GFX.visible = True        
        self.position = start
        App._add(self)
    
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, val):
        self._start = val
        self._newSegment(self._start, self._end, self._style)

        
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, val):
        self._end = val
        self.la = LineAsset(self._start, self._end, style)
        
    def step(self):
        self.start = (self.start[0]+1, self.start[1])


lines = [LineSegment((300*sin(x)+300,300*cos(x)+300), (-300*sin(x)+300,-300*cos(x)+300)) for x in range(50)]
#l = LineSegment((200,200), (500,500))
g = 0
class MathApp(App):
    def step(self):
        global g
        for spr in MathApp.getSpritesbyClass(LineSegment):
            for l in lines:
                g = g + 1
                l.start = (300*sin(g)+300,300*cos(g)+300)
            pass

ap = MathApp()
ap.run()