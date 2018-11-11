try:
    from ggame.sysdeps import *
except:
    from sysdeps import *

from ggame.asset import *
from ggame.event import *

class App(object):
    """
    The `ggame.App` class is a (typically subclassed) class that encapsulates
    handling of the display system, and processing user events. The `ggame.App` 
    class also manages lists of all `ggame.Sprite` instances in the application.

    When subclassing `ggame.App` you may elect to instantiate most of your
    sprite objects in the initialization section.

    Processing that must occur on a per-frame basis may be included by overriding
    the `ggame.App.step` method. This is also an appropriate location to call
    similar 'step' methods for your various customized sprite classes.

    Once your application class has been instantiated, begin the frame drawing
    process by calling its `ggame.App.run` method.

    NOTE: Only **one** instance of an `ggame.App` class or subclass may be 
    instantiated at a time.
    """
    spritelist = []
    """List of all sprites currently active in the application."""
    _eventdict = {}
    _spritesdict = {}
    _spritesadded = False
    _win = None

    def __init__(self, *args):
        """
        The `ggame.App` class is called either by specifying the desired app window size
        in pixels, as two parameters (e.g. `myapp = App(640,480)`), or by providing
        no size parameters at all (e.g. `myapp = App()`), in which case, the full browser
        window size is used.
        """
        if App._win == None and (len(args) == 0 or len(args) == 2):
            x = y = 0
            if len(args) == 2:
                x = args[0]
                y = args[1]
            App._win = GFX_Window(x, y, type(self)._destroy)
            self.width = App._win.width
            self.height = App._win.height
            # Add existing sprites to the window
            if not App._spritesadded and len(App.spritelist) > 0:
                App._spritesadded = True
                for sprite in App.spritelist:
                    App._win.add(sprite.GFX)
            App._win.bind(KeyEvent.keydown, self._keyEvent)
            App._win.bind(KeyEvent.keyup, self._keyEvent)
            App._win.bind(KeyEvent.keypress, self._keyEvent)
            App._win.bind(MouseEvent.mousewheel, self._mouseEvent)
            App._win.bind(MouseEvent.mousemove, self._mouseEvent)
            App._win.bind(MouseEvent.mousedown, self._mouseEvent)
            App._win.bind(MouseEvent.mouseup, self._mouseEvent)
            App._win.bind(MouseEvent.click, self._mouseEvent)
            App._win.bind(MouseEvent.dblclick, self._mouseEvent)

        
    def _routeEvent(self, event, evtlist):
        for callback in reversed(evtlist):
            if not event.consumed:
                callback(event)
        
    def _keyEvent(self, hwevent):
        evtlist = App._eventdict.get(
            (hwevent.type, KeyEvent.keys.get(hwevent.keyCode,0)), [])
        evtlist.extend(App._eventdict.get((hwevent.type, '*'), []))
        if len(evtlist) > 0:
            evt = KeyEvent(hwevent)
            self._routeEvent(evt, evtlist)
        return False

    def _mouseEvent(self, hwevent):
        evtlist = App._eventdict.get(hwevent.type, [])
        if len(evtlist) > 0:
            evt = MouseEvent(type(self),hwevent)
            self._routeEvent(evt, evtlist)
        return False

    @classmethod
    def _add(cls, obj):
        if App._win != None:
            App._win.add(obj.GFX)
        App.spritelist.append(obj)
        if type(obj) not in App._spritesdict:
            App._spritesdict[type(obj)] = []
        App._spritesdict[type(obj)].append(obj)

    @classmethod
    def _remove(cls, obj):
        if App._win != None:
            App._win.remove(obj.GFX)
        App.spritelist.remove(obj)
        App._spritesdict[type(obj)].remove(obj)
        
    def _animate(self, dummy):
        if self.userfunc:
            self.userfunc()
        else:
            self.step()
        App._win.animate(self._animate)

    @classmethod
    def _destroy(cls, *args):
        """
        This will close the display window/tab, remove all references to 
        sprites and place the `App` class in a state in which a new 
        application could be instantiated.
        """ 
        if App._win:
            App._win.unbind(KeyEvent.keydown)
            App._win.unbind(KeyEvent.keyup)
            App._win.unbind(KeyEvent.keypress)
            App._win.unbind(MouseEvent.mousewheel)
            App._win.unbind(MouseEvent.mousemove)
            App._win.unbind(MouseEvent.mousedown)
            App._win.unbind(MouseEvent.mouseup)
            App._win.unbind(MouseEvent.click)
            App._win.unbind(MouseEvent.dblclick)
            App._win.destroy()
        App._win = None
        for s in list(App.spritelist):
            s.destroy()
        App.spritelist = []
        App._spritesdict = {}
        App._eventdict = {}
        App._spritesadded = False

    @classmethod
    def listenKeyEvent(cls, eventtype, key, callback):
        """
        Register to receive keyboard events. The `eventtype` parameter is a 
        string that indicates what type of key event to receive (value is one
        of: `'keydown'`, `'keyup'` or `'keypress'`). The `key` parameter is a 
        string indicating which key (e.g. `'space'`, `'left arrow'`, etc.) to 
        receive events for. The `callback` parameter is a reference to a 
        function or method that will be called with the `ggame.KeyEvent` object
        when the event occurs.

        See the source for `ggame.KeyEvent.keys` for a list of key names
        to use with the `key` paramter.
        """
        evtlist = App._eventdict.get((eventtype, key), [])
        if not callback in evtlist:
            evtlist.append(callback)
        App._eventdict[(eventtype, key)] = evtlist

    @classmethod
    def listenMouseEvent(cls, eventtype, callback):
        """
        Register to receive mouse events. The `eventtype` parameter is
        a string that indicates what type of mouse event to receive (
        value is one of: `'mousemove'`, `'mousedown'`, `'mouseup'`, `'click'`, 
        `'dblclick'` or `'mousewheel'`). The `callback` parameter is a 
        reference to a function or method that will be called with the 
        `ggame.MouseEvent` object when the event occurs.
        """
        evtlist = App._eventdict.get(eventtype, [])
        if not callback in evtlist:
            evtlist.append(callback)
        App._eventdict[eventtype] = evtlist

    @classmethod
    def unlistenKeyEvent(cls, eventtype, key, callback):
        """
        Use this method to remove a registration to receive a particular
        keyboard event. Arguments must exactly match those used when
        registering for the event.
        """
        App._eventdict[(eventtype,key)].remove(callback)

    @classmethod
    def unlistenMouseEvent(cls, eventtype, callback):
        """
        Use this method to remove a registration to receive a particular
        mouse event. Arguments must exactly match those used when
        registering for the event.
        """
        App._eventdict[eventtype].remove(callback)

    @classmethod
    def getSpritesbyClass(cls, sclass):
        """
        Returns a list of all active sprites of a given class.
        """
        return App._spritesdict.get(sclass, [])
    
    def step(self):
        """
        The `ggame.App.step` method is called once per animation frame. Override
        this method in your own subclass of `ggame.App` to perform periodic 
        calculations, such as checking for sprite collisions, or calling
        'step' functions in your own customized sprite classes.

        The base class `ggame.App.step` method is empty and is intended to be overriden.
        """
        pass
    
    def run(self, userfunc = None):
        """
        Calling the `ggame.App.run` method begins the animation process whereby the 
        `ggame.App.step` method is called once per animation frame. Set `userfunc`
        to any function which shall be called once per animation frame.
        """
        self.userfunc = userfunc
        App._win.animate(self._animate)


        
