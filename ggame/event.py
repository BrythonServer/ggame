class _Event(object):

    def __init__(self, hwevent):
        self.hwevent = hwevent
        """The underlying system event object."""
        self.type = hwevent.type
        """String representing the type of received event."""
        self.consumed = False
        """
        Set the `consumed` member of the event to prevent the event
        from being received by any more handler methods.
        """
        
class MouseEvent(_Event):
    """
    The `ggame.MouseEvent` class encapsulates information regarding a user mouse
    action that is being reported by the system.
    """    

    mousemove = "mousemove"
    """Constant identifying a `mousemove` event."""
    mousedown = "mousedown"
    """Constant identifying a `mousedown` event."""
    mouseup = "mouseup"
    """Constant identifying a `mouseup` event."""
    click = "click"
    """Constant identifying a button `click` event."""
    dblclick = "dblclick"
    """Constant identifying a button `dblclick` event."""
    mousewheel = "wheel"
    """Constant identifying a mouse `wheel` scroll event."""
    
    def __init__(self, appclass, hwevent):
        """
        The event is initialized by the system, with a `hwevent` input parameter.
        """
        super().__init__(hwevent)
        self.wheelDelta = 0
        """Integer representing up/down motion of the scroll wheel."""
        if self.type == self.mousewheel:
            self.wheelDelta = hwevent.deltaY
        else:
            self.wheelDelta = 0
        rect = appclass._win._renderer.view.getBoundingClientRect()
        xscale = appclass._win.width/rect.width
        yscale = appclass._win.height/rect.height
        self.x = (hwevent.clientX - rect.left) * xscale
        """The window x-coordinate of the mouse pointer when the event occurred."""
        self.y = (hwevent.clientY - rect.top) * yscale
        """The window y-coordinate of the mouse pointer when the event occurred."""


class KeyEvent(_Event):
    """
    The `ggame.KeyEvent` class encapsulates information regarding a user keyboard
    action that is being reported by the system.
    """    

    no_location = 0
    """Constant indicating no specific location for the key event."""
    right_location = 2
    """Constant indicating the key event was on the right hand side of the keyboard."""
    left_location = 1
    """Constant indicating the key event was on the left hand side of the keyboard."""
    keydown = "keydown"
    """Constant indicating the key was pressed down."""
    keyup = "keyup"
    """Constant indicating the key was released."""
    keypress = "keypress"
    """Constant indicating the combination of keydown, followed by keyup."""
    keys = {8: 'backspace',
        9: 'tab',
        13: 'enter',
        16: 'shift',
        17: 'ctrl',
        18: 'alt',
        19: 'pause/break',
        20: 'caps lock',
        27: 'escape',
        32: 'space',
        33: 'page up',
        34: 'page down',
        35: 'end',
        36: 'home',
        37: 'left arrow',
        38: 'up arrow',
        39: 'right arrow',
        40: 'down arrow',
        45: 'insert',
        46: 'delete',
        48: '0',
        49: '1',
        50: '2',
        51: '3',
        52: '4',
        53: '5',
        54: '6',
        55: '7',
        56: '8',
        57: '9',
        65: 'a',
        66: 'b',
        67: 'c',
        68: 'd',
        69: 'e',
        70: 'f',
        71: 'g',
        72: 'h',
        73: 'i',
        74: 'j',
        75: 'k',
        76: 'l',
        77: 'm',
        78: 'n',
        79: 'o',
        80: 'p',
        81: 'q',
        82: 'r',
        83: 's',
        84: 't',
        85: 'u',
        86: 'v',
        87: 'w',
        88: 'x',
        89: 'y',
        90: 'z',
        91: 'left window key',
        92: 'right window key',
        93: 'select key',
        96: 'numpad 0',
        97: 'numpad 1',
        98: 'numpad 2',
        99: 'numpad 3',
        100: 'numpad 4',
        101: 'numpad 5',
        102: 'numpad 6',
        103: 'numpad 7',
        104: 'numpad 8',
        105: 'numpad 9',
        106: 'multiply',
        107: 'add',
        109: 'subtract',
        110: 'decimal point',
        111: 'divide',
        112: 'f1',
        113: 'f2',
        114: 'f3',
        115: 'f4',
        116: 'f5',
        117: 'f6',
        118: 'f7',
        119: 'f8',
        120: 'f9',
        121: 'f10',
        122: 'f11',
        123: 'f12',
        144: 'num lock',
        145: 'scroll lock',
        186: 'semicolon',
        187: 'equal sign',
        188: 'comma',
        189: 'dash',
        190: 'period',
        191: 'forward slash',
        192: 'grave accent',
        219: 'open bracket',
        220: 'back slash',
        221: 'close bracket',
        222: 'single quote'}    
    """Dictionary mapping key code integers to textual key description."""
    
    def __init__(self, hwevent):
        """
        The event is initialized by the system, with a `hwevent` input parameter.
        """
        super().__init__(hwevent)
        self.keynum = hwevent.keyCode
        """The `keynum` attribute identifies a keycode (number)."""
        self.key = self.keys[hwevent.keyCode]
        """The `key` attribute identifes the key in text form (e.g. 'back slash')."""
