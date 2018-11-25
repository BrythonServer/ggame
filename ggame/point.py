from abc import ABCMeta, abstractmethod
from ggame.mathapp import _MathVisual, MathApp
from ggame.asset import Color, LineStyle, CircleAsset, ImageAsset


class _Point(_MathVisual, metaclass=ABCMeta):
    """
    Abstract base class for all point classes.
    
    :param Asset asset: A valid ggame Asset object
    :param tuple(float,float) pos: The position (physical or logical)
    """

    _posinputsdef = ['pos']
    _nonposinputsdef = []

    def __init__(self, asset, *args, **kwargs):
        super().__init__(asset, *args, **kwargs)
        self._touchAsset()
        self.center = (0.5, 0.5)

    def __call__(self):
        return self._posinputs.pos()

    def step(self):
        """
        Perform periodic processing.
        """
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        """
        Determine if a physical point is considered to be touching this point.
        
        :param tuple(int,int) ppos: Physical screen coordinates.
        :rtype: boolean
        :returns: True if touching, False otherwise.
        """
        return MathApp.distance(ppos, self._pposinputs.pos) < self._sstdinputs.size
        
    def translate(self, pdisp):
        """ 
        Perform necessary processing in response to being moved by the mouse/UI.
        
        :param tuple(int,int) pdisp: Translation vector (x,y) in physical screen
            units.
        :returns: None
        """
        ldisp = MathApp.translatePhysicalToLogical(pdisp)
        pos = self._posinputs.pos()
        self._posinputs = self._posinputs._replace(pos=self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1])))
        self._touchAsset()
        
    def distanceTo(self, otherpoint):
        """
        Compute the distance to another :class:`_Point` object.
        
        :param _Point otherpoint: A reference to the other :class:`_Point`
        :rtype: float
        :returns: The distance (in logical units) to the other point
        """
        try:
            pos = self._posinputs.pos
            opos = otherpoint._posinputs.pos
            return MathApp.distance(pos, opos())
        except AttributeError:
            return otherpoint  # presumably a scalar - use this distance




class Point(_Point):
    """
    Basic point object representing any point in a geometrical sense. 
    An instantiated Point object is *callable* and will return a tuple
    with its logical position as an (x,y) pair.
    
    
    :param tuple(float,float) pos: Position in physical or logical units.

    :param \**kwargs:
        See below

    :Optional Keyword Arguments:
        * **positioning** (*str*) One of 'logical' (default) or 'physical'
        * **size** (*int*) Radius of the point (in pixels)
        * **color** (*Color*) Valid :class:`~ggame.asset.Color` object
        * **style** (*LineStyle*) Valid :class:`~ggame.asset.LineStyle` object
            
    Example::
    
        from ggame.asset import Color
        from ggame.point import Point
        from ggame.mathapp import MathApp

        p1 = Point((0,1), color=Color(0xff8000, 1.0))
        p1.movable = True
        # An orange point that can be moved
        
        p2 = Point(lambda: (p1()[0], p1()[1]+1))
        # A point position based on P1
        p3 = Point((1,0))
        # A third, fixed point
        
        MathApp().run()
    
    """
    _defaultsize = 5
    _defaultstyle = LineStyle(0, Color(0, 1))


    def __init__(self, *args, **kwargs):
        super().__init__(CircleAsset(self._defaultsize, 
            self._defaultstyle, self._defaultcolor), *args, **kwargs)


    def _buildAsset(self):
        return CircleAsset(self._stdinputs.size(),
                            self._stdinputs.style(),
                            self._stdinputs.color())



class ImagePoint(_Point):
    """
    :class:`~ggame.point.Point` object that uses an image as its on-screen
        representation.
    
    :param str url: Location of an image file (png, jpg)

    :param \*args:
        See below
    :param \**kwargs:
        See below

    :Required Arguments:
        * **pos** (*tuple(float,float)*) Position in physical or logical units.
    

    :Optional Keyword Arguments:
        * **positioning** (*str*) One of 'logical' (default) or 'physical'
        * **frame** (*Frame*) The sub-frame location of image within the image file
        * **qty** (*int*) The number of sub-frames, when used as a sprite sheet
        * **direction** (*str*) One of 'horizontal' (default) or 'vertical'
        * **margin** (*int*) Pixels between sub-frames if sprite sheet
    """


    def __init__(self, url, *args, **kwargs):
        frame = kwargs.get('frame', None)
        qty = kwargs.get('qty', 1)
        direction = kwargs.get('direction', 'horizontal')
        margin = kwargs.get('margin', 0)
        self._imageasset = ImageAsset(url, frame, qty, direction, margin)
        super().__init__(self._imageasset, *args, **kwargs)


    def _buildAsset(self):
        return self._imageasset

    def physicalPointTouching(self, ppos):
        """
        Determine if a physical point is considered to be touching point's 
        image.
        
        :param tuple(int,int) ppos: Physical screen coordinates.
        :rtype: boolean
        :returns: True if touching, False otherwise.
        """
        self._setExtents()  # ensure xmin, xmax are correct
        x, y = ppos
        return x >= self.xmin and x < self.xmax and y >= self.ymin and y <= self.ymax
