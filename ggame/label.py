from ggame.mathbase import _MathVisual
from ggame.asset import TextAsset

class Label(_MathVisual):
    
    posinputsdef = ['pos']
    nonposinputsdef = ['text']
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** position of label
        * **text** text contents of label
        """
        super().__init__(TextAsset(""), *args, **kwargs)
        self._touchAsset()

    def _buildAsset(self):
        return TextAsset(self.nposinputs.text(), 
                            style="{0}px Courier".format(self.stdinputs.size()),
                            width=self.stdinputs.width(),
                            fill=self.stdinputs.color())

    def __call__(self):
        return self.nposinputs.text()

    def physicalPointTouching(self, ppos):
        _ppos = self.spposinputs.pos
        return (ppos[0] >= _ppos[0] and 
            ppos[0] <= _ppos[0] + self.sstdinputs.width and
            ppos[1] >= _ppos[1] and 
            ppos[1] <= _ppos[1] + self.sstdinputs.size)

    def translate(self, pdisp):
        pass
