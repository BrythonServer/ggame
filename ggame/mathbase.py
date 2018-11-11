from abc import ABCMeta, abstractmethod
from collections import namedtuple
from ggame.mathapp import MathApp
from ggame.sprite import Sprite
from ggame.asset import Color, LineStyle

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
        self.mouseisdown = False
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
        
    def mousedown(self):
        self.mouseisdown = True
        
    def mouseup(self):
        self.mouseisdown = False

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
    
