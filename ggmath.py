# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, Sprite, App

ls = LineStyle(3, Color(0x000000, 1))
la = LineAsset(100, 100, ls)
#sp = Sprite(la, (100,100))

class LineSegment(Sprite):
    def __init__(self, start, end, style=LineStyle(1, Color(0,1))):
        self.la = LineAsset(end[0]-start[0], end[1]-start[1], style)
        super().__init__(self.la, start)
        
l = LineSegment((100,100), (200,200))

ap = App()
ap.run()