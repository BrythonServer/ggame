from abc import ABCMeta, abstractmethod
from ggame.mathbase import _MathVisual
from ggame.asset import Color, LineStyle, CircleAsset


class _Point(_MathVisual, metaclass=ABCMeta):

    posinputsdef = ['pos']
    nonposinputsdef = []

    def __init__(self, asset, *args, **kwargs):
        """
        Required Inputs
        
        * **asset** asset object to use
        * **pos** position of point
        """
        super().__init__(asset, *args, **kwargs)
        self._touchAsset()
        self.center = (0.5, 0.5)

    def __call__(self):
        return self.posinputs.pos()

    def step(self):
        pass  # FIXME
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        return MathApp.distance(ppos, self.pposinputs.pos) < self.sstdinputs.size
        
    def translate(self, pdisp):
        ldisp = MathApp.translatePhysicalToLogical(pdisp)
        pos = self.posinputs.pos()
        self.posinputs = self.posinputs._replace(pos=self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1])))
        self._touchAsset()
        
    def distanceTo(self, otherpoint):
        try:
            pos = self.posinputs.pos
            opos = otherpoint.posinputs.pos
            return MathApp.distance(pos, opos())
        except AttributeError:
            return otherpoint  # presumably a scalar - use this distance




class Point(_Point):


    defaultsize = 5
    defaultstyle = LineStyle(0, Color(0, 1))


    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** position of point
        """
        super().__init__(CircleAsset(self.defaultsize, 
            self.defaultstyle, self.defaultcolor), *args, **kwargs)


    def _buildAsset(self):
        return CircleAsset(self.stdinputs.size(),
                            self.stdinputs.style(),
                            self.stdinputs.color())



class ImagePoint(_Point):


    def __init__(self, url, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file
        * **pos** position of point
        
        Optional Inputs
        * **frame** sub-frame location of image within file
        * **qty** number of sub-frames, when used as sprite sheet
        * **direction** one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        """
        frame = kwargs.get('frame', None)
        qty = kwargs.get('qty', 1)
        direction = kwargs.get('direction', 'horizontal')
        margin = kwargs.get('margin', 0)
        self._imageasset = ImageAsset(url, frame, qty, direction, margin)
        super().__init__(self._imageasset, *args, **kwargs)


    def _buildAsset(self):
        return self._imageasset

    def physicalPointTouching(self, ppos):
        self._setExtents()  # ensure xmin, xmax are correct
        x, y = ppos
        return x >= self.xmin and x < self.xmax and y >= self.ymin and y <= self.ymax
