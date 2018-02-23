from math import pi, degrees, radians, atan2, sin, cos
from ggame import LineStyle, Color
from ggmath import MathApp, Circle, ImagePoint, Timer

class Rocket(ImagePoint):
    
    def __init__(self, planet, **kwargs):
        self._xy = (0,0)
        self.planet = planet
        self.bmurl = kwargs.get('bitmap', 'rocket.png') # default rocket png
        self.bitmapframe = kwargs.get('bitmapframe', None) #
        self.bitmapqty = kwargs.get('bitmapqty', 1) # Number of images in bitmap
        self.bitmapdir = kwargs.get('bitmapdir', 'horizontal') # animation orientation
        self.bitmapmargin = kwargs.get('bitmapmargin', 0) # bitmap spacing
        self.tickrate = kwargs.get('tickrate', 30) # dynamics calcs per sec
        # dynamic parameters
        self.timezoom = self.Eval(kwargs.get('timezoom', 0)) # 1,2,3 faster, -1, slower
        # end dynamic 
        super().__init__(self._getposition, 
            self.bmurl, 
            self.bitmapframe, 
            self.bitmapqty, 
            self.bitmapdir,
            self.bitmapmargin)
        self.scale = kwargs.get('bitmapscale', 0.1) # small
        initvel = kwargs.get('velocity', 0) # initial velocity
        initdird = kwargs.get('directiond', 0) # initial direction, degrees
        initdir = kwargs.get('direction', radians(initdird))
        tanomaly = kwargs.get('tanomaly', pi/2) # position angle
        tanomaly = radians(kwargs.get('tanomalyd', degrees(tanomaly))) 
        altitude = kwargs.get('altitude', 0) #
        r = altitude + self.planet.radius
        self.xyposition = (r*cos(tanomaly), r*sin(tanomaly))
        MathApp.listenKeyEvent('keydown', 'left arrow', self.turn)
        MathApp.listenKeyEvent('keydown', 'right arrow', self.turn)
        self.timer = Timer()
        self.timer.callEvery(1/self.tickrate, self.dynamics)
        self.V = [initvel * cos(initdir), initvel * sin(initdir)]

    
    # override recommended!
    def thrust(self):
        return 0

    # override recommended!
    def mass(self):
        return 1

    def dynamics(self, timer):
        print("dynamics")
        tick = 10**self.timezoom()/self.tickrate

        # 4th order runge-kutta method (https://sites.temple.edu/math5061/files/2016/12/final_project.pdf)
        # and http://spiff.rit.edu/richmond/nbody/OrbitRungeKutta4.pdf  (succinct, but with a typo)
        k1v = self.ar(self._xy)
        k1r = self.V
        k2v = self.ar(self.vadd(self._xy, self.vmul(tick/2, k1r)))
        k2r = self.vadd(self.V, self.vmul(tick/2, k1v))
        k3v = self.ar(self.vadd(self._xy, self.vmul(tick/2, k2r)))
        k3r = self.vadd(self.V, self.vmul(tick/2, k2v))
        k4v = self.ar(self.vadd(self._xy, self.vmul(tick, k3r)))
        k4r = self.vadd(self.V, self.vmul(tick, k3v))
        self.V = [self.V[i] + tick/6*(k1v[i] + 2*k2v[i] + 2*k3v[i] + k4v[i]) for i in (0,1)]
        self._xy = [self._xy[i] + tick/6*(k1r[i] + 2*k2r[i] + 2*k3r[i] + k4r[i]) for i in (0,1)]
        self._touchAsset()

        if self.altitude < 0:
            self.V = [0,0]
            self.altitude = 0

    
    # generic force as a function of position
    def fr(self, pos):
        t = self.thrust()
        G = 6.674E-11
        r = MathApp.distance((0,0), pos)
        uvec = (-pos[0]/r, -pos[1]/r)
        fg = G*self.mass()*self.planet.mass/r**2
        F = [x*fg for x in uvec]
        return [F[0] + t*cos(self.rotation), F[1] + t*sin(self.rotation)]

    # geric acceleration as a function of position
    def ar(self, pos):
        m = self.mass()
        F = self.fr(pos)
        return [F[i]/m for i in (0,1)]
        
    def vadd(self, v1, v2):
        return [v1[i]+v2[i] for i in (0,1)]
    
    def vmul(self, s, v):
        return [s*v[i] for i in (0,1)]
    
    def fgrav(self):
        G = 6.674E-11
        r = self.r
        uvec = (-self._xy[0]/r, -self._xy[1]/r)
        F = G*self.mass()*self.planet.mass/r**2
        return [x*F for x in uvec]
    
    def turn(self, event):
        increment = pi/50 * (1 if event.key == "left arrow" else -1)
        self.rotation += increment
            
    def _getposition(self):
        return self._xy
    
    @property
    def xyposition(self):
        return self._xy
        
    @xyposition.setter
    def xyposition(self, pos):
        self._xy = pos
        self._touchAsset()

    @property
    def tanomalyd(self):
        return degrees(self.tanomaly)
        
    @tanomalyd.setter
    def tanomalyd(self, angle):
        self.tanomaly = radians(angle)

    @property
    def altitude(self):
        return MathApp.distance(self._pos(), (0,0)) - self.planet.radius
        
    @altitude.setter
    def altitude(self, alt):
        r = alt + self.planet.radius
        self.xyposition = (r*cos(self.tanomaly), r*sin(self.tanomaly))
        self._touchAsset()

    @property
    def tanomaly(self):
        pos = self._pos()
        return atan2(pos[1],pos[0])
        
    @tanomaly.setter
    def tanomaly(self, angle):
        r = self.r
        self.xyposition = (r*cos(angle), r*sin(angle))
        self._touchAsset()
            
    @property
    def r(self):
        return self.altitude + self.planet.radius
        
        
    


class Planet(MathApp):
    
    def __init__(self, rocket, **kwargs):
        self.scale = kwargs.get('scale', 10)  # 10 pixels per meter default
        self.radius = kwargs.get('radius', 6.371E6) # Earth - meters
        self.mass = kwargs.get('mass', 5.9722E24) # Earth - kg
        self.color = kwargs.get('color', 0x008040)  # greenish
        super().__init__(self.scale)
        self.rocket = rocket(self, **kwargs)  
        self.viewaltitude = kwargs.get('viewalt', self.rocket.altitude) # how high to look
        self.viewanomaly = kwargs.get('viewanom', self.rocket.tanomaly)  # where to look
        self.viewanomalyd = kwargs.get('viewanomd', degrees(self.viewanomaly))
        self.planetcircle = Circle(
            (0,0), 
            self.radius, 
            LineStyle(1, Color(self.color,1)), 
            Color(self.color,0.5))
        r = self.radius + self.viewaltitude
        self.viewPosition = (r*cos(self.viewanomaly), r*sin(self.viewanomaly))
        self.run()


# test code here
if __name__ == "__main__":
    
    #Planet(Rocket, scale=0.0001, timezoom=2.2, altitude=804672, direction=0, velocity=8000)  # 500 miles, orbital velocity
    
    t = Timer()
    t.callEvery(1/10, tfunc)
    
    
    def tfunc(t):
        print('tick')
