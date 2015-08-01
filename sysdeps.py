from browser import window, document
from javascript import JSObject, JSConstructor

GFX = JSObject(window.PIXI)
GFX_Rectangle = JSConstructor(GFX.Rectangle)
GFX_Texture = JSObject(GFX.Texture)
GFX_Texture_fromImage = JSConstructor(GFX_Texture.fromImage)
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

if __name__ == "__main__":
    def closefunc():
        print("Closing Window")
    
    w = GFX_Window(100, 100, closefunc)
    print(dir(w))
    print("Test Complete")
    
    