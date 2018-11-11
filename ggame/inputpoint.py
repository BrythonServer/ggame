from ggame.point import ImagePoint
from ggame.asset import Frame

class InputImageButton(ImagePoint):
    
    def __init__(self, url, callback, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file
        * **callback** reference of a function to execute, passing this button object
        * **pos** position of point
        
        Optional Inputs
        * **frame** sub-frame location of image within file
        * **qty** number of sub-frames, when used as sprite sheet
        * **direction** one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        """
        super().__init__(url, *args, **kwargs)
        self.center = (0,0)
        self._callback = callback
        self.selectable = True
        self.firstImage()
        self.mousewasdown = self.mouseisdown

    def select(self):
        super().select()
        if self._callback: self._callback(self)
        self.unselect()

    def unselect(self):
        super().unselect()

    def __call__(self):
        # code for controlling the button image state only works if the
        # button state is being monitored!
        if self.mouseisdown != self.mousewasdown:
            if self.mouseisdown:
                self.nextImage()
            else:
                self.firstImage()
            self.mousewasdown = self.mouseisdown
        return self.mouseisdown
        

class InputImageToggle(ImagePoint):

    def __init__(self, url, statelist, initindex, *args, **kwargs):
        """
        Required Inputs
        
        * **url** location of image file
        * **statelist** list of values to correspond with toggle states
        * **initindex** index to initial toggle state
        * **pos** position of point
        
        Optional Inputs
        * **frame** sub-frame location of image within file
        * **direction** for sprite sheet one of 'horizontal' (default) or 'vertical'
        * **margin** pixels between sub-frames if sprite sheet
        * Note the qty of images is equal to length of the statelist
        """
        self.statelist = statelist
        kwargs.setdefault('qty', len(statelist))
        super().__init__(url, *args, **kwargs)
        self.center = (0,0)
        self.selectable = True
        self.togglestate = initindex
        self.setImage(self.togglestate)

    def select(self):
        super().select()
        self.togglestate += 1
        if self.togglestate == len(self.statelist):
            self.togglestate = 0
        self.setImage(self.togglestate)
        self.unselect()

    def __call__(self):
        return self.statelist[self.togglestate]
    
    
class MetalToggle(InputImageToggle):
    def __init__(self, initindex, *args, **kwargs):
        """
        Required Inputs
        
        * **initindex** index to initial toggle state
        * **pos** position of toggle
        """
        kwargs.setdefault('frame', Frame(0,0,110,150))
        super().__init__("ggimages/toggle-up-down.png", [True, False], initindex, *args, **kwargs)
        self.scale = 0.4
        


class GlassButton(InputImageButton):
    
    def __init__(self, callback, *args, **kwargs):
        """
        Required Inputs
        
        * **callback** reference of a function to execute, passing this button object
        * **pos** position of point
        """        
        kwargs.setdefault('frame', Frame(0,0,100,100))
        kwargs.setdefault('qty', 2)
        super().__init__("ggimages/button-round.png", callback, *args, **kwargs)
        self.scale = 0.3
