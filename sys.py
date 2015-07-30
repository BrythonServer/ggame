from browser import window, document
from javascript import JSObject, JSConstructor

GFX = JSObject(window.PIXI)
GFX_Rectangle = JSConstructor(GFX.Rectangle)
GFX_Texture = JSObject(GFX.Texture)
GFX_Texture_fromImage = JSConstructor(GFX_Texture.fromImage)
GFX_Sprite = JSConstructor(GFX.Sprite)
GFX_Graphics = JSConstructor(GFX.Graphics)()
GFX_Text = JSConstructor(GFX.Text)
SND = JSObject(window.buzz)
GFX_Stage = JSConstructor(GFX.Container)()
GFX_DetectRenderer = GFX.autoDetectRenderer 
