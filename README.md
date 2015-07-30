# ggame
The simple cross-platform sprite and game platform for Brython Server (Pygame, Tkinter to follow?).

Ggame stands for a couple of things: "good game" (of course!) and also "git game" or "github game" 
because it is designed to operate with [Brython Server](http://runpython.com) in concert with
Github as a backend file store.

## Functionality Goals

The ggame library is intended to be trivially easy to use. For example:

    from ggame import App, ImageAsset, Sprite
    
    # Create the app, with a 500x500 pixel stage
    app = App(500,500)  
    # Load an image asset for the app
    grass = ImageAsset(app, "ggame/bunny.png")
    # Create a displayed object using the asset
    Sprite(grass, (100,100))
    # Run the app
    app.run()


## Installing ggame

Before using ggame with your Python source repository on Github, you should add the ggame source
tree to your repository. You can, of course, just clone the project in to your projecgt, but you
will probably find the following method to be easier to maintain and keep up-to-date with the 
latest ggame sources: add ggame as a git subtree.

### Adding as Subtree

From the same directory as your own python sources, execute the following terminal commands:

    git remote add -f ggame https://github.com/BrythonServer/ggame.git
    git merge -s ours --no-commit ggame/master
    mkdir ggame
    git read-tree --prefix=ggame/ -u ggame/master
    git commit -m "Merge ggame project as our subdirectory"
    
If you want to pull in updates from ggame in the future:
    
    git pull -s subtree ggame master
    

