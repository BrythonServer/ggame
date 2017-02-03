# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, Sprite, App

ls = LineStyle(3, Color(0x000000, 1))
la = LineAsset(100, 100, ls)
#sp = Sprite(la, (100,100))

class LineSegment(Sprite):
    def __init__(self, start, end, style=LineStyle(1, Color(0,1))):
        self._start = start
        self._end = end
        self.la = LineAsset(end[0]-start[0], end[1]-start[1], style)
        super().__init__(self.la, start)
        
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, val):
        self._start = val
        self.GFX.currentPath.points[0] = self._start[0]
        self.GFX.currentPath.points[1] = self._start[1]
        
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, val):
        self._end = val
        self.GFX.currentPath.points[2] = self._end[0]
        self.GFX.currentPath.points[3] = self._end[1]
        
    def step(self):
        self.start = (self.start[0]+1, self.start[1])
        
        
l = LineSegment((100,100), (200,200))

class MathApp(App):
    
    def step(self):
        for spr in MathApp.getSpritesbyClass(LineSegment):
            spr.step()

ap = MathApp()
ap.run()