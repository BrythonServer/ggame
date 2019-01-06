"""
MathApp indicator classes for displaying two-state or boolean values.
"""
import os
from ggame.mathapp import _MathVisual
from ggame.asset import Frame, ImageAsset


class ImageIndicator(_MathVisual):
    """
    Use a sprite sheet image to indicate integer or boolean values.

    Required Inputs

    :param str url: Location of image file consisting of a multi-image sprite sheet.
    :param (float,float) pos: Position in physical or logical units. May be a
        :class:`ggame.point.Point` instance, a literal (x,y) pair, or a function
        that returns an (x,y) pair.
    :param int value: The state of the indicator. May be a function that returns
        a suitable (integer) value.

    :param \\**kwargs:
        See below


    :Optional Keyword Arguments:

    * **positioning** (*str*) One of 'logical' (default) or 'physical'
    * **frame** (*:class:`ggame.asset.Frame`*) Sub-frame location of sub-image within
        the main image.
    * **qty** (*int*) The number of sub-frames, when used as sprite sheet.
    * **direction** (*str*) One of 'horizontal' (default) or 'vertical'.
    * **margin** (*int*) Number of pixels between sub-frames if sprite sheet.

    Example:

    .. literalinclude:: ../examples/indicatorimageindicator.py


    """

    _posinputsdef = ["pos"]
    _nonposinputsdef = ["value"]

    def __init__(self, url, *args, **kwargs):
        kwargs.setdefault("frame", None)
        kwargs.setdefault("qty", 1)
        kwargs.setdefault("direction", "horizontal")
        kwargs.setdefault("margin", 0)
        super().__init__(
            ImageAsset(
                url,
                kwargs["frame"],
                kwargs["qty"],
                kwargs["direction"],
                kwargs["margin"],
            ),
            *args,
            **kwargs
        )
        self.center = (0, 0)

    def _buildAsset(self):
        # pylint: disable=no-member
        inval = self._nposinputs.value()
        # pylint: enable=no-member
        if inval:
            self.setImage(1)
        elif not inval:
            self.setImage(0)
        else:
            self.setImage(inval)
        return self.asset

    def physicalPointTouching(self, ppos):
        self.setExtents()  # ensure xmin, xmax are correct
        x, y = ppos
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    def translate(self, pdisp):
        pass


class LEDIndicator(ImageIndicator):
    """
    Subclass of ImageIndicator using a red LED on/off image.

    Required Inputs

    :param (float,float) pos: Position in physical or logical units. May be a
        :class:`ggame.point.Point` instance, a literal (x,y) pair, or a function
        that returns an (x,y) pair.
    :param int value: The state of the indicator. May be a function that returns
        a suitable (integer) value.

    :param \\**kwargs:
        See below

    :Optional Keyword Arguments:

        * **positioning** (*str*) One of 'logical' (default) or 'physical'

    Example:

    .. literalinclude:: ../examples/indicatorledindicator.py

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("frame", Frame(0, 0, 600, 600))
        kwargs.setdefault("qty", 2)
        # differences in online vs. local operation
        try:
            thispath = os.path.dirname(__file__)
            imagepath = os.path.join(thispath, "../ggimages")
        except NameError:
            imagepath = "ggimages"
        super().__init__(os.path.join(imagepath, "red-led-off-on.png"), *args, **kwargs)
        self.scale = 0.05
