"""
Line objects for MathApp applications
"""

from ggame.mathapp import _MathVisual
from ggame.asset import LineAsset


class LineSegment(_MathVisual):
    """
    Create a line segment on the screen. This is a subclass of
    :class:`~ggame.sprite.Sprite` and
    :class:`~ggame.mathapp._MathVisual` but most of the inherited members are of
    little use and are not shown in the documentation.


    :param \\*args:
        See below
    :param \\**kwargs:
        See below

    :Required Arguments:
        * **pos** (*tuple(float,float)*) Starting point of the segment, which may
            be a literal tuple of floats, or a reference to any object or
            function that returns or evaluates to a tuple of floats.
        * **end** (*tuple(float,float)*) Ending point of the segment (see above)


    :Optional Keyword Arguments:
        * **positioning** (*str*) One of 'logical' or 'physical'
        * **style** (*LineStyle*) Valid :class:`~ggame.asset.LineStyle` object

    Example::

        from ggame.point import Point
        from ggame.line import LineSegment
        from ggame.mathapp import MathApp

        p1 = Point((2,1))
        ls = LineSegment(p1, Point((1,1)))

        MathApp().run()
    """

    _posinputsdef = ["pos", "end"]

    def __init__(self, *args, **kwargs):
        super().__init__(LineAsset(0, 0, self._defaultstyle), *args, **kwargs)
        self.touchAsset()

    def _buildAsset(self):
        # pylint: disable=no-member
        start = self._pposinputs.pos
        end = self._pposinputs.end
        # pylint: enable=no-member
        self.position = start
        return LineAsset(end[0] - start[0], end[1] - start[1], self._stdinputs.style())

    def physicalPointTouching(self, ppos):
        """
        This method always returns False.
        """
        return False

    def translate(self, pdisp):
        """
        This method is not implemented.
        """
