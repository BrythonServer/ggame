from ggame import App, ImageAsset, Sprite
# Create a displayed object at 100,100 using an image asset
Sprite(ImageAsset("bunny.png"), (100,100))
# Create the app, with a default stage
app = App()  
# Run the app
app.run()