def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

if module_exists('browser') and module_exists('javascript'):

  from browser import window, document
  from javascript import JSObject, JSConstructor
  
  GFX = JSObject(window.PIXI)
  GFX_Rectangle = JSConstructor(GFX.Rectangle)
  GFX_Texture = JSConstructor(GFX.Texture)
  GFX_Texture_fromImage = JSConstructor(GFX.Texture.fromImage)
  GFX_Sprite = JSConstructor(GFX.Sprite)
  GFX_Graphics = JSConstructor(GFX.Graphics)()
  GFX_Text = JSConstructor(GFX.Text)
  GFX_DetectRenderer = GFX.autoDetectRenderer 
  SND = JSObject(window.buzz)
  SND_Sound = JSConstructor(SND.sound)
  
  class GFX_Window(object):
    
    def __init__(self, width, height, onclose):
      self._w = window.open("", "")
      self._stage = JSConstructor(GFX.Container)()
      self._renderer = GFX.autoDetectRenderer(width, height, {'transparent':True})
      self._w.document.body.appendChild(self._renderer.view)
      self._w.onunload = onclose
  
    def bind(self, evtspec, callback):
      self._w.document.body.bind(evtspec, callback)
      
    def add(self, obj):
      self._stage.addChild(obj)
      
    def remove(self, obj):
      self._stage.removeChild(obj)
      
    def animate(self, stepcallback):
      self._renderer.render(self._stage)
      self._w.requestAnimationFrame(stepcallback)
      
    def destroy(self):
      SND.all().stop()
      self._stage.destroy()
  

elif module_exists('pygame'):

  pass

else:
  
  from PIL import Image

  class _body(object):
    
    def __init__(self):
      self.events = {}

    def appendChild(self, obj):
      self.child = obj

    def bind(self, evt, action):
      self.events[evt] = action
      print("Binding {} to {}".format(evt, action))

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
        target('dummy')
        print("Animation frame")

  class _Container(object):

    def __init__(self):
      pass

    def destroy(self):
      pass

  class _Renderer(object):
    
    def __init__(self, x, y, argsdict):
      self.x = x
      self.y = y
      self.argsdict = argsdict
      self.view = 'view'
      print("Rendering created with {}x{} area".format(x, y))

    def render(self, stage):
      pass

  class _GFX(object):
    
    def __init__(self):
      self.Container = _Container
      self.autoDetectRenderer = _Renderer

  window = _window()

  GFX = _GFX()

  #document = object()
  
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
 
    def __init__(self, img='', crossdomain=False):
      self.name = img
      self.crossdomain = crossdomain
      if img == '':
        self.img = None
        self.basewidth = 0
        self.baseheight = 0
      else:
        self.img = Image.open(img)
        self.basewidth = self.img.width
        self.baseheight = self.img.height
        print("Texture from image {}, {}x{} pixels".format(img, self.basewidth, self.baseheight))
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
      print("Texture from base texture {}, {}x{} subframe {}x{}".format(inst.name, inst.basewidth, inst.baseheight, inst.framerect.width, inst.framerect.height))
      return inst

    def destroy(self):
      try:
        self.img.close()
        print("Destroying an image")
      except:
        print("Destroying a non-image")

  GFX_Texture = _Texture.fromTexture
  
  GFX_Texture_fromImage = _Texture  

  
  def GFX_Sprite():
    pass

  class _GFX_Graphics(object):

    def __init__(self):
      self.cleared = None
      self.visible = True
      self.width = None
      self.color = None
      self.alpha = None
      self.fillcolor = None
      self.fillalpha = None
      self.x = None
      self.y = None
      self.rwidth = None
      self.rheight = None
      self.radius = None

    def clone(self):
      clone = type(self)()
      clone.cleared = self.cleared
      clone.visible = self.visible
      clone.width = self.width
      clone.color = self.color
      clone.alpha = self.alpha
      clone.fillalpha = self.fillalpha
      clone.fillcolor = self.fillcolor
      clone.x = self.x
      clone.y = self.y
      clone.rwidth = self.rwidth
      clone.rheight = self.rheight
      clone.radius = self.radius
      return clone

    def clear(self):
      self.cleared = True

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
      self.rwidth = w
      self.rheight = h
      self.cleared = False
      print("Rectangle {}x{} at {},{}".format(w,h,x,y))
      return self

    def drawCircle(self, x, y, radius):
      self.x = x
      self.y = y
      self.radius = radius
      self.cleared = False
      print("Circle, radius {} at {},{}".format(radius,x,y))
      return self  

  _globalGraphics = _GFX_Graphics()

  GFX_Graphics = _globalGraphics

  
  def GFX_Text():
    pass
  
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

    def play(self):
      print("Playing sound object {}".format(self.url))

  SND_Sound = _SND_Sound

  
  class GFX_Window(object):
    
    def __init__(self, width, height, onclose):
      self._w = window.open("", "")
      self._stage = JSConstructor(GFX.Container)()
      self._renderer = GFX.autoDetectRenderer(width, height, {'transparent':True})
      self._w.document.body.appendChild(self._renderer.view)
      self._w.onunload = onclose
  
    def bind(self, evtspec, callback):
      self._w.document.body.bind(evtspec, callback)
      
    def add(self, obj):
      self._stage.addChild(obj)
      
    def remove(self, obj):
      self._stage.removeChild(obj)
      
    def animate(self, stepcallback):
      self._renderer.render(self._stage)
      self._w.requestAnimationFrame(stepcallback)
      
    def destroy(self):
      SND.all().stop()
      self._stage.destroy()
  
    
