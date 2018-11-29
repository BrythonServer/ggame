"""
These mathematics and geometry extensions subclass the :class:`~ggame.app.App` 
and :class:`~ggame.sprite.Sprite` classes to create a framework for building
apps that mimic some of the functionality of online math tools like Geogebra.

This :mod:`~ggame.mathapp` module implements base classes for
:class:`~ggame.sprite.Sprite`-based classes defined in this module.

These extensions are very experimental and are not fully developed!
"""

from abc import ABCMeta, abstractmethod
from time import time
from math import sqrt
from collections import namedtuple
from ggame.sprite import Sprite
from ggame.asset import Color, LineStyle, ImageAsset
from ggame.app import App


class MathApp(App):
    """
    MathApp is a subclass of the ggame :class:`~ggame.app.App` class. It 
    incorporates the following extensions:
    
    * Support for zooming the display using the mouse wheel
    * Support for click-dragging the display using the mouse button
    * Automatic execution of step functions in all objects and sprites
        sub-classed from :class:`_MathDynamic`.
        
    :param float scale: Optional parameter sets the initial scale of the
        display in units of pixels per logical unit. The default is 200.
        
    :returns: MathApp instance
    """
    
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
        self.listenMouseEvent("click", self._handleMouseClick)
        self.listenMouseEvent("mousedown", self._handleMouseDown)
        self.listenMouseEvent("mouseup", self._handleMouseUp)
        self.listenMouseEvent("mousemove", self._handleMouseMove)
        self.listenMouseEvent("wheel", self._handleMouseWheel)
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None
        self.mouseDownObject = None
        self.mouseX = self.mouseY = None
        self._touchAllVisuals()
        self.selectedObj = None
        MathApp.time = time()

    def step(self):
        """
        The step method overrides :func:`~ggame.app.App.step` in the 
        :class:`~ggame.app.App` class, executing step functions in all
        objects subclassed from :class:`_MathDynamic`.
        """
        MathApp.time = time()
        for spr in self._mathDynamicList:
            spr.step()

    def _touchAllVisuals(self):
        # touch all visual object assets to use scaling
        for obj in self._mathVisualList:
            obj._touchAsset(True)


    @classmethod
    def logicalToPhysical(cls, lp):
        """
        Transform screen coordinates from logical to physical space. Output
        depends on the current 'zoom' and 'pan' of the screen.
        
        :param tuple(float,float) lp: Logical screen coordinates (x, y)
        
        :rtype: tuple(float,float)
        
        :returns: Physical screen coordinates (x, y)
        """
        
        xxform = lambda xvalue, xscale, xcenter, physwidth: int((xvalue-xcenter)*xscale + physwidth/2)
        yxform = lambda yvalue, yscale, ycenter, physheight: int(physheight/2 - (yvalue-ycenter)*yscale)

        try:
            return (xxform(lp[0], cls._scale, cls._xcenter, cls._win.width),
                yxform(lp[1], cls._scale, cls._ycenter, cls._win.height))
        except AttributeError:
            return lp
            
    @classmethod
    def physicalToLogical(cls, pp):
        """
        Transform screen coordinates from physical to logical space. Output
        depends on the current 'zoom' and 'pan' of the screen.
        
        :param tuple(float,float) lp: Physical screen coordinates (x, y)
        
        :rtype: tuple(float,float)
        
        :returns: Logical screen coordinates (x, y)
        """
        
        xxform = lambda xvalue, xscale, xcenter, physwidth: (xvalue - physwidth/2)/xscale + xcenter
        yxform = lambda yvalue, yscale, ycenter, physheight: (physheight/2 - yvalue)/yscale + ycenter

        try:
            return (xxform(pp[0], cls._scale, cls._xcenter, cls._win.width),
                yxform(pp[1], cls._scale, cls._ycenter, cls._win.height))
        except AttributeError:
            return pp
            
    @classmethod
    def translateLogicalToPhysical(cls, pp):
        """
        Transform screen translation from logical to physical space. Output
        only depends on the current 'zoom' of the screen.
        
        :param tuple(float,float) lp: Logical screen translation pair 
            (delta x, delta y)
        
        :rtype: tuple(float,float)
        
        :returns: Physical screen translation ordered pair (delta x, delta y)
        """
        
        xxform = lambda xvalue, xscale: xvalue*xscale
        yxform = lambda yvalue, yscale: -yvalue*yscale

        try:
            return (xxform(pp[0], cls._scale), yxform(pp[1], cls._scale))
        except AttributeError:
            return pp

    @classmethod
    def translatePhysicalToLogical(cls, pp):
        """
        Transform screen translation from physical to logical space. Output
        only depends on the current 'zoom' of the screen.
        
        :param tuple(float,float) lp: Physical screen translation pair 
            (delta x, delta y)
        
        :rtype: tuple(float,float)
        
        :returns: Logical screen translation ordered pair (delta x, delta y)
        """
        
        xxform = lambda xvalue, xscale: xvalue/xscale
        yxform = lambda yvalue, yscale: -yvalue/yscale

        try:
            return (xxform(pp[0], cls._scale), yxform(pp[1], cls._scale))
        except AttributeError:
            return pp

    def _handleMouseClick(self, event):
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

    def _handleMouseDown(self, event):
        self.mouseDown = True
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None
        for obj in self._mathSelectableList:
            if obj.physicalPointTouching((event.x, event.y)):
                obj.mousedown()
                self.mouseDownObject = obj
                break
        for obj in self._mathMovableList:
            if obj.physicalPointTouching((event.x, event.y)) and not (obj.strokable and obj.canstroke((event.x,event.y))):
                self.mouseCapturedObject = obj
                break
        if not self.mouseCapturedObject:
            for obj in self._mathStrokableList:
                if obj.canstroke((event.x, event.y)):
                    self.mouseStrokedObject = obj
                    break

    def _handleMouseUp(self, event):
        if self.mouseDownObject:
            self.mouseDownObject.mouseup()
            self.mouseDownObject = None
        self.mouseDown = False
        self.mouseCapturedObject = None
        self.mouseStrokedObject = None

    def _handleMouseMove(self, event):
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
    
    def _handleMouseWheel(self, event):
        zoomfactor = event.wheelDelta/100
        zoomfactor = 1+zoomfactor if zoomfactor > 0 else 1+zoomfactor
        if zoomfactor > 1.2:
            zoomfactor = 1.2
        elif zoomfactor < 0.8:
            zoomfactor = 0.8
        MathApp._scale *= zoomfactor
        self._touchAllVisuals()
        self._viewNotify("zoom")
        
    @property
    def viewPosition(self):
        """
        Attribute is used to get or set the current logical coordinates 
        at the center of the screen as a tuple of floats (x,y).
        """
        return (MathApp._xcenter, MathApp._ycenter)
        
    @viewPosition.setter
    def viewPosition(self, pos):
        MathApp._xcenter, MathApp._ycenter = pos
        self._touchAllVisuals()
        self._viewNotify("translate")
        
    @classmethod   
    def addViewNotification(cls, handler):
        """
        Register a function or method to be called in the event the view
        position or zoom changes.
        
        :param function handler: The function or method to be called
        :returns: Nothing
        """
        cls._viewNotificationList.append(handler)
        
    @classmethod   
    def removeViewNotification(cls, handler):
        """
        Remove a function or method from the list of functions to be called
        in the event of a view position or zoom change.
        
        :param function handler: The function or method to be removed
        :returns: Nothing
        """
        cls._viewNotificationList.remove(handler)
    
    def _viewNotify(self, viewchange):
        for handler in self._viewNotificationList:
            handler(viewchange = viewchange, scale = self._scale, center = (self._xcenter, self._ycenter))
        
     
    @classmethod   
    def distance(cls, pos1, pos2):
        """
        Utility for calculating the distance between any two points.
        
        :param tuple(float,float) pos1: The first point
        :param tuple(float,float) pos2: The second point
        :rtype: float
        :returns: The distance between the two points (using Pythagoras)
        """
        return sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
        
    @property
    def scale(self):
        """
        Attribute reports the current view scale (pixels per logical unit).
        """
        return self._scale
        
    @property
    def width(self):
        """
        Attribute reports the physical screen width (pixels).
        """
        return App._win.width

    @width.setter
    def width(self, value):
        pass

            
    @classmethod
    def _addVisual(cls, obj):
        """ FIX ME """
        if isinstance(obj, _MathVisual):
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
        if isinstance(obj, _MathVisual) and not obj in cls._mathMovableList:
            cls._mathMovableList.append(obj)
            
    @classmethod
    def _removeMovable(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathMovableList:
            cls._mathMovableList.remove(obj)

    @classmethod
    def _addSelectable(cls, obj):
        if isinstance(obj, _MathVisual) and not obj in cls._mathSelectableList:
            cls._mathSelectableList.append(obj)
            
    @classmethod
    def _removeSelectable(cls, obj):
       if isinstance(obj, _MathVisual)  and obj in cls._mathSelectableList:
            cls._mathSelectableList.remove(obj)

    @classmethod
    def _addStrokable(cls, obj):
        if isinstance(obj, _MathVisual) and not obj in cls._mathStrokableList:
            cls._mathStrokableList.append(obj)
            
    @classmethod
    def _removeStrokable(cls, obj):
        if isinstance(obj, _MathVisual) and obj in cls._mathStrokableList:
            cls._mathStrokableList.remove(obj)

    @classmethod
    def _destroy(cls, *args):
        """
        This will clean up any class level storage.
        """ 
        App._destroy(*args)  # hit the App class first
        MathApp.time = None
        MathApp._mathVisualList = [] 
        MathApp._mathDynamicList = []
        MathApp._mathMovableList = []
        MathApp._mathSelectableList = []
        MathApp._mathStrokableList = []
        MathApp._viewNotificationList = []
        

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
    """
    Abstract Base Class for all visual, potentially dynamic objects.
    
    :param Asset asset: A valid ggame asset object.
    
    :param list args: A list of required positional or non-positional arguments
        as named in the _posinputsdef and _nonposinputsdef lists overridden
        by child classes.
        
    :param \**kwargs:
        See below

    :Optional Keyword Arguments:
        * **positioning** (*string*) One of 'logical' or 'physical'
        * **size** (*int*) Size of the object (in pixels)
        * **width** (*int*) Width of the object (in pixels)
        * **color** (*Color*) Valid :class:`~ggame.asset.Color` object
        * **style** (*LineStyle*) Valid :class:`~ggame.asset.LineStyle` object
    """
    
    _posinputsdef = []  # a list of names (string) of required positional inputs
    _nonposinputsdef = []  # a list of names (string) of required non positional inputs
    _defaultsize = 15
    _defaultwidth = 200
    _defaultcolor = Color(0, 1)
    _defaultstyle = LineStyle(1, Color(0, 1))
    
    
    def __init__(self, asset, *args, **kwargs):
        MathApp._addVisual(self)
        #Sprite.__init__(self, asset, args[0])
        _MathDynamic.__init__(self)
        self._movable = False
        self._selectable = False
        self._strokable = False
        self.selected = False
        """
        True if object is currently selected by the UI. 
        """
        self.mouseisdown = False
        """
        True if object is tracking UI mouse button as down. 
        """
        self._positioning = kwargs.get('positioning', 'logical')
        # positional inputs
        self._PI = namedtuple('PI', self._posinputsdef)
        # nonpositional inputs
        self._NPI = namedtuple('NPI', self._nonposinputsdef)
        # standard inputs (not positional)
        standardargs = ['size','width','color','style']
        self._SI = namedtuple('SI', standardargs)
        # correct number of args?
        if len(args) != len(self._posinputsdef) + len(self._nonposinputsdef):
            raise TypeError("Incorrect number of parameters provided")
        self._args = args
        # generated named tuple of functions from positional inputs
        self._posinputs = self._PI(*[self.Eval(p) for p in args][:len(self._posinputsdef)])
        self._getPhysicalInputs()
        # first positional argument must be a sprite position!
        Sprite.__init__(self, asset, self._pposinputs[0])
        # generated named tuple of functions from nonpositional inputs
        if len(self._nonposinputsdef) > 0:
            self._nposinputs = self._NPI(*[self.Eval(p) for p in args][(-1*len(self._nonposinputsdef)):])
        else:
            self._nposinputs = []
        self._stdinputs = self._SI(self.Eval(kwargs.get('size', self._defaultsize)),
                                    self.Eval(kwargs.get('width', self._defaultwidth)),
                                    self.Eval(kwargs.get('color', self._defaultcolor)),
                                    self.Eval(kwargs.get('style', self._defaultstyle)))
        self._sposinputs = self._PI(*[0]*len(self._posinputs))
        self._spposinputs = self._PI(*self._pposinputs)
        self._snposinputs = self._NPI(*[0]*len(self._nposinputs))
        self._sstdinputs = self._SI(*[0]*len(self._stdinputs))

    def step(self):
        self._touchAsset()
        
    def _saveInputs(self, inputs):
        self._sposinputs, self._spposinputs, self._snposinputs, self._sstdinputs = inputs
        
    def _getInputs(self):
        self._getPhysicalInputs()
        return (self._PI(*[p() for p in self._posinputs]),
            self._PI(*self._pposinputs),
            self._NPI(*[p() for p in self._nposinputs]),
            self._SI(*[p() for p in self._stdinputs]))

    
    def _getPhysicalInputs(self):
        """
        Translate all positional inputs to physical
        """
        pplist = []
        if self._positioning == 'logical':
            for p in self._posinputs:
                pval = p()
                try:
                    pp = MathApp.logicalToPhysical(pval)
                except AttributeError:
                    pp = MathApp._scale * pval
                pplist.append(pp)
        else:
            # already physical
            pplist = [p() for p in self._posinputs]
        self._pposinputs = self._PI(*pplist)
    
    def _inputsChanged(self, saved):
        return self._spposinputs != saved[1] or self._snposinputs != saved[2] or self._sstdinputs != saved[3]

    
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
        self.position = self._pposinputs.pos
            
    @property
    def positioning(self):
        """
        Whether object was created with 'logical' or 'physical' positioning. 
        """
        return self._positioning
    
    @positioning.setter
    def positioning(self, val):
        pass
    
    @property
    def movable(self):
        """
        Whether object can be moved. Set-able and get-able. 
        """
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
        """
        Whether object can be selected by the UI. Set-able and get-able.
        """
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
        """
        Whether the object supports a click-drag input from the UI mouse. 
        Set-able and get-able. 
        """
        return self._strokable
        
    @strokable.setter
    def strokable(self, val):
        self._strokable = val
        if val:
            MathApp._addStrokable(self)
        else:
            MathApp._removeStrokable(self)

    def select(self):
        """
        Place the object in a 'selected' state. 
        
        :param: None
        :returns: None 
        """
        self.selected = True

    def unselect(self):
        """
        Place the object in an 'unselected' state. 
        
        :param: None
        :returns: None
        """
        self.selected = False
        
    def mousedown(self):
        """
        Inform the object of a 'mouse down' event. 
        
        :param: None 
        :returns: None 
        """
        self.mouseisdown = True
        
    def mouseup(self):
        """
        Inform the object of a 'mouse up' event. 
        
        :param: None 
        :returns: None 
        """
        self.mouseisdown = False

    def processEvent(self, event):
        """
        Inform the object of a generic ggame event. 
        
        :param event: The ggame event object to receive and process. 
        :returns: None 
        
        This method is intended to be overridden.
        """
        pass

    @abstractmethod
    def physicalPointTouching(self, ppos):
        """
        Determine if a physical point is considered to be touching this object.
        
        :param tuple(int,int) ppos: Physical screen coordinates.
        :rtype: boolean
        :returns: True if touching, False otherwise.
        
        This method **must** be overridden.
        """
        pass
    
    @abstractmethod
    def translate(self, pdisp):
        """ 
        Perform necessary processing in response to being moved by the mouse/UI.
        
        :param tuple(int,int) pdisp: Translation vector (x,y) in physical screen
            units.
        :returns: None
        
        This method **must** be overridden.
        """
        pass
    
    def stroke(self, ppos, pdisp):
        """
        Perform necessary processing in response to click-drag action by the
        mouse/UI.
        
        :param tuple(int,int) ppos: Physical coordinates of stroke start.
        :param tuple(int,int) pdisp: Translation vector of stroke action in
            physical screen units.
        :returns: None
        
        This method is intended to be overridden.
        """
        pass
    
    def canStroke(self, ppos):
        """
        Can the object respond to beginning a stroke action at the given
        position.
        
        :param tuple(int,int) ppos: Physical coordinates of stroke start.
        :rtype: Boolean
        :returns: True if the object can respond, False otherwise.
        
        This method is intended to be overridden.
        """
        return False
    
    def _touchAsset(self, force = False):
        inputs = self._getInputs()
        changed = self._inputsChanged(inputs)
        if changed:
            self._saveInputs(inputs)
        if changed or force:
            self._updateAsset(self._buildAsset())

    
    @abstractmethod
    def _buildAsset(self):
        pass
    