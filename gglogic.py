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
        super().__init__()
        
    @property
    def Out(self):
        return True and not self.In()

    @property
    def In(self):
        return self._input

    @In.setter
    def In(self, val):
        self._input = self.Eval(val)
        


# test code here
if __name__ == "__main__":
    
    from ggmath import GlassButton, LEDIndicator
    
    app = MathApp()


    button = GlassButton(None, (0,0))
    LED = LEDIndicator((0,-1), button)
    
    app.run()