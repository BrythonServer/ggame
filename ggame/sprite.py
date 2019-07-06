"""
Sprite class for encapsulating all visible objects in ggame applications.
"""
import os
import math
from ggame.sysdeps import GFX_Sprite
from ggame.asset import (
    RectangleAsset,
    CircleAsset,
    ImageAsset,
    PolygonAsset,
    EllipseAsset,
    TextAsset,
    LineAsset,
)
from ggame.app import App

# pylint: disable=useless-object-inheritance
class Sprite(object):  # pylint: disable=too-many-public-methods
    """
    The Sprite class combines the idea of a visual/graphical asset, a
    position on the screen, and *behavior*. Although the Sprite can be
    used as-is, it is generally subclassed to give it some desired behavior.

    When subclassing the Sprite class, you may customize the initialization
    code to use a specific asset. A 'step' or 'poll' method may be added
    for handling per-frame actions (e.g. checking for collisions). Step or poll
    functions are not automatically called by the :class:`~ggame.app.App` class,
    but you may subclass the :class:`~ggame.app.App` class in order to do this.

    Furthermore, you may wish to define event callback methods in your customized
    sprite class. With customized creation, event handling, and periodic processing
    you can achieve fully autonomous behavior for your sprite objects.

    :param asset asset: An existing graphical asset

    :param tuple(int,int) pos:  The sprite position may be provided, which
        specifies the starting (x,y) coordinates of the sprite on the screen.
        By default, the position of a sprite defines the location of its upper-left
        hand corner. This behavior can be modified by customizing its
        :data:`center`.

    :param asset edgedef: An edge definition asset may be provided, which
        specifies an asset that will be used to define the boundaries of
        the sprite for the purpose of collision detection. If no `edgedef`
        asset is given, the required asset is used, which will be a rectangular
        asset in the case of an image texture. This option is typically used
        to define a visible image outline for a texture-based sprite that has
        a transparent texture image background.

    :returns: Nothing. If the position is on screen the sprite will be displayed
        in the browser.

    Example of use:

    .. literalinclude:: ../examples/spritesprite.py

    This creates a sprite using the 'player.png' image, positioned with its
    upper-left corner at coordinates (100,100) and with a 50 pixel radius
    circular collision border.

    """

    def __init__(self, asset, pos=(0, 0), edgedef=None):
        self._index = 0
        if isinstance(asset, ImageAsset):
            self.asset = asset
            try:
                self.gfx = GFX_Sprite(asset.gfx)  # gfx is PIXI Sprite
            except:  # pylint: disable=bare-except
                self.gfx = None
                raise
        elif isinstance(
            asset, (RectangleAsset, CircleAsset, EllipseAsset, PolygonAsset, LineAsset)
        ):
            self.asset = asset
            self.gfx = GFX_Sprite(asset.gfx.generateTexture())
        elif isinstance(asset, TextAsset):
            self.asset = asset.clone()
            self.gfx = self.asset.gfx  # gfx is PIXI Text (from Sprite)
            self.gfx.visible = True
        if not edgedef:
            self.edgedef = asset
        else:
            self.edgedef = edgedef
        self.xmin = self.xmax = self.ymin = self.ymax = 0
        self.position = pos
        """Tuple indicates the position of the sprite on the screen."""
        self._extentsdirty = True
        """Boolean indicates if extents must be calculated before collision test"""
        self._createBaseVertices()
        self._absolutevertices = None
        self.setExtents()
        App.add(self)

    def _createBaseVertices(self):
        """
        Create sprite-relative list of vertex coordinates for boundary
        """
        self._basevertices = []
        assettype = type(self.edgedef)
        if assettype in [RectangleAsset, ImageAsset, TextAsset]:
            self._basevertices = [
                (0, 0),
                (0, self.edgedef.height),
                (self.edgedef.width, self.edgedef.height),
                (self.edgedef.width, 0),
            ]
        elif assettype in [PolygonAsset, LineAsset]:
            if assettype is PolygonAsset:
                self._basevertices = self.edgedef.path[:-1]
            elif assettype is LineAsset:
                self._basevertices = [
                    (0, 0),
                    (self.edgedef.delta_x, self.edgedef.delta_y),
                ]
            xpoints, ypoints = zip(*self._basevertices)
            xmin = min(xpoints)
            ymin = min(ypoints)
            xpoints = [x - xmin for x in xpoints]
            ypoints = [y - ymin for y in ypoints]
            self._basevertices = list(zip(xpoints, ypoints))
        elif assettype is EllipseAsset:
            w = self.edgedef.halfw * 2
            h = self.edgedef.halfh * 2
            self._basevertices = [(0, 0), (0, h), (w, h), (w, 0)]

    def _xformVertices(self):
        """
        Create window-relative list of vertex coordinates for boundary
        """
        # find center as sprite-relative points (note sprite may be scaled)
        x = self.width * self.fxcenter / self.scale
        y = self.height * self.fycenter / self.scale
        if self.scale != 1.0:
            sc = self.scale
            # center-relative, scaled coordinates
            crsc = [((xp - x) * sc, (yp - y) * sc) for xp, yp in self._basevertices]
        else:
            crsc = [(xp - x, yp - y) for xp, yp in self._basevertices]

        # absolute, rotated coordinates
        c = math.cos(self.rotation)
        s = math.sin(self.rotation)
        self._absolutevertices = [
            (self.x + x * c + y * s, self.y + -x * s + y * c) for x, y in crsc
        ]

    def setExtents(self):
        """
        update min/max x and y based on position, center, width, height
        """
        if self._extentsdirty:
            if isinstance(self.edgedef, CircleAsset):
                th = (
                    math.atan2(self.fycenter - 0.5, 0.5 - self.fxcenter) + self.rotation
                )
                d = self.edgedef.radius * 2 * self.scale
                l = (
                    math.sqrt(
                        math.pow(self.fxcenter - 0.5, 2)
                        + math.pow(self.fycenter - 0.5, 2)
                    )
                    * d
                )
                self.xmin = self.x + int(l * math.cos(th)) - d // 2
                self.ymin = self.y - int(l * math.sin(th)) - d // 2
                self.xmax = self.xmin + d
                self.ymax = self.ymin + d
            else:
                # Build vertex list
                self._xformVertices()
                x, y = zip(*self._absolutevertices)
                self.xmin = min(x)
                self.xmax = max(x)
                self.ymin = min(y)
                self.ymax = max(y)
            self._extentsdirty = False

    def firstImage(self):
        """
        Select and display the *first* image used by this sprite. This only
        does something useful if the asset is an :class:`~ggame.asset.ImageAsset`
        defined with multiple images.
        """
        self.gfx.texture = self.asset[0]

    def lastImage(self):
        """
        Select and display the *last* image used by this sprite. This only
        does something useful if the asset is an :class:`~ggame.asset.ImageAsset`
        defined with multiple images.
        """
        self.gfx.texture = self.asset[-1]

    def nextImage(self, wrap=False):
        """
        Select and display the *next* image used by this sprite.
        If the current image is already the *last* image, then
        the image is not advanced.

        :param boolean wrap: If `True`, then calling
            :meth:`nextImage` on the last image will cause the *first*
            image to be loaded.

        This only does something useful if the asset is an
        :class:`~ggame.asset.ImageAsset` defined with multiple images.
        """
        self._index += 1
        if self._index >= len(self.asset):
            if wrap:
                self._index = 0
            else:
                self._index = len(self.asset) - 1
        self.gfx.texture = self.asset[self._index]

    def prevImage(self, wrap=False):
        """
        Select and display the *previous* image used by this sprite.
        If the current image is already the *first* image, then
        the image is not changed.

        :param boolean wrap: If `True`, then calling
            :meth:`prevImage` on the first image will cause the *last*
            image to be loaded.

        This only does something useful if the asset is an
        :class:`~ggame.asset.ImageAsset` defined with multiple images.
        """
        self._index -= 1
        if self._index < 0:
            if wrap:
                self._index = len(self.asset) - 1
            else:
                self._index = 0
        self.gfx.texture = self.asset[self._index]

    def setImage(self, index=0):
        """
        Select the image to display by giving its `index`.

        :param int index: An index to specify the image to display.
            A value of zero represents the *first* image in the asset.

        This is equivalent to setting the :data:`index` property
        directly.

        This only does something useful if the asset is an
        :class:`~ggame.asset.ImageAsset` defined with multiple images.
        """
        self.index = index

    def rectangularCollisionModel(self):
        """
        Obsolete. No op.
        """

    def circularCollisionModel(self):
        """
        Obsolete. No op.
        """

    @property
    def index(self):
        """
        This is an integer index into the list of images available for this sprite.
        """
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        try:
            self.gfx.texture = self.asset[self._index]
        except:  # pylint: disable=bare-except
            self._index = 0
            self.gfx.texture = self.asset[self._index]

    @property
    def width(self):
        """
        This is an integer representing the display width of the sprite.
        Assigning a value to the width will scale the image horizontally.
        """
        return self.gfx.width

    @width.setter
    def width(self, value):
        self.gfx.width = value
        self._extentsdirty = True

    @property
    def height(self):
        """
        This is an integer representing the display height of the sprite.
        Assigning a value to the height will scale the image vertically.
        """
        return self.gfx.height

    @height.setter
    def height(self, value):
        self.gfx.height = value
        self._extentsdirty = True

    @property
    def x(self):
        """
        This represents the x-coordinate of the sprite on the screen. Assigning
        a value to this attribute will move the sprite horizontally.
        """
        return self.gfx.position.x

    @x.setter
    def x(self, value):
        delta_x = value - self.gfx.position.x
        self.xmax += delta_x
        self.xmin += delta_x
        # Adjust extents directly with low overhead
        self.gfx.position.x = value

    @property
    def y(self):
        """
        This represents the y-coordinate of the sprite on the screen. Assigning
        a value to this attribute will move the sprite vertically.
        """
        return self.gfx.position.y

    @y.setter
    def y(self, value):
        delta_y = value - self.gfx.position.y
        self.ymax += delta_y
        self.ymin += delta_y
        # Adjust extents directly with low overhead
        self.gfx.position.y = value

    @property
    def position(self):
        """
        This represents the (x,y) coordinates of the sprite on the screen. Assigning
        a value to this attribute will move the sprite to the new coordinates.
        """
        return (self.gfx.position.x, self.gfx.position.y)

    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def fxcenter(self):
        """
        This represents the horizontal position of the sprite "center", as a floating
        point number between 0.0 and 1.0. A value of 0.0 means that the x-coordinate
        of the sprite refers to its left hand edge. A value of 1.0 refers to its
        right hand edge. Any value in between may be specified. Values may be assigned
        to this attribute.
        """
        try:
            return self.gfx.anchor.x
        except:  # pylint: disable=bare-except
            return 0.0

    @fxcenter.setter
    def fxcenter(self, value):
        try:
            self.gfx.anchor.x = value
            self._extentsdirty = True
        except:  # pylint: disable=bare-except
            pass

    @property
    def fycenter(self):
        """
        This represents the vertical position of the sprite "center", as a floating
        point number between 0.0 and 1.0. A value of 0.0 means that the x-coordinate
        of the sprite refers to its top edge. A value of 1.0 refers to its
        bottom edge. Any value in between may be specified. Values may be assigned
        to this attribute.
        """
        try:
            return self.gfx.anchor.y
        except:  # pylint: disable=bare-except
            return 0.0

    @fycenter.setter
    def fycenter(self, value):
        try:
            self.gfx.anchor.y = value
            self._extentsdirty = True
        except:  # pylint: disable=bare-except
            pass

    @property
    def center(self):
        """
        This attribute represents the horizontal and vertical position of the
        sprite "center" as a tuple of floating point numbers. See the
        descriptions for :data:`fxcenter` and :data:`fycenter` for
        more details.
        """
        try:
            return (self.gfx.anchor.x, self.gfx.anchor.y)
        except:  # pylint: disable=bare-except
            return (0.0, 0.0)

    @center.setter
    def center(self, value):
        try:
            self.gfx.anchor.x = value[0]
            self.gfx.anchor.y = value[1]
            self._extentsdirty = True
        except:  # pylint: disable=bare-except
            pass

    @property
    def visible(self):
        """
        This boolean attribute may be used to change the visibility of the sprite.
        Setting `~ggame.Sprite.visible` to `False` will prevent the sprite from
        rendering on the screen.
        """
        return self.gfx.visible

    @visible.setter
    def visible(self, value):
        self.gfx.visible = value

    @property
    def scale(self):
        """
        This attribute may be used to change the size of the sprite ('scale' it) on the
        screen. Value may be a floating point number. A value of 1.0 means that the
        sprite image will keep its original size. A value of 2.0 would double it, etc.
        """
        try:
            return self.gfx.scale.x
        except AttributeError:
            return 1.0

    @scale.setter
    def scale(self, value):
        self.gfx.scale.x = value
        self.gfx.scale.y = value
        self._extentsdirty = True

    @property
    def rotation(self):
        """
        This attribute may be used to change the rotation of the sprite on the screen.
        Value may be a floating point number. A value of 0.0 means no rotation. A value
        of 1.0 means  a rotation of 1 radian in a counter-clockwise direction. One
        radian is 180/pi or approximately 57.3 degrees.
        """
        try:
            return -self.gfx.rotation
        except AttributeError:
            return 0.0

    @rotation.setter
    def rotation(self, value):
        if self.gfx.rotation != -value:
            self.gfx.rotation = -value
            self._extentsdirty = True

    @classmethod
    def collidingCircleWithPoly(cls, circ, poly):  # pylint: disable=unused-argument
        """
        Determine if a CircleAsset sprite overlaps with a PolygonAsset sprite. This
        method is called after determining that the two objects are overlapping in their
        overall extents.

        :param Sprite circ: A CircleAsset-based sprite.
        :param Sprite poly: A PolygonAsset-based sprite.
        :returns: True if the sprites are overlapping, False otherwise.
        :rtype: boolean
        """
        return True  # no implementation yet

    def collidingPolyWithPoly(
        self, obj
    ):  # pylint: disable=unused-argument, no-self-use
        """
        Determine if a pair of PolygonAsset-based sprites are overlapping. This
        method is called after determining that the two objects are overlapping in their
        overall extents. This should onlyb e called if `self` is a PolygonAsset-based
        sprite.

        :param Sprite obj: A PolygonAsset-based sprite.
        :returns: True if slef overlaps with obj, False otherwise.
        :rtype: boolean
        """
        return True  # no implementation yet

    def collidingWith(self, obj):
        """
        Determine if this sprite is currently overlapping another
        sprite object.

        :param Sprite obj: A reference to another Sprite object.

        :rtype: boolean

        :returns: `True` if this the sprites are overlapping, `False` otherwise.
        """
        if self is obj:
            return False
        self.setExtents()
        obj.setExtents()
        # Gross check for overlap will usually rule out a collision
        if (
            self.xmin > obj.xmax
            or self.xmax < obj.xmin
            or self.ymin > obj.ymax
            or self.ymax < obj.ymin
        ):
            return False
        # Otherwise, perform a careful overlap determination
        if isinstance(self.asset, CircleAsset):
            if isinstance(obj.asset, CircleAsset):
                # two circles .. check distance between
                sx = (self.xmin + self.xmax) / 2
                sy = (self.ymin + self.ymax) / 2
                ox = (obj.xmin + obj.xmax) / 2
                oy = (obj.ymin + obj.ymax) / 2
                d = math.sqrt((sx - ox) ** 2 + (sy - oy) ** 2)
                return d <= self.width / 2 + obj.width / 2
            return self.collidingCircleWithPoly(self, obj)
        if isinstance(obj.asset, CircleAsset):
            return self.collidingCircleWithPoly(obj, self)
        return self.collidingPolyWithPoly(obj)

    def collidingWithSprites(self, sclass=None):
        """
        Determine if this sprite is colliding with any other sprites
        of a certain class.

        :param class sclass: A class identifier that is either :class:`Sprite`
            or a subclass of it that identifies the class of sprites to check
            for collisions. If `None` then all objects that are subclassed from
            the :class:`Sprite` class are checked.

        :rtype: list

        :returns: A (potentially empty) list of sprite objects of the given
            class that are overlapping with this sprite.
        """
        if sclass is None:
            slist = App.spritelist
        else:
            slist = App.getSpritesbyClass(sclass)
        return list(filter(self.collidingWith, slist))

    @staticmethod
    def getImagePath(imagename):
        """
        Determine a path to the ggame-provided image that will work for both online
        (runpython.org) and locally installed ggame libraries. Do not use this with
        user-provided images.

        :param str imagename: The name of an image file found inside the
            ggame/images folder.
        """
        # differences in online vs. local operation
        try:
            thispath = os.path.dirname(__file__)
            imagepath = os.path.join(thispath, "images")
        except NameError:
            imagepath = "images"
        return os.path.join(imagepath, imagename)

    def destroy(self):
        """
        Prevent the sprite from being displayed or checked in collision
        detection. Once this is called, the sprite can no longer be displayed
        or used. If you only want to prevent a sprite from being displayed,
        set the :data:`visible` attribute to `False`.
        """
        try:
            App.remove(self)
            self.gfx.destroy()
        except ValueError:
            pass
