def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

# PYTHON 3 and PYGAME DEPENDENCIES
if module_exists('pygame'):

  import pygame
  
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
  
  class _GFX_Rectangle(pygame.Rect):
    pass
  
  GFX_Rectangle = _GFX_Rectangle
 
  class _Texture(object):
 
    def __init__(self, img='', crossdomain=False):
      self.name = img
      if not img == '':
        self.img = pygame.image.load(img)  # pygame surface
        self.basewidth = self.img.get_width()
        self.baseheight = self.img.get_height()
        self.width = self.basewidth
        self.height = self.baseheight
        print("Texture from image {}, {}x{} pixels".format(img, self.basewidth, self.baseheight))
        self.baserect = _GFX_Rectangle(0, 0, self.basewidth, self.baseheight)
        self.framerect = self.baserect

    @classmethod
    def fromTexture(cls, texture, frame):
      inst = cls()
      inst.img = pygame.Surface((frame.width, frame.height))
      inst.img.blit(texture.img, (0,0), frame)
      inst.name = texture.name
      inst.basewidth = texture.basewidth
      inst.baseheight = texture.baseheight
      inst.baserect = texture.baserect
      inst.framerect = frame
      inst.width = frame.width
      inst.height = frame.height
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
      self.basetexture = texture
      self.texture = self.basetexture
      self.visible = True
      self.pos = vector(0,0)
      self.anch = vector(0,0)
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
      self.position = vector(0,0)

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
      self.position = vector(x,y)
      self.rwidth = w
      self.rheight = h
      self.width = w
      self.height = h
      self.cleared = False
      print("Rectangle {}x{} at {},{}".format(w,h,x,y))
      return self

    def drawCircle(self, x, y, radius):
      self.x = x
      self.y = y
      self.position = vector(x,y)
      self.radius = radius
      self.cleared = False
      self.width = radius*2
      self.height = radius*2
      print("Circle, radius {} at {},{}".format(radius,x,y))
      return self  

    def drawEllipse(self, x, y, hw, hh):
      self.x = x
      self.y = y
      self.position = vector(x,y)
      self.ehw = hw
      self.ehh = hh
      self.width = hw*2
      self.height = hh*2
      self.cleared = False
      print("Ellipse, {}x{} at {},{}".format(hw,hh,x,y))
      return self

    def drawPolygon(self, jpath):
      self.jpath = jpath
      self.cleared = False
      self.position = vector(jpath[0],jpath[1])
      x = []
      y = []
      for i in range(0,len(jpath)-1,2):
        x.append(jpath[i])
        y.append(jpath[i+1])
      self.width = max(x)-min(x)
      self.height = max(y)-min(y)
      print("Polygon")
      return self

    def moveTo(self, x, y):
      self.x = x
      self.y = y
      self.position = vector(x,y)
      return self

    def lineTo(self, x, y):
      self.xto = x
      self.yto = y
      self.width = abs(x)
      self.height = abs(y)
      self.cleared = False
      print("Line from {},{} to {},{}".format(self.x, self.y, x, y))
      return self 

  class _GFX_Text(object):

    def __init__(self, text, styledict):
      self.text = text
      self.styledict = styledict
      self.alpha = None
      self.visible = None
      self.width = 99
      self.height = 99
      self.position = vector(0,0)
      print("Text: {} in {}".format(text, styledict['font']))

    def clone(self):
      clone = type(self)(self.text, self.styledict)
      return clone

    def destroy(self):
      self.text = ''


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

    def play(self):
      print("Playing sound object {}".format(self.url))

  SND_Sound = _SND_Sound


  class HwEvent(object):

    evtmap = {2: 'keydown', 3: 'keyup', 4: 'mousemove', 5: 'mousedown', 6: 'mouseup'}
    keymap = {304:16,
              303:16,
              306:17,
              308:18,
              301:20,
              276:37,
              273:38,
              275:39,
              274:40,
              97:65,
              98:66,
              99:67,
              100:68,
              101:69,
              102:70,
              103:71,
              104:72,
              105:73,
              106:74,
              107:75,
              108:76,
              109:77,
              110:78,
              111:79,
              112:80,
              113:81,
              114:82,
              115:83,
              116:84,
              117:85,
              118:86,
              119:87,
              120:88,
              121:89,
              122:90,
              282:112,
              283:113,
              284:114,
              285:115,
              286:116,
              287:117,
              288:118,
              289:119,
              290:120,
              291:121,
              292:122,
              293:123,
              59:186,
              61:187,
              44:188,
              46:190,
              45:189,
              47:191,
              96:192,
              92:220,
              91:219,
              93:221,
              39:222}

    def __init__(self, pevent):
      self.type = HwEvent.evtmap.get(pevent.type, None)
      if self.type in ['keydown', 'keyup']:
        self.keyCode = HwEvent.keymap.get(pevent.key, pevent.key)
      elif self.type in ['mousemove', 'mousedown', 'mouseup']:
        self.wheelDelta = 0
        if self.type != 'mousemove' and pevent.button == 5:
          if self.type == 'mousedown':
            self.wheelDelta = 1
          else:
            self.wheelDelta = -1
        self.clientX = pevent.pos[0]
        self.clientY = pevent.pos[1]

  class GFX_Window(object):
    
    def __init__(self, width, height, onclose):
      pygame.init()
      self._w = pygame.display.set_mode((width, height))
      self.clock = pygame.time.Clock()
      self.sprites = []
      self.animatestarted = False
      self.bindings = {}
      self.onclose = onclose
      self.stop = False
      #self._w = window.open("", "")
      #self._stage = JSConstructor(GFX.Container)()
      #self._renderer = GFX.autoDetectRenderer(width, height, {'transparent':True})
      #self._w.document.body.appendChild(self._renderer.view)
      #self._w.onunload = onclose
  
    def bind(self, evtspec, callback):
      self.bindings[evtspec] = callback

    def add(self, obj):
      self.sprites.append(obj)
      #self._stage.addChild(obj)
      
    def remove(self, obj):
      self.sprites.remove(obj)
      #self._stage.removeChild(obj)
      
    def animate(self, stepcallback):
      # do stuff required to display
      self._w.fill(pygame.Color('white'))
      for s in self.sprites:
        self._w.blit(s.texture.img, (s.pos.x, s.pos.y))
      pygame.display.flip()
      events = pygame.event.get()
      for event in events:
        hwevent = HwEvent(event)
        if hwevent.type != None:
          self.bindings[hwevent.type](hwevent)
        if event.type == 12:
          print("Close!")
          self.onclose()
          self.destroy()
          self.stop = True
      if not self.animatestarted:
        self.animatestarted = True
        while not self.stop:
          self.clock.tick_busy_loop(30)
          stepcallback(0)
      #self._renderer.render(self._stage)
      #self._w.requestAnimationFrame(stepcallback)
      
    def destroy(self):
      pass
      #SND.all().stop()
      #self._stage.destroy()
  
    
