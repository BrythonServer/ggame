# ggmath - ggame extensions for geometry and mathematics in the browser

from ggame import Color, LineStyle, LineAsset, CircleAsset, Sprite, App
from ggame import TextAsset, ImageAsset, PolygonAsset
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
        self.reset()
        self.step()
        MathApp._addDynamic(self)  # always dynamically defined
        
    def reset(self):
        self._reset = MathApp.time
        
    def step(self):
        self.time = MathApp.time - self._reset
        

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


    

class Point(_MathVisual):
    
    def __init__(self, pos, size=5, color=Color(0,1), style=LineStyle(0, Color(0,1))):
        self._pos = self.Eval(pos)  # create a *callable* position function
        self._ppos = MathApp.logicalToPhysical(self._pos()) # physical position
        self._size = size
        self._color = color
        self._style = style
        super().__init__(CircleAsset(size, style, color), self._ppos)
        self.center = (0.5, 0.5)
        
    def __call__(self):
        return self._pos()

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

    def step(self):
        self._touchAsset()

    def physicalPointTouching(self, ppos):
        return MathApp.distance(ppos, self._ppos) < self._size
        
    def translate(self, pdisp):
        ldisp = MathApp.translatePhysicalToLogical(pdisp)
        pos = self._pos()
        self._pos = self.Eval((pos[0] + ldisp[0], pos[1] + ldisp[1]))
        self._touchAsset()




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
    
    _xscale = 200   # pixels per unit
    _yscale = 200
    _xcenter = 0    # center of screen in units
    _ycenter = 0    
    _mathVisualList = [] #
    _mathDynamicList = []
    _mathMovableList = []
    _mathSelectableList = []
    time = time()
    
    def __init__(self, scale=(_xscale, _yscale)):
        super().__init__()
        MathApp._xscale = scale[0]   # pixels per unit
        MathApp._yscale = scale[1]
        # register event callbacks
        self.listenMouseEvent("click", self.handleMouseClick)
        self.listenMouseEvent("mousedown", self.handleMouseDown)
        self.listenMouseEvent("mouseup", self.handleMouseUp)
        self.listenMouseEvent("mousemove", self.handleMouseMove)
        self.listenMouseEvent("mousewheel", self.handleMouseWheel)
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
            return (xxform(lp[0], cls._xscale, cls._xcenter, cls._win.width),
                yxform(lp[1], cls._yscale, cls._ycenter, cls._win.height))
        except AttributeError:
            return lp
            
    @classmethod
    def physicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale, xcenter, physwidth: (xvalue - physwidth/2)/xscale + xcenter
        yxform = lambda yvalue, yscale, ycenter, physheight: (physheight/2 - yvalue)/yscale + ycenter

        try:
            return (xxform(pp[0], cls._xscale, cls._xcenter, cls._win.width),
                yxform(pp[1], cls._yscale, cls._ycenter, cls._win.height))
        except AttributeError:
            return pp
            
    @classmethod
    def translatePhysicalToLogical(cls, pp):
        xxform = lambda xvalue, xscale: xvalue/xscale
        yxform = lambda yvalue, yscale: -yvalue/yscale

        try:
            return (xxform(pp[0], cls._xscale), yxform(pp[1], cls._yscale))
        except AttributeError:
            return pp

    @classmethod
    def translateLogicalToPhysical(cls, pp):
        xxform = lambda xvalue, xscale: xvalue*xscale
        yxform = lambda yvalue, yscale: -yvalue*yscale

        try:
            return (xxform(pp[0], cls._xscale), yxform(pp[1], cls._yscale))
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
        pass
     
    @classmethod   
    def distance(cls, pos1, pos2):
        return sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
            
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


class PointMass(Point):

    def __init__(self, pos):
        super().__init__(pos)
        self.mass = 1
        self.lastTime = MathApp.time
        self.V = (0,0)
        self.g = -9.81   #0
        self._setDynamic() # always dynamic

    def step(self):
        super().step()
        dt = MathApp.time - self.lastTime
        self.lastTime = MathApp.time
        A = self.acceleration
        dV = tuple(a*dt for a in A)
        A = tuple(v*dt for v in dV)
        B = tuple(a*0.5*dt*dt for a in A)
        dP = tuple(map(add, A, B))
        self.V = tuple(map(add, self.V, dV))
        self._pos = self.Eval(tuple(map(add, self._pos(), dP)))
        self._ppos = MathApp.logicalToPhysical(self._pos())
        
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
        
    pm1 = PointMass((0.1,0))

    p1 = Point((0,0))
    p1.movable = True
    p2 = Point((2,0))
    p2.movable = True
    p3 = Point((3,0))
    t = Timer()
    p4 = Point(lambda :(3, (int(t.time*100) % 400)/100))
    
    #p5 = Point(lambda :nextcoord())
    
    LineSegment(p1,p4)

    l1 = Label((-4,2), lambda: "Elapsed Time: {0:.0}".format(t.time), size=20, width=400, positioning="logical")
    i1 = InputNumeric((200,300), 99.9, size=20, positioning="physical")
    l2 = Label((-4,1), lambda: "{0}".format(i1()), size=20)
    b1 = InputButton((200,350), "RESET", lambda: t.reset(), size=20, positioning="physical")
    
    

    ap = MathApp((100,100))
    ap.run()