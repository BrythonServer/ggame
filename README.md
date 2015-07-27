# ggame
Simple cross-platform sprite and game platform for Brython and/or Pygame.

## Functionality Goals

The runsprites library is intended to be trivially easy to use. For example:

    from runsprites import Sprite
    
    s = Sprite('bunny.jpg')   # Create a graphics screen with a centered image-based sprite
    s.position = (10,10)      # Move the image to coordinates x=10, y=10 (positive y == up)

The runsprites should be architecturally *possible* under both Brython/PIXI and Pygame.

In order to achieve this trivial use case, "run loop" must function as an independent thread. Possible?
