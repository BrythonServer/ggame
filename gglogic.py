# gglogic boolean logic device simulations for ggmath

from ggmath import MathApp, _MathDynamic
from abc import ABCMeta, abstractmethod


class BoolNot(_MathDynamic):
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **name** identifying text name
        """
        self.name = args[0]
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
        


# test code here
if __name__ == "__main__":
    
    from ggmath import GlassButton, LEDIndicator
    

    IC1 = BoolNot("IC1")
    button = GlassButton(None, (0,0))
    LED = LEDIndicator((0,-1), IC1)
    IC1.In = button 
    
    app = MathApp()
    app.run()