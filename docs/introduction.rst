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

.. literalinclude:: /examples/onebunny.py
   :language: python



## Extensions

The `ggame` library has been extended with [ggmath](/ggame/ggmath.html) for geometry
exploration in a manner reminiscent of Geogebra, and [ggrocket](/ggame/ggrocket.html)
for tools and classes to use with rocket and orbital simulations.

## Overview

There are three major components to the `ggame` system: Assets, Sprites and the App.

### Assets

Asset objects (i.e. `ggame.ImageAsset`, etc.) typically represent separate files that
are provided by the "art department". These might be background images, user interface
images, or images that represent objects in the game. In addition, `ggame.SoundAsset` 
is used to represent sound files (`.wav` or `.mp3` format) that can be played in the 
game.

Ggame also extends the asset concept to include graphics that are generated dynamically
at run-time, such as geometrical objects, e.g. rectangles, lines, etc.

### Sprites

All of the visual aspects of the game are represented by instances of `ggame.Sprite` or
subclasses of it. 

### App

Every ggame application must create a single instance of the `ggame.App` class (or 
a sub-class of it). Creating an instance of the `ggame.App` class will initiate 
creation of a pop-up window on your browser. Executing the app's `run` method will
begin the process of refreshing the visual assets on the screen. 

### Events

No game is complete without a player and players produce events. Your code handles user
input by registering to receive keyboard and mouse events using `ggame.App.listenKeyEvent` and
`ggame.App.listenMouseEvent` methods.

## Execution Environment

Ggame is designed to be executed in a web browser using [Brython](http://brython.info/),
[Pixi.js](http://www.pixijs.com/) and [Buzz](http://buzz.jaysalvat.com/). The easiest
way to do this is by executing from [runpython](http://runpython.com), with source
code residing on [github](http://github.com).

To use Ggame in your own application, you may create a folder called
`ggame` in your project. Within `ggame`, copy the `ggame.py`, `sysdeps.py` and 
`__init__.py` files from the [ggame project](https://github.com/BrythonServer/ggame).

When using `ggame` from within [runpython](http://runpython.com), the Github
`ggame` repository is automatically placed on the import search path.

## Geometry

When referring to screen coordinates, note that the x-axis of the computer screen
is *horizontal* with the zero position on the left hand side of the screen. The 
y-axis is *vertical* with the zero position at the **top** of the screen.

Increasing positive y-coordinates correspond to the downward direction on the 
computer screen. Note that this is **different** from the way you may have learned
about x and y coordinates in math class!
