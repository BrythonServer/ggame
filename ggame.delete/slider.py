"""
MathApp input class for accepting user numeric input with a "slider" control.
"""

from ggame.mathapp import MathApp, _MathVisual
from ggame.asset import RectangleAsset, LineStyle, Color
from ggame.sprite import Sprite


class Slider(_MathVisual):
    """
    Create a 'slider' style numeric input control on the screen. This is a
    subclass of :class:`~ggame.sprite.Sprite` and
    :class:`~ggame.mathapp._MathVisual` but most of the inherited
    members are of little use and are not shown in the documentation.


    :param \\*args:
        See below
    :param \\**kwargs:
        See below

    :Required Arguments:
        * **pos**  (*tuple(float,float)*) Screen position of the slider, which may
            be a literal tuple of floats, or a reference to any object or
            function that returns or evaluates to a tuple of floats.
        * **minval** (*float*) The minimum value of the slider
        * **maxval** (*float*) The maximum value of the slider
        * **initial** (*float*) The initial value of the slider


    :Optional Keyword Arguments:
        * **steps** (*int*) Number of steps between minval and maxval (default 50)
        * **leftkey** (*str*) Name of a keyboard key that will make the
            slider control step down (move left) (default None). See
            :class:`~ggame.event.KeyEvent` for a list of names.
        * **rightkey** (*str*) Name of a keyboard key that will make the slider
            control step up (move right) (default None)
        * **centerkey** (*str*) Name of a keyboard key that will make the slider
            move to its center position (default None)
        * **positioning** (*str*) One of 'logical' or 'physical'
        * **size** (*int*) Width of the slider (in pixels)
        * **color** (*Color*) Valid :class:`~ggame.asset.Color` object
        * **style** (*LineStyle*) Valid :class:`~ggame.asset.LineStyle` object

    Example:

    .. literalinclude:: ../examples/sliderslider.py

    """

    _posinputsdef = ["pos"]
    _nonposinputsdef = ["minval", "maxval", "initial"]

    def __init__(self, *args, **kwargs):
        super().__init__(RectangleAsset(1, 1), *args, **kwargs)
        self._val = self._nposinputs.initial()  # pylint: disable=no-member
        self._steps = kwargs.get("steps", 50)
        self._step = (
            self._nposinputs.maxval()  # pylint: disable=no-member
            - self._nposinputs.minval()  # pylint: disable=no-member
        ) / self._steps
        self._leftctrl = kwargs.get("leftkey", None)
        self._rightctrl = kwargs.get("rightkey", None)
        self._centerctrl = kwargs.get("centerkey", None)
        self.selectable = True  # must be after super init!
        self.strokable = True  # this enables grabbing/slideing the thumb
        self.thumbcaptured = False
        self._thumbwidth = max(self._stdinputs.width() / 40, 1)
        self._thumb = Sprite(
            RectangleAsset(
                self._thumbwidth,
                self._stdinputs.size() - 2,
                LineStyle(1, self._stdinputs.color()),
                self._stdinputs.color(),
            ),
            self._thumbXY(),
        )
        self.touchAsset()
        if self._leftctrl:
            MathApp.listenKeyEvent("keydown", self._leftctrl, self._moveLeft)
        if self._rightctrl:
            MathApp.listenKeyEvent("keydown", self._rightctrl, self._moveRight)
        if self._centerctrl:
            MathApp.listenKeyEvent("keydown", self._centerctrl, self._moveCenter)

    def _thumbXY(self):
        minval = self._nposinputs.minval()  # pylint: disable=no-member
        maxval = self._nposinputs.maxval()  # pylint: disable=no-member
        return (
            self._spposinputs.pos[0]
            + (self._val - minval)
            * (self._sstdinputs.width - self._thumbwidth)
            / (maxval - minval),
            self._spposinputs.pos[1] + 1,
        )

    def __call__(self):
        return self._val

    @property
    def value(self):
        """
        Report value of the slider. Attribute is get-able and set-able.
        """
        return self._val

    @value.setter
    def value(self, val):
        self._setval(val)

    def _buildAsset(self):
        self._setThumb()
        return RectangleAsset(
            self._stdinputs.width(),
            self._stdinputs.size(),
            line=self._stdinputs.style(),
            fill=Color(0, 0),
        )

    def _setThumb(self):
        self._thumb.position = self._thumbXY()

    def step(self):
        pass

    def _setval(self, val):
        minval = self._nposinputs.minval()  # pylint: disable=no-member
        maxval = self._nposinputs.maxval()  # pylint: disable=no-member
        if val <= minval:
            self._val = minval
        elif val >= maxval:
            self._val = maxval
        else:
            self._val = (
                round((val - minval) * self._steps / (maxval - minval)) * self._step
                + minval
            )
        self._setThumb()

    def increment(self, step):
        """
        Increment the slider value.

        :param float step: The amount by which the slider control should be adjusted.
        :returns: None
        """

        self._setval(self._val + step)

    def select(self):
        super().select()
        if not self._leftctrl:
            MathApp.listenKeyEvent("keydown", "left arrow", self._moveLeft)
        if not self._rightctrl:
            MathApp.listenKeyEvent("keydown", "right arrow", self._moveRight)
        MathApp.listenMouseEvent("click", self._mouseClick)

    def unselect(self):
        super().unselect()
        try:
            if not self._leftctrl:
                MathApp.unlistenKeyEvent("keydown", "left arrow", self._moveLeft)
            if not self._rightctrl:
                MathApp.unlistenKeyEvent("keydown", "right arrow", self._moveRight)
            MathApp.unlistenMouseEvent("click", self._mouseClick)
        except ValueError:
            pass

    def _mouseClick(self, event):
        if self.physicalPointTouching((event.x, event.y)):
            if event.x > self._thumb.x + self._thumbwidth:
                self._moveRight(event)
            elif event.x < self._thumb.x:
                self._moveLeft(event)

    def _moveLeft(self, _event):
        self.increment(-self._step)

    def _moveRight(self, _event):
        self.increment(self._step)

    def _moveCenter(self, _event):
        self._val = (self._snposinputs.minval + self._snposinputs.maxval) / 2
        self._setThumb()

    def canstroke(self, ppos):
        """
        Function returns true if the given physical position corresponds with a part
        of the slider that can be dragged (i.e. the thumb).

        :param (float,float) ppos: Physical screen coordinates.
        :return: True if the position represents a draggable part of the control.
        :rtype: boolean

        """
        return self.physicalPointTouchingThumb(ppos)

    def stroke(self, ppos, pdisp):
        """
        Function performs the action of stroking or click-dragging on the slider
        control (i.e. dragging the thumb).

        :param (float, float) ppos: Physical screen coordinates.
        :param (float, float) pdisp: Physical displacement vector.
        :return: None

        """
        _ppos = self._spposinputs.pos
        minval = self._snposinputs.minval
        maxval = self._snposinputs.maxval
        xpos = ppos[0] + pdisp[0]
        self.value = (xpos - _ppos[0]) * (
            maxval - minval
        ) / self._sstdinputs.width + minval

    def physicalPointTouching(self, ppos):
        _ppos = self._spposinputs.pos
        return (
            ppos[0] >= _ppos[0]
            and ppos[0] <= _ppos[0] + self._sstdinputs.width
            and ppos[1] >= _ppos[1]
            and ppos[1] <= _ppos[1] + self._sstdinputs.size
        )

    def physicalPointTouchingThumb(self, ppos):
        """
        Determine if a physical screen location is touching the slider "thumb".

        :param (float, float) ppos: Physical screen coordinates.
        :returns: True if touching, False otherwise.
        :rtype: boolean
        """

        thumbpos = self._thumbXY()
        return (
            ppos[0] >= thumbpos[0]
            and ppos[0] <= thumbpos[0] + self._thumbwidth + 2
            and ppos[1] >= thumbpos[1]
            and ppos[1] <= thumbpos[1] + self._sstdinputs.size - 2
        )

    def translate(self, pdisp):
        pass

    def destroy(self):
        self._thumb.destroy()
        super().destroy()
