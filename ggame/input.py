from ggame.label import Label
from ggame.asset import TextAsset

class InputNumeric(Label):
    
    def __init__(self, pos, val, **kwargs):
        """
        Required Inputs
        
        * **pos** position of button
        * **val** initial value of input
        
        Optional Keyword Input
        * **fmt** a Python format string (default is {0.2})
        """
        self._fmt = kwargs.get('fmt', '{0.2}')
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
        return TextAsset(self.nposinputs.text(), 
                            style="bold {0}px Courier".format(self.stdinputs.size()),
                            width=self.stdinputs.width(),
                            fill=self.stdinputs.color())

    def select(self):
        super().select()
        if self._callback: self._callback(self)
        self.unselect()

    def unselect(self):
        super().unselect()

