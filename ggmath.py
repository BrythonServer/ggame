# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from ggame import TextAsset, ImageAsset, PolygonAsset, RectangleAsset
from abc import ABCMeta, abstractmethod
from operator import add

from math import sin, cos, sqrt, pi
from time import time



class _MathDynamic(metaclass=ABCMeta):
    
    def __init__(self):
        self._dynamic = False  # not switched on, by default!
    
    def destroy(self):
        MathApp._removeDynamic(self)

    @abstractmethod
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
        self.selected = False
    
    def destroy(self):
        MathApp._removeVisual(self)
        MathApp._removeMovable(self)
        _MathDynamic.destroy(self)
        Sprite.destroy(self)

    def _updateAsset(self, asset):
        visible = self.GFX.visible
        if App._win != None:
            App._win.remove(self.GFX)
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
            
    @abstractmethod
    def _newAsset(self):    
        pass

    @abstractmethod
    def _touchAsset(self):
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
            
            
    def __call__(self):
        return self._val

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
    
    def increment(self, step):
        self._val = self._val + step
        if self._val <= self._min:
            self._val = self._min
        elif self._val >= self._max:
            self._val = self._max
        self.setThumb()
        
    def select(self):
        super().select()
        MathApp.listenKeyEvent("keydown", "left arrow", self.moveLeft)
        MathApp.listenKeyEvent("keydown", "right arrow", self.moveRight)
        MathApp.listenMouseEvent("click", self.mouseClick)

    def unselect(self):
        super().unselect()
        try:
            MathApp.unlistenKeyEvent("keydown", "left arrow", self.moveLeft)
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
    
    
    def physicalPointTouching(self, ppos):
        return (ppos[0] >= self._ppos[0] and 
            ppos[0] <= self._ppos[0] + self._width and
            ppos[1] >= self._ppos[1] and 
            ppos[1] <= self._ppos[1] + self._size)

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
                style="{0}px Arial".format(self._size), 
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
                style="{0}px Arial".format(size),
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
    
    def __init__(self, center, radius, style=LineStyle(1, Color(0,1)), fill=Color(0,1)):
        """
        Radius may be scalar or point
        """
        self._center = self.Eval(center)  # save function
        self._radius = self.Eval(radius)
        self._style = style
        self._color = fill
        self._pcenter = MathApp.logicalToPhysical(self._center())
        try:
            self._pradius = MathApp.distance(self._center(), self._radius()) * MathApp.scale
        except AttributeError:
            self._pradius = self._radius()*MathApp.scale
            
        super().__init__(CircleAsset(self._pcenter, self._pradius, 
            style, fill), self._pcenter)

    def _newAsset(self, center, radius, fill, style):
        pcenter = MathApp.logicalToPhysical(center())
        try:
            pradius = center().distanceTo(radius) * MathApp.scale
        except AttributeError:
            pradius = radius * MathApp.scale
        if pcenter != self._pcenter or pradius != self._pradius:
            self._pcenter = pcenter
            self._pradius = pradius
            self._updateAsset(CircleAsset(self._pcenter, self._pradius, style, fill))
            self.position = pcenter

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
    time = time()
    
    def __init__(self, scale=_scale):
        super().__init__()
        MathApp._scale = scale   # pixels per unit
        # register event callbacks
        self.listenMouseEvent("click", self.handleMouseClick)
        self.listenMouseEvent("mousedown", self.handleMouseDown)
        self.listenMouseEvent("mouseup", self.handleMouseUp)
        self.listenMouseEvent("mousemove", self.handleMouseMove)
        self.listenMouseEvent("wheel", self.handleMouseWheel)
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseX = self.mouseY = None
        self._touchAllVisuals()
        self.selectedObj = None

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
        for obj in self._mathMovableList:
            if obj.physicalPointTouching((event.x, event.y)):
                self.mouseCapturedObject = obj
                break

    def handleMouseUp(self, event):
        self.mouseDown = False
        self.mouseCapturedObject = None

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
            else:
                lmove = self.translatePhysicalToLogical((dx, dy))
                MathApp._xcenter -= lmove[0]
                MathApp._ycenter -= lmove[1]
                self._touchAllVisuals()
                        

    def handleMouseWheel(self, event):
        zoomfactor = event.wheelDelta/100
        zoomfactor = 1+zoomfactor if zoomfactor > 0 else 1+zoomfactor
        if zoomfactor > 1.2:
            zoomfactor = 1.2
        elif zoomfactor < 0.8:
            zoomfactor = 0.8
        MathApp._scale *= zoomfactor
        self._touchAllVisuals()
     
    @classmethod   
    def distance(cls, pos1, pos2):
        return sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
        
    @classmethod
    @property
    def scale(cls):
        return MathApp._scale
            
    @classmethod
    def _addVisual(cls, obj):
        if isinstance(obj, _MathVisual):
            cls._mathVisualList.append(obj)
            
    @classmethod
    def _removeVisual(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathVisualList:
            cls._mathVisualList.remove(obj)

    @classmethod
    def _addDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and obj not in cls._mathDynamicList:
            cls._mathDynamicList.append(obj)
            
    @classmethod
    def _removeDynamic(cls, obj):
        if isinstance(obj, _MathDynamic) and obj in cls._mathDynamicList:
            cls._mathDynamicList.remove(obj)

    @classmethod
    def _addMovable(cls, obj):
        if isinstance(obj, _MathVisual) and obj not in cls._mathMovableList:
            cls._mathMovableList.append(obj)
            
    @classmethod
    def _removeMovable(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathMovableList:
            cls._mathMovableList.remove(obj)

    @classmethod
    def _addSelectable(cls, obj):
        if isinstance(obj, _MathVisual) and obj not in cls._mathSelectableList:
            cls._mathSelectableList.append(obj)
            
    @classmethod
    def _removeSelectable(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathSelectableList:
            cls._mathSelectableList.remove(obj)


class PointMass(ImagePoint):

    def __init__(self, pos):
        super().__init__(pos, 'bunny.png')
        self.mass = 1
        self.lastTime = MathApp.time
        self.V = (0,0)
        self.g = -9.81   #0
        self._setDynamic() # always dynamic

    def step(self):
        dt = MathApp.time - self.lastTime
        self.lastTime = MathApp.time
        A = self.acceleration
        dV = tuple(a*dt for a in A)
        A = tuple(v*dt for v in self.V)
        B = tuple(a*0.5*dt*dt for a in A)
        dP = tuple(map(add, A, B))
        self.V = tuple(map(add, self.V, dV))
        self._pos = self.Eval(tuple(map(add, self._pos(), dP)))
        super().step()

    @property
    def force(self):
        return self.forceAt(self._pos)
    
    def forceAt(self, pos):
        return self.forceGrav(pos)
    
    def forceGrav(self, pos):
        return (0,self.mass*self.g)
      
    @property
    def acceleration(self):
        F = self.force
        return tuple(f/self.mass for f in F)
        



# test code here
if __name__ == "__main__":
    
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
    

    p1 = Point((0,0))
    p1.movable = True
    c1 = Circle(p1, 1.5)
    
    s1 = Slider((200, 400), 0, 10, 2, positioning='physical',
        leftkey="a", rightkey="d", centerkey="s")
    
    p2 = Point((2,0))
    p2.movable = True
    p3 = Point((3,0))

    t = Timer()
    p4 = Point(lambda :(3, (int(t.time*100) % 400)/100))
    
    #p5 = Point(lambda :nextcoord())

    ip1 = ImagePoint((0.1,0), 'bunny.png')


    
    LineSegment(p1,p4)

    l1 = Label((-4,2), lambda: "Elapsed Time: {0:.0}".format(t.time), size=20, width=400, positioning="logical")
    i1 = InputNumeric((200,300), 99.9, size=20, positioning="physical")
    #l2 = Label((-4,1), lambda: "{0}".format(i1()), size=20)
    l3 = Label((-4,1), lambda: "{0:4.2f}".format(s1()), size=20)
    b1 = InputButton((200,350), "RESET", lambda: t.reset(), size=20, positioning="physical")
    
    
    t.callAfter(1, one)
    #t.callAfter(2, two)
    #t.callAfter(3, three)
    #t.callAt(10, ten)
    t.callEvery(1, tick)
    t.callEvery(0.1, rotate)
    

    ap = MathApp(100)
    ap.run()