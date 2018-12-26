from ggame.astro import Planet, Rocket

earth = Planet(viewscale=0.00005)
earth.run()

rocket1 = Rocket(earth, altitude=400000, velocity=7670, timezoom=2)