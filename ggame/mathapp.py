from time import time
from math import sqrt
from ggame.app import App


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
        self.mouseDownObject = None
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
            obj._touchAsset(True)


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

    def handleMouseUp(self, event):
        if self.mouseDownObject:
            self.mouseDownObject.mouseup()
            self.mouseDownObject = None
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
        MathApp._mathVisualList = [] 
        MathApp._mathDynamicList = []
        MathApp._mathMovableList = []
        MathApp._mathSelectableList = []
        MathApp._mathStrokableList = []
        MathApp._viewNotificationList = []
        

