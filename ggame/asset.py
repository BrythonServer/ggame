# asset.py

"""
ggame assets and related objects (:class:`Color` and :class:`LineStyle`) are
classes that encapsulate and represent displayable images. A single asset 
may be used in multiple sprites. Animated assets may be created from any 
image that includes multiple images within it (i.e. a sprite sheet).
"""

try:
    from ggame.sysdeps import *
except:
    from sysdeps import *

class Frame(object):
    """
    Frame is a utility class for expressing the idea of a rectangular region.
    
    Initializing parameters describe the position of the upper-left corner
    of the frame, and the frame's width and height. The units are *typically*
    in pixels, though a frame can be generic.
    
    :param int x: X-coordinate of frame upper-left corner
    :param int y: Y-coordinate of frame upper-left corner
    :param int w: Width of the frame
    :param int h: Height of the frame
    """
    
    def __init__(self, x, y, w, h):

        self.GFX = GFX_Rectangle(x,y,w,h)
        """
        `GFX` is a reference to the underlying object provided by the system.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    @property
    def x(self):
        """
        X-coordinate of the upper left hand corner of this frame.
        """
        return self.GFX.x
    
    @x.setter
    def x(self, value):
        self.GFX.x = value
        
    @property
    def y(self):
        """
        Y-coordinate of the upper left hand corner of this frame.
        """
        return self.GFX.y
    
    @y.setter
    def y(self, value):
        self.GFX.y = value
    
    @property
    def w(self):
        """
        Width of the frame.
        """
        return self.GFX.width
    
    @w.setter
    def w(self, value):
        self.GFX.width = value
        
    @property
    def h(self):
        """
        Height of the frame.
        """
        return self.GFX.height
        
    @h.setter
    def h(self, value):
        self.GFX.height = value
    
    @property
    def center(self):
        """
        The `center` property computes a coordinate pair (tuple) for the 
        center of the frame.

        The `center` property, when set, redefines the `x` and `y` properties
        of the frame in order to make the center agree with the coordinates
        (tuple) assigned to it.
        """

        return (self.x + self.w//2, self.y + self.h//2)
    
    @center.setter
    def center(self, value):
        c = self.center
        self.x += value[0] - c[0]
        self.y += value[1] - c[1]

class _Asset(object):
    """
    Base class for all game asset objects.
    
    The `ggame.Asset` class is set up to understand the concept
    of multiple instances of an asset. This is currently only used for image-based
    assets.
    """

    def __init__(self):
        self.GFXlist = [None,]
        """A list of the underlying system objects used to represent this asset."""

    @property
    def GFX(self):
        """
        `GFX` property represents the underlying system object used to represent
        this asset. If this asset is composed of multiple assets, then the **first**
        asset is referenced by `GFX`.
        """
        return self.GFXlist[0]
        
    @GFX.setter
    def GFX(self, value):
        self.GFXlist[0] = value
        
    def __len__(self):
        return len(self.GFXlist)
        
    def __getitem__(self, key):
        return self.GFXlist[key]
        
    def __setitem__(self, key, value):
        self.GFXlist[key] = value
        
    def __iter__(self):
        class Iter():
            def __init__(self, image):
                self.obj = image
                self.n = len(image.GFXlist)
                self.i = 0
                
            def __iter__(self):
                return self
                
            def __next__(self):
                if self.i ==self.n:
                    raise StopIteration
                self.i += 1
                return self.obj.GFXlist[self.i]
        return Iter(self)

    def destroy(self):
        """
        Destroy or deallocate any underlying graphics resources used by the
        asset. Call this method on any asset that is no longer being used.
        """
        if hasattr(self, 'GFX'):
            try:
                for gfx in self.GFXlist:
                    try:
                        gfx.destroy(True)
                    except:
                        pass
            except:
                pass
        
        
class ImageAsset(_Asset):
    """
    The ImageAsset class connects ggame to a specific image **file**.

    :param str url: All ImageAsset instances must specify a file name or 
        url where a jpg or png image is located.

    :param Frame frame: If the desired sprite image exists in only a smaller 
        sub-section of the original image, then specify an area `within` the
        image using `frame` parameter, which must be a valid :class:`Frame` 
        instance.

    :param int qty=0: If the image file actually is a *collection* of images, such 
        as a so-called *sprite sheet*, then the ImageAsset class supports 
        defining a list of images, provided they exist in the original image 
        as a **row** of evenly spaced images or a **column** of images. To 
        specify this, provide the `qty` (quantity) of images in the row or 
        column.
    
    :param str direction='horizontal': For an image *sprite sheet*, specify whether the images
        are oriented in a `'vertical'` or `'horizontal'` arrangement.
        
    :param int margin=0: If there is a gap between successive images in an image
        *sprite sheet*, then specify the size of the gap (in pixels). When 
        used in this way, the `frame` parameter must define the
        area of only the **first** image in the collection; all subsequent 
        images in the list are assumed to be the same size, but separated by the
        `margin` value.
    """

    def __init__(self, url, frame=None, qty=1, direction='horizontal', margin=0):
        super().__init__()
        self.url = url
        """
        A string that represents the path or url of the original file.
        """
        del self.GFXlist[0]
        self.width = self.height = 0
        self.append(url, frame, qty, direction, margin)

    def _subframe(self, texture, frame):
        return GFX_Texture(texture, frame.GFX)
        
    def append(self, url, frame=None, qty=1, direction='horizontal', margin=0):
        """
        Append a texture asset from a new image file (or url). This method
        allows you to build a collection of images into an asset (such as you
        might need for an animated sprite), but without using a single 
        sprite sheet image.

        The parameters for the `append` method are identical to those 
        supplied to the :class:`ImageAsset` initialization method. 

        This method allows you to build up an asset that consists of 
        multiple rows or columns of images in a sprite sheet or sheets.
        """
        GFX = GFX_Texture_fromImage(url, False)
        dx = 0
        dy = 0
        for i in range(qty):
            if not frame is None:
                self.width = frame.w
                self.height = frame.h
                if direction == 'horizontal':
                    dx = frame.w + margin
                elif direction == 'vertical':
                    dy = frame.h + margin
                f = Frame(frame.x + dx * i, frame.y + dy * i, frame.w, frame.h)
                GFX = self._subframe(GFX, f)
            else:
                self.width = GFX.width
                self.height = GFX.height
            self.GFXlist.append(GFX)


class Color(object):
    """
    The Color class is used to represent colors and/or colors with
    transparency.

    :param int color: an integer in the conventional format (usually 
        as a hexadecimal literal, e.g. 0xffbb33 that represents 
        the three color components, red, green and blue)
        
    :param float alpha: a transparency value, or `alpha` as a floating-point 
        number in the range of 0.0 to 1.0 where 0.0 represents 
        completely transparent and 1.0 represents completely opaque.
    
    Example::

        red = Color(0xff0000, 1.0)

    """
    _colornames = {
        0xffffff: 'white',
        0x000000: 'black'
    }
    
    def __init__(self, color, alpha):
        self.color = color
        self.alpha = alpha
        self.name = "Color(0x{0:06X}, {1})".format(int(self.color), self.alpha)
        if alpha == 1.0:
            self.name = self._colornames.get(self.color, self.name)
        
    def __eq__(self, other):
        return type(self) is type(other) and self.color == other.color and self.alpha == other.alpha
        
    def __repr__(self):
        return self.name

black = Color(0x000000, 1.0)
"""
Default black color
"""
white = Color(0xffffff, 1.0)
"""
Default white color
"""

class LineStyle(object):
    """
    The LineStyle class is used to represent line style when
    drawing geometrical objects such as rectangles, ellipses, etc.

    :param int width: the `width` of the line in pixels
    
    :param Color color: the `color` as a valid :class:`Color` instance. 
    
    Example::

        line = LineStyle(3, Color(0x00ff00, 1.0))
        
    This defines a 3-pixel wide green line.
    """
    
    def __init__(self, width, color):
        """
        """
        self.width = width
        self.color = color

    def __eq__(self, other):
        return type(self) is type(other) and self.width == other.width and self.color == other.color

    def __repr__(self):
        return "LineStyle({}, {})".format(self.width, self.color)
        


blackline = LineStyle(1, black)
"""
Default thin black line
"""
whiteline = LineStyle(1, white)
"""
Default thin white line
"""

class _GraphicsAsset(_Asset):
    
    def __init__(self):
        super().__init__()
        GFX_Graphics.clear()
        

class _CurveAsset(_GraphicsAsset):

    def __init__(self, line):
        super().__init__()
        GFX_Graphics.lineStyle(line.width, line.color.color, line.color.alpha)

class _ShapeAsset(_CurveAsset):

    def __init__(self, line, fill):
        super().__init__(line)
        GFX_Graphics.beginFill(fill.color, fill.alpha)
    

class RectangleAsset(_ShapeAsset):
    """
    The RectangleAsset is a "virtual" asset that is created on the
    fly without requiring creation of an image file.

    :param int width: Rectangle width, in pixels
    :param int height: Rectangle height, in pixels
    :param LineStyle line=blackline: The color and width of the rectangle border
    :param Color fill=black: The color of the rectangle body
    """

    def __init__(self, width, height, line=blackline, fill=black):
        super().__init__(line, fill)
        self.width = width
        self.height = height
        self.GFX = GFX_Graphics.drawRect(0, 0, self.width, self.height).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        

class CircleAsset(_ShapeAsset):
    """
    The `ggame.CircleAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file.

    :param int radius: Circle radius, in pixels
    :param LineStyle line=blackline: The color and width of the circle border
    :param Color fill=black: The color of the circle body
    """    

    def __init__(self, radius, line=blackline, fill=black):
        super().__init__(line, fill)
        self.radius = radius
        self.GFX = GFX_Graphics.drawCircle(0, 0, self.radius).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        
class EllipseAsset(_ShapeAsset):
    """
    The `ggame.EllipseAsset` is a "virtual" asset that is created on the 
    fly without requiring creation of an image file.

    :param int halfw: Ellipse semi-axis dimension in the horizontal direction
        (half the width of the ellipse), in pixels
    :param int halfh: Ellipse semi-axis dimension in the vertical direction
        (half the height of the ellipse), in pixels
    :param LineStyle line=blackline: The color and width of the ellipse border
    :param Color fill=black: The color of the ellipse body

    """

    def __init__(self, halfw, halfh, line=blackline, fill=black):
        super().__init__(line, fill)
        self.halfw = halfw
        self.halfh = halfh
        self.GFX = GFX_Graphics.drawEllipse(0, 0, self.halfw, self.halfh).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        
class PolygonAsset(_ShapeAsset):
    """
    The PolygonAsset is a "virtual" asset that is created on the
    fly without requiring creation of an image file.
    
    Note: you should not specificy absolute screen coordinates for this
    asset, since you will use the :class:`Sprite` position to locate your 
    polygon on the screen.

    :param list path: A list of pixel-coordinate tuples. These coordinates should 
        not be in absolute screen coordinates, but should be relative to the
        desired 'center' of the resulting :class:`Sprite`. The final 
        coordinate pair in the list must be the same as the first.
    :param LineStyle line=blackline: The color and width of the ellipse border
    :param Color fill=black: The color of the ellipse body
        
    Example::
    
        poly = PolygonAsset([(0,0), (50,50), (50,100), (0,0)], 
            LineStyle(4, black), 
            Color(0x80FF00, 0.8)))

    """

    def __init__(self, path, line=blackline, fill=black):
        super().__init__(line, fill)
        self.path = path
        jpath = []
        for point in self.path:
            jpath.extend(point)
        self.GFX = GFX_Graphics.drawPolygon(jpath).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
    

class LineAsset(_CurveAsset):
    """
    The LineAsset is a "virtual" asset that is created on the
    fly without requiring creation of an image file. A LineAsset instance
    represents a single line segment.

    Note: you should not specificy absolute screen coordinates for this
    asset, since you will use the :class:`Sprite` position to locate your 
    line on the screen. The line segment will begin at pixel coordinates (0,0),
    and will end at the (x,y) coordinates given below.

    As the LineAsset does not cover a region, only a :class:`LineStyle` 
    argument must be supplied (`line`) to specify the color.

    :param int x: x-coordinate of the line endpoint, in pixel units
    :param int y: y-coordinate of the line endpoint, in pixel units
    :param LineStyle line=blackline: The color and width of the ellipse border
    """

    def __init__(self, x, y, line=blackline):
        super().__init__(line)
        self.deltaX = x
        """This attribute represents the `x` parameter supplied during instantiation."""
        self.deltaY = y
        """This attribute represents the `y` parameter supplied during instantiation."""
        GFX_Graphics.moveTo(0, 0)
        self.GFX = GFX_Graphics.lineTo(self.deltaX, self.deltaY).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False

class TextAsset(_GraphicsAsset):
    """
    The TextAsset is a "virtual" asset that is created on the fly
    without requiring creation of an image file. A TextAsset instance
    represents a block of text, together with its styling (font, color, etc.).

    :param str text: The text that should be displayed

    :param \**kwargs: Optional formatting and style attributes (below)
    
    :param str style='20px Arial': Text style, size and typeface. Example:: 
    
            'italic 20pt Helvetica'
        
    :keyword int width=100: Width of the text block on screen, in pixels. 
    :param Color fill=black: :class:`Color` instance to specify color
        and transparency of the text. 
    :param str align='left': Alignment style of the block. One of 'left',
        'center', or 'right'. 

    Full example::
    
        ta = TextAsset("Sample Text", 
            style="bold 40pt Arial", 
            width=250, 
            fill=Color(0x1122ff, 1.0))

    """
 
    def __init__(self, text, **kwargs):
        """
        """
        super().__init__()
        self.text = text
        self.style = kwargs.get('style', '20px Arial')
        width = kwargs.get('width', 100)
        self.fill = kwargs.get('fill', Color(0, 1))
        self.align = kwargs.get('align', 'left')
        self.GFX = GFX_Text(self.text, 
            {'font': self.style,
                'fill' : self.fill.color,
                'align' : self.align,
                'wordWrap' : True,
                'wordWrapWidth' : width,
                })
        self.GFX.alpha = self.fill.alpha
        self.GFX.visible = False
        
    def _clone(self):
        return type(self)(self.text,
            style = self.style,
            width = self.width,
            fill = self.fill,
            align = self.align)
    
    @property
    def width(self):
        return self.GFX.width
        
    @property
    def height(self):
        return self.GFX.height

