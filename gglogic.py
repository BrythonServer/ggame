# gglogic boolean logic device simulations for ggmath

from ggmath import MathApp, _MathDynamic
from abc import ABCMeta, abstractmethod

class _BoolDevice(_MathDynamic, metaclass=ABCMeta):

    def __init__(self, mininputqty, *args, **kwargs):
        """
        Required Inputs
        
        * **mininputqty** minimum number of inputs possible
        
        Optional keyword arguments
        
        * **namedinputs** list of input names
        """
        self.In = [None]*mininputqty
        self.Enable = True
        namedinputs = kwargs.get('namedinputs', [])
        self._indict = {name:Eval(None) for name in namedinputs}
        self.ingetvalue = False
        self.lastget = None
        

    @property
    def In(self):
        return self._input
    
    @In.setter
    def In(self, val):
        try:
            self._input = [self.Eval(v) for v in list(val)]
        except TypeError:
            self._input = [self.Eval(val)]
            
    # Enable attribute controls the "tri-state" of output
    @property
    def Enable(self):
        return self._enable
    
    @Enable.setter
    def Enable(self, val):
        self._enable = self.Eval(val)
        
    # decorator for _getvalue
    def recursiontrap(handler):
        def trapmagic(self):
            if not self.ingetvalue:
                self.ingetvalue = True
                self.lastget = handler(self)
                self.ingetvalue = False
                return self.lastget
            else:
                self.ingetvalue = False
                return self.lastget
                
        return trapmagic 
    
    @abstractmethod
    def _getvalue(self):
        return None
    
    def _inputState(self, value):
        """
        interprets a value that could be single input or a list of inputs!
        """
        try:
            inputs = [].extend(value)
        except TypeError:
            inputs = [value]
        scalars = [v() for v in inputs]
        ones = scalars.count(True) + scalars.count(1)
        zeros = scalars.count(False) + scalars.count(0)
        if ones > 0 and zeros > 0:
            raise ValueError("Conflicting inputs found")
        if ones > 0:
            return True
        elif zeros > 0:
            return False
        else: 
            return None
    
    def __call__(self):
        if self.Enable:
            return self._getvalue()
        else:
            return None
    
    def GetInput(self, inputname):
        return self._inputState(self._indict[inputname])

    def SetInput(self, inputname, reference):
        self._indict[inputname] = self.Eval(reference)
    


class _BoolOneInput(_BoolDevice):

    def __init__(self, *args, **kwargs):
        """ 
        No Required Inputs
        """
        super().__init__(1)

    
class _BoolMultiInput(_BoolDevice):

    def __init__(self, *args, **kwargs):
        """ 
        No Required Inputs
        """
        super().__init__(2)


class BoolNOT(_BoolOneInput):

    def _getvalue(self):
        inval = self._inputState(self.In[0])
        if inval == None:
            return True  # equivalent to an "open" input
        else:
            return not inval


class BoolAND(_BoolMultiInput):
    
    def _getvalue(self):
        for v in self._input:
            if not self._inputState(v):
                return False
        return True
        
class BoolNOR(_BoolMultiInput):
    
    def _getvalue(self):
        for v in self._input:
            if self._inputState(v):
                return False
        return True
        

class TestDevice(_BoolOneInput):
    
    def __init__(self, *args, **kwargs):
        kwargs['namedinputs'] = ['in1', 'in2']
        super().__init__(*args, **kwargs)
        
    def out1(self):
        return self.GetInput('in1') and self.GetInput('in2')
        
    def out2(self):
        return self.GetInput('in1') or self.GetInput('in2')
        
    def _getvalue(self):
        return None
        
        
        

    

# test code here
if __name__ == "__main__":
    
    from ggmath import GlassButton, LEDIndicator, MetalToggle
    

    """
    IC1 = BoolNOT()
    IC2 = BoolAND()
    
    b1 = MetalToggle(1, (1,0))
    b2 = MetalToggle(1, (1,0.3))
    db1 = LEDIndicator((1.3,0), b1)
    db2 = LEDIndicator((1.3,0.3), b2)

    b3 = MetalToggle(1, (1,0.6))
    b4 = MetalToggle(1, (1,0.9))
    db1 = LEDIndicator((1.3,0.6), b3)
    db2 = LEDIndicator((1.3,0.9), b4)


    d2 = LEDIndicator((1.5,0.45), IC2)
    
    IC2.In = b1, b2
    IC2.In = IC2.In + [b3, b4]
    
    button = GlassButton(None, (0,0))
    LED = LEDIndicator((0,-1), IC1)
    IC1.In = button 


    t1 = MetalToggle(1, (1,-1))
    t2 = MetalToggle(1, (1, -1.3))
    td = TestDevice()
    dt1 = LEDIndicator((1.3, -1), t1)
    dt2 = LEDIndicator((1.3, -1.3), t2)
    dtd1 = LEDIndicator((1.5, -1), td.out1)
    dtd2 = LEDIndicator((1.5, -1.3), td.out2)
    td.SetInput('in1', t1)
    td.SetInput('in2', t2)
    """
    
    IC1 = BoolNOR()
    IC2 = BoolNOR()
    
    b1 = GlassButton(None, (0,0))
    b2 = GlassButton(None, (0,-0.5))
    
    IC1.In = b1, b1
    IC2.In = b2, b2
    
    d1 = LEDIndicator((0.5,0), IC1)
    d2 = LEDIndicator((0.5,-0.5), IC2)
    
    app = MathApp()
    app.run()