"""
MathApp label classes for displaying text.
"""

from ggame.mathapp import _MathVisual
from ggame.asset import TextAsset


class Label(_MathVisual):
    """
    Create a text label on the screen. This is a
    subclass of :class:`~ggame.sprite.Sprite` and
    :class:`~ggame.mathapp._MathVisual` but most of the inherited
    members are of little use and are not shown in the documentation.

    :param \\*args:
        See below
    :param \\**kwargs:
        See below

    :Required Arguments:
        * **pos**  (*tuple(float,float)*) Screen position of the label, which may
            be a literal tuple of floats, or a reference to any object or
            function that returns or evaluates to a tuple of floats.
        * **text** (*str*) Text to appear in the label. This may be a literal
            string or a reference to any object or function that returns or
            evaluates to a string.

    :Optional Keyword Arguments:
        * **positioning** (*str*) One of 'logical' or 'physical'
        * **size** (*int*) Size of text font (in pixels)
        * **width** (*int*) Width of the label (in pixels)
        * **color** (*Color*) Valid :class:`~ggame.asset.Color` object

    Example:

    .. literalinclude:: ../examples/labellabel.py

    """

    _posinputsdef = ["pos"]
    _nonposinputsdef = ["text"]

    def __init__(self, *args, **kwargs):
        """
        Required Inputs

        * **pos** position of label
        * **text** text contents of label
        """
        super().__init__(TextAsset(""), *args, **kwargs)
        self.touchAsset()

    def _buildAsset(self):
        return TextAsset(
            self._nposinputs.text(),  # pylint: disable=no-member
            style="{0}px Courier".format(self._stdinputs.size()),
            width=self._stdinputs.width(),
            fill=self._stdinputs.color(),
        )

    def __call__(self):
        return self._nposinputs.text()  # pylint: disable=no-member

    def physicalPointTouching(self, ppos):
        _ppos = self._spposinputs.pos
        return (
            ppos[0] >= _ppos[0]
            and ppos[0] <= _ppos[0] + self._sstdinputs.width
            and ppos[1] >= _ppos[1]
            and ppos[1] <= _ppos[1] + self._sstdinputs.size
        )

    def translate(self, pdisp):
        pass
