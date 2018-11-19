***********
Mathematics
***********

These mathematics and geometry extensions subclass the :class:`~ggame.app.App` 
and :class:`~ggame.sprite.Sprite` classes to create a framework for building
apps that mimic some of the functionality of online math tools like Geogebra.

These extensions are very experimental and are not fully developed!

ggMath Application Class
========================

.. module:: ggame.mathapp

.. autoclass:: MathApp

    .. autoattribute:: viewPosition
    .. autoattribute:: scale
    .. autoattribute:: width

    .. automethod:: getSpritesbyClass
    .. automethod:: listenKeyEvent
    .. automethod:: listenMouseEvent
    .. automethod:: unlistenKeyEvent
    .. automethod:: unlistenMouseEvent
    .. automethod:: run
    .. automethod:: logicalToPhysical
    .. automethod:: physicalToLogical
    .. automethod:: translateLogicalToPhysical
    .. automethod:: translatePhysicalToLogical
    .. automethod:: distance
    .. automethod:: addViewNotification
    .. automethod:: removeViewNotification
    
    