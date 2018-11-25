"""
ggame extensions for modeling spacecraft in planetary orbit
"""

from math import pi, degrees, radians, atan2, sin, cos, sqrt
from ggame.asset import LineStyle, Color
from ggame.mathapp import MathApp
from ggame.circle import Circle
from ggame.point import ImagePoint
from ggame.timer import Timer
from ggame.label import Label

class Rocket(ImagePoint):
    """
    Rocket is a class for simulating the motion of a projectile through space, 
    acted upon by arbitrary forces (thrust) and by gravitaitonal 
    attraction to a single planetary object.

    Initialize the Rocket object. 
    
    Example:
    
        rocket1 = Rocket(earth, altitude=400000, velocity=7670, timezoom=2)
   
    Required parameters:
    
    * **planet**:  Reference to a `Planet` object.
    
    Optional keyword parameters are supported:
    
    * **bitmap**:  url of a suitable bitmap image for the rocket (png recommended)
      default is `ggimages/rocket.png`
    * **bitmapscale**:  scale factor for bitmap. Default is 0.1
    * **velocity**:  initial rocket speed. default is zero.
    * **directiond**:  initial rocket direction in degrees. Default is zero.
    * **direction**:  initial rocket direction in radians. Default is zero.
    * **tanomalyd**:  initial rocket true anomaly in degrees. Default is 90.
    * **tanomaly**:  initial rocket true anomaly in radians. Default is pi/2.
    * **altitude**:  initial rocket altitude in meters. Default is zero.
    * **showstatus**:  boolean displays flight parameters on screen. Default
      is True.
    * **statuspos**:  tuple with x,y coordinates of flight parameters. 
      Default is upper left.
    * **statuslist**: list of status names to include in flight parameters. 
      Default is all, consisting of: "velocity", "acceleration", "course",
      "altitude", "thrust", "mass", "trueanomaly", "scale", "timezoom",
      "shiptime"
    * **leftkey**: a `ggame` key identifier that will serve as the 
      "rotate left" key while controlling the ship. Default is 'left arrow'.
    * **rightkey**: a `ggame` key identifier that will serve as the 
      "rotate right" key while controlling the ship. Default is 'right arrow'.
    
    Following parameters may be set as a constant value, or pass in the
    name of a function that will return the value dynamically or the
    name of a `ggmath` UI control that will return the value.
    
    * **timezoom**  scale factor for time zoom. Factor = 10^timezoom
    * **heading**  direction to point the rocket in (must be radians)
    * **mass**  mass of the rocket (must be kg)
    * **thrust**  thrust of the rocket (must be N)

    Animation related parameters may be ignored if no sprite animation:
    
    * **bitmapframe**  ((x1,y1),(x2,y2)) tuple defines a region in the bitmap
    * **bitmapqty**  number of bitmaps -- used for animation effects
    * **bitmapdir**  "horizontal" or "vertical" use with animation effects
    * **bitmapmargin**  pixels between successive animation frames
    * **tickrate**  frequency of spacecraft dynamics calculations (Hz)
    
    """

    def __init__(self, planet, **kwargs):
        self._xy = (1000000,1000000)
        self.planet = planet
        self.bmurl = kwargs.get('bitmap', 'ggimages/rocket.png') # default rocket png
        self.bitmapframe = kwargs.get('bitmapframe', None) #
        self.bitmapqty = kwargs.get('bitmapqty', 1) # Number of images in bitmap
        self.bitmapdir = kwargs.get('bitmapdir', 'horizontal') # animation orientation
        self.bitmapmargin = kwargs.get('bitmapmargin', 0) # bitmap spacing
        self.tickrate = kwargs.get('tickrate', 30) # dynamics calcs per sec
        # status display
        statusfuncs = [ self.velocityText,
                        self.accelerationText,
                        self.courseDegreesText,
                        self.altitudeText,
                        self.thrustText,
                        self.massText,
                        self.trueAnomalyDegreesText,
                        self.scaleText,
                        self.timeZoomText,
                        self.shipTimeText]
        statuslist = [  "velocity",
                        "acceleration",
                        "course",
                        "altitude",
                        "thrust",
                        "mass",
                        "trueanomaly",
                        "scale",
                        "timezoom",
                        "shiptime"]
        
        self.showstatus = kwargs.get('showstatus', True) # show stats
        self.statuspos = kwargs.get('statuspos', [10,10])  # position of stats
        self.statusselect = kwargs.get('statuslist', statuslist)
        self.localheading = 0
        # dynamic parameters
        self.timezoom = self.Eval(kwargs.get('timezoom', self.gettimezoom)) # 1,2,3 faster, -1, slower
        self.heading = self.Eval(kwargs.get('heading', self.getheading)) # must be radians
        self.mass = self.Eval(kwargs.get('mass', self.getmass)) # kg
        self.thrust = self.Eval(kwargs.get('thrust', self.getthrust)) # N
        # end dynamic 
        super().__init__(self.bmurl,
            self._getposition, 
            frame = self.bitmapframe, 
            qty = self.bitmapqty, 
            direction = self.bitmapdir,
            margin = self.bitmapmargin)
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
        leftkey = kwargs.get('leftkey', 'left arrow')
        rightkey = kwargs.get('rightkey', 'right arrow')
        if self.heading == self.getheading:
            Planet.listenKeyEvent('keydown', leftkey, self.turn)
            Planet.listenKeyEvent('keydown', rightkey, self.turn)
        self.timer = Timer()
        self.shiptime = 0  # track time on shipboard
        self.timer.callEvery(1/self.tickrate, self.dynamics)
        self.lasttime = self.timer.time
        self.V = [initvel * cos(initdir), initvel * sin(initdir)]
        self.A = [0,0]
        # keep track of on-screen resources
        self._labels = []
        # set up status display
        if self.showstatus:
            self.addStatusReport(statuslist, statusfuncs, self.statusselect)

    # override or define externally!
    def getthrust(self):
        """
        User override function for dynamically determining thrust force.
        """
        return 0

    # override or define externally!
    def getmass(self):
        """
        User override function for dynamically determining rocket mass.
        """
        return 1

    # override or define externally!
    def getheading(self):
        """
        User override function for dynamically determining the heading.
        """
        return self.localheading
        
    # override or define externally!
    def gettimezoom(self):
        """
        User override function for dynamically determining the timezoom.
        """
        return 0

    # add a status reporting function to status display
    def addStatusReport(self, statuslist, statusfuncs, statusselect):
        """
        Accept list of all status names, all status text functions, and
        the list of status names that have been selected for display.
        """
        statusdict = {n:f for n, f in zip(statuslist, statusfuncs)}
        for name in statusselect:
            if name in statusdict:
                self._labels.append(
                    Label(
                        self.statuspos[:], 
                        statusdict[name], 
                        size=15, 
                        positioning='physical', 
                        width=250))
                self.statuspos[1] += 25

    # functions available for reporting flight parameters to UI
    def velocityText(self):
        """
        Report the velocity in m/s as a text string.
        """
        return "Velocity:     {0:8.1f} m/s".format(self.velocity)
        
    def accelerationText(self):
        """
        Report the acceleration in m/s as a text string.
        """
        return "Acceleration: {0:8.1f} m/s²".format(self.acceleration)
        
    def courseDegreesText(self):
        """
        Report the heading in degrees (zero to the right) as a text string.
        """
        return "Course:       {0:8.1f}°".format(degrees(atan2(self.V[1], self.V[0])))

    def thrustText(self):
        """
        Report the thrust level in Newtons as a text string.
        """
        return "Thrust:       {0:8.1f} N".format(self.thrust())
        
    def massText(self):
        """
        Report the spacecraft mass in kilograms as a text string.
        """
        return "Mass:         {0:8.1f} kg".format(self.mass())
        
    def trueAnomalyDegreesText(self):
        """
        Report the true anomaly in degrees as a text string.
        """
        return "True Anomaly: {0:8.1f}°".format(self.tanomalyd)
        
    def trueAnomalyRadiansText(self):
        """
        Report the true anomaly in radians as a text string.
        """
        return "True Anomaly: {0:8.4f}".format(self.tanomaly)
        
    def altitudeText(self):
        """
        Report the altitude in meters as a text string.
        """
        return "Altitude:     {0:8.1f} m".format(self.altitude)
        
    def radiusText(self):
        """
        Report the radius (distance to planet center) in meters as a text string.
        """
        return "Radius:       {0:8.1f} m".format(self.r)
        
    def scaleText(self):
        """
        Report the view scale (pixels/meter) as a text string.
        """
        return "View Scale:   {0:8.6f} px/m".format(self.planet.scale)
    
    def timeZoomText(self):
        """
        Report the time acceleration as a text string.
        """
        return "Time Zoom:    {0:8.1f}".format(float(self.timezoom()))
        
    def shipTimeText(self):
        """
        Report the elapsed time as a text string.
        """
        return "Elapsed Time: {0:8.1f} s".format(float(self.shiptime))
    


            
    def dynamics(self, timer):
        """
        Perform one iteration of the simulation using runge-kutta 4th order method.
        """
        # set time duration equal to time since last execution
        tick = 10**self.timezoom()*(timer.time - self.lasttime)
        self.shiptime = self.shiptime + tick
        self.lasttime = timer.time
        # 4th order runge-kutta method (https://sites.temple.edu/math5061/files/2016/12/final_project.pdf)
        # and http://spiff.rit.edu/richmond/nbody/OrbitRungeKutta4.pdf  (succinct, but with a typo)
        self.A = k1v = self.ar(self._xy)
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
            self.A = [0,0]
            self.altitude = 0

    # generic force as a function of position
    def fr(self, pos):
        """
        Compute the net force vector on the rocket, as a function of the 
        position vector.
        """
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
        """
        Compute the acceleration vector of the rocket, as a function of the 
        position vector.
        """
        m = self.mass()
        F = self.fr(pos)
        return [F[i]/m for i in (0,1)]
        
    def vadd(self, v1, v2):
        """
        Vector add utility.
        """
        return [v1[i]+v2[i] for i in (0,1)]
    
    def vmul(self, s, v):
        """
        Scalar vector multiplication utility.
        """
        return [s*v[i] for i in (0,1)]
        
    def vmag(self, v):
        """
        Vector magnitude function.
        """
        return sqrt(v[0]**2 + v[1]**2)
    
    def fgrav(self):
        """
        Vector force due to gravity, at current position.
        """
        G = 6.674E-11
        r = self.r
        uvec = (-self._xy[0]/r, -self._xy[1]/r)
        F = G*self.mass()*self.planet.mass/r**2
        return [x*F for x in uvec]
    
    def turn(self, event):
        """
        Respond to left/right turning key events.
        """
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
        alt = Planet.distance(self._xy, (0,0)) - self.planet.radius
        return alt
        
    @altitude.setter
    def altitude(self, alt):
        r = alt + self.planet.radius
        self._xy = (r*cos(self.tanomaly), r*sin(self.tanomaly))

    @property
    def velocity(self):
        return self.vmag(self.V)
    
    @property
    def acceleration(self):
        return self.vmag(self.A)
        
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
    """
    Initialize the Planet object. 

    Optional keyword parameters are supported:
    
    * **viewscale**  pixels per meter in graphics display. Default is 10.
    * **radius**  radius of the planet in meters. Default is Earth radius.
    * **planetmass** mass of the planet in kg. Default is Earth mass.
    * **color** color of the planet. Default is greenish (0x008040).
    * **viewalt** altitude of initial viewpoint in meters. Default is rocket 
      altitude.
    * **viewanom** true anomaly (angle) of initial viewpoint in radians. 
      Default is the rocket anomaly.
    * **viewanomd** true anomaly (angle) of initial viewpoing in degrees.
      Default is the rocket anomaly.
    
    """
    
    def __init__(self, **kwargs):
        scale = kwargs.get('viewscale', 10)  # 10 pixels per meter default
        self.radius = kwargs.get('radius', 6.371E6) # Earth - meters
        self.mass = kwargs.get('planetmass', 5.9722E24) # Earth - kg
        self.color = kwargs.get('color', 0x008040)  # greenish
        self.kwargs = kwargs # save it for later..
        super().__init__(scale)

    def run(self, rocket=None):
        """
        Execute the Planet (and Rocket) simulation.

        Optional parameters:
        
        * **rocket** Reference to a Rocket object - sets the initial view
        """
        if rocket:
            viewalt = rocket.altitude
            viewanom = rocket.tanomaly
        else:
            viewalt = 0
            viewanom = pi/2
        self.viewaltitude = self.kwargs.get('viewalt', viewalt) # how high to look
        self.viewanomaly = self.kwargs.get('viewanom', viewanom)  # where to look
        self.viewanomalyd = self.kwargs.get('viewanomd', degrees(self.viewanomaly))
        self._planetcircle = Circle(
            (0,0), 
            self.radius, 
            style = LineStyle(1, Color(self.color,1)), 
            color = Color(self.color,0.5))
        r = self.radius + self.viewaltitude
        self.viewPosition = (r*cos(self.viewanomaly), r*sin(self.viewanomaly))
        super().run()
