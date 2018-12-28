"""
Example of using Rocket class.
"""
from ggame.astro import Planet, Rocket

EARTH = Planet(viewscale=0.00005)
EARTH.run()

ROCKET = Rocket(EARTH, altitude=400000, velocity=7670, timezoom=2)
