try:
    from ggame.sysdeps import *
except:
    from sysdeps import *
import math
from ggame.asset import *
from ggame.app import *


class Sprite(object):
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
    
    Example::
    
        from ggame.sprite import Sprite
        from ggame.asset import ImageAsset, CircleAsset
        from ggame.app import App
        
        player = Sprite(
            ImageAsset("player.png", 
            (100,100), 
            CircleAsset(50))

        App().run()

    This creates a sprite using the 'player.png' image, positioned with its
    upper-left corner at coordinates (100,100) and with a 50 pixel radius 
    circular collision border. 

    """
 
    _rectCollision = "rect"
    _circCollision = "circ"
    
    def __init__(self, asset, pos=(0,0), edgedef=None):
        """
        """
        self._index = 0
        if type(asset) == ImageAsset:
            self.asset = asset
            try:
                #self.GFX = GFX_Sprite()
                self.GFX = GFX_Sprite(asset.GFX) # GFX is PIXI Sprite
            except:
                self.GFX = None
        elif type(asset) in [RectangleAsset, 
            CircleAsset, 
            EllipseAsset, 
            PolygonAsset,
            LineAsset,
            ]:
            self.asset = asset
            self.GFX = GFX_Sprite(asset.GFX.generateTexture())
            #self.GFX = asset.GFX.clone() # GFX is PIXI Graphics (from Sprite)
            #self.GFX.visible = True
        elif type(asset) in [TextAsset]:
            self.asset = asset._clone()
            self.GFX = self.asset.GFX # GFX is PIXI Text (from Sprite)
            self.GFX.visible = True
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
        self._setExtents()
        """Initialize the extents (xmax, xmin, etc.) for collision detection"""
        App._add(self)
        
    def _createBaseVertices(self):
        """
        Create sprite-relative list of vertex coordinates for boundary
        """
        self._basevertices = []
        assettype = type(self.edgedef)
        if assettype in [RectangleAsset, ImageAsset, TextAsset]:
            self._basevertices = [(0,0), 
                (0,self.edgedef.height), 
                (self.edgedef.width,self.edgedef.height),
                (self.edgedef.width,0)]
        elif assettype is PolygonAsset:
            self._basevertices = self.edgedef.path[:-1]
        elif assettype is LineAsset:
            self._basevertices = [(0,0), 
                (self.edgedef.deltaX, self.edgedef.deltaY)]
        elif assettype is EllipseAsset:
            w = self.edgedef.halfw * 2
            h = self.edgedef.halfh * 2
            self._basevertices = [(0,0), (0,h), (w,h), (w,0)]

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
            crsc = [((xp-x)*sc,(yp-y)*sc) for xp,yp in self._basevertices]
        else:
            crsc = [(xp-x,yp-y) for xp,yp in self._basevertices]
            
        # absolute, rotated coordinates
        c = math.cos(self.rotation)
        s = math.sin(self.rotation)
        self._absolutevertices = [(self.x + x*c + y*s, self.y + -x*s + y*c) 
                                    for x,y in crsc]


    def _setExtents(self):
        """
        update min/max x and y based on position, center, width, height
        """
        if self._extentsdirty:
            if type(self.asset) is CircleAsset:
                th = math.atan2(
                    self.fycenter - 0.5, 0.5 - self.fxcenter) + self.rotation
                D = self.width
                L = math.sqrt(math.pow(self.fxcenter - 0.5, 2) + 
                    math.pow(self.fycenter - 0.5, 2)) * D
                self.xmin = self.x + int(L*math.cos(th)) - D//2
                self.ymin = self.y - int(L*math.sin(th)) - D//2
                self.xmax = self.xmin + D
                self.ymax = self.ymin + D
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
        self.GFX.texture = self.asset[0]
    
    def lastImage(self):
        """
        Select and display the *last* image used by this sprite. This only 
        does something useful if the asset is an :class:`~ggame.asset.ImageAsset`
        defined with multiple images.
        """
        self.GFX.texture = self.asset[-1]
    
    def nextImage(self, wrap = False):
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
                self._index = len(self.asset)-1
        self.GFX.texture = self.asset[self._index]
    
    def prevImage(self, wrap = False):
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
                self._index = len(self.asset)-1
            else:
                self._index = 0
        self.GFX.texture = self.asset[self._index]
    
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
        pass
    
    def circularCollisionModel(self):
        """
        Obsolete. No op.
        """
        pass
    
    

    @property
    def index(self):
        """This is an integer index into the list of images available for this sprite."""
        return self._index
        
    @index.setter
    def index(self, value):
        self._index = value
        try:
            self.GFX.texture = self.asset[self._index]
        except:
            self._index = 0
            self.GFX.texture = self.asset[self._index]

    @property
    def width(self):
        """
        This is an integer representing the display width of the sprite.
        Assigning a value to the width will scale the image horizontally.
        """
        return self.GFX.width
        
    @width.setter
    def width(self, value):
        self.GFX.width = value
        self._extentsdirty = True
    
    @property
    def height(self):
        """
        This is an integer representing the display height of the sprite.
        Assigning a value to the height will scale the image vertically.
        """
        return self.GFX.height
    
    @height.setter
    def height(self, value):
        self.GFX.height = value
        self._extentsdirty = True
        
    @property
    def x(self):
        """
        This represents the x-coordinate of the sprite on the screen. Assigning
        a value to this attribute will move the sprite horizontally.
        """
        return self.GFX.position.x
        
    @x.setter
    def x(self, value):
        deltax = value - self.GFX.position.x
        self.xmax += deltax
        self.xmin += deltax
        """Adjust extents directly with low overhead"""
        self.GFX.position.x = value

    @property
    def y(self):
        """
        This represents the y-coordinate of the sprite on the screen. Assigning
        a value to this attribute will move the sprite vertically.
        """
        return self.GFX.position.y
        
    @y.setter
    def y(self, value):
        deltay = value - self.GFX.position.y
        self.ymax += deltay
        self.ymin += deltay
        """Adjust extents directly with low overhead"""
        self.GFX.position.y = value

    @property
    def position(self):
        """
        This represents the (x,y) coordinates of the sprite on the screen. Assigning
        a value to this attribute will move the sprite to the new coordinates.
        """
        return (self.GFX.position.x, self.GFX.position.y)
        
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
            return self.GFX.anchor.x
        except:
            return 0.0
        
    @fxcenter.setter
    def fxcenter(self, value):
        try:
            self.GFX.anchor.x = value
            self._extentsdirty = True
        except:
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
            return self.GFX.anchor.y
        except:
            return 0.0
        
    @fycenter.setter
    def fycenter(self, value):
        try:
            self.GFX.anchor.y = value
            self._extentsdirty = True
        except:
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
            return (self.GFX.anchor.x, self.GFX.anchor.y)
        except:
            return (0.0, 0.0)
        
    @center.setter
    def center(self, value):
        try:
            self.GFX.anchor.x = value[0]
            self.GFX.anchor.y = value[1]
            self._extentsdirty = True
        except:
            pass
    
    @property
    def visible(self):
        """
        This boolean attribute may be used to change the visibility of the sprite. Setting
        `~ggame.Sprite.visible` to `False` will prevent the sprite from rendering on the 
        screen.
        """
        return self.GFX.visible
    
    @visible.setter
    def visible(self, value):
        self.GFX.visible = value

    @property
    def scale(self):
        """
        This attribute may be used to change the size of the sprite ('scale' it) on the 
        screen. Value may be a floating point number. A value of 1.0 means that the sprite
        image will keep its original size. A value of 2.0 would double it, etc.
        """
        try:
            return self.GFX.scale.x
        except AttributeError:
            return 1.0
        
    @scale.setter
    def scale(self, value):
        self.GFX.scale.x = value
        self.GFX.scale.y = value
        self._extentsdirty = True

    @property
    def rotation(self):
        """
        This attribute may be used to change the rotation of the sprite on the screen.
        Value may be a floating point number. A value of 0.0 means no rotation. A value 
        of 1.0 means  a rotation of 1 radian in a counter-clockwise direction. One radian
        is 180/pi or approximately 57.3 degrees.
        """
        try:
            return -self.GFX.rotation
        except AttributeError:
            return 0.0
        
    @rotation.setter
    def rotation(self, value):
        self.GFX.rotation = -value
        if value:
            self._extentsdirty = True

    @classmethod
    def collidingCircleWithPoly(cls, circ, poly):
        return True
    
    def collidingPolyWithPoly(self, obj):
        return True

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
        else:
            self._setExtents()
            obj._setExtents()
            # Gross check for overlap will usually rule out a collision
            if (self.xmin > obj.xmax
                or self.xmax < obj.xmin
                or self.ymin > obj.ymax
                or self.ymax < obj.ymin):
                return False
            # Otherwise, perform a careful overlap determination
            elif type(self.asset) is CircleAsset:
                if type(obj.asset) is CircleAsset:
                    # two circles .. check distance between
                    sx = (self.xmin + self.xmax) / 2
                    sy = (self.ymin + self.ymax) / 2
                    ox = (obj.xmin + obj.xmax) / 2
                    oy = (obj.ymin + obj.ymax) / 2
                    d = math.sqrt((sx-ox)**2 + (sy-oy)**2)
                    return d <= self.width/2 + obj.width/2
                else:
                    return self.collidingCircleWithPoly(self, obj)
            else:
                if type(obj.asset) is CircleAsset:
                    return self.collidingCircleWithPoly(obj, self)
                else:
                    return self.collidingPolyWithPoly(obj)
                
                

    def collidingWithSprites(self, sclass = None):
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

    def destroy(self):
        """
        Prevent the sprite from being displayed or checked in collision 
        detection. Once this is called, the sprite can no longer be displayed
        or used. If you only want to prevent a sprite from being displayed, 
        set the :data:`visible` attribute to `False`.
        """
        App._remove(self)
        self.GFX.destroy()
