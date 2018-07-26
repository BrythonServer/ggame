# gglogic boolean logic device simulations for ggmath

from ggmath import MathApp, _MathDynamic
from abc import ABCMeta, abstractmethod

class _BoolDevice(_MathDynamic, metaclass=ABCMeta):

    def __init__(self, mininputqty, *args, **kwargs):
        """
        Required Inputs
        
        * **mininputqty** minimum number of inputs possible
        """
        self.In = [None]*mininputqty
        self.Enable = True

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
    
    def __call__(self):
        if self.Enable:
            return super().__call__()
        else:
            return None
        


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

    def __call__(self):
        inval = self.In[0]()
        if inval == None:
            return True  # equivalent to an "open" input
        else:
            return not inval


class BoolAND(_BoolMultiInput):
    
    def __call__(self):
        for v in self._input:
            if not v():
                return False
        return True
        

# test code here
if __name__ == "__main__":
    
    from ggmath import GlassButton, LEDIndicator, MetalToggle
    

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
    
    app = MathApp()
    app.run()