def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


if module_exists("browser") and module_exists("javascript"):

    from browser import window, document, load
    from javascript import JSObject, JSConstructor

    major = window.__BRYTHON__.implementation[0]
    minor = window.__BRYTHON__.implementation[1]
    if major == 3 and minor >= 3 or major > 3:
        GFX = window.PIXI
        GFX_Rectangle = GFX.Rectangle.new
        GFX_Texture = GFX.Texture.new
        GFX_Texture_fromImage = GFX.Texture.fromImage.new
        GFX_Sprite = GFX.Sprite.new
        GFX_Graphics = GFX.Graphics.new()
        GFX_Text = GFX.Text.new
        GFX_NewStage = GFX.Container.new
        SND = window.buzz
        SND_Sound = SND.sound.new
    else:
        GFX = JSObject(window.PIXI)
        GFX_Rectangle = JSConstructor(GFX.Rectangle)
        GFX_Texture = JSConstructor(GFX.Texture)
        GFX_Texture_fromImage = JSConstructor(GFX.Texture.fromImage)
        GFX_Sprite = JSConstructor(GFX.Sprite)
        GFX_Graphics = JSConstructor(GFX.Graphics)()
        GFX_Text = JSConstructor(GFX.Text)
        GFX_NewStage = JSConstructor(GFX.Container)
        SND = JSObject(window.buzz)
        SND_Sound = JSConstructor(SND.sound)
    GFX_DetectRenderer = GFX.autoDetectRenderer

    class GFX_Window(object):
        def __init__(self, width, height, onclose):
            canvas = window.document.getElementById("ggame-canvas")
            if canvas:
                self._w = window
                window.bsUI.graphicsmode()
                options = {"transparent": True, "antialias": True, "view": canvas}
                attachpoint = window.document.getElementById("graphics-column")
                w, h = attachpoint.clientWidth, attachpoint.clientHeight
            else:
                self._w = window.open("", "")
                w, h = self._w.innerWidth * 0.9, self._w.innerHeight * 0.9
                options = {"transparent": True, "antialias": True}
                attachpoint = self._w.document.body
            GFX.utils._saidHello = True
            # ugly hack to block pixi banner
            self._stage = GFX_NewStage()
            self.width = width if width != 0 else int(w)
            self.height = height if height != 0 else int(h)
            self.renderer = GFX.autoDetectRenderer(self.width, self.height, options)
            attachpoint.appendChild(self.renderer.view)
            self._w.ggame_quit = onclose

        def bind(self, evtspec, callback):
            self._w.document.body.unbind(evtspec)
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
            self.renderer.destroy()


elif module_exists("pygame"):

    try:
        from ggame.pygamedeps import *
    except ImportError:
        from pygamedeps import *

else:
    try:
        from ggame.headlessdeps import *
    except ImportError:
        from headlessdeps import *
