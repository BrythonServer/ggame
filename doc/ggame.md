Module ggame
------------

Variables
---------
GFX

GFX_Texture

SND

document

window

Classes
-------
App 
    Singleton base class for ggame applications

    Ancestors (in MRO)
    ------------------
    ggame.App
    builtins.object

    Static methods
    --------------
    __init__(self, *args)

    destroy(self, dummy)

    listenKeyEvent(self, eventtype, key, callback)
        eventtype : "keydown", "keyup", "keypress"
        key : e.g. "space", "a" or "*" for ALL!
        callback : function name to receive events

    listenMouseEvent(self, eventtype, callback)

    run(self, userfunc=None)

    step(self)

    unlistenKeyEvent(self, eventtype, key, callback)

    unlistenMouseEvent(self, eventtype, callback)

CircleAsset 
    Ancestors (in MRO)
    ------------------
    ggame.CircleAsset
    ggame.ShapeAsset
    ggame.CurveAsset
    ggame.GraphicsAsset
    builtins.object

    Static methods
    --------------
    __init__(self, radius, line, fill)

    destroy(self)

    Instance variables
    ------------------
    GFX

    radius

Color 
    Ancestors (in MRO)
    ------------------
    ggame.Color
    builtins.object

    Static methods
    --------------
    __init__(self, color, alpha)
        color : integer e.g. 0xffff00
        alpha : float 0-1

    Instance variables
    ------------------
    alpha

    color

CurveAsset 
    Ancestors (in MRO)
    ------------------
    ggame.CurveAsset
    ggame.GraphicsAsset
    builtins.object

    Descendents
    -----------
    ggame.ShapeAsset
    ggame.LineAsset

    Static methods
    --------------
    __init__(self, line)

    destroy(self)

EllipseAsset 
    Ancestors (in MRO)
    ------------------
    ggame.EllipseAsset
    ggame.ShapeAsset
    ggame.CurveAsset
    ggame.GraphicsAsset
    builtins.object

    Static methods
    --------------
    __init__(self, halfw, halfh, line, fill)

    destroy(self)

    Instance variables
    ------------------
    GFX

    halfh

    halfw

Event 
    Ancestors (in MRO)
    ------------------
    ggame.Event
    builtins.object

    Descendents
    -----------
    ggame.MouseEvent
    ggame.KeyEvent

    Static methods
    --------------
    __init__(self, hwevent)

    Instance variables
    ------------------
    consumed

    hwevent

    type

Frame 
    Ancestors (in MRO)
    ------------------
    ggame.Frame
    builtins.object

    Static methods
    --------------
    __init__(self, x, y, w, h)

    Instance variables
    ------------------
    GFX

    center

    h

    w

    x

    y

GraphicsAsset 
    Ancestors (in MRO)
    ------------------
    ggame.GraphicsAsset
    builtins.object

    Descendents
    -----------
    ggame.CurveAsset
    ggame.TextAsset

    Static methods
    --------------
    destroy(self)

ImageAsset 
    Ancestors (in MRO)
    ------------------
    ggame.ImageAsset
    builtins.object

    Static methods
    --------------
    __init__(self, url)

    Instance variables
    ------------------
    GFX

    url

KeyEvent 
    Ancestors (in MRO)
    ------------------
    ggame.KeyEvent
    ggame.Event
    builtins.object

    Class variables
    ---------------
    keydown

    keypress

    keys

    keyup

    left_location

    no_location

    right_location

    Static methods
    --------------
    __init__(self, hwevent)

    Instance variables
    ------------------
    key

    keynum

LineAsset 
    Ancestors (in MRO)
    ------------------
    ggame.LineAsset
    ggame.CurveAsset
    ggame.GraphicsAsset
    builtins.object

    Static methods
    --------------
    __init__(self, x, y, line)

    destroy(self)

    Instance variables
    ------------------
    GFX

    deltaX

    deltaY

LineStyle 
    Ancestors (in MRO)
    ------------------
    ggame.LineStyle
    builtins.object

    Static methods
    --------------
    __init__(self, width, color)
        width : line width pixels
        color : integer e.g. 0xffff00
        alpha : float 0-1

    Instance variables
    ------------------
    color

    width

MouseEvent 
    Ancestors (in MRO)
    ------------------
    ggame.MouseEvent
    ggame.Event
    builtins.object

    Class variables
    ---------------
    click

    dblclick

    mousedown

    mousemove

    mouseup

    mousewheel

    Static methods
    --------------
    __init__(self, hwevent)

    Instance variables
    ------------------
    x

    y

PolygonAsset 
    Ancestors (in MRO)
    ------------------
    ggame.PolygonAsset
    ggame.ShapeAsset
    ggame.CurveAsset
    ggame.GraphicsAsset
    builtins.object

    Static methods
    --------------
    __init__(self, path, line, fill)

    destroy(self)

    Instance variables
    ------------------
    GFX

    path

RectangleAsset 
    Ancestors (in MRO)
    ------------------
    ggame.RectangleAsset
    ggame.ShapeAsset
    ggame.CurveAsset
    ggame.GraphicsAsset
    builtins.object

    Static methods
    --------------
    __init__(self, width, height, line, fill)

    destroy(self)

    Instance variables
    ------------------
    GFX

    height

    width

ShapeAsset 
    Ancestors (in MRO)
    ------------------
    ggame.ShapeAsset
    ggame.CurveAsset
    ggame.GraphicsAsset
    builtins.object

    Descendents
    -----------
    ggame.RectangleAsset
    ggame.CircleAsset
    ggame.EllipseAsset
    ggame.PolygonAsset

    Static methods
    --------------
    __init__(self, line, fill)

    destroy(self)

Sound 
    Ancestors (in MRO)
    ------------------
    ggame.Sound
    builtins.object

    Static methods
    --------------
    __init__(self, asset)

    loop(self)

    play(self)

    stop(self)

    Instance variables
    ------------------
    SND

    asset

    volume

SoundAsset 
    Ancestors (in MRO)
    ------------------
    ggame.SoundAsset
    builtins.object

    Static methods
    --------------
    __init__(self, url)

    Instance variables
    ------------------
    url

Sprite 
    Ancestors (in MRO)
    ------------------
    ggame.Sprite
    builtins.object

    Static methods
    --------------
    __init__(self, asset, position=(0, 0), frame=False)

    destroy(self)

    Instance variables
    ------------------
    app

    height

    position

    visible

    width

    x

    y

TextAsset 
    Ancestors (in MRO)
    ------------------
    ggame.TextAsset
    ggame.GraphicsAsset
    builtins.object

    Static methods
    --------------
    __init__(self, text, **kwargs)
        app : the App reference
        text : text to display
        style = : default "20px Arial", e.g. "italic 20pt Helvetica"
        width = : width of text area (pixels), default 100
        fill = : color of text, default black
        align = : align style, default "left". "left", "center", "right"

    clone(self)

    destroy(self)

    Instance variables
    ------------------
    GFX

    align

    fill

    style

    text

    width
