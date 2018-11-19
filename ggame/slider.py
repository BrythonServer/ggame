from ggame.mathapp import MathApp, _MathVisual
from ggame.asset import RectangleAsset
from ggame.sprite import Sprite

class Slider(_MathVisual):
    
    posinputsdef = ['pos']
    nonposinputsdef = ['minval','maxval','initial']

    def __init__(self, *args, **kwargs):
        super().__init__(
            RectangleAsset(1, 1), *args, **kwargs)
        self._val = self.nposinputs.initial()
        self._steps = kwargs.get('steps', 50)
        self._step = (self.nposinputs.maxval()-self.nposinputs.minval())/self._steps
        self._leftctrl = kwargs.get('leftkey', None)
        self._rightctrl = kwargs.get('rightkey', None)
        self._centerctrl = kwargs.get('centerkey', None)
        self.selectable = True  # must be after super init!
        self.strokable = True  # this enables grabbing/slideing the thumb
        self.thumbcaptured = False
        self._thumbwidth = max(self.stdinputs.width()/40, 1)
        self.thumb = Sprite(RectangleAsset(self._thumbwidth, 
            self.stdinputs.size()-2, LineStyle(1, self.stdinputs.color()), self.stdinputs.color()), 
            self.thumbXY())
        self._touchAsset()
        if self._leftctrl:
            MathApp.listenKeyEvent("keydown", self._leftctrl, self.moveLeft)
        if self._rightctrl:
            MathApp.listenKeyEvent("keydown", self._rightctrl, self.moveRight)
        if self._centerctrl:
            MathApp.listenKeyEvent("keydown", self._centerctrl, self.moveCenter)

    def thumbXY(self):
        minval = self.nposinputs.minval()
        maxval = self.nposinputs.maxval()
        return (self.spposinputs.pos[0]+(self._val-minval)*
                (self.sstdinputs.width-self._thumbwidth)/(maxval-minval),
                self.spposinputs.pos[1]+1)
            
    def __call__(self):
        return self._val

    @property
    def value(self):
        return self._val
        
    @value.setter
    def value(self, val):
        self._setval(val)

    def _buildAsset(self):
        self.setThumb()
        return RectangleAsset(
            self.stdinputs.width(), self.stdinputs.size(), 
            line=self.stdinputs.style(), fill=Color(0,0))

    def setThumb(self):
        self.thumb.position = self.thumbXY()
                
    def step(self):
        pass
    
    def _setval(self, val):
        minval = self.nposinputs.minval()
        maxval = self.nposinputs.maxval()
        if val <= minval:
            self._val = minval
        elif val >= maxval:
            self._val = maxval
        else:
            self._val = round((val - minval)*self._steps/(maxval-minval))*self._step + minval
        self.setThumb()
        
    def increment(self, step):
        self._setval(self._val + step)
        
    def select(self):
        super().select()
        if not self._leftctrl:
            MathApp.listenKeyEvent("keydown", "left arrow", self.moveLeft)
        if not self._rightctrl:
            MathApp.listenKeyEvent("keydown", "right arrow", self.moveRight)
        MathApp.listenMouseEvent("click", self.mouseClick)

    def unselect(self):
        super().unselect()
        try:
            if not self._leftctrl:
                MathApp.unlistenKeyEvent("keydown", "left arrow", self.moveLeft)
            if not self._rightctrl:
                MathApp.unlistenKeyEvent("keydown", "right arrow", self.moveRight)
            MathApp.unlistenMouseEvent("click", self.mouseClick)
        except ValueError:
            pass

    def mouseClick(self, event):
        if self.physicalPointTouching((event.x, event.y)):
            if event.x > self.thumb.x + self._thumbwidth:
                self.moveRight(event)
            elif event.x < self.thumb.x:
                self.moveLeft(event)
                
    def moveLeft(self, event):
        self.increment(-self._step)

    def moveRight(self, event):
        self.increment(self._step)
        
    def moveCenter(self, event):
        self._val = (self.snposinputs.minval + self.snposinputs.maxval)/2
        self.setThumb()
        
    def canstroke(self, ppos):
        return self.physicalPointTouchingThumb(ppos)
        
    def stroke(self, ppos, pdisp):
        _ppos = self.spposinputs.pos
        minval = self.snposinputs.minval
        maxval = self.snposinputs.maxval
        xpos = ppos[0] + pdisp[0]
        self.value = (xpos - _ppos[0])*(maxval-minval)/self.sstdinputs.width + minval

    def physicalPointTouching(self, ppos):
        _ppos = self.spposinputs.pos
        return (ppos[0] >= _ppos[0] and 
            ppos[0] <= _ppos[0] + self.sstdinputs.width and
            ppos[1] >= _ppos[1] and 
            ppos[1] <= _ppos[1] + self.sstdinputs.size)

    def physicalPointTouchingThumb(self, ppos):
        thumbpos = self.thumbXY()
        return (ppos[0] >= thumbpos[0] and 
            ppos[0] <= thumbpos[0] + self._thumbwidth + 2 and
            ppos[1] >= thumbpos[1] and 
            ppos[1] <= thumbpos[1] + self.sstdinputs.size - 2)

    def translate(self, pdisp):
        pass

