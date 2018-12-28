"""
Example of using Sprite class.
"""
from ggame.sprite import Sprite
from ggame.asset import ImageAsset, CircleAsset
from ggame.app import App

PLAYER = Sprite(ImageAsset("bunny.png"), (100, 100), CircleAsset(50))

App().run()
