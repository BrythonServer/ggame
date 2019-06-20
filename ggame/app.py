"""
The ggame :class:`App` class encapsulates functionality required for
initiating a graphics window in the browser, executing code using Javascript
animate, routing browser UI events (e.g. mouse and keyboard input) to
user Python code, and managing graphics elements (instances of
:class:`Sprite`, for example).
"""

# app.py

import traceback
from ggame.sysdeps import GFX_Window
from ggame.event import MouseEvent, KeyEvent


class App:
    """
    The :class:`App` class is a (typically subclassed) class that encapsulates
    handling of the display system, and processing user events. The :class:`App`
    class also manages lists of all :class:`Sprite` instances in the
    application.

    When subclassing :class:`App` you may elect to instantiate most of your
    sprite objects in the initialization section.

    Processing that must occur on a per-frame basis may be included by
    overriding the :meth:`~App.run` method. This is also an appropriate
    location to call similar 'step' methods for your various customized sprite
    classes.

    Once your application class has been instantiated, begin the frame drawing
    process by calling its :meth:`~App.run` method.

    The :class:`App` class is instantiated either by specifying the desired app
    window size in pixels, as two parameters:::

        myapp = App(640,480)

    or by providing no size parameters at all:::

        myapp = App()

    in which case, the full browser window size is used.

    NOTE: Only **one** instance of an :class:`App` class or subclass may be
    instantiated at a time.
    """

    spritelist = []
    """
    List of all sprites currently active in the application.
    """
    _eventdict = {}
    _spritesdict = {}
    _spritesadded = False
    win = None

    def __init__(self, *args):
        if App.win is None and (not args or len(args) == 2):
            x = y = 0
            if len(args) == 2:
                x = args[0]
                y = args[1]
            App.win = GFX_Window(x, y, type(self).destroy)
            App.width = App.win.width
            App.height = App.win.height
            # Add existing sprites to the window
            if not App._spritesadded and App.spritelist:
                App._spritesadded = True
                for sprite in App.spritelist:
                    App.win.add(sprite.gfx)
            App.win.bind(KeyEvent.keydown, type(self)._keyEvent)
            App.win.bind(KeyEvent.keyup, type(self)._keyEvent)
            App.win.bind(KeyEvent.keypress, type(self)._keyEvent)
            App.win.bind(MouseEvent.mousewheel, type(self)._mouseEvent)
            App.win.bind(MouseEvent.mousemove, type(self)._mouseEvent)
            App.win.bind(MouseEvent.mousedown, type(self)._mouseEvent)
            App.win.bind(MouseEvent.mouseup, type(self)._mouseEvent)
            App.win.bind(MouseEvent.click, type(self)._mouseEvent)
            App.win.bind(MouseEvent.dblclick, type(self)._mouseEvent)
        self.userfunc = None

    @classmethod
    def _routeEvent(cls, event, evtlist):
        for callback in reversed(evtlist):
            if not event.consumed:
                try:
                    callback(event)
                except BaseException:
                    traceback.print_exc()
                    raise

    @classmethod
    def _keyEvent(cls, hwevent):
        evtlist = App._eventdict.get(
            (hwevent.type, KeyEvent.keys.get(hwevent.keyCode, 0)), []
        )
        evtlist.extend(App._eventdict.get((hwevent.type, "*"), []))
        if evtlist:
            evt = KeyEvent(hwevent)
            cls._routeEvent(evt, evtlist)
        return False

    @classmethod
    def _mouseEvent(cls, hwevent):
        evtlist = App._eventdict.get(hwevent.type, [])
        if evtlist:
            evt = MouseEvent(cls, hwevent)
            cls._routeEvent(evt, evtlist)
        return False

    @classmethod
    def add(cls, obj):
        """
        Add a sprite object to the global lists.

        :param Sprite obj: The sprite reference to add.
        :returns: None
        """
        if App.win is not None:
            App.win.add(obj.gfx)
        App.spritelist.append(obj)
        # find out if sprite type is in dictionary without triggering pylint
        if not App._spritesdict.get(type(obj), False):
            App._spritesdict[type(obj)] = []
        App._spritesdict[type(obj)].append(obj)

    @classmethod
    def remove(cls, obj):
        """
        Remove a sprite object from the global lists.

        :param Sprite obj: The sprite reference to remove.
        :returns: None
        """
        App.spritelist.remove(obj)
        # remove from underlying layer only if existed in ours
        if App.win is not None:
            App.win.remove(obj.gfx)
        App._spritesdict[type(obj)].remove(obj)

    def _animate(self, _dummy):
        if App.win:
            try:
                if self.userfunc:
                    self.userfunc()
                else:
                    self.step()
            except BaseException:
                traceback.print_exc()
                raise
            App.win.animate(self._animate)

    @classmethod
    def destroy(cls):
        """
        This will close the display window/tab, remove all references to
        sprites and place the `App` class in a state in which a new
        application could be instantiated.
        """
        if App.win:
            App.win.unbind(KeyEvent.keydown)
            App.win.unbind(KeyEvent.keyup)
            App.win.unbind(KeyEvent.keypress)
            App.win.unbind(MouseEvent.mousewheel)
            App.win.unbind(MouseEvent.mousemove)
            App.win.unbind(MouseEvent.mousedown)
            App.win.unbind(MouseEvent.mouseup)
            App.win.unbind(MouseEvent.click)
            App.win.unbind(MouseEvent.dblclick)
        for s in list(App.spritelist):
            s.destroy()
        App.win.destroy()
        App.win = None
        App.spritelist = []
        App._spritesdict = {}
        App._eventdict = {}
        App._spritesadded = False

    @classmethod
    def listenKeyEvent(cls, eventtype, key, callback):
        """
        Register to receive keyboard events.

        :param str eventtype:  The type of key event to
            receive (value is one of: `'keydown'`, `'keyup'` or `'keypress'`).

        :param str key:  Identify the keyboard key (e.g. `'space'`,
            `'left arrow'`, etc.) to receive events for.

        :param function callback:  The function or method that will be
            called with the :class:`~ggame.event.KeyEvent` object when the
            event occurs.

        :returns: Nothing

        See the source for :class:`~ggame.event.KeyEvent` for a list of key
        names
        to use with the `key` paramter.
        """
        evtlist = App._eventdict.get((eventtype, key), [])
        if callback not in evtlist:
            evtlist.append(callback)
        App._eventdict[(eventtype, key)] = evtlist

    @classmethod
    def listenMouseEvent(cls, eventtype, callback):
        """
        Register to receive mouse events.

        :param str eventtype: The type of mouse event to
            receive (value is one of: `'mousemove'`, `'mousedown'`, `'mouseup'`,
            `'click'`, `'dblclick'` or `'mousewheel'`).

        :param function callback: The function or method that will be
            called with the :class:`ggame.event.MouseEvent` object when the
            event occurs.

        :returns: Nothing
        """
        evtlist = App._eventdict.get(eventtype, [])
        if callback not in evtlist:
            evtlist.append(callback)
        App._eventdict[eventtype] = evtlist

    @classmethod
    def unlistenKeyEvent(cls, eventtype, key, callback):
        """
        Use this method to remove a registration to receive a particular
        keyboard event. Arguments must exactly match those used when
        registering for the event.

        :param str eventtype:  The type of key event to stop
            receiving (value is one of: `'keydown'`, `'keyup'` or `'keypress'`).

        :param str key:  The keyboard key (e.g. `'space'`,
            `'left arrow'`, etc.) to stop receiving events for.

        :param function callback:  The function or method that will no longer
            be called with the :class:`~ggame.event.KeyEvent` object when the
            event occurs.

        :returns: Nothing

        See the source for :class:`~ggame.event.KeyEvent` for a list of key
        names to use with the `key` paramter.

        """
        App._eventdict[(eventtype, key)].remove(callback)

    @classmethod
    def unlistenMouseEvent(cls, eventtype, callback):
        """
        Use this method to remove a registration to receive a particular
        mouse event. Arguments must exactly match those used when
        registering for the event.

        :param str eventtype: The type of mouse event to stop receiving events
            for (value is one of: `'mousemove'`, `'mousedown'`, `'mouseup'`,
            `'click'`, `'dblclick'` or `'mousewheel'`).

        :param function callback: The function or method that will no longer be
            called with the :class:`ggame.event.MouseEvent` object when the
            event occurs.

        :returns: Nothing
        """
        App._eventdict[eventtype].remove(callback)

    @classmethod
    def getSpritesbyClass(cls, sclass):
        """
        Returns a list of all active sprites of a given class.

        :param class sclass: A class name (e.g. 'Sprite') or subclass.

        :returns: A (potentially empty) list of sprite references.
        """
        return App._spritesdict.get(sclass, [])[:]

    def step(self):
        """
        The :meth:`~App.step` method is called once per animation frame.
        Override this method in your own subclass of :class:`App` to perform
        periodic calculations, such as checking for sprite collisions, or
        calling 'step' functions in your own customized sprite classes.

        The base class :meth:`~App.step` method is empty and is intended to be
        overriden.

        :returns: Nothing

        """

    def run(self, userfunc=None):
        """
        Calling the :meth:`~App.run` method begins the animation process
        whereby the :meth:`~App.step` method is called once per animation frame.

        :param function userfunc: Any function or method which shall be
            called once per animation frame.

        :returns: Nothing
        """
        self.userfunc = userfunc
        App.win.animate(self._animate)
