import unittest
from ggame.astro import Rocket, Planet
import time

class TestAstroMethods(unittest.TestCase):

    def test_astro(self):
        earth = Planet(viewscale=0.00005)
        earth.run()
    
        rocket1 = Rocket(earth, altitude=400000, velocity=7670, timezoom=2)
        rocket2 = Rocket(earth, altitude=440000, velocity=7670, timezoom=2, statuspos=[300,10])

        for i in range(10):
            time.sleep(1/60)
            earth.step()

        Planet._destroy()


if __name__ == '__main__':
    unittest.main()
