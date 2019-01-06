import sys
from ggame.app import App

sys.path.append("..")

import examples.bunnyhop
import examples.onebunny

# Asset Examples
import examples.assetcolor
import examples.assetlinestyle
import examples.assetimage
import examples.assetpolygon
import examples.assettext

# Circle Examples
import examples.circlecircle

# Astro Examples
import examples.astroplanet
import examples.astrorocket

# Indicator Examples
import examples.indicatorimageindicator
import examples.indicatorledindicator

# Input Examples
import examples.inputinputbutton
import examples.inputinputnumeric

# InputPoint Examples
import examples.inputpointglassbutton
import examples.inputpointinputimagebutton

# Label Examples
import examples.labellabel

# Timer Examples
import examples.timertimer

# Point Examples
import examples.pointpoint

# Slider Examples
import examples.sliderslider

# Sprite Examples
import examples.spritesprite


# Cleanup
for s in App.spritelist[:]:
    try:
        s.destroy()
    except ValueError:
        pass
