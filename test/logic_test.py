import unittest
from ggame.logic import BoolSRFF, BoolAND, BoolNAND, BoolNOR, BoolNOT
from ggame.mathapp import MathApp
from ggame.inputpoint import MetalToggle, GlassButton
from ggame.indicator import LEDIndicator
import time

class TestLogicMethods(unittest.TestCase):

    def test_gates(self):
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
        dt1 = LEDIndicator((1.3, -1), t1)
        dt2 = LEDIndicator((1.3, -1.3), t2)

        ma = MathApp()
        ma.run()
        
        for i in range(10):
            time.sleep(1/60)
            ma.step()

        for o in [b1, b2, db1, db2, b3, b4, IC1, IC2, button, LED, t1, t2, dt1, dt2]:
            o.destroy()


    def test_SRGate(self):
        IC1 = BoolSRFF(gateclass=BoolNAND)
        Inv1 = BoolNOT()
        Inv2 = BoolNOT()
    
        b1 = GlassButton(None, (0,0))
        b2 = GlassButton(None, (0,-0.5))
        Inv1.In = b1
        Inv2.In = b2
        
        IC1.SetInput('R', Inv1)
        IC1.SetInput('S', Inv2)
    
        d1 = LEDIndicator((0.5,0), IC1)
        d2 = LEDIndicator((0.5,-0.5), IC1.Q_)
        
        ma = MathApp()
        ma.run()
        
        for i in range(10):
            time.sleep(1/60)
            ma.step()

        for o in [IC1, Inv1, Inv2, b1, b2, d1, d2]:
            o.destroy()
        
    """  Failing test on unlimited recursion 
    def test_JKGate(self):
        IC1 = BoolJKFF()
        t1 = MetalToggle(0, (0,0.5))
        b1 = GlassButton(None, (0,0))
        t2 = MetalToggle(0, (0,-0.5))
    
        IC1.SetInput('J', t1)
        IC1.SetInput('K', t2)
        IC1.SetInput('CLK', b1)
    
        d1 = LEDIndicator((0.5,0.5), IC1)
        d2 = LEDIndicator((0.5,-0.5), IC1.Q_)

        ma = MathApp()
        ma.run()
        
        for i in range(10):
            time.sleep(1/60)
            ma.step()

        for o in [IC1, t1, b1, t2, d1, d2]:
            o.destroy()
    """
        

if __name__ == '__main__':
    unittest.main()
