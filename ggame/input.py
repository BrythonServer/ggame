from ggame.label import Label
from ggame.asset import TextAsset
from ggame.mathapp import MathApp

class InputNumeric(Label):
    """
    Create a :class:`~ggame.label.Label` that can be selected to accept
    new **numeric** input from the keyboard. This is a 
    subclass of :class:`~ggame.sprite.Sprite` and 
    :class:`~ggame.mathapp._MathVisual` but most of the inherited 
    members are of little use and are not shown in the documentation. 

    :param tuple(float,float) pos: Screen position of the control, which may
            be a literal tuple of floats, or a reference to any object or 
            function that returns or evaluates to a tuple of floats.
            
    :param float val: Initial value of the input text

    :param \**kwargs:
        See below

    :Optional Keyword Arguments:
        * **fmt** (*str*) a Python format string (default is {0:.2f})
        * **positioning** (*str*) One of 'logical' or 'physical'
        * **size** (*int*) Size of text font (in pixels)
        * **width** (*int*) Width of the label (in pixels)
        * **color** (*Color*) Valid :class:`~ggame.asset.Color` object
        
    Example::
    
        from ggame.input import InputNumeric
        from ggame.mathapp import MathApp
        
        p = InputNumeric(
            (300, 275),     # screen coordinates of input
            3.14,           # initial value
            positioning="physical") # use physical coordinates

        MathApp().run()
    """
    
    def __init__(self, pos, val, **kwargs):
        self._fmt = kwargs.get('fmt', '{0:.2f}')
        self._val = self.Eval(val)()  # initialize to simple numeric
        self._savedval = self._val
        self._updateText()
        super().__init__(pos, self._textValue, **kwargs)
        self.selectable = True
        
    def _textValue(self):
        return self._text()

    def _updateText(self):
        self._text = self.Eval(self._fmt.format(self._val))

    def processEvent(self, event):
        if event.key in "0123456789insertdelete":
            key = event.key
            if event.key == 'insert':
                key = '-'
            elif event.key == 'delete':
                key = '.'
            if self._text() == "0":
                self._text = self.Eval("")
            self._text = self.Eval(self._text() + key)
            self._touchAsset()
        elif event.key in ['enter','escape']:
            if event.key == 'enter':
                try:
                    self._val = float(self._text())
                except ValueError:
                    self._val = self._savedval
                self._savedval = self._val
            self.unselect()
            

    def select(self):
        super().select()
        self._savedval = self._val
        self._val = 0
        self._updateText()
        self._touchAsset()
        MathApp.listenKeyEvent("keypress", "*", self.processEvent)

    def unselect(self):
        super().unselect()
        self._val = self._savedval
        self._updateText()
        self._touchAsset()
        try:
            MathApp.unlistenKeyEvent("keypress", "*", self.processEvent)
        except ValueError:
            pass

    def __call__(self):
        return self._val


class InputButton(Label):
    """
    Create a :class:`~ggame.label.Label` that can be clicked with a mouse
    to execute a user-defined function. This is a 
    subclass of :class:`~ggame.sprite.Sprite` and 
    :class:`~ggame.mathapp._MathVisual` but most of the inherited 
    members are of little use and are not shown in the documentation. 

    :param function callback: A reference to a function to execute, passing 
        this button object, when the button is clicked
    :param tuple(float,float) pos: Screen position of the control, which may
            be a literal tuple of floats, or a reference to any object or 
            function that returns or evaluates to a tuple of floats.
            
    :param float val: Initial value of the input text

    :param \*args:
        See below
    :param \**kwargs:
        See below

    :Required Arguments:
        * **pos**  (*tuple(float,float)*) Screen position of the button, which may
            be a literal tuple of floats, or a reference to any object or 
            function that returns or evaluates to a tuple of floats.
        * **text** (*str*) Text to appear in the button. This may be a literal
            string or a reference to any object or function that returns or
            evaluates to a string.


    :Optional Keyword Arguments:
        * **positioning** (*str*) One of 'logical' or 'physical'
        * **size** (*int*) Size of text font (in pixels)
        * **width** (*int*) Width of the label (in pixels)
        * **color** (*Color*) Valid :class:`~ggame.asset.Color` object
        
    Example::
    
        from ggame.asset import Color
        from ggame.label import InputButton
        from ggame.mathapp import MathApp
    
        def pressbutton(buttonobj):
            print("InputButton pressed!")
    
        InputButton(
            pressbutton,            # reference to handler
            (20,80),                # physical location on screen
            "Press Me",             # text to display
            size=15,                # text size (pixels)
            positioning="physical") # use physical coordinates

        MathApp().run()
    """
    
    def __init__(self, callback, *args,  **kwargs):
        """
        Required Inputs
        
        * **pos** position of button
        * **text** text of button
        * **callback** reference of a function to execute, passing this button object
        """
        super().__init__(*args, **kwargs)
        self._touchAsset()
        self._callback = callback
        self.selectable = True

    def _buildAsset(self):
        return TextAsset(self._nposinputs.text(), 
                            style="bold {0}px Courier".format(self._stdinputs.size()),
                            width=self._stdinputs.width(),
                            fill=self._stdinputs.color())

    def select(self):
        super().select()
        if self._callback: self._callback(self)
        self.unselect()

    def unselect(self):
        super().unselect()

