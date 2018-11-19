from ggame.mathapp import _MathVisual
from ggame.asset import LineAsset


class LineSegment(_MathVisual):
    
    posinputsdef = ['pos','end']
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** start position of segment
        * **end** end position of segment
        
        Optional Inputs
        
        * **style** line style (thickness, color)
        """
        super().__init__(LineAsset(0,0, self.defaultstyle), *args, **kwargs)
        self._touchAsset()
        
    def _buildAsset(self):
        start = self.pposinputs.pos
        end = self.pposinputs.end
        self.position = start
        return LineAsset(end[0]-start[0],
                            end[1]-start[1],
                            self.stdinputs.style())

    def physicalPointTouching(self, ppos):
        return False

    def translate(self, pdisp):
        pass

