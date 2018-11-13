.. module:: ggame


Introduction
============

Ggame is **not** intended to be a full-featured gaming API, with every bell and 
whistle. It is designed primarily as a tool for teaching computer programming, 
recognizing that the ability to create engaging and interactive games is a 
powerful motivator for many progamming students. Accordingly, any functional or 
performance enhancements that *can* be reasonably implemented by the user are 
left as an exercise. 

Functionality Goals
___________________

The ggame library is intended to be trivially easy to use. For example:

.. literalinclude:: ../examples/onebunny.py
   :language: python



Extensions
__________

Ggame is being extended for geometry exploration in a manner 
reminiscent of Geogebra, digital logic simulation, and with tools and 
classes to use with rocket and orbital simulations.

Overview
________

There are three major pieces in a ggame app: assets, sprites and the app itself.

Assets
^^^^^^

Asset objects (i.e. ``ImageAsset``, etc.) typically represent separate files that
are provided by the "art department". These might be background images, user interface
images, or images that represent objects in the game. In addition, ``SoundAsset`` 
are used to represent sound files (.wav or .mp3 format) that can be played in the 
game.

Ggame also extends the asset concept to include graphics that are generated dynamically
at run-time, such as geometrical objects, e.g. rectangles, lines, etc.

Sprites
^^^^^^^

All of the visual aspects of the game are represented by instances of ``Sprite`` or
subclasses of it. 

App
^^^

Every ggame application must create a single instance of the :class:`App` class (or 
a sub-class of it). Create an instance of the :class:`App` class to draw a 
graphics canvas in your browser window. Execute the app's :meth:`~App.run` method to
start refreshing and redrawing the visual assets on the screen. 

Events
^^^^^^

No game is complete without a player and players make events. Your code handles 
user input by registering to receive keyboard and mouse events using
:meth:`~App.listenKeyEvent` and :meth:`~App.listenMouseEvent` methods of the :class:`App` class.

Execution Environment
_____________________

Ggame is designed to execute in a web browser using `Brython <http://brython.info/>`_,
`Pixi.js <http://www.pixijs.com/>`_ and `Buzz <http://buzz.jaysalvat.com/>`_. 
The easiest way to do this is by executing from 
`runpython <https://runpython.org>`_, with your source code stored at 
`github <http://github.com>`_. When you use ggame from within 
`runpython <https://runpython.org>`_, the Github ggame repository is 
automatically placed on the import search path.

Geometry
________

When referring to screen coordinates, note that the x-axis of the computer screen
is *horizontal* with the zero position on the left hand side of the screen. The 
y-axis is *vertical* with the zero position at the **top** of the screen.

Increasing positive y-coordinates correspond to the downward direction on the 
computer screen. Note that this is **different** from the way you may have learned
about x and y coordinates in math class!


