try:
    from ggame.sysdeps import *
except:
    from sysdeps import *

class Frame(object):
    """
    Frame is a utility class for expressing the idea of a rectangular region.
    """
    
    def __init__(self, x, y, w, h):
        """
        Initialization for the `ggame.Frame` objects.

        `x` and `y` are coordinates of the upper left hand corner of the frame.
 
        `w` and `h` are the width and height of the frame rectangle.
        """

        self.GFX = GFX_Rectangle(x,y,w,h)
        """
        `GFX` is a reference to the underlying object provided by the system.
        """
        self.x = x
        """
        X-coordinate of the upper left hand corner of this `ggame.Frame`.
        """
        self.y = y
        """
        Y-coordinate of the upper left hand corner of this `ggame.Frame`.
        """
        self.w = w
        """
        Width of the `ggame.Frame`.
        """
        self.h = h
        """
        Height of the `ggame.Frame`.
        """
    
    @property
    def x(self):
        return self.GFX.x
    
    @x.setter
    def x(self, value):
        self.GFX.x = value
        
    @property
    def y(self):
        return self.GFX.y
    
    @y.setter
    def y(self, value):
        self.GFX.y = value
    
    @property
    def w(self):
        return self.GFX.width
    
    @w.setter
    def w(self, value):
        self.GFX.width = value
        
    @property
    def h(self):
        return self.GFX.height
        
    @h.setter
    def h(self, value):
        self.GFX.height = value
    
    @property
    def center(self):
        """
        `center` property computes a coordinate pair (tuple) for the 
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
    The `ImageAsset` class connects ggame to a specific image **file**.
    """

    def __init__(self, url, frame=None, qty=1, direction='horizontal', margin=0):
        """
        All `ggame.ImageAsset` instances must specify a file name or url with
        the `url` parameter.

        If the desired sprite image exists in only a smaller sub-section of the 
        original image, then the are can be specified by providing the
        `frame` parameter, which must be a valid `ggame.Frame` object.

        If image file actually is a *collection* of images, such as a so-called
        *sprite sheet*, then the `ImageAsset` class supports defining a list
        of images, provided they exist in the original image as a **row**
        of evenly spaced images or a **column** of images. To specify this,
        provide the `qty` (quantity) of images in the row or column, the
        `direction` of the list ('horizontal' or 'vertical' are supported),
        and an optional `margin`, if there is a gap between successive 
        images. When used in this way, the `frame` parameter must define the
        area of the **first** image in the collection; all subsequent images
        in the list are assumed to be the same size.
        """
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
        supplied to the `ggame.ImageAsset` initialization method. 

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
    The `ggame.Color` class is used to represent colors and/or colors with
    transparency.
    """

    def __init__(self, color, alpha):
        """
        A `ggame.Color` instance must specify both a `color` as an integer
        in the conventional format (usually as a hexadecimal literal, e.g.
        0xffbb33 that represents the three color components, red, green 
        and blue), and a transparency value, or `alpha` as a floating
        point number in the range of 0.0 to 1.0 where 0.0 represents 
        completely transparent and 1.0 represents completely solid.

        Example: `red = Color(0xff0000, 1.0)`

        """
        self.color = color
        self.alpha = alpha
        
    def __eq__(self, other):
        return type(self) is type(other) and self.color == other.color and self.alpha == other.alpha
        
black = Color(0, 1.0)
"""
Default black color
"""
white = Color(0xffffff, 1.0)
"""
Default white color
"""

class LineStyle(object):
    """
    The `ggame.LineStyle` class is used to represent line style when
    drawing geometrical objects such as rectangles, ellipses, etc.
    """
    
    def __init__(self, width, color):
        """
        When creating a `ggame.LineStyle` instances you must specify 
        the `width` of the line in pixels and the `color` as a valid
        `ggame.Color` instance.

        Example: `line = LineStyle(3, Color(0x00ff00, 1.0))` will define
        a 3 pixel wide green line.
        """
        self.width = width
        self.color = color

    def __eq__(self, other):
        return type(self) is type(other) and self.width == other.width and self.color == other.color

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
    The `ggame.RectangleAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file.
    """

    def __init__(self, width, height, line=blackline, fill=black):
        """
        Creation of a `ggame.RectangleAsset` requires specification of the 
        rectangle `width` and `height` in pixels, the `line` (as a proper
        `ggame.LineStyle` instance) and fill properties (as a `ggame.Color`
        instance).
        """
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
    """    

    def __init__(self, radius, line=blackline, fill=black):
        """
        Creation of a `ggame.CircleAsset` requires specification of the circle
        `radius` in pixels, the `line` (as a proper `ggame.LineStyle` instance)
        and fill properties (as a `ggame.Color` instance).
        """
        super().__init__(line, fill)
        self.radius = radius
        self.GFX = GFX_Graphics.drawCircle(0, 0, self.radius).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        
class EllipseAsset(_ShapeAsset):
    """
    The `ggame.EllipseAsset` is a "virtual" asset that is created on the 
    fly without requiring creation of an image file.
    """

    def __init__(self, halfw, halfh, line=blackline, fill=black):
        """
        Creation of a `ggame.EllipseAsset` requires specification of the ellipse
        `halfw`, or semi-axis length in the horizontal direction (half of the
        ellipse width) and the `halfh`, or semi-axis length in the vertical direction.
        `line` (as `ggame.LineStyle` instance) and `fill` (as `ggame.Color` instance)
        must also be provided.
        """
        super().__init__(line, fill)
        self.halfw = halfw
        self.halfh = halfh
        self.GFX = GFX_Graphics.drawEllipse(0, 0, self.halfw, self.halfh).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        
class PolygonAsset(_ShapeAsset):
    """
    The `ggame.PolygonAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file.
    """

    def __init__(self, path, line=blackline, fill=black):
        """
        Creation of a `ggame.PolygonAsset` requires specification of a 
        `path` consisting of a list of coordinate tuples. `line` and 
        `fill` arguments (instances of `ggame.LineStyle` and `ggame.Color`,
        respectively) must also be supplied. The final coordinate in the 
        list must be the same as the first.

        Example: `poly = PolygonAsset([(0,0), (50,50), (50,100), (0,0)], linesty, fcolor)`
        """
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
    The `ggame.LineAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file. A `LineAsset` instance
    represents a single line segment.
    """

    def __init__(self, x, y, line=blackline):
        """
        Creation of a `ggame.LineAsset` requires specification of an `x` and
        `y` coordinate for the endpoint of the line. The starting point of the
        line is implied as coordinates (0,0). Note that when this asset is 
        used in a `ggame.Sprite` class, the sprite's `x` and `y` coordinates
        will control the location of the line segment on the screen.

        As the `ggame.LineAsset` does not cover a region, only a `ggame.LineStyle` 
        argument must be supplied (`line`).
        """
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
    The `ggame.TextAsset` is a "virtual" asset that is created on the fly
    without requiring creation of an image file. A `TextAsset` instance
    represents a block of text, together with its styling (font, color, etc.).
    """
 
    def __init__(self, text, **kwargs):
        """
        The `ggame.TextAsset` must be created with a string as the `text` parameter.
        
        The remaining optional arguments must be supplied as keyword parameters. These
        parameters are described under the class attributes, below:
        """
        super().__init__()
        self.text = text
        self.style = kwargs.get('style', '20px Arial')
        """A string that specifies style, size and typeface (e.g. `'italic 20pt Helvetica'` or `'20px Arial'`)"""
        width = kwargs.get('width', 100)
        """Width of the text block on the screen, in pixels."""
        self.fill = kwargs.get('fill', Color(0, 1))
        """A valid `ggame.Color` instance that specifies the color and transparency of the text."""
        self.align = kwargs.get('align', 'left')
        """The alignment style of the text. One of: `'left'`, `'center'`, or `'right'`."""
        self.GFX = GFX_Text(self.text, 
            {'font': self.style,
                'fill' : self.fill.color,
                'align' : self.align,
                'wordWrap' : True,
                'wordWrapWidth' : width,
                })
        """The `GFX` property represents the underlying system object."""
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

