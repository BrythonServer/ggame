# app.py
"""
The ggame :class:`App` class encapsulates functionality required for
initiating a graphics window in the browser, executing code using Javascript
animate, routing browser UI events (e.g. mouse and keyboard input) to
user Python code, and managing graphics elements (instances of
:class:`Sprite`, for example).
"""

import traceback
from ggame.sysdeps import GFX_Window
from ggame.event import KeyEvent, MouseEvent


class App(object):
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
    _win = None

    def __init__(self, *args):
        if self._win is None and (len(args) == 0 or len(args) == 2):
            x = y = 0
            if len(args) == 2:
                x = args[0]
                y = args[1]
            self._win = GFX_Window(x, y, type(self).destroy)
            self.width = self._win.width
            self.height = self._win.height
            # Add existing sprites to the window
            if not self._spritesadded and len(self.spritelist) > 0:
                self._spritesadded = True
                for sprite in self.spritelist:
                    self._win.add(sprite.gfx)
            self._win.bind(KeyEvent.keydown, self._keyEvent)
            self._win.bind(KeyEvent.keyup, self._keyEvent)
            self._win.bind(KeyEvent.keypress, self._keyEvent)
            self._win.bind(MouseEvent.mousewheel, self._mouseEvent)
            self._win.bind(MouseEvent.mousemove, self._mouseEvent)
            self._win.bind(MouseEvent.mousedown, self._mouseEvent)
            self._win.bind(MouseEvent.mouseup, self._mouseEvent)
            self._win.bind(MouseEvent.click, self._mouseEvent)
            self._win.bind(MouseEvent.dblclick, self._mouseEvent)
        self.userfunc = None

    def _keyEvent(self, hwevent):
        evtlist = self._eventdict.get(
            (hwevent.type, KeyEvent.keys.get(hwevent.keyCode, 0)), [])
        evtlist.extend(self._eventdict.get((hwevent.type, '*'), []))
        if len(evtlist) > 0:
            evt = KeyEvent(hwevent)
            evt.route(evtlist)
        return False

    def _mouseEvent(self, hwevent):
        evtlist = self._eventdict.get(hwevent.type, [])
        if len(evtlist) > 0:
            evt = MouseEvent(self, hwevent)
            evt.route(evtlist)
        return False

    @classmethod
    def _add(cls, obj):
        if cls._win is not None:
            cls._win.add(obj.gfx)
        cls.spritelist.append(obj)
        # pylint: disable=unidiomatic-typecheck
        if type(obj) not in cls._spritesdict:
            cls._spritesdict[type(obj)] = []
        cls._spritesdict[type(obj)].append(obj)

    @classmethod
    def _remove(cls, obj):
        if cls._win is not None:
            cls._win.remove(obj.gfx)
        cls.spritelist.remove(obj)
        cls._spritesdict[type(obj)].remove(obj)

    def _animate(self, dummy):
        try:
            if self.userfunc:
                self.userfunc()
            else:
                self.step()
        except BaseException:
            traceback.print_exc()
            raise
        if self._win:
            self._win.animate(self._animate)

    @classmethod
    def destroy(cls):
        """
        This will close the display window/tab, remove all references to
        sprites and place the `App` class in a state in which a new
        application could be instantiated.
        """
        if cls._win:
            cls._win.unbind(KeyEvent.keydown)
            cls._win.unbind(KeyEvent.keyup)
            cls._win.unbind(KeyEvent.keypress)
            cls._win.unbind(MouseEvent.mousewheel)
            cls._win.unbind(MouseEvent.mousemove)
            cls._win.unbind(MouseEvent.mousedown)
            cls._win.unbind(MouseEvent.mouseup)
            cls._win.unbind(MouseEvent.click)
            cls._win.unbind(MouseEvent.dblclick)
            cls._win.destroy()
        cls._win = None
        for s in list(cls.spritelist):
            s.destroy()
        cls.spritelist = []
        cls._spritesdict = {}
        cls._eventdict = {}
        cls._spritesadded = False

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
        names to use with the `key` paramter.
        """
        evtlist = cls._eventdict.get((eventtype, key), [])
        if callback not in evtlist:
            evtlist.append(callback)
        cls._eventdict[(eventtype, key)] = evtlist

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
        evtlist = cls._eventdict.get(eventtype, [])
        if callback not in evtlist:
            evtlist.append(callback)
        cls._eventdict[eventtype] = evtlist

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
        cls._eventdict[(eventtype, key)].remove(callback)

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
        cls._eventdict[eventtype].remove(callback)

    @classmethod
    def getSpritesbyClass(cls, sclass):
        """
        Returns a list of all active sprites of a given class.

        :param class sclass: A class name (e.g. 'Sprite') or subclass.

        :returns: A (potentially empty) list of sprite references.
        """
        return cls._spritesdict.get(sclass, [])

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
        pass

    def run(self, userfunc=None):
        """
        Calling the :meth:`~App.run` method begins the animation process
        whereby the :meth:`~App.step` method is called once per animation frame.

        :param function userfunc: Any function or method which shall be
            called once per animation frame.

        :returns: Nothing
        """
        self.userfunc = userfunc
        self._win.animate(self._animate)
