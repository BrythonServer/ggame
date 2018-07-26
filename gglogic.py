# gglogic boolean logic device simulations for ggmath

from ggmath import MathApp, _MathDynamic
from abc import ABCMeta, abstractmethod


class BoolNOT(_MathDynamic):
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        """
        self._input = self.Eval(None)
        super().__init__()


    def __call__(self):
        inval = self.In()
        if inval == None:
            return True  # equivalent to an "open" input
        else:
            return not inval

    @property
    def In(self):
        return self._input

    @In.setter
    def In(self, val):
        self._input = self.Eval(val)
        

class BoolAND(_MathDynamic):
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        """
        self._input = [self.Eval(None), self.Eval(None)]
        super().__init__()

    def __cal__(self):
        for v in self._input:
            if not v():
                return False
        return True
        
    @property
    def In(self):
        return self._input
    
    @In.setter
    def In(self, val)
        self._input = [self.Eval(v) for v in list(val)]


# test code here
if __name__ == "__main__":
    
    from ggmath import GlassButton, LEDIndicator
    

    IC1 = BoolNOT()
    IC2 = BoolAND()
    
    b1 = GlassButton(None, (1,0))
    b2 = GlassButton(None, (1,0.2))
    d2 = LEDIndicator((1.5,0.1), IC2)
    
    button = GlassButton(None, (0,0))
    LED = LEDIndicator((0,-1), IC1)
    IC1.In = button 
    
    app = MathApp()
    app.run()