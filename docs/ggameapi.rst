Ggame
=====

.. module:: ggame.app

App
___

.. autoclass:: App
    
    .. autoattribute:: spritelist
    
    .. automethod:: getSpritesbyClass
    
    .. automethod:: listenKeyEvent
    
    .. automethod:: listenMouseEvent
    
    .. automethod:: unlistenKeyEvent
    
    .. automethod:: unlistenMouseEvent
    
    .. automethod:: run
    
    .. automethod:: step
        

.. automodule:: ggame.asset

Frame
_____

.. autoclass:: Frame
    :exclude-members: GFX
    
    .. autoattribute:: x
    .. autoattribute:: y
    .. autoattribute:: w
    .. autoattribute:: h
    .. autoattribute:: center
    
Color
_____

.. autoclass:: Color

LineStyle
_________

.. autoclass:: LineStyle

Predefined Colors and Lines
___________________________

.. autodata:: black
.. autodata:: white
.. autodata:: blackline
.. autodata:: whiteline

ImageAsset
__________

.. autoclass:: ImageAsset
    :members:
    :inherited-members:
    :exclude-members: GFX

RectangleAsset
______________

.. autoclass:: RectangleAsset
    :members:
    :inherited-members:
    :exclude-members: GFX

EllipseAsset
____________

.. autoclass:: EllipseAsset
    :members:
    :inherited-members:
    :exclude-members: GFX

PolygonAsset
____________

.. autoclass:: PolygonAsset
    :members:
    :inherited-members:
    :exclude-members: GFX

LineAsset
_________

.. autoclass:: LineAsset
    :members:
    :inherited-members:
    :exclude-members: GFX, deltaX, deltaY

TextAsset
_________

.. autoclass:: TextAsset
    :members:
    :inherited-members:
    :exclude-members: GFX

