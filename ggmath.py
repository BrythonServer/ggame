# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from ggame import TextAsset, ImageAsset, PolygonAsset, RectangleAsset
from abc import ABCMeta, abstractmethod
from operator import add
from collections import namedtuple

from math import sin, cos, sqrt, pi
from time import time



class _MathDynamic(metaclass=ABCMeta):
    
    def __init__(self):
        self._dynamic = False  # not switched on, by default!
    
    def destroy(self):
        MathApp._removeDynamic(self)

    def step(self):
        pass
    
    def Eval(self, val):
        if callable(val):
            self._setDynamic() # dynamically defined .. must step
            return val
        else:
            return lambda : val  
            
    def _setDynamic(self):
        MathApp._addDynamic(self)
        self._dynamic = True
            

class _MathVisual(Sprite, _MathDynamic, metaclass=ABCMeta):
    
    def __init__(self, asset, pos):
        MathApp._addVisual(self)
        Sprite.__init__(self, asset, pos)
        _MathDynamic.__init__(self)
        self._movable = False
        self._selectable = False
        self._strokable = False
        self.selected = False
    
    def destroy(self):
        MathApp._removeVisual(self)
        MathApp._removeMovable(self)
        MathApp._removeStrokable(self)
        _MathDynamic.destroy(self)
        Sprite.destroy(self)

    def _updateAsset(self, asset):
        visible = self.GFX.visible
        if App._win != None:
            App._win.remove(self.GFX)
            self.GFX.destroy()
        self.asset = asset
        self.GFX = self.asset.GFX
        self.GFX.visible = visible        
        if App._win != None:
            App._win.add(self.GFX)
            
    @property
    def movable(self):
        return self._movable
        
    @movable.setter
    def movable(self, val):
        if not self._dynamic:
            self._movable = val
            if val:
                MathApp._addMovable(self)
            else:
                MathApp._removeMovable(self)

    @property
    def selectable(self):
        return self._selectable
        
    @selectable.setter
    def selectable(self, val):
        self._selectable = val
        if val:
            MathApp._addSelectable(self)
        else:
            MathApp._removeSelectable(self)

    @property
    def strokable(self):
        return self._strokable
        
    @strokable.setter
    def strokable(self, val):
        self._strokable = val
        if val:
            MathApp._addStrokable(self)
        else:
            MathApp._removeStrokable(self)

    def select(self):
        self.selected = True


    def unselect(self):
        self.selected = False

    def processEvent(self, event):
        pass

    # define how your class responds to mouse clicks - returns True/False
    @abstractmethod
    def physicalPointTouching(self, ppos):
        pass
    
    # define how your class responds to being moved (physical units)
    @abstractmethod
    def translate(self, pdisp):
        pass
    
    # define how your class responds to being stroked (physical units)
    def stroke(self, ppos, pdisp):
        pass
    
    # is the mousedown in a place that will result in a stroke?
    def canstroke(self, ppos):
        return False
    
    @abstractmethod
    def _newAsset(self):    
        pass

    @abstractmethod
    def _touchAsset(self):
        pass

class _MathVisual2(Sprite, _MathDynamic, metaclass=ABCMeta):
    
    posinputsdef = []  # a list of names (string) of required positional inputs
    nonposinputsdef = []  # a list of names (string) of required non positional inputs
    defaultsize = 15
    defaultwidth = 200
    defaultcolor = Color(0, 1)
    defaultstyle = LineStyle(1, Color(0, 1))
    
    
    def __init__(self, asset, *args, **kwargs):
        """
        Required inputs
        
        * **asset** a ggame asset
        * **args** the list of required positional and nonpositional arguments,
          as named in the posinputsdef and nonposinputsdef lists
        * **kwargs** all other optional keyword arguments:
          positioning - logical (default) or physical, size, width, color, style
          movable
        
        """
        
        MathApp._addVisual(self)
        #Sprite.__init__(self, asset, args[0])
        _MathDynamic.__init__(self)
        self._movable = False
        self._selectable = False
        self._strokable = False
        self.selected = False
        # 
        self.positioning = kwargs.get('positioning', 'logical')
        # positional inputs
        self.PI = namedtuple('PI', self.posinputsdef)
        # nonpositional inputs
        self.NPI = namedtuple('NPI', self.nonposinputsdef)
        # standard inputs (not positional)
        standardargs = ['size','width','color','style']
        self.SI = namedtuple('SI', standardargs)
        # correct number of args?
        if len(args) != len(self.posinputsdef) + len(self.nonposinputsdef):
            raise TypeError("Incorrect number of parameters provided")
        self.args = args
        # generated named tuple of functions from positional inputs
        self.posinputs = self.PI(*[self.Eval(p) for p in args][:len(self.posinputsdef)])
        self._getPhysicalInputs()
        # first positional argument must be a sprite position!
        Sprite.__init__(self, asset, self.pposinputs[0])
        # generated named tuple of functions from nonpositional inputs
        if len(self.nonposinputsdef) > 0:
            self.nposinputs = self.NPI(*[self.Eval(p) for p in args][(-1*len(self.nonposinputsdef)):])
        else:
            self.nposinputs = []
        self.stdinputs = self.SI(self.Eval(kwargs.get('size', self.defaultsize)),
                                    self.Eval(kwargs.get('width', self.defaultwidth)),
                                    self.Eval(kwargs.get('color', self.defaultcolor)),
                                    self.Eval(kwargs.get('style', self.defaultstyle)))
        self.sposinputs = self.PI(*[0]*len(self.posinputs))
        self.spposinputs = self.PI(*self.pposinputs)
        self.snposinputs = self.NPI(*[0]*len(self.nposinputs))
        self.sstdinputs = self.SI(*[0]*len(self.stdinputs))

    def step(self):
        self._touchAsset()
        
    def _saveInputs(self, inputs):
        self.sposinputs, self.spposinputs, self.snposinputs, self.sstdinputs = inputs
        
    def _getInputs(self):
        self._getPhysicalInputs()
        return (self.PI(*[p() for p in self.posinputs]),
            self.PI(*self.pposinputs),
            self.NPI(*[p() for p in self.nposinputs]),
            self.SI(*[p() for p in self.stdinputs]))

    
    def _getPhysicalInputs(self):
        """
        Translate all positional inputs to physical
        """
        pplist = []
        if self.positioning == 'logical':
            for p in self.posinputs:
                pval = p()
                try:
                    pp = MathApp.logicalToPhysical(pval)
                except AttributeError:
                    pp = MathApp._scale * pval
                pplist.append(pp)
        else:
            # already physical
            pplist = [p() for p in self.posinputs]
        self.pposinputs = self.PI(*pplist)
    
    def _inputsChanged(self, saved):
        return self.spposinputs != saved[1] or self.snposinputs != saved[2] or self.sstdinputs != saved[3]

    
    def destroy(self):
        MathApp._removeVisual(self)
        MathApp._removeMovable(self)
        MathApp._removeStrokable(self)
        _MathDynamic.destroy(self)
        Sprite.destroy(self)

    def _updateAsset(self, asset):
        if type(asset) != ImageAsset:
            visible = self.GFX.visible
            if App._win != None:
                App._win.remove(self.GFX)
                self.GFX.destroy()
            self.asset = asset
            self.GFX = self.asset.GFX
            self.GFX.visible = visible        
            if App._win != None:
                App._win.add(self.GFX)
            self.position = self.pposinputs.pos
            
    @property
    def movable(self):
        return self._movable
        
    @movable.setter
    def movable(self, val):
        if not self._dynamic:
            self._movable = val
            if val:
                MathApp._addMovable(self)
            else:
                MathApp._removeMovable(self)

    @property
    def selectable(self):
        return self._selectable
        
    @selectable.setter
    def selectable(self, val):
        self._selectable = val
        if val:
            MathApp._addSelectable(self)
        else:
            MathApp._removeSelectable(self)

    @property
    def strokable(self):
        return self._strokable
        
    @strokable.setter
    def strokable(self, val):
        self._strokable = val
        if val:
            MathApp._addStrokable(self)
        else:
            MathApp._removeStrokable(self)

    def select(self):
        self.selected = True


    def unselect(self):
        self.selected = False

    def processEvent(self, event):
        pass

    # define how your class responds to mouse clicks - returns True/False
    @abstractmethod
    def physicalPointTouching(self, ppos):
        pass
    
    # define how your class responds to being moved (physical units)
    @abstractmethod
    def translate(self, pdisp):
        pass
    
    # define how your class responds to being stroked (physical units)
    def stroke(self, ppos, pdisp):
        pass
    
    # is the mousedown in a place that will result in a stroke?
    def canstroke(self, ppos):
        return False
    
    def _touchAsset(self):
        inputs = self._getInputs()
        if self._inputsChanged(inputs):
            self._saveInputs(inputs)
            self._updateAsset(self._buildAsset())
    
    @abstractmethod
    def _buildAsset(self):
        pass
    

class Label2(_MathVisual2):
    
    posinputsdef = ['pos']
    nonposinputsdef = ['text']
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** position of label
        * **text** text contents of label
        """
        super().__init__(TextAsset(""), *args, **kwargs)
        self._touchAsset()

    def _buildAsset(self):
        return TextAsset(self.nposinputs.text(), 
                            style="{0}px Courier".format(self.stdinputs.size()),
                            width=self.stdinputs.width(),
                            fill=self.stdinputs.color())

    def __call__(self):
        return self.nposinputs.text()

    def physicalPointTouching(self, ppos):
        _ppos = self.spposinputs.pos
        return (ppos[0] >= _ppos[0] and 
            ppos[0] <= _ppos[0] + self.sstdinputs.width and
            ppos[1] >= _ppos[1] and 
            ppos[1] <= _ppos[1] + self.sstdinputs.size)

    def translate(self, pdisp):
        pass


class InputNumeric2(Label2):
    
    def __init__(self, pos, val, **kwargs):
        """
        Required Inputs
        
        * **pos** position of button
        * **val** initial value of input
        
        Optional Keyword Input
        * **fmt** a Python format string (default is {0.2})
        """
        self._fmt = kwargs.get('fmt', '{0.2}')
        self._val = self.Eval(val)()  # initialize to simple numeric
        self._savedval = self._val
        self._updateText()
        super().__init__(pos, self._textValue, **kwargs)
        self.selectable = True
        
    def _textValue(self):
        return self._text()

    def _updateText(self):
        self._text = self.Eval(self._fmt.format(self._val))

    def processEvent(self, event):
        if event.key in "0123456789insertdelete":
            key = event.key
            if event.key == 'insert':
                key = '-'
            elif event.key == 'delete':
                key = '.'
            if self._text() == "0":
                self._text = self.Eval("")
            self._text = self.Eval(self._text() + key)
            self._touchAsset()
        elif event.key in ['enter','escape']:
            if event.key == 'enter':
                try:
                    self._val = float(self._text())
                except ValueError:
                    self._val = self._savedval
                self._savedval = self._val
            self.unselect()
            

    def select(self):
        super().select()
        self._savedval = self._val
        self._val = 0
        self._updateText()
        self._touchAsset()
        MathApp.listenKeyEvent("keypress", "*", self.processEvent)

    def unselect(self):
        super().unselect()
        self._val = self._savedval
        self._updateText()
        self._touchAsset()
        try:
            MathApp.unlistenKeyEvent("keypress", "*", self.processEvent)
        except ValueError:
            pass

    def __call__(self):
        return self._val


class InputButton2(Label2):
    
    def __init__(self, pos, text, callback, **kwargs):
        """
        Required Inputs
        
        * **pos** position of button
        * **text** text of button
        * **callback** reference of a function to execute, passing this button object
        """
        super().__init__(pos, text, **kwargs)
        self._touchAsset()
        self._callback = callback
        self.selectable = True

    def _buildAsset(self):
        return TextAsset(self.nposinputs.text(), 
                            style="bold {0}px Courier".format(self.stdinputs.size()),
                            width=self.stdinputs.width(),
                            fill=self.stdinputs.color())

    def select(self):
        super().select()
        if self._callback: self._callback(self)
        self.unselect()

    def unselect(self):
        super().unselect()

        
class _Point2(_MathVisual2, metaclass=ABCMeta):

    posinputsdef = ['pos']
    nonposinputsdef = []

    def __init__(self, pos, asset, **kwargs):
        """
        Required Inputs
        
        * **pos** position of point
        * **asset** asset object to use
        """
        super().__init__(asset, pos, **kwargs)
        self._touchAsset()
        self.center = (0.5, 0.5)

    def __call__(self):
        return self.posinputs.pos

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


"""
class ImagePoint2(_Point2):
    def __init__(self, pos, url, **kwargs):
        self._url = url
        #self._frame = kwargs.get('frame', None)
        #self._qty = kwargs.get('qty', 1)
        #self._direction = kwargs.get('direction', 'horizontal')
        #self._margin = kwargs.get('margin', 0)
        super().__init__(pos, self._buildAsset(), **kwargs)

    def _buildAsset(self):
        print("in ImagePoint2 buildAsset for ", self._url)
        return CircleAsset(10, self.defaultstyle, self.defaultcolor)
        #return ImageAsset(self._url)
        
        
class ImagePoint(_Point):
    def __init__(self, pos, url, frame=None, qty=1, direction='horizontal', margin=0):
        super().__init__(pos, ImageAsset(url, frame, qty, direction, margin))

    def _newAsset(self, pos):
        ppos = MathApp.logicalToPhysical(pos())
        if ppos != self._ppos:
            self._ppos = ppos
            self.position = ppos

    def _touchAsset(self):
        self._newAsset(self._pos)


 
"""



class Point2(_Point2):


    defaultsize = 5
    defaultstyle = LineStyle(0, Color(0, 1))


    def __init__(self, pos, **kwargs):
        """
        Required Inputs
        
        * **pos** position of point
        """
        size = kwargs.get('size', self.defaultsize)
        color = kwargs.get('color', self.defaultcolor)
        style = kwargs.get('style', self.defaultstyle)
        super().__init__(pos, CircleAsset(size, style, color), **kwargs)


    def _buildAsset(self):
        return CircleAsset(self.stdinputs.size(),
                            self.stdinputs.style(),
                            self.stdinputs.color())

# Can we simply handle another child of _Point2?
class ImagePoint2(_Point2):


    defaultsize = 5
    defaultstyle = LineStyle(0, Color(0, 1))


    def __init__(self, pos, url, **kwargs):
        """
        Required Inputs
        
        * **pos** position of point
        * **url** location of image file
        
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
        size = kwargs.get('size', self.defaultsize)
        color = kwargs.get('color', self.defaultcolor)
        style = kwargs.get('style', self.defaultstyle)
        self._imageasset = ImageAsset(url, frame, qty, direction, margin)
        super().__init__(pos, self._imageasset, **kwargs)


    def _buildAsset(self):
        return self._imageasset




class Slider2(_MathVisual2):
    
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

    
class Timer(_MathDynamic):
    
    def __init__(self):
        super().__init__()
        self.once = []
        self.callbacks = {}
        self.reset()
        self.step()
        self._start = self._reset  #first time
        self.next = None
        MathApp._addDynamic(self)  # always dynamically defined
        
    def reset(self):
        self._reset = MathApp.time
        
    def step(self):
        nexttimers = []
        calllist = []
        self.time = MathApp.time - self._reset
        while self.once and self.once[0][0] <= MathApp.time:
            tickinfo = self.once.pop(0)
            if tickinfo[1]:  # periodic?
                nexttimers.append((tickinfo[1], self.callbacks[tickinfo][0]))  # delay, callback
            calllist.append(self.callbacks[tickinfo].pop(0)) # remove callback and queue it
            if not self.callbacks[tickinfo]: # if the callback list is empty
                del self.callbacks[tickinfo] # remove the dictionary entry altogether
        for tickadd in nexttimers:
            self.callAfter(tickadd[0], tickadd[1], True)  # keep it going
        for call in calllist:
            call(self)

    def callAfter(self, delay, callback, periodic=False):
        key = (MathApp.time + delay, delay if periodic else 0)
        self.once.append(key)
        callbacklist = self.callbacks.get(key, [])
        callbacklist.append(callback)
        self.callbacks[key] = callbacklist
        self.once.sort()
        
    def callAt(self, time, callback):
        self.callAfter(time-self.time, callback)
        
    def callEvery(self, period, callback):
        self.callAfter(period, callback, True)

    def __call__(self):
        return self.time

class Slider(_MathVisual):
    
    def __init__(self, pos, minval, maxval, initial, *args, **kwargs):
        self._pos = self.Eval(pos)
        self._min = minval
        self._max = maxval
        self.initial = initial
        self._val = initial
        
        self._steps = kwargs.get('steps', 50)
        self._step = (self._max-self._min)/self._steps
        self._leftctrl = kwargs.get('leftkey', None)
        self._rightctrl = kwargs.get('rightkey', None)
        self._centerctrl = kwargs.get('centerkey', None)
        self._positioning = kwargs.get('positioning', 'logical')
        self._size = kwargs.get('size', 20)
        self._width = kwargs.get('width', 200)
        self.color = kwargs.get('color', Color(0,1))
        if self._positioning == "physical":
            self._ppos = self._pos()
        else:
            self._ppos = MathApp.logicalToPhysical(self._pos())
        
        super().__init__(RectangleAsset(self._width, self._size,
            LineStyle(1, self.color), Color(0,0)), self._ppos)
        self.selectable = True  # must be after super init!
        self.strokable = True  # this enables grabbing/slideing the thumb
        self._thumbwidth = max(self._width/40, 1)
        if self._leftctrl:
            MathApp.listenKeyEvent("keydown", self._leftctrl, self.moveLeft)
        if self._rightctrl:
            MathApp.listenKeyEvent("keydown", self._rightctrl, self.moveRight)
        if self._centerctrl:
            MathApp.listenKeyEvent("keydown", self._centerctrl, self.moveCenter)

        self.thumb = Sprite(RectangleAsset(self._thumbwidth, 
            self._size-2, LineStyle(1, self.color), self.color), 
            self.thumbXY())
            
        self.thumbcaptured = False
            
    def __call__(self):
        return self._val

    @property
    def value(self):
        return self._val
        
    @value.setter
    def value(self, val):
        self._setval(val)

    def thumbXY(self):
        return (self._ppos[0]+(self._val-self._min)*
                (self._width-self._thumbwidth)/(self._max-self._min),
                self._ppos[1]+1)
            
    def _newAsset(self, pos):
        if self._positioning != "physical":
            ppos = MathApp.logicalToPhysical(pos())
        else:
            ppos = pos()
        if ppos != self._ppos:
            self._ppos = ppos
            self.position = ppos
            self.setThumb()
            
    def _touchAsset(self):
        self._newAsset(self._pos)
        
    def setThumb(self):
        self.thumb.position = self.thumbXY()
                
    def step(self):
        pass
    
    def _setval(self, val):
        if val <= self._min:
            self._val = self._min
        elif val >= self._max:
            self._val = self._max
        else:
            #self._val = val
            self._val = round((val - self._min)*self._steps/(self._max-self._min))*self._step + self._min
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
        self._val = (self._min + self._max)/2
        self.setThumb()
        
    def canstroke(self, ppos):
        return self.physicalPointTouchingThumb(ppos)
        
    def stroke(self, ppos, pdisp):
        xpos = ppos[0] + pdisp[0]
        self.value = (xpos - self._ppos[0])*(self._max-self._min)/self._width + self._min

    def physicalPointTouching(self, ppos):
        return (ppos[0] >= self._ppos[0] and 
            ppos[0] <= self._ppos[0] + self._width and
            ppos[1] >= self._ppos[1] and 
            ppos[1] <= self._ppos[1] + self._size)

    def physicalPointTouchingThumb(self, ppos):
        thumbpos = self.thumbXY()
        return (ppos[0] >= thumbpos[0] and 
            ppos[0] <= thumbpos[0] + self._thumbwidth + 2 and
            ppos[1] >= thumbpos[1] and 
            ppos[1] <= thumbpos[1] + self._size - 2)

    def translate(self, pdisp):
        pass
    


class Label(_MathVisual):
    
    def __init__(self, pos, text, positioning="logical", size=10, width=200, color=Color(0,1)):
        self._text = self.Eval(text) # create a *callable* text value function
        self._ptext = self._text()
        self._pos = self.Eval(pos)
        self._positioning = positioning
        self._size = size
        self._width = width
        self._color = color
        if self._positioning == "physical":
            self._ppos = self._pos()
        else:
            self._ppos = MathApp.logicalToPhysical(self._pos())
            
        super().__init__(TextAsset(self._ptext, 
                style="{0}px Courier".format(self._size), 
                width=self._width,
                color=self._color), 
            self._ppos)

    def _newAsset(self, pos, text, size, width, color):    
        if self._positioning != "physical":
            ppos = MathApp.logicalToPhysical(pos())
        else:
            ppos = pos()
        text = text()
        if ppos != self._ppos or text != self._ptext:
            self._ppos = ppos
            self._ptext = text
            self._updateAsset(TextAsset(text, 
                style="{0}px Courier".format(size),
                width=width,
                color=color))
            self.position = ppos
        
    def __call__(self):
        return self._text()

    def _touchAsset(self):
        self._newAsset(self._pos, self._text, self._size, self._width, self._color)

    def step(self):
        self._touchAsset()
    
    def physicalPointTouching(self, ppos):
        return (ppos[0] >= self._ppos[0] and 
            ppos[0] <= self._ppos[0] + self._width and
            ppos[1] >= self._ppos[1] and 
            ppos[1] <= self._ppos[1] + self._size)

    def translate(self, pdisp):
        pass


class InputButton(Label):
    
    def __init__(self, pos, text, callback, positioning="logical", 
            size=10, width=200, color=Color(0,1)):
        self._callback = callback
        super().__init__(pos, text, positioning=positioning,
            size=size, width=width, color=color)
        self.selectable = True

    def select(self):
        super().select()
        self._callback()
        self.unselect()

    def unselect(self):
        super().unselect()

        
class InputNumeric(Label):

    def __init__(self, pos, val, fmt="{0.2}", positioning="logical", size=10, 
            width=200, color=Color(0,1)):
        self._fmt = fmt
        self._val = self.Eval(val)()  # initialize to simple numeric
        self._savedval = self._val
        self._updateText()
        super().__init__(pos, self._text, positioning=positioning, 
            size=size, width=width, color=color)
        self.selectable = True

    def _updateText(self):
        self._text = self.Eval(self._fmt.format(self._val))

    def processEvent(self, event):
        if event.key in "0123456789insertdelete":
            key = event.key
            if event.key == 'insert':
                key = '-'
            elif event.key == 'delete':
                key = '.'
            if self._text() == "0":
                self._text = self.Eval("")
            self._text = self.Eval(self._text() + key)
            self._touchAsset()
        elif event.key in ['enter','escape']:
            if event.key == 'enter':
                try:
                    self._val = float(self._text())
                except ValueError:
                    self._val = self._savedval
                self._savedval = self._val
            self.unselect()
            

    def select(self):
        super().select()
        self._savedval = self._val
        self._val = 0
        self._updateText()
        self._touchAsset()
        MathApp.listenKeyEvent("keypress", "*", self.processEvent)

    def unselect(self):
        super().unselect()
        self._val = self._savedval
        self._updateText()
        self._touchAsset()
        try:
            MathApp.unlistenKeyEvent("keypress", "*", self.processEvent)
        except ValueError:
            pass

    def __call__(self):
        return self._val


class _Point(_MathVisual, metaclass=ABCMeta):
    
    def __init__(self, pos, asset):
        self._pos = self.Eval(pos)  # create a *callable* position function
        self._ppos = MathApp.logicalToPhysical(self._pos()) # physical position
        super().__init__(asset, self._ppos)
        self.center = (0.5, 0.5)
        
    def __call__(self):
        return self._pos()

    def step(self):
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        return MathApp.distance(ppos, self._ppos) < self._size
        
    def translate(self, pdisp):
        ldisp = MathApp.translatePhysicalToLogical(pdisp)
        pos = self._pos()
        self._pos = self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1]))
        self._touchAsset()
        
    def distanceTo(self, otherpoint):
        try:
            pos = self._pos()
            opos = otherpoint._pos()
            return MathApp.distance(self._pos(), otherpoint._pos())
        except AttributeError:
            return otherpoint  # presumably a scalar - use this distance


class Point(_Point):

    def __init__(self, pos, size=5, color=Color(0,1), style=LineStyle(0, Color(0,1))):
        self._size = size
        self._color = color
        self._style = style
        super().__init__(pos, CircleAsset(size, style, color))

    def _newAsset(self, pos, size, color, style):
        ppos = MathApp.logicalToPhysical(pos())
        if size != self._size or color != self._color or style != self._style:
            self._updateAsset(CircleAsset(size, style, color))
            self._size = size
            self._color = color
            self._style = style
            
        if ppos != self._ppos:
            self._ppos = ppos
            self.position = ppos

    def _touchAsset(self):
        self._newAsset(self._pos, self._size, self._color, self._style)



class ImagePoint(_Point):
    def __init__(self, pos, url, frame=None, qty=1, direction='horizontal', margin=0):
        super().__init__(pos, ImageAsset(url, frame, qty, direction, margin))

    def _newAsset(self, pos):
        ppos = MathApp.logicalToPhysical(pos())
        if ppos != self._ppos:
            self._ppos = ppos
            self.position = ppos

    def _touchAsset(self):
        self._newAsset(self._pos)


    

class LineSegment(_MathVisual):
    
    def __init__(self, start, end, style=LineStyle(1, Color(0,1))):
        self._start = self.Eval(start)  # save function
        self._end = self.Eval(end)
        self._style = style
        self._pstart = MathApp.logicalToPhysical(self._start())
        self._pend = MathApp.logicalToPhysical(self._end())
        super().__init__(LineAsset(self._pend[0]-self._pstart[0], 
            self._pend[1]-self._pstart[1], style), self._pstart)

    def _newAsset(self, start, end, style):
        pstart = MathApp.logicalToPhysical(start())
        pend = MathApp.logicalToPhysical(end())
        if pstart != self._pstart or pend != self._pend:
            self._pstart = pstart
            self._pend = pend
            self._updateAsset(LineAsset(pend[0]-pstart[0], pend[1]-pstart[1], style))
            self.position = pstart

    def _touchAsset(self):
        self._newAsset(self._start, self._end, self._style)
    
    @property
    def start(self):
        return self._start()

    @start.setter
    def start(self, val):
        newval = self.Eval(val)
        if newval != self._start:
            self._start = newval
            self._touchAsset()

    @property
    def end(self):
        return self._end()

    @end.setter
    def end(self, val):
        newval = self.Eval(val)
        if newval != self._end:
            self._end = newval
            self._touchAsset()
        
    def step(self):
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        return False
        
    def translate(self, pdisp):
        pass

class Circle(_MathVisual):
    
    def __init__(self, center, radius, style=LineStyle(1, Color(0,1)), fill=Color(0,0)):
        """
        Radius may be scalar or point
        """
        self._center = self.Eval(center)  # save function
        self._radius = self.Eval(radius)
        self._style = style
        self._color = fill
        self._pcenter = MathApp.logicalToPhysical(self._center())
        super().__init__(CircleAsset(0, style, fill), (0,0))
        self._pradius = -1
        self._touchAsset()
        self.fxcenter = self.fycenter = 0.5

    def _newAsset(self, center, radius, fill, style):
        pcenter = MathApp.logicalToPhysical(center())
        try:
            pradius = MathApp.distance(center(), radius()) * MathApp._scale
        except AttributeError:
            pradius = radius() * MathApp._scale
        if pcenter != self._pcenter or pradius != self._pradius:
            self._pcenter = pcenter
            self._pradius = pradius
            asset = self._buildAsset(pcenter, pradius, style, fill)
            self._updateAsset(asset)
            self.position = pcenter

    def _buildAsset(self, pcenter, pradius, style, fill):
        ymax = pcenter[1]+pradius
        ymin = pcenter[1]-pradius
        xmax = pcenter[0]+pradius
        xmin = pcenter[0]-pradius
        try:
            if ymin > MathApp.height or ymax < 0 or xmax < 0 or xmin > MathApp.width:
                return CircleAsset(pradius, style, fill)
            elif pradius > 2*MathApp.width:
                # here begins unpleasant hack to overcome crappy circles
                poly = self._buildPolygon(pcenter, pradius)
                if len(poly):
                    passet = PolygonAsset(poly, style, fill)
                    return passet
        except AttributeError:
            return CircleAsset(pradius, style, fill)
        return CircleAsset(pradius, style, fill)

    def _buildPolygon(self, pcenter, pradius):
        """
        pcenter is in screen relative coordinates.
        returns a coordinate list in circle relative coordinates
        """
        xcepts = [self._findIntercepts(pcenter, pradius, 0,0,0,MathApp.height),
            self._findIntercepts(pcenter, pradius, 0,0,MathApp.width,0),
            self._findIntercepts(pcenter, pradius, MathApp.width,0,MathApp.width,MathApp.height),
            self._findIntercepts(pcenter, pradius, 0,MathApp.height, MathApp.width, MathApp.height)]
        ilist = []
        for x in xcepts:
            if x and len(x) < 2:
                ilist.extend(x)
        #ilist is a list of boundary intercepts that are screen-relative
        if len(ilist) > 1:
            xrange = ilist[-1][0] - ilist[0][0]
            yrange = ilist[-1][1] - ilist[0][1]
            numpoints = 20
            inx = 0
            for i in range(numpoints):
                icepts =  self._findIntercepts(pcenter, pradius, 
                    pcenter[0], pcenter[1], 
                    ilist[0][0] + xrange*(i+1)/(numpoints+1),
                    ilist[0][1] + yrange*(i+1)/(numpoints+1))
                if len(icepts):
                    ilist.insert(inx+1, icepts[0])
                    inx = inx + 1
            self._addBoundaryVertices(ilist, pcenter, pradius)
            ilist.append(ilist[0])
            ilist = [(i[0] - pcenter[0], i[1] - pcenter[1]) for i in ilist]
        return ilist
        
    def _addBoundaryVertices(self, plist, pcenter, pradius):
        """
        Sides 0=top, 1=right, 2=bottom, 3=left
        """
        #figure out rotation in point sequence
        cw = 0
        try:
            rtst = plist[0:3]+[plist[0]]
            for p in range(3):
                cw = cw + (rtst[p+1][0]-rtst[p][0])*(rtst[p+1][1]+rtst[p][1])
        except IndexError:
            #print(plist)
            return
        cw = self._sgn(cw)
        cw = 1 if cw < 0 else 0
        vertices = ((-100,-100),
            (MathApp.width+100,-100),
            (MathApp.width+100,MathApp.height+100),
            (-100,MathApp.height+100))
        nextvertex = [(vertices[0],vertices[1]),
                        (vertices[1],vertices[2]),
                        (vertices[2],vertices[3]),
                        (vertices[3],vertices[0])]
        nextsides = [(3,1),(0,2),(1,3),(2,0)]
        edges = ((None,0),(MathApp.width,None),(None,MathApp.height),(0,None))
        endside = startside = None
        for side in range(4):
            if endside is None and (edges[side][0] == round(plist[-1][0]) or edges[side][1] == round(plist[-1][1])):
                endside = side
            if startside is None and (edges[side][0] == round(plist[0][0]) or edges[side][1] == round(plist[0][1])):
                startside = side
        iterations = 0
        while startside != endside:
            iterations = iterations + 1
            if iterations > 20:
                break
            if endside != None and startside != None:   #  and endside != startside
                plist.append(nextvertex[endside][cw])
                endside = nextsides[endside][cw]

    def _sgn(self, x):
        return 1 if x >= 0 else -1

    def _findIntercepts(self, c, r, x1, y1, x2, y2):
        """
        c (center) and x and y values are physical, screen relative.
        function returns coordinates in screen relative format
        """
        x1n = x1 - c[0]
        x2n = x2 - c[0]
        y1n = y1 - c[1]
        y2n = y2 - c[1]
        dx = x2n-x1n
        dy = y2n-y1n
        dr = sqrt(dx*dx + dy*dy)
        D = x1n*y2n - x2n*y1n
        disc = r*r*dr*dr - D*D
        dr2 = dr*dr
        if disc <= 0:  # less than two solutions
            return []
        sdisc = sqrt(disc)
        x = [(D*dy + self._sgn(dy)*dx*sdisc)/dr2 + c[0],  (D*dy - self._sgn(dy)*dx*sdisc)/dr2 + c[0]]
        y = [(-D*dx + abs(dy)*sdisc)/dr2 + c[1], (-D*dx - abs(dy)*sdisc)/dr2 + c[1]]
        getcoords = lambda x, y, c: [(x,y)] if x>=0 and x<=MathApp.width and y>=0 and y<=MathApp.height else []
        res = getcoords(x[0], y[0], c)
        res.extend(getcoords(x[1], y[1], c))
        return res



    def _touchAsset(self):
        self._newAsset(self._center, self._radius, self._color, self._style)

    @property
    def center(self):
        return self._center()

    @center.setter
    def center(self, val):
        newval = self.Eval(val)
        if newval != self._center:
            self._center = newval
            self._touchAsset()

    @property
    def radius(self):
        return self._radius()

    @radius.setter
    def radius(self, val):
        newval = self.Eval(val)
        if newval != self._radius:
            self._radius = newval
            self._touchAsset()
        
    def step(self):
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        r = MathApp.distance(self._pcenter, ppos)
        inner = self._pradius - self.style.width/2
        outer = self._pradius + self.style.width/2
        return r <= outer and r >= inner

    def translate(self, pdisp):
        pass



class Bunny():
    
    """Bunny class is similar to turtle. Needs refinement.
    
    Example use:
    
        b = Bunny()
        b.PenDown()
        for i in range(100):
            b.Right(1.5)
            b.Move(i/25)

    """
    
    def __init__ (self):
        self.GoTo(0,0)
        self.Color(0)
        self.PenUp() 
        self.SetAngle(0)

    def PenUp(self):
        self.down = False

    def PenDown(self):
        self.down = True
        
    def Color(self, color):
        self.color = Color(color,1)
        
    def GoTo(self, x, y):
        self.pos = (x,y)
        
    def SetAngle(self, a):
        self.angle = a
        
    def Right(self, da):
        self.angle = self.angle - da
        
    def Left(self, da):
        self.angle = self.angle + da
        
    def Move(self, d):
        next = (self.pos[0] + d*cos(self.angle), self.pos[1] + d*sin(self.angle))
        LineSegment(Point(self.pos, 0), Point(next, 0), LineStyle(1, self.color))
        self.pos = next

    #def physicalPointTouching(self, ppos):
    #    return MathApp.distance(ppos, self._ppos) < self._size
        
    #def translate(self, pdisp):
    #    ldisp = MathApp.translatePhysicalToLogical(pdisp)
    #    pos = self._pos()
    #    self._pos = self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1]))
    #    self._touchAsset()


class MathApp(App):
    
    _scale = 200   # pixels per unit
    _xcenter = 0    # center of screen in units
    _ycenter = 0    
    _mathVisualList = [] #
    _mathDynamicList = []
    _mathMovableList = []
    _mathSelectableList = []
    _mathStrokableList = []
    _viewNotificationList = []
    time = time()
    
    def __init__(self, scale=_scale):
        super().__init__()
        MathApp.width = self.width
        MathApp.height = self.height
        MathApp._scale = scale   # pixels per unit
        # register event callbacks
        self.listenMouseEvent("click", self.handleMouseClick)
        self.listenMouseEvent("mousedown", self.handleMouseDown)
        self.listenMouseEvent("mouseup", self.handleMouseUp)
        self.listenMouseEvent("mousemove", self.handleMouseMove)
        self.listenMouseEvent("wheel", self.handleMouseWheel)
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None
        self.mouseX = self.mouseY = None
        self._touchAllVisuals()
        self.selectedObj = None
        MathApp.time = time()

    def step(self):
        MathApp.time = time()
        for spr in self._mathDynamicList:
            spr.step()

    def _touchAllVisuals(self):
        # touch all visual object assets to use scaling
        for obj in self._mathVisualList:
            obj._touchAsset()


    @classmethod
    def logicalToPhysical(cls, lp):
        xxform = lambda xvalue, xscale, xcenter, physwidth: int((xvalue-xcenter)*xscale + physwidth/2)
        yxform = lambda yvalue, yscale, ycenter, physheight: int(physheight/2 - (yvalue-ycenter)*yscale)

        try:
            return (xxform(lp[0], cls._scale, cls._xcenter, cls._win.width),
                yxform(lp[1], cls._scale, cls._ycenter, cls._win.height))
        except AttributeError:
            return lp
            
    @classmethod
    def physicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale, xcenter, physwidth: (xvalue - physwidth/2)/xscale + xcenter
        yxform = lambda yvalue, yscale, ycenter, physheight: (physheight/2 - yvalue)/yscale + ycenter

        try:
            return (xxform(pp[0], cls._scale, cls._xcenter, cls._win.width),
                yxform(pp[1], cls._scale, cls._ycenter, cls._win.height))
        except AttributeError:
            return pp
            
    @classmethod
    def translatePhysicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale: xvalue/xscale
        yxform = lambda yvalue, yscale: -yvalue/yscale

        try:
            return (xxform(pp[0], cls._scale), yxform(pp[1], cls._scale))
        except AttributeError:
            return pp

    @classmethod
    def translateLogicalToPhysical(cls, pp):
        xxform = lambda xvalue, xscale: xvalue*xscale
        yxform = lambda yvalue, yscale: -yvalue*yscale

        try:
            return (xxform(pp[0], cls._scale), yxform(pp[1], cls._scale))
        except AttributeError:
            return pp

    def handleMouseClick(self, event):
        found = False
        for obj in self._mathSelectableList:
            if obj.physicalPointTouching((event.x, event.y)):
                found = True
                if not obj.selected: 
                    obj.select()
                    self.selectedObj = obj
        if not found and self.selectedObj:
            self.selectedObj.unselect()
            self.selectedObj = None

    def handleMouseDown(self, event):
        self.mouseDown = True
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None
        for obj in self._mathMovableList:
            if obj.physicalPointTouching((event.x, event.y)) and not (obj.strokable and obj.canstroke((event.x,event.y))):
                self.mouseCapturedObject = obj
                break
        if not self.mouseCapturedObject:
            for obj in self._mathStrokableList:
                if obj.canstroke((event.x, event.y)):
                    self.mouseStrokedObject = obj
                    break

    def handleMouseUp(self, event):
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None

    def handleMouseMove(self, event):
        if not self.mouseX:
            self.mouseX = event.x
            self.mouseY = event.y
        dx = event.x - self.mouseX
        dy = event.y - self.mouseY
        self.mouseX = event.x
        self.mouseY = event.y
        if self.mouseDown:
            if self.mouseCapturedObject:
                self.mouseCapturedObject.translate((dx, dy))
            elif self.mouseStrokedObject:
                self.mouseStrokedObject.stroke((self.mouseX,self.mouseY), (dx,dy))
            else:
                lmove = self.translatePhysicalToLogical((dx, dy))
                MathApp._xcenter -= lmove[0]
                MathApp._ycenter -= lmove[1]
                self._touchAllVisuals()
                self._viewNotify("translate")
    
    @property
    def viewPosition(self):
        return (MathApp._xcenter, MathApp._ycenter)
        
    @viewPosition.setter
    def viewPosition(self, pos):
        MathApp._xcenter, MathApp._ycenter = pos
        self._touchAllVisuals()
        self._viewNotify("translate")
        
    def handleMouseWheel(self, event):
        zoomfactor = event.wheelDelta/100
        zoomfactor = 1+zoomfactor if zoomfactor > 0 else 1+zoomfactor
        if zoomfactor > 1.2:
            zoomfactor = 1.2
        elif zoomfactor < 0.8:
            zoomfactor = 0.8
        MathApp._scale *= zoomfactor
        self._touchAllVisuals()
        self._viewNotify("zoom")
        
    @classmethod   
    def addViewNotification(cls, handler):
        cls._viewNotificationList.append(handler)
        
    @classmethod   
    def removeViewNotification(cls, handler):
        cls._viewNotificationList.remove(handler)
    
    def _viewNotify(self, viewchange):
        for handler in self._viewNotificationList:
            handler(viewchange = viewchange, scale = self._scale, center = (self._xcenter, self._ycenter))
        
     
    @classmethod   
    def distance(cls, pos1, pos2):
        return sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
        
    @property
    def scale(self):
        return self._scale
        
    @property
    def width(cls):
        return App._win.width
            
    @classmethod
    def _addVisual(cls, obj):
        """ FIX ME """
        if isinstance(obj, _MathVisual) or isinstance(obj, _MathVisual2):
            cls._mathVisualList.append(obj)
            
    @classmethod
    def _removeVisual(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathVisualList:
            cls._mathVisualList.remove(obj)

    @classmethod
    def _addDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and not obj in cls._mathDynamicList:
            cls._mathDynamicList.append(obj)
            
    @classmethod
    def _removeDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and obj in cls._mathDynamicList:
            cls._mathDynamicList.remove(obj)

    @classmethod
    def _addMovable(cls, obj):
        if (isinstance(obj, _MathVisual) or isinstance(obj, _MathVisual2)) and not obj in cls._mathMovableList:
            cls._mathMovableList.append(obj)
            
    @classmethod
    def _removeMovable(cls, obj):
        if (isinstance(obj, _MathVisual) or isinstance(obj, _MathVisual2)) and obj in cls._mathMovableList:
            cls._mathMovableList.remove(obj)

    @classmethod
    def _addSelectable(cls, obj):
        if (isinstance(obj, _MathVisual) or isinstance(obj, _MathVisual2)) and not obj in cls._mathSelectableList:
            cls._mathSelectableList.append(obj)
            
    @classmethod
    def _removeSelectable(cls, obj):
       if (isinstance(obj, _MathVisual) or isinstance(obj, _MathVisual2))  and obj in cls._mathSelectableList:
            cls._mathSelectableList.remove(obj)

    @classmethod
    def _addStrokable(cls, obj):
        if (isinstance(obj, _MathVisual) or isinstance(obj, _MathVisual2)) and not obj in cls._mathStrokableList:
            cls._mathStrokableList.append(obj)
            
    @classmethod
    def _removeStrokable(cls, obj):
        if (isinstance(obj, _MathVisual) or isinstance(obj, _MathVisual2)) and obj in cls._mathStrokableList:
            cls._mathStrokableList.remove(obj)

    @classmethod
    def _destroy(cls, *args):
        """
        This will clean up any class level storage.
        """ 
        App._destroy(*args)  # hit the App class first
        MathApp._mathVisualList = [] 
        MathApp._mathDynamicList = []
        MathApp._mathMovableList = []
        MathApp._mathSelectableList = []
        MathApp._mathStrokableList = []
        MathApp._viewNotificationList = []
        



# test code here
if __name__ == "__main__":
    
    
    """
    
    index = 0
    coordlist = [(1,1), (2,1), (2,0), (1,2), (1,1)]
    
    def nextcoord():
        global index
        if index == len(coordlist):
            index = 0
        retval = coordlist[index]
        index = index + 1
        return retval
        
    def one(t):
        print("one")
        
    def two(t):
        print("two")
        
    def three(t):
        t.callAt(10, ten)
        print("three")
    
    def ten(t):
        print("ten")
        
    def tick(t):
        print("tick")
        
    #pm1 = PointMass((0.1,0))
    
    def rotate(timer):
        ip1.rotation += 0.01
    



    #p1 = Point((0,0))
    #p1.movable = True
    #c1 = Circle(p1, 1.5, LineStyle(3, Color(0x0000ff,1)), Color(0x0000ff,0.3))
    
    #s1 = Slider((200, 400), 0, 10, 2, positioning='physical',
    #    leftkey="a", rightkey="d", centerkey="s")
    
    #p2 = Point((2,0))
    #p2.movable = True
    #p3 = Point((3,0))

    #t = Timer()
    #p4 = Point(lambda :(3, (int(t.time*100) % 400)/100))
    
    #p5 = Point(lambda :nextcoord())

    #ip1 = ImagePoint((0.1,0), 'bunny.png')


    
    #LineSegment(p1,p4)

    #l1 = Label((-4,2), lambda: "Elapsed Time: {0:.0}".format(t.time), size=20, width=400, positioning="logical")
    #i1 = InputNumeric((200,300), 99.9, size=20, positioning="physical")
    #l2 = Label((-4,1), lambda: "{0}".format(i1()), size=20)
    #l3 = Label((-4,1), lambda: "{0:4.2f}".format(s1()), size=20)
    #b1 = InputButton((200,350), "RESET", lambda: t.reset(), size=20, positioning="physical")
    
    
    #t.callAfter(1, one)
    #t.callAfter(2, two)
    #t.callAfter(3, three)
    #t.callAt(10, ten)
    #t.callEvery(1, tick)
    #t.callEvery(0.1, rotate)

    def step(t):
        global vx, vy, x, y
        fx = 0
        fy = mass * g
        ax = thrust()*cos(sat.rotation)
        ay = fy / mass + thrust()*sin(sat.rotation)
        x = x + vx * tick + 0.5 * ax * tick**2
        y = y + vy * tick + 0.5 * ay * tick**2
        vx = vx + ax*tick
        vy = vy + ay*tick
        
        if y < 0:
            y = 0
            vy = 0
            
        vslider.value = vy
        

    def velocitytext():
        return "Velocity: ({0:2.4},{1:2.4})".format(vx,vy)

    def getposition():
        return (x,y)
    
            
    def turnleft(event):
        sat.rotation += 0.01
        
    def turnright(event):
        sat.rotation -= 0.01

    tick = 0.02
    x = 0
    y = 100
    vx = vy = 0
    mass = 1
    g = -9.81
    
    sat = Rocket(getposition)
    sat.rotation = pi/2
    sat.scale = 0.1
    MathApp.listenKeyEvent('keydown', 'left arrow', turnleft)
    MathApp.listenKeyEvent('keydown', 'right arrow', turnright)

    thrust = Slider((100, 100), -50, 50, 0, positioning='physical', steps=200,
        leftkey="down arrow", rightkey="up arrow", centerkey="space")
    vslider = Slider((100, 125), -50, 50, 0, positioning='physical')
    Label((100,150), velocitytext, size=15, positioning="physical")
    #westp = Point((-100000,0))
    #eastp = Point((100000,0))
    #ground = LineSegment(westp, eastp)


    
    #MathApp.addViewNotification(zoomCheck)
    """


    def step(timer):
        print(id(timer))

    def labelcoords():
        return (100 + vslider1(), 175)
        
    def buttoncoords():
        return (300 + vslider1(), 175)
        
    def labelcolor():
        colorval =   vslider1()
        return Color(colorval*256,1)

    def pressbutton(caller):
        print("button pressed: ", caller)

    #vslider = Slider((100, 125), -50, 50, 0, positioning='physical', steps=10)
    vslider1 = Slider2((100, 150), 0, 250, 125, positioning='physical', steps=10)

    label = Label2(labelcoords, "whatevs", size=15, positioning="physical", color=labelcolor)
    button = InputButton2(buttoncoords, "Press Me", pressbutton, size=15, positioning="physical")
    numinput = InputNumeric2((300, 275), 3.14, positioning="physical")

    
    p1 = Point2((0,0), color=Color(0x008000, 1))
    p1.movable = True
    
    p2 = Point2((0,-1))
    
    p3 = Point2((1.2,0))
    
    

    ip = ImagePoint2((1,0), 'bunny.png')
    #ip = ImagePoint2((1,0))

   
    def zoomCheck(**kwargs):
        viewtype = kwargs.get('viewchange')
        scale = kwargs.get('scale')
        print(ap.scale)
    
    #pcenter = Point((0, -5000000))
    # c1 = Circle((0,-5000000), 5000000, LineStyle(1, Color(0x008040,1)), Color(0x008400,0.5))
    ap = MathApp()

    #ap.addViewNotification(zoomCheck)
    ap.run()
    
    
    """
    """
    
