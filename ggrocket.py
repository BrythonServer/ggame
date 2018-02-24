# ggrocket - ggmath extensions for modeling spacecraft in planetary orbit

from math import pi, degrees, radians, atan2, sin, cos, sqrt
from ggame import LineStyle, Color
from ggmath import MathApp, Circle, ImagePoint, Timer, Label

class Rocket(ImagePoint):

    def __init__(self, planet, **kwargs):
        """
        Initialize the Rocket object. 
        Required parameters:
        :planet:  Reference to a Planet object.
        
        Optional keyword parameters are supported:
        :bitmap:  url of a suitable bitmap image for the rocket (png recommended)
                    default is `rocket.png`
        :bitmapscale:  scale factor for bitmap. Default is 0.1
        :velocity:  initial rocket speed. default is zero.
        :directiond:  initial rocket direction in degrees. Default is zero.
        :direction:  initial rocket direction in radians. Default is zero.
        :tanomalyd:  initial rocket true anomaly in degrees. Default is 90.
        :tanomaly:  initial rocket true anomaly in radians. Default is pi/2.
        :altitude:  initial rocket altitude in meters. Default is zero.
        :showstatus:  boolean displays flight parameters on screen. Default is True.
        
        Following parameters may be set as a constant value, or pass in the
        name of a function that will return the value dynamically or the
        name of a `ggmath` UI control that will return the value
        :timezoom:  scale factor for time zoom. Factor = 10**timezoom
        :heading:  direction to point the rocket in (must be radians)
        :mass:  mass of the rocket (must be kg)
        :thrust:  thrust of the rocket (must be N)

        Animation related parameters may be ignored if no sprite animation:
        :bitmapframe:  ((x1,y1),(x2,y2)) tuple defines a region in the bitmap
        :bitmapqty:  number of bitmaps -- used for animation effects
        :bitmapdir:  "horizontal" or "vertical" use with animation effects
        :bitmapmargin:  pixels between successive animation frames
        :tickrate:  frequency of spacecraft dynamics calculations (Hz)
        """
        self._xy = (1000000,1000000)
        self.planet = planet
        self.bmurl = kwargs.get('bitmap', 'rocket.png') # default rocket png
        self.bitmapframe = kwargs.get('bitmapframe', None) #
        self.bitmapqty = kwargs.get('bitmapqty', 1) # Number of images in bitmap
        self.bitmapdir = kwargs.get('bitmapdir', 'horizontal') # animation orientation
        self.bitmapmargin = kwargs.get('bitmapmargin', 0) # bitmap spacing
        self.tickrate = kwargs.get('tickrate', 30) # dynamics calcs per sec
        self.showstatus = kwargs.get('showstatus', True) # show stats
        self.localheading = 0
        # dynamic parameters
        self.timezoom = self.Eval(kwargs.get('timezoom', self.gettimezoom)) # 1,2,3 faster, -1, slower
        self.heading = self.Eval(kwargs.get('heading', self.getheading)) # must be radians
        self.mass = self.Eval(kwargs.get('mass', self.getmass)) # kg
        self.thrust = self.Eval(kwargs.get('thrust', self.getthrust)) # N
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
        self._xy = (r*cos(tanomaly), r*sin(tanomaly))
        # default heading control if none provided by user
        if self.heading == self.getheading:
            Planet.listenKeyEvent('keydown', 'left arrow', self.turn)
            Planet.listenKeyEvent('keydown', 'right arrow', self.turn)
        self.timer = Timer()
        self.timer.callEvery(1/self.tickrate, self.dynamics)
        self.V = [initvel * cos(initdir), initvel * sin(initdir)]
        # set up status display
        if self.showstatus:
            showparms = [self.velocityText,
                        self.courseDegreesText,
                        self.altitudeText,
                        self.thrustText,
                        self.massText,
                        self.trueAnomalyDegreesText,
                        self.scaleText,
                        self.timeZoomText]
            for i in range(len(showparms)):
                Label((10,10+i*25), showparms[i], size=15, positioning="physical")

    
    # override or define externally!
    def getthrust(self):
        return 0

    # override or define externally!
    def getmass(self):
        return 1

    # override or define externally!
    def getheading(self):
        return self.localheading
        
    # override or define externally!
    def gettimezoom(self):
        return 0

    # functions available for reporting flight parameters to UI
    def velocityText(self):
        """
        Report the velocity in m/s
        """
        return "Velocity: {0:4.6} m/s".format(self.vmag(self.V))
        
    def courseDegreesText(self):
        """
        Report the heading in degrees (zero to the right)
        """
        return "Course: {0:4.6}°".format(degrees(atan2(self.V[1], self.V[0])))

    def thrustText(self):
        """
        Report the thrust level in Newtons
        """
        return "Thrust: {0:4.6} N".format(self.thrust())
        
    def massText(self):
        """
        Report the spacecraft mass in kilograms
        """
        return "Mass: {0:4.6} kg".format(self.mass())
        
    def trueAnomalyDegreesText(self):
        """
        Report the true anomaly in degrees
        """
        return "True Anomaly: {0:4.6}°".format(self.tanomalyd)
        
    def trueAnomalyRadiansText(self):
        """
        Report the true anomaly in radians
        """
        return "True Anomaly: {0:4.6}".format(self.tanomaly)
        
    def altitudeText(self):
        """
        Report the altitude in meters
        """
        return "Altitude: {0:4.6} m".format(self.altitude)
        
    def radiusText(self):
        """
        Report the radius (distance to planet center) in meters
        """
        return "Radius: {0:4.6} m".format(self.r)
        
    def scaleText(self):
        """
        Report the view scale (pixels/meter)
        """
        return "View Scale: {0:6.4} px/m".format(self.planet._scale)
    
    def timeZoomText(self):
        """
        Report the time acceleration
        """
        return "Time Zoom: {0:4.6}".format(float(self.timezoom()))
    


            
    def dynamics(self, timer):
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
        if self.altitude < 0:
            self.V = [0,0]
            self.altitude = 0
            
        print(self._xy[1])

    # generic force as a function of position
    def fr(self, pos):
        self.rotation = self.heading()
        t = self.thrust()
        G = 6.674E-11
        r = Planet.distance((0,0), pos)
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
        
    def vmag(self, v):
        return sqrt(v[0]**2 + v[1]**2)
    
    def fgrav(self):
        G = 6.674E-11
        r = self.r
        uvec = (-self._xy[0]/r, -self._xy[1]/r)
        F = G*self.mass()*self.planet.mass/r**2
        return [x*F for x in uvec]
    
    def turn(self, event):
        increment = pi/50 * (1 if event.key == "left arrow" else -1)
        self.localheading += increment
            
    def _getposition(self):
        return self._xy
    
    @property
    def xyposition(self):
        return self._xy
        
    @xyposition.setter
    def xyposition(self, pos):
        self._xy = pos
        #self._touchAsset()

    @property
    def tanomalyd(self):
        return degrees(self.tanomaly)
        
    @tanomalyd.setter
    def tanomalyd(self, angle):
        self.tanomaly = radians(angle)

    @property
    def altitude(self):
        return Planet.distance(self._xy, (0,0)) - self.planet.radius
        
    @altitude.setter
    def altitude(self, alt):
        r = alt + self.planet.radius
        print("altitude.set ", r, self.tanomaly)
        self._xy = (r*cos(self.tanomaly), r*sin(self.tanomaly))
        #self._touchAsset()

    @property
    def tanomaly(self):
        #pos = self._pos()
        return atan2(self._xy[1],self._xy[0])
        
    @tanomaly.setter
    def tanomaly(self, angle):
        r = self.r
        self._xy = (r*cos(angle), r*sin(angle))
        self._touchAsset()
            
    @property
    def r(self):
        return self.altitude + self.planet.radius

        
        
    


class Planet(MathApp):
    
    def __init__(self, rocket, **kwargs):
        """
        Initialize the Planet object. 
        Required parameters:
        :rocket:  Name of a Rocket-based class.

        All of the Rocket optional keyword parameters are supported and will
        be passed to the rocket class `__init__` function during instantiation.
        
        Optional keyword parameters are supported:
        :scale:  pixels per meter in graphics display. Default is 10.
        :radius:  radius of the planet in meters. Default is Earth radius.
        :mass: mass of the planet in kg. Default is Earth mass.
        :color: color of the planet. Default is greenish (0x008040).
        :viewalt: altitude of initial viewpoint in meters. 
            Default is rocket altitude.
        :viewanom: true anomaly (angle) of initial viewpoint in radians. 
            Default is the rocket anomaly.
        :viewanomd: true anomaly (angle) of initial viewpoing in degrees.
            Default is the rocket anomaly.
        """
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
    Planet(Rocket, altitude = 100)  # 500 miles, orbital velocity
    #Planet(Rocket)


