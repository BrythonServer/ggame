"""
MathApp GUI input pushbutton and toggle controls.
"""

from ggame.point import ImagePoint
from ggame.asset import Frame


class InputImageButton(ImagePoint):
    """
    :class:`~ggame.point.ImagePoint` object that uses an image as its on-screen and
        activates a callback function when pressed.

    :Required Arguments:

    :param str url: Location of an image file (png, jpg)
    :param function callback: Reference to a function to execute, passing this
        button object.

    :param \\*args:
        See below
    :param \\**kwargs:
        See below

    :Required Arguments:
        * **pos** (*tuple(float,float)*) Position in physical or logical units.

    :Optional Keyword Arguments:
        * **positioning** (*str*) One of 'logical' (default) or 'physical'
        * **frame** (*Frame*) The sub-frame location of image within the image file
        * **qty** (*int*) The number of sub-frames, when used as a sprite sheet
        * **direction** (*str*) One of 'horizontal' (default) or 'vertical'
        * **margin** (*int*) Pixels between sub-frames if sprite sheet

    Example:

    .. literalinclude:: ../examples/inputpointinputimagebutton.py

    """

    def __init__(self, url, callback, *args, **kwargs):
        super().__init__(url, *args, **kwargs)
        self.center = (0, 0)
        self._callback = callback
        self.selectable = True
        self.firstImage()
        self.mousewasdown = self.mouseisdown

    def select(self):
        super().select()
        if self._callback:
            self._callback(self)
        self.unselect()

    def unselect(self):
        super().unselect()

    def __call__(self):
        # code for controlling the button image state only works if the
        # button state is being monitored!
        if self.mouseisdown != self.mousewasdown:
            if self.mouseisdown:
                self.nextImage()
            else:
                self.firstImage()
            self.mousewasdown = self.mouseisdown
        return self.mouseisdown


class InputImageToggle(ImagePoint):
    """
    Spritesheet-based input control that toggles through a set of states with each
    mouseclick.

    :Required Inputs:

    :param str url: Location of image file consisting of a multi-image sprite sheet.
    :param list statelist: List of values to correspond with toggle states.
    :param int initindex: Index to initial toggle state.
    :param (float,float) pos: Position in physical or logical units. May be a
        :class:`ggame.point.Point` instance, a literal (x,y) pair, or a function
        that returns an (x,y) pair.

    :param \\**kwargs:
        See below

    :Optional Keyword Arguments:

    * **positioning** (*str*) One of 'logical' (default) or 'physical'
    * **frame** (*:class:`ggame.asset.Frame`*) Sub-frame location of sub-image within
        the main image.
    * **direction** (*str*) One of 'horizontal' (default) or 'vertical'.
    * **margin** (*int*) Number of pixels between sub-frames if sprite sheet.

    """

    def __init__(self, url, statelist, initindex, *args, **kwargs):
        self.statelist = statelist
        kwargs.setdefault("qty", len(statelist))
        super().__init__(url, *args, **kwargs)
        self.center = (0, 0)
        self.selectable = True
        self.togglestate = initindex
        self.setImage(self.togglestate)

    def select(self):
        super().select()
        self.togglestate += 1
        if self.togglestate == len(self.statelist):
            self.togglestate = 0
        self.setImage(self.togglestate)
        self.unselect()

    def __call__(self):
        return self.statelist[self.togglestate]


class MetalToggle(InputImageToggle):
    """
    Metal toggle input control that toggles through two states with each
    mouseclick.

    :Required Inputs:

    :param int initindex: Index to initial toggle state (0 or 1).
    :param (float,float) pos: Position in physical or logical units. May be a
        :class:`ggame.point.Point` instance, a literal (x,y) pair, or a function
        that returns an (x,y) pair.

    Example:

    .. literalinclude:: ../examples/indicatorledindicator.py

    """

    def __init__(self, initindex, *args, **kwargs):
        kwargs.setdefault("frame", Frame(0, 0, 110, 150))
        super().__init__(
            "ggimages/toggle-up-down.png", [True, False], initindex, *args, **kwargs
        )
        self.scale = 0.4


class GlassButton(InputImageButton):
    """
    Glass button input control that triggers a callback when clicked.

    :Required Inputs:

    :param function callback: Reference to a function to execute, passing this button
        object as an argument.
    :param (float,float) pos: Position in physical or logical units. May be a
        :class:`ggame.point.Point` instance, a literal (x,y) pair, or a function
        that returns an (x,y) pair.

    Example:

    .. literalinclude:: ../examples/inputpointglassbutton.py

    """

    def __init__(self, callback, *args, **kwargs):
        kwargs.setdefault("frame", Frame(0, 0, 100, 100))
        kwargs.setdefault("qty", 2)
        super().__init__("ggimages/button-round.png", callback, *args, **kwargs)
        self.scale = 0.3
