import os


def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


if module_exists("PIL"):

    from PIL import Image

    class _body(object):
        def __init__(self):
            self.events = {}

        def appendChild(self, obj):
            self.child = obj

        def bind(self, evt, action):
            self.events[evt] = action
            print("Binding {} to {}".format(evt, action))

        def unbind(self, evt):
            print("Unbinding {}".format(evt))

    class _document(object):
        def __init__(self):
            self.body = _body()

    class _window(object):
        def __init__(self):
            self.document = _document()
            self.animatex = 0

        def open(self, s1, s2):
            return self

        def requestAnimationFrame(self, target):
            if self.animatex < 10:
                self.animatex += 1
                target("dummy")
                print("Animation frame")

    class _Container(object):
        def __init__(self):
            self.things = []

        def destroy(self):
            del self.things

        def addChild(self, obj):
            self.things.append(obj)

        def removeChild(self, obj):
            self.things.remove(obj)

    class getBoundingClientRect(object):
        left = 0
        top = 0
        width = 1
        height = 1

    class renderView(object):
        def getBoundingClientRect(self):
            return getBoundingClientRect()

    class _Renderer(object):
        def __init__(self, x, y, argsdict):
            self.x = x
            self.y = y
            self.argsdict = argsdict
            self.view = renderView()
            print("Rendering created with {}x{} area".format(x, y))

        def render(self, stage):
            pass

    class _GFX(object):
        def __init__(self):
            self.Container = _Container
            self.autoDetectRenderer = _Renderer
            self.width = 0
            self.height = 0

    window = _window()

    GFX = _GFX()

    # document = object()

    def JSConstructor(cls):
        return cls

    def JSObject(obj):
        return obj

    class _GFX_Rectangle(object):
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.width = w
            self.height = h

    GFX_Rectangle = _GFX_Rectangle

    class _Texture(object):
        def __init__(self, img="", crossdomain=False):
            self.name = img
            self.crossdomain = crossdomain
            if img == "":
                self.img = None
                self.basewidth = 0
                self.baseheight = 0
                self.width = 0
                self.height = 0
            else:
                try:
                    self.img = Image.open(img)
                except (OSError, IOError) as e:
                    thispath = os.path.abspath(__file__)
                    thispath = os.path.dirname(thispath)
                    ggameimg = os.path.join(thispath, img)
                    self.img = Image.open(ggameimg)

                self.basewidth = self.img.width
                self.baseheight = self.img.height
                self.width = self.basewidth
                self.height = self.baseheight
                print(
                    "Texture from image {}, {}x{} pixels".format(
                        img, self.basewidth, self.baseheight
                    )
                )
            self.baserect = _GFX_Rectangle(0, 0, self.basewidth, self.baseheight)
            self.framerect = self.baserect

        @classmethod
        def fromTexture(cls, texture, frame):
            inst = cls()
            inst.img = texture.img
            inst.name = texture.name
            inst.basewidth = texture.basewidth
            inst.baseheight = texture.baseheight
            inst.baserect = texture.baserect
            inst.framerect = frame
            inst.width = frame.width
            inst.height = frame.height
            print(
                "Texture from base texture {}, {}x{} subframe {}x{}".format(
                    inst.name,
                    inst.basewidth,
                    inst.baseheight,
                    inst.framerect.width,
                    inst.framerect.height,
                )
            )
            return inst

        def destroy(self):
            try:
                self.img.close()
                print("Destroying an image")
            except:
                print("Destroying a non-image")

    GFX_Texture = _Texture.fromTexture

    GFX_Texture_fromImage = _Texture

    class vector(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __getitem__(self, key):
            if key == 0:
                return self.x
            elif key == 1:
                return self.y
            else:
                raise KeyError

        def __setitem(self, key, value):
            if key == 0:
                self.x = value
            elif key == 1:
                self.y = value
            else:
                raise KeyError

    class GFX_Sprite(object):
        def __init__(self, texture):
            self.texture = texture
            self.visible = True
            self.pos = vector(0, 0)
            self.anch = vector(0, 0)
            self.scal = vector(1.0, 1.0)
            self.width = texture.width
            self.height = texture.height
            self.rotation = 0.0

        @property
        def position(self):
            return self.pos

        @position.setter
        def position(self, value):
            self.pos.x = value[0]
            self.pos.y = value[1]

        @property
        def anchor(self):
            return self.anch

        @anchor.setter
        def anchor(self, value):
            self.anch.x = value[0]
            self.anch.y = value[1]

        @property
        def scale(self):
            return self.scal

        @scale.setter
        def scale(self, value):
            self.scal.x = value[0]
            self.scal.y = value[1]

        def destroy(self):
            pass

    class _GFX_Graphics(object):
        def __init__(self):
            self.clear()

        def clear(self):
            self.cleared = True
            self.visible = True
            self.lwidth = None
            self.color = None
            self.alpha = None
            self.fillcolor = None
            self.fillalpha = None
            self.x = None
            self.y = None
            self.rwidth = None
            self.rheight = None
            self.radius = None
            self.ehw = None
            self.ehh = None
            self.xto = None
            self.yto = None
            self.jpath = None
            self.width = None
            self.height = None
            self.position = vector(0, 0)

        def destroy(self):
            self.clear()

        def clone(self):
            clone = type(self)()
            clone.cleared = self.cleared
            clone.visible = self.visible
            clone.lwidth = self.lwidth
            clone.color = self.color
            clone.alpha = self.alpha
            clone.fillalpha = self.fillalpha
            clone.fillcolor = self.fillcolor
            clone.x = self.x
            clone.y = self.y
            clone.rwidth = self.rwidth
            clone.rheight = self.rheight
            clone.radius = self.radius
            clone.ehw = self.ehw
            clone.ehh = self.ehh
            clone.xto = self.xto
            clone.yto = self.yto
            clone.jpath = self.jpath
            clone.width = self.width
            clone.height = self.height
            clone.position = self.position
            return clone

        def lineStyle(self, width, color, alpha):
            self.width = width
            self.color = color
            self.alpha = alpha

        def beginFill(self, color, alpha):
            self.fillcolor = color
            self.fillalpha = alpha

        def drawRect(self, x, y, w, h):
            self.x = x
            self.y = y
            self.position = vector(x, y)
            self.rwidth = w
            self.rheight = h
            self.width = w
            self.height = h
            self.cleared = False
            print("Rectangle {}x{} at {},{}".format(w, h, x, y))
            return self

        def drawCircle(self, x, y, radius):
            self.x = x
            self.y = y
            self.position = vector(x, y)
            self.radius = radius
            self.cleared = False
            self.width = radius * 2
            self.height = radius * 2
            print("Circle, radius {} at {},{}".format(radius, x, y))
            return self

        def drawEllipse(self, x, y, hw, hh):
            self.x = x
            self.y = y
            self.position = vector(x, y)
            self.ehw = hw
            self.ehh = hh
            self.width = hw * 2
            self.height = hh * 2
            self.cleared = False
            print("Ellipse, {}x{} at {},{}".format(hw, hh, x, y))
            return self

        def drawPolygon(self, jpath):
            self.jpath = jpath
            self.cleared = False
            self.position = vector(jpath[0], jpath[1])
            x = []
            y = []
            for i in range(0, len(jpath) - 1, 2):
                x.append(jpath[i])
                y.append(jpath[i + 1])
            self.width = max(x) - min(x)
            self.height = max(y) - min(y)
            print("Polygon")
            return self

        def moveTo(self, x, y):
            self.x = x
            self.y = y
            self.position = vector(x, y)
            return self

        def lineTo(self, x, y):
            self.xto = x
            self.yto = y
            self.width = abs(x)
            self.height = abs(y)
            self.cleared = False
            print("Line from {},{} to {},{}".format(self.x, self.y, x, y))
            return self

        def generateTexture(self):
            return _Texture()

    class _GFX_Text(object):
        def __init__(self, text, styledict):
            self.text = text
            self.styledict = styledict
            self.alpha = None
            self.visible = None
            self.width = 99
            self.height = 99
            self.position = vector(0, 0)
            print("Text: {} in {}".format(text, styledict["font"]))

        def clone(self):
            clone = type(self)(self.text, self.styledict)
            return clone

        def destroy(self):
            self.text = ""

    GFX_Text = _GFX_Text

    _globalGraphics = _GFX_Graphics()

    GFX_Graphics = _globalGraphics

    def GFX_DetectRenderer():
        pass

    class _SND_all(object):
        def __init__(self):
            pass

        def stop(self):
            print("Stopping all sounds")

    class _SND(object):
        def __init__(self):
            self.all = _SND_all

    SND = _SND()

    class _SND_Sound(object):
        def __init__(self, url):
            self.url = url
            print("Creating sound object {}".format(url))

        def load(self):
            pass

        def loop(self):
            pass

        def stop(self):
            pass

        def getVolume(self):
            pass

        def setVolume(self, vol):
            pass

        def play(self):
            print("Playing sound object {}".format(self.url))

    SND_Sound = _SND_Sound

    class GFX_Window(object):
        def __init__(self, width, height, onclose):
            self._w = window.open("", "")
            self.width = width if width > 0 else 100
            self.height = height if height > 0 else 100
            self._stage = JSConstructor(GFX.Container)()
            self.renderer = GFX.autoDetectRenderer(width, height, {"transparent": True})
            self._w.document.body.appendChild(self.renderer.view)
            self._w.onunload = onclose

        def bind(self, evtspec, callback):
            self._w.document.body.bind(evtspec, callback)

        def unbind(self, evtspec):
            self._w.document.body.unbind(evtspec)

        def add(self, obj):
            self._stage.addChild(obj)

        def remove(self, obj):
            self._stage.removeChild(obj)

        def animate(self, stepcallback):
            self.renderer.render(self._stage)
            self._w.requestAnimationFrame(stepcallback)

        def destroy(self):
            SND.all().stop()
            self._stage.destroy()
