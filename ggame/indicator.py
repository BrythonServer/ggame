from ggame.mathapp import _MathVisual
from ggame.asset import Frame, ImageAsset

class ImageIndicator(_MathVisual):

    _posinputsdef = ['pos']
    _nonposinputsdef = ['value']

    def __init__(self, url, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file consisting of two image sprite sheet
        * **pos** position of point
        * **value** state of the indicator (True/False or integer)

        Optional Inputs
        * **frame** sub-frame location of image within file
        * **qty** number of sub-frames, when used as sprite sheet
        * **direction** one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        """
        kwargs.setdefault('frame', None)
        kwargs.setdefault('qty', 1)
        kwargs.setdefault('direction', 'horizontal')
        kwargs.setdefault('margin', 0)
        super().__init__(
            ImageAsset(url, 
                kwargs['frame'], 
                kwargs['qty'], 
                kwargs['direction'], 
                kwargs['margin']), 
            *args, **kwargs)
        self.center = (0,0)

    def _buildAsset(self):
        inval = self._nposinputs.value()
        if inval == True:
            self.setImage(1)
        elif inval == False:
            self.setImage(0)
        else:
            self.setImage(inval)
        return self.asset

    def physicalPointTouching(self, ppos):
        self._setExtents()  # ensure xmin, xmax are correct
        x, y = ppos
        return x >= self.xmin and x < self.xmax and y >= self.ymin and y <= self.ymax

    def translate(self, pdisp):
        pass


class LEDIndicator(ImageIndicator):
    
    def __init__(self, *args, **kwargs):
        """
        Required Inputs
        
        * **pos** position of point
        * **value** state of the indicator (True/False or integer)

        """
        kwargs.setdefault('frame', Frame(0,0,600,600))
        kwargs.setdefault('qty', 2)
        super().__init__("ggimages/red-led-off-on.png", *args, **kwargs)
        self.scale = 0.05
